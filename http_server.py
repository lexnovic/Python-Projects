import os
import socket
import threading
import sys


def handle_client(client_socket, file_directory):
    data = client.recv(1024).decode()
    req = data.split('\r\n')
    path = req[0].split(" ")[1]

    # Handle the root URL "/"
    if path == "/":
        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 13\r\n\r\nHello, World!".encode()

    # Handle the /echo/ path
    elif path.startswith("/echo/"):
        value = path.split("/echo/")[1]
        length = len(value)
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {length}\r\n\r\n{value}".encode()

    # Handle the /user-agent/ path
    elif path.startswith("/user-agent"):
        user_agent = req[2].split(": ")[1]
        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode()

    # Handle the /files/ path for GET and POST
    elif url.startswith("/files/"):
        directory = sys.argv[2]
        filename = path[7:]

        # POST Request: Write file
        if method == "POST":
            headers = request_full.split("\r\n")
            content_length = 0

            if content_length > 0:
                # Read the remaining body based on content length
                body = b''
                while len(body) < content_length:
                    body += client_socket.recv(min(1024, content_length - len(body)))
                body = body.decode('utf-8')

                try:
                    with open(f"{file_directory}/{filename}", 'w') as f:
                        f.write(body)
                    response = "HTTP/1.1 201 Created\r\n\r\n".encode()
                except Exception as e:
                    response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else:
                response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()

        # GET Request: Read file
        elif method == "GET":
            try:
                with open(f"/{directory}/{filename}", "r") as f:
                    body = f.read()
                response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(body)}\r\n\r\n{body}".encode()
            except Exception as e:
                response = f"HTTP/1.1 404 Not Found\r\n\r\n".encode()
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

    # Send the response to the client
    client.send(response)


def main():
    # Check if the directory flag is present
    if "--directory" in sys.argv:
        dir_index = sys.argv.index("--directory") + 1
        if dir_index < len(sys.argv):
            file_directory = sys.argv[dir_index]
        else:
            print("Error: --directory flag requires a path argument.")
            sys.exit(1)
    else:
        # Provide a default directory if the flag is missing
        file_directory = "/tmp"
        print(f"Warning: --directory flag is missing. Using default directory: {file_directory}")

    print(f"Serving files from directory: {file_directory}")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client_socket, client_address = server_socket.accept()
        threading.Thread(target=handle_client, args=(client_socket, file_directory))


if __name__ == "__main__":
    main()
