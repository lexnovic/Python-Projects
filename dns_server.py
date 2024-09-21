import socket


def ParseFlags(flags):
    qr = (flags >> 15) & 0b1  # 1 bit for Query/Response Indicator (QR)
    opcode = (flags >> 11) & 0b1111  # 4 bits for Operation Code (OPCODE)
    aa = (flags >> 10) & 0b1  # 1 bit for Authoritative Answer (AA)
    tc = (flags >> 9) & 0b1  # 1 bit for Truncation (TC)
    rd = (flags >> 8) & 0b1  # 1 bit for Recursion Desired (RD)
    ra = (flags >> 7) & 0b1  # 1 bit for Recursion Available (RA)
    z = (flags >> 4) & 0b111  # 3 bits for Reserved (Z)
    rcode = flags & 0b1111  # 4 bits for Response Code (RCODE)
    return qr, opcode, aa, tc, rd, ra, z, rcode


def construct_flags(qr, opcode, aa, tc, rd, ra, z, rcode):
    flags = (qr << 15) | (opcode << 11) | (aa << 10) | (tc << 9) | (rd << 8)
    flags |= (ra << 7) | (z << 4) | rcode
    return flags


def HeaderParse(buf):
    header_bytes = buf[:12]
    packet_id = int.from_bytes(header_bytes[:2], byteorder="big")
    flags = int.from_bytes(header_bytes[2:4], byteorder="big")
    qdcount = int.from_bytes(header_bytes[4:6], byteorder="big")
    ancount = 1  # We are setting this to 1 as we will provide one answer
    nscount = 0
    arcount = 0

    # Parse the flags
    qr, opcode, aa, tc, rd, ra, z, rcode = ParseFlags(flags)

    # Set flags for the response
    qr = 1  # Response
    rcode = 4  # No error

    # Rebuild the flags
    parsed_flags = construct_flags(qr, opcode, aa, tc, rd, ra, z, rcode)

    # Create the response header
    header = packet_id.to_bytes(2, byteorder="big") + parsed_flags.to_bytes(2, byteorder="big")
    header += qdcount.to_bytes(2, byteorder="big") + ancount.to_bytes(2, byteorder="big")
    header += nscount.to_bytes(2, byteorder="big") + arcount.to_bytes(2, byteorder="big")

    return header


def QuestionParse(buf):
    offset = 12
    name = []
    while True:
        length = buf[offset]
        offset += 1
        if length == 0:
            break
        name.append(buf[offset:offset + length].decode('utf-8'))
        offset += length

    domain_name = ".".join(name)
    qtype = int.from_bytes(buf[offset:offset + 2], byteorder='big')
    qclass = int.from_bytes(buf[offset + 2:offset + 4], byteorder='big')
    offset += 4

    # Return the question section as well (important for the response)
    question_section = buf[12:offset]

    return domain_name, qtype, qclass, question_section, offset


def EncodeDomainName(domain_name):
    parts = domain_name.split(".")
    encoded_name = b""
    for part in parts:
        length = len(part)
        encoded_name += bytes([length]) + part.encode("utf-8")
    encoded_name += b"\x00"
    return encoded_name


def AnswerCreate(domain_name):
    name = EncodeDomainName(domain_name)
    record_type = b"\x00\x01"  # Type A (IPv4 address)
    record_class = b"\x00\x01"  # Class IN (Internet)
    ttl = b"\x00\x00\x00\x3c"  # Time-to-live (60 seconds)
    length = b"\x00\x04"  # Data length (4 bytes for an IPv4 address)
    data = b"\x08\x08\x08\x08"  # IP address (8.8.8.8)

    # Construct the answer section
    answer = name + record_type + record_class + ttl + length + data
    return answer


def main():
    print("Logs from your program will appear here!")

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(("127.0.0.1", 2053))

    while True:
        try:
            buf, source = udp_socket.recvfrom(512)

            # Parse the header and question sections
            header = HeaderParse(buf)
            domain_name, qtype, qclass, question_section, offset = QuestionParse(buf)

            # Create the answer based on the domain name from the question
            answer = AnswerCreate(domain_name)

            # Create the full response by combining the header, question, and answer
            response = header + question_section + answer

            udp_socket.sendto(response, source)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break


if __name__ == "__main__":
    main()
