import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

def execute(cmd):
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd),
                                     stderr=subprocess.STDOUT)
    return output.decode()
    class NetDog:
        def __init__(self, args, buffer=None):
            self_args = args
            self.buffer = buffer
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            def run(self):
                if self.args.listen:
                    self.listen()
                else:
                    self.send()
        def send(self):
            self.socket.connect((self.args.target, self.args.port))
            if self.buffer:
                self.socket.send(self.buffer)

            try:
                while True:
                    recv_len = 1
                    response = ''
                    while recv_len:
                        data = self.socket.recv(4096)
                        recv_len = len(data)
                        response += data.decode()
                        if recv_len < 4096:
                            break
                        if response:
                            print(response)
                            buffer = input('> ')
                            buffer += '\n'
                            self.socket.send(buffer.encode())
            except KeyboardInterrupt:
                print('Session terminated.')
                self.socket.close()
                sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, aelf.args.port))
        self.socket.listen(5)
        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'NetDog: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client.socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Netdog v. 0.1',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Examples:
            netdog.py -t <IP_ADDRESS> -p <PORT> -l -c # command shell
            netdog.py -t <IP_ADDRESS> -p <PORT> -l -u=mytest.txt # upload to file
            netdog.py -t <IP_ADDRESS> -p <PORT> -l -e=\"cat /etc/passwd" # executable command
            echo 'ABC' | ./netdog.py -t <IP_ADDRESS> -p <PORT> # echo text to server port
            netdog.py -t <IP_ADDRESS> -p <PORT> # connect to server'''))
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--execute', action='store_ture', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5051, help='specify port')
    parser.add_argument('-t', '--target', default='192.168.1.107', help='specify IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nd = NetDog(args, buffer.encode())
    nd.run()