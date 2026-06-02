import time
import psutil

def format_bytes(value):
    if value < 1024:
        return f"{value} B"
    if value < 1024 ** 2:
        return f"{value / 1024:.2f} KB"
    return f"{value / 1024 ** 2:.2f} MB"

def main():
    duration = 15

    print(f"Подсчёт сетевого трафика за {duration} секунд...")
    print("Откройте браузер или обновите страницу, чтобы появился трафик.\n")

    start = psutil.net_io_counters()

    time.sleep(duration)

    end = psutil.net_io_counters()

    incoming = end.bytes_recv - start.bytes_recv
    outgoing = end.bytes_sent - start.bytes_sent

    print("Отчёт:")
    print(f"Входящий трафик:  {format_bytes(incoming)}")
    print(f"Исходящий трафик: {format_bytes(outgoing)}")

if __name__ == "__main__":
    main()