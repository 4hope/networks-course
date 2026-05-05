from socket import *
import time

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 12000

client_socket = socket(AF_INET, SOCK_DGRAM)

client_socket.settimeout(1.0)

for sequence_number in range(1, 11):
    send_time = time.time()

    message = f"Ping {sequence_number} {send_time}"

    try:
        client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))

        response, server_address = client_socket.recvfrom(1024)

        receive_time = time.time()
        rtt = receive_time - send_time

        print(f"Received from server: {response.decode()}")
        print(f"RTT: {rtt:.6f} seconds")
        print()

    except timeout:
        print(f"Ping {sequence_number}: Request timed out")
        print()

client_socket.close()