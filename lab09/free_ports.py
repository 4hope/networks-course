import socket
import sys


def is_port_free(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.bind((ip, port))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def main():
    if len(sys.argv) != 4:
        print("Неправильное количество аргументов")
        return

    ip = sys.argv[1]

    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    if start_port < 0 or end_port > 65535 or start_port > end_port:
        print("Диапазон портов должен быть от 0 до 65535.")
        return

    print(f"IP-адрес: {ip}")
    print(f"Диапазон портов: {start_port}-{end_port}")
    print("Свободные порты:")

    found = False

    for port in range(start_port, end_port + 1):
        if is_port_free(ip, port):
            print(port)
            found = True

    if not found:
        print("Свободные порты в указанном диапазоне не найдены.")


if __name__ == "__main__":
    main()