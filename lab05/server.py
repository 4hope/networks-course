import argparse
import smtplib
from email.message import EmailMessage

FROM_EMAIL = "nadezdaosipova247@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
SMTP_LOGIN = "nadezdaosipova247@gmail.com"


def send_email(to_email, subject, body, fmt, stmt_password):
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    if fmt == "txt":
        msg.set_content(body)
    else:
        msg.add_alternative(body, subtype="html")

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_LOGIN, stmt_password)
        server.send_message(msg)


parser = argparse.ArgumentParser()
parser.add_argument("to")
parser.add_argument("subject")
parser.add_argument("format", choices=["txt", "html"])
parser.add_argument("body")
parser.add_argument("stmt_password")
args = parser.parse_args()

send_email(args.to, args.subject, args.body, args.format, args.stmt_password)
print("Письмо отправлено")