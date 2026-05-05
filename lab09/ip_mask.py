import subprocess
import ipaddress
import re


def cidr_to_netmask(cidr):
    network = ipaddress.IPv4Network(f"0.0.0.0/{cidr}")
    return str(network.netmask)


def get_ip_and_mask():
    result = subprocess.run(
        ["ip", "-o", "-4", "addr", "show", "scope", "global"],
        capture_output=True,
        text=True
    )

    addresses = []

    for line in result.stdout.splitlines():
        match = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)/(\d+)", line)

        if match:
            ip = match.group(1)
            cidr = int(match.group(2))
            mask = cidr_to_netmask(cidr)
            addresses.append((ip, mask))

    return addresses


if __name__ == "__main__":
    addresses = get_ip_and_mask()

    if not addresses:
        print("Не удалось найти IP-адрес и маску сети.")
    else:
        for ip, mask in addresses:
            print(f"IP-адрес компьютера: {ip}")
            print(f"Маска сети: {mask}")