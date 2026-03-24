import socket
import sys

BUFFER_SIZE = 4096


def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
        return

    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    if not filename.startswith("/"):
        filename = "/" + filename

    request = (
        f"GET {filename} HTTP/1.1\r\n"
        f"Host: {server_host}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    client_socket.sendall(request.encode("utf-8"))

    response = b""
    while True:
        data = client_socket.recv(BUFFER_SIZE)
        if not data:
            break
        response += data

    client_socket.close()

    print(response.decode("utf-8", errors="ignore"))


if __name__ == "__main__":
    main()