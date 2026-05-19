import socket
import struct
import time
import os
import argparse

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11

def checksum(data):
    s = 0

    if len(data) % 2 == 1:
        data += b'\x00'

    for i in range(0, len(data), 2):
        word = data[i] << 8 | data[i + 1]
        s += word

    while s > 0xffff:
        s = (s & 0xffff) + (s >> 16)

    return ~s & 0xffff

def create_packet(packet_id, seq):
    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, 0, packet_id, seq)
    data = b"hello"

    chksum = checksum(header + data)

    header = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, chksum, packet_id, seq)

    return header + data

def traceroute(host, count):
    dest_ip = socket.gethostbyname(host)

    print(f"Tracing route to {host} [{dest_ip}]")
    print()

    packet_id = os.getpid() & 0xffff
    seq = 0
    max_ttl = 30
    timeout = 2

    for ttl in range(1, max_ttl + 1):
        print(f"{ttl:2d}", end="  ")

        last_ip = None
        reached = False

        for _ in range(count):
            seq += 1

            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.settimeout(timeout)
            sock.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)

            packet = create_packet(packet_id, seq)

            start = time.time()
            sock.sendto(packet, (dest_ip, 0))

            try:
                answer, addr = sock.recvfrom(1024)
                finish = time.time()

                rtt = (finish - start) * 1000
                last_ip = addr[0]

                ip_header_len = (answer[0] & 15) * 4
                icmp_header = answer[ip_header_len:ip_header_len + 8]
                icmp_type, code, chksum, recv_id, recv_seq = struct.unpack("!BBHHH", icmp_header)

                print(f"{rtt:.2f} ms", end="  ")

                if icmp_type == ICMP_ECHO_REPLY:
                    reached = True

            except socket.timeout:
                print("*", end="  ")

            sock.close()

        if last_ip is not None:
            print(last_ip)
        else:
            print("*")

        if reached:
            break

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("-c", "--count", type=int, default=3)

    args = parser.parse_args()

    traceroute(args.host, args.count)

if __name__ == "__main__":
    main()