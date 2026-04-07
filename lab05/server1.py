import argparse
import socket
import ssl
import base64

FROM_EMAIL = "nadezdaosipova247@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def recv_response(sock):
    data = sock.recv(4096).decode()
    print(data.strip())
    return data


def send_command(sock, command):
    print(">>>", command.strip())
    sock.send((command + "\r\n").encode())
    return recv_response(sock)


def send_email(to_email, subject, body, password):
    context = ssl.create_default_context()

    with socket.create_connection((SMTP_HOST, SMTP_PORT)) as raw_sock:
        with context.wrap_socket(raw_sock, server_hostname=SMTP_HOST) as sock:
            recv_response(sock)

            send_command(sock, f"EHLO localhost")

            send_command(sock, "AUTH LOGIN")
            send_command(sock, base64.b64encode(FROM_EMAIL.encode()).decode())
            send_command(sock, base64.b64encode(password.encode()).decode())

            send_command(sock, f"MAIL FROM:<{FROM_EMAIL}>")
            send_command(sock, f"RCPT TO:<{to_email}>")
            send_command(sock, "DATA")

            message = (
                f"From: {FROM_EMAIL}\r\n"
                f"To: {to_email}\r\n"
                f"Subject: {subject}\r\n"
                f"Content-Type: text/plain; charset=utf-8\r\n"
                f"\r\n"
                f"{body}\r\n"
                f".\r\n"
            )

            print(">>> sending message body")
            sock.send(message.encode("utf-8"))
            recv_response(sock)

            send_command(sock, "QUIT")


parser = argparse.ArgumentParser()
parser.add_argument("to")
parser.add_argument("subject")
parser.add_argument("body")
parser.add_argument("password")
args = parser.parse_args()

send_email(args.to, args.subject, args.body, args.password)
print("Письмо отправлено")