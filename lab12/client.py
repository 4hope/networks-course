import socket
import threading
import tkinter as tk
import time
import os

def start_client():
    ip = ip_entry.get()
    port = int(port_entry.get())
    packets_count = int(packets_entry.get())
    packet_size = int(size_entry.get())

    def client_work():
        try:
            status_var.set("Подключение...")

            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((ip, port))

            start_time = time.time()

            header = f"{packets_count};{packet_size};{start_time}\n"
            client_socket.sendall(header.encode())

            status_var.set("Отправка данных...")

            for i in range(packets_count):
                data = os.urandom(packet_size)
                client_socket.sendall(data)

            client_socket.close()

            status_var.set("Данные отправлены")

        except Exception as e:
            status_var.set("Ошибка: " + str(e))

    thread = threading.Thread(target=client_work)
    thread.daemon = True
    thread.start()

window = tk.Tk()
window.title("Отправитель TCP")
window.geometry("500x270")

ip_var = tk.StringVar(value="127.0.0.1")
port_var = tk.StringVar(value="8080")
packets_var = tk.StringVar(value="1000")
size_var = tk.StringVar(value="1024")
status_var = tk.StringVar(value="Не отправлено")

tk.Label(window, text="IP адрес получателя").grid(row=0, column=0, padx=20, pady=10, sticky="w")
ip_entry = tk.Entry(window, textvariable=ip_var, width=25)
ip_entry.grid(row=0, column=1, padx=20, pady=10)

tk.Label(window, text="Порт получателя").grid(row=1, column=0, padx=20, pady=10, sticky="w")
port_entry = tk.Entry(window, textvariable=port_var, width=25)
port_entry.grid(row=1, column=1, padx=20, pady=10)

tk.Label(window, text="Количество пакетов").grid(row=2, column=0, padx=20, pady=10, sticky="w")
packets_entry = tk.Entry(window, textvariable=packets_var, width=25)
packets_entry.grid(row=2, column=1, padx=20, pady=10)

tk.Label(window, text="Размер пакета, байт").grid(row=3, column=0, padx=20, pady=10, sticky="w")
size_entry = tk.Entry(window, textvariable=size_var, width=25)
size_entry.grid(row=3, column=1, padx=20, pady=10)

tk.Label(window, text="Статус").grid(row=4, column=0, padx=20, pady=10, sticky="w")
tk.Entry(window, textvariable=status_var, width=25).grid(row=4, column=1, padx=20, pady=10)

tk.Button(window, text="Отправить", command=start_client).grid(row=5, column=0, columnspan=2, pady=20)

window.mainloop()