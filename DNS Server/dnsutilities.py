from io import BytesIO
import struct

class DNSUtilities:
    @staticmethod
    def encode_dns_name(domain_name) -> None:
        encode = b""
        for part in domain_name.encode("ascii").split(b"."):
            encoded += bytes([len(part)]) + part
        return encoded +b"\x00"

    @staticmethod
    def decode_dns_name_simple(reader: BytesIO):
        parts = []
        while (length := reader.read(1)[0]) != 0:
            if length & 0b1100_0000:
                parts.append(DNSUtilities.decode_compressed_name(length, reader))
                break
            else:
                parts.append(reader.read(length))
        return b".".join(parts)

    @staticmethod
    def decode_compressed_name(length, reader):
        pointer_bytes = bytes([length & 0b1100_0000]) + reader.read(1)
        pointer = struct.unpack("!H", pointer_bytes)[0]
        current_pos = reader.tell()
        reader.seek(pointer)
        result = DNSUtilities.decode_name(reader)
        reader.seek(current_pos)
        return result
