def checksum(data):
    s = 0

    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            word = (data[i] << 8) + data[i + 1]
        else:
            word = data[i] << 8

        s += word

        while s > 0xFFFF:
            s = (s & 0xFFFF) + (s >> 16)

    return ~s & 0xFFFF


def check_checksum(data, check_sum):
    s = 0

    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            word = (data[i] << 8) + data[i + 1]
        else:
            word = data[i] << 8

        s += word

        while s > 0xFFFF:
            s = (s & 0xFFFF) + (s >> 16)

    s += check_sum

    while s > 0xFFFF:
        s = (s & 0xFFFF) + (s >> 16)

    return s == 0xFFFF

data1 = b"hello"
cs1 = checksum(data1)
print("Тест 1")
print("Проверка:", check_checksum(data1, cs1))
print()

data2 = bytearray(b"hello")
cs2 = checksum(data2)
data2[0] = data2[0] ^ 1
print("Тест 2")
print("Проверка:", check_checksum(data2, cs2))
print()

data3 = bytes([0x12, 0x34, 0x56])
cs3 = checksum(data3)
print("Тест 3")
print("Проверка:", check_checksum(data3, cs3))
print()

data4 = bytearray(data3)
data4[2] = data4[2] ^ 1
print("Тест 4")
print("Проверка:", check_checksum(data4, cs3))