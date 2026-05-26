import socket
import threading
import time
import tkinter as tk

def read_line(sock):
    data = b""

    while not data.endswith(b"\n"):
        part = sock.recv(1)

        if not part:
            break

        data += part

    return data.decode()

def start_server():
    ip = ip_entry.get()
    port = int(port_entry.get())

    def server_work():
        try:
            status_var.set("Ожидание клиента...")

            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((ip, port))
            server_socket.listen(1)

            client_socket, address = server_socket.accept()
            status_var.set(f"Клиент подключился: {address[0]}")

            header = read_line(client_socket)
            parts = header.strip().split(";")

            packets_count = int(parts[0])
            packet_size = int(parts[1])
            start_time = float(parts[2])

            received_bytes = 0

            while True:
                data = client_socket.recv(4096)

                if not data:
                    break

                received_bytes += len(data)

            end_time = time.time()
            elapsed = end_time - start_time

            if elapsed <= 0:
                elapsed = 0.001

            received_packets = received_bytes // packet_size
            lost_packets = packets_count - received_packets
            speed = received_bytes / elapsed

            speed_var.set(f"{speed:.2f} B/s")
            packets_var.set(f"{received_packets} из {packets_count}")
            lost_var.set(str(lost_packets))
            bytes_var.set(str(received_bytes))
            status_var.set("Приём завершён")

            client_socket.close()
            server_socket.close()

        except Exception as e:
            status_var.set("Ошибка: " + str(e))

    thread = threading.Thread(target=server_work)
    thread.daemon = True
    thread.start()


window = tk.Tk()
window.title("Получатель TCP")
window.geometry("500x330")

ip_var = tk.StringVar(value="127.0.0.1")
port_var = tk.StringVar(value="8080")
speed_var = tk.StringVar(value="")
packets_var = tk.StringVar(value="")
lost_var = tk.StringVar(value="")
bytes_var = tk.StringVar(value="")
status_var = tk.StringVar(value="Не запущено")

tk.Label(window, text="Введите IP").grid(row=0, column=0, padx=20, pady=10, sticky="w")
ip_entry = tk.Entry(window, textvariable=ip_var, width=25)
ip_entry.grid(row=0, column=1, padx=20, pady=10)

tk.Label(window, text="Порт для получения").grid(row=1, column=0, padx=20, pady=10, sticky="w")
port_entry = tk.Entry(window, textvariable=port_var, width=25)
port_entry.grid(row=1, column=1, padx=20, pady=10)

tk.Label(window, text="Скорость передачи").grid(row=2, column=0, padx=20, pady=10, sticky="w")
tk.Entry(window, textvariable=speed_var, width=25).grid(row=2, column=1, padx=20, pady=10)

tk.Label(window, text="Получено пакетов").grid(row=3, column=0, padx=20, pady=10, sticky="w")
tk.Entry(window, textvariable=packets_var, width=25).grid(row=3, column=1, padx=20, pady=10)

tk.Label(window, text="Потерянные пакеты").grid(row=4, column=0, padx=20, pady=10, sticky="w")
tk.Entry(window, textvariable=lost_var, width=25).grid(row=4, column=1, padx=20, pady=10)

tk.Label(window, text="Получено байт").grid(row=5, column=0, padx=20, pady=10, sticky="w")
tk.Entry(window, textvariable=bytes_var, width=25).grid(row=5, column=1, padx=20, pady=10)

tk.Label(window, text="Статус").grid(row=6, column=0, padx=20, pady=10, sticky="w")
tk.Entry(window, textvariable=status_var, width=25).grid(row=6, column=1, padx=20, pady=10)

tk.Button(window, text="Получить", command=start_server).grid(row=7, column=0, columnspan=2, pady=15)

window.mainloop()