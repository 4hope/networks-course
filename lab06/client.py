from ftplib import FTP
import os


class FTPClientApp:
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.ftp = FTP()

    def connect(self) -> None:
        self.ftp.connect(self.host, self.port, timeout=10)
        self.ftp.login(self.username, self.password)
        self.ftp.set_pasv(True)

    def disconnect(self) -> None:
        try:
            self.ftp.quit()
        except Exception:
            pass

    def list_files_and_dirs(self) -> None:
        try:
            items = self.ftp.nlst()
            if not items:
                print("Папка пуста")
                return
            for item in items:
                print(item)
        except Exception as e:
            print("Не удалось получить список файлов:", repr(e))

    def upload_file(self, local_path: str, remote_filename: str | None = None) -> None:
        if not os.path.isfile(local_path):
            print("Файл не найден")
            return

        if remote_filename is None:
            remote_filename = os.path.basename(local_path)

        try:
            with open(local_path, "rb") as file:
                self.ftp.storbinary(f"STOR {remote_filename}", file)
            print("Файл загружен")
        except Exception as e:
            print("Ошибка загрузки файла:", repr(e))

    def download_file(self, remote_filename: str, local_path: str | None = None) -> None:
        if local_path is None:
            local_path = remote_filename

        try:
            with open(local_path, "wb") as file:
                self.ftp.retrbinary(f"RETR {remote_filename}", file.write)
            print("Файл скачан")
        except Exception as e:
            print("Ошибка скачивания файла:", repr(e))


def main():
    host = input("Хост: ").strip() or "127.0.0.1"
    port_input = input("Порт: ").strip()
    port = int(port_input) if port_input else 21
    username = input("Логин: ").strip() or "TestUser"
    password = input("Пароль: ").strip() or "0000"

    app = FTPClientApp(host, port, username, password)

    try:
        app.connect()
        print("Подключение выполнено")
    except Exception as e:
        print("Не удалось подключиться к серверу:", repr(e))
        return

    try:
        while True:
            print("\n1 - Список файлов")
            print("2 - Загрузить файл")
            print("3 - Скачать файл")
            print("4 - Выход")

            choice = input("Выбор: ").strip()

            if choice == "1":
                app.list_files_and_dirs()
            elif choice == "2":
                local_path = input("Путь к локальному файлу: ").strip()
                remote_name = input("Имя на сервере: ").strip()
                app.upload_file(local_path, remote_name if remote_name else None)
            elif choice == "3":
                remote_name = input("Имя файла на сервере: ").strip()
                local_path = input("Сохранить как: ").strip()
                app.download_file(remote_name, local_path if local_path else None)
            elif choice == "4":
                break
            else:
                print("Неизвестная команда")
    finally:
        app.disconnect()


if __name__ == "__main__":
    main()