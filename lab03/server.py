import os
import socket
import sys
from urllib.parse import unquote

HOST = "127.0.0.2"
BUFFER_SIZE = 4096


def send_response(conn, status_line, content_type, body):
    headers = [
        status_line,
        f"Content-Length: {len(body)}",
        f"Content-Type: {content_type}",
        "Connection: close",
        "",
        ""
    ]
    response = "\r\n".join(headers).encode("utf-8") + body
    conn.sendall(response)


def get_content_type(filename):
    ext = os.path.splitext(filename)[1].lower()
    if ext in [".html", ".htm"]:
        return "text/html; charset=utf-8"
    if ext == ".txt":
        return "text/plain; charset=utf-8"
    if ext == ".jpg" or ext == ".jpeg":
        return "image/jpeg"
    if ext == ".png":
        return "image/png"
    if ext == ".gif":
        return "image/gif"
    if ext == ".css":
        return "text/css; charset=utf-8"
    if ext == ".js":
        return "application/javascript; charset=utf-8"
    return "application/octet-stream"


def safe_path(request_path):
    request_path = request_path.split("?", 1)[0]
    request_path = unquote(request_path)

    if request_path == "/":
        request_path = "/index.html"

    request_path = request_path.lstrip("/")

    normalized = os.path.normpath(request_path)
    if normalized.startswith("..") or os.path.isabs(normalized):
        return None

    return normalized


def handle_client(conn):
    request = conn.recv(BUFFER_SIZE).decode("utf-8", errors="ignore")
    if not request:
        return

    lines = request.splitlines()
    if not lines:
        return

    request_line = lines[0]
    parts = request_line.split()

    _, path, _ = parts

    file_path = safe_path(path)

    if not os.path.isfile(file_path):
        body = b"<h1>404 Not Found</h1>"
        send_response(conn, "HTTP/1.1 404 Not Found", "text/html; charset=utf-8", body)
        return

    with open(file_path, "rb") as f:
        body = f.read()
    content_type = get_content_type(file_path)
    send_response(conn, "HTTP/1.1 200 OK", content_type, body)


def main():
    if len(sys.argv) != 2:
        print("Usage: python server.py <server_port>")
        return

    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, port))
    server_socket.listen(1)

    print(f"Server is running at http://{HOST}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connected by {addr}")
        handle_client(conn)
        conn.close()


if __name__ == "__main__":
    main()