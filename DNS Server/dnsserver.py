import socket
from io import BytesIO
from dnsmessage import DNSMessage
from dnsrecord import DNSRecord, RClass, RType
from dnsquestion import DNSQuestion, QClass, QType

class DNSServer:
    def __init__(self, ip, port):
        self.port = port
        self.ip = ip
        self.udp_socket = None

    def run(self):
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_socket.bind((self.ip, self.port))

        while True:
            try:

                buf, source = udp_socket.recvfrom(512)

                print(buf)
                reader = BytesIO(buf)
                request = DNSMessage()
                request.from_bytes(reader)

                response = DNSMessage()
                response.create_response(request)

                response_data = response.to_bytes()
                print(f'response: {response_data}')
                udp_socket.sendto(response_data, source)

            except Exception as e:
                print(f"Error handling DNS Message: {e}")
                break