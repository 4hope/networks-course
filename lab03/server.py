import os
import socket
import sys
import threading
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
    if ext in [".jpg", ".jpeg"]:
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


def handle_client(conn, addr, semaphore):
    print(f"Connected by {addr}")

    try:
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

        if file_path is None or not os.path.isfile(file_path):
            body = b"<h1>404 Not Found</h1>"
            send_response(conn, "HTTP/1.1 404 Not Found", "text/html; charset=utf-8", body)
            return

        with open(file_path, "rb") as f:
            body = f.read()

        content_type = get_content_type(file_path)
        send_response(conn, "HTTP/1.1 200 OK", content_type, body)

    finally:
        conn.close()
        semaphore.release()
        print(f"Connection with {addr} closed")


def main():
    port = int(sys.argv[1])
    concurrency_level = int(sys.argv[2])

    semaphore = threading.Semaphore(concurrency_level)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, port))
    server_socket.listen(5)

    print(f"Server is running at http://{HOST}:{port}")
    print(f"Max concurrent threads: {concurrency_level}")

    while True:
        conn, addr = server_socket.accept()

        semaphore.acquire()

        client_thread = threading.Thread(
            target=handle_client,
            args=(conn, addr, semaphore)
        )
        client_thread.start()


if __name__ == "__main__":
    main()