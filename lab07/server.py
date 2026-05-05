from socket import *
import random

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12000

server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

print(f"Ping Server is running on {SERVER_HOST}:{SERVER_PORT}")

while True:
    message, client_address = server_socket.recvfrom(1024)

    if random.random() < 0.2:
        print(f"Packet from {client_address} lost")
        continue

    modified_message = message.decode().upper()
    server_socket.sendto(modified_message.encode(), client_address)

    print(f"Received from {client_address}: {message.decode()}")
    print(f"Sent back: {modified_message}")