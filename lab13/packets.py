def bytes_to_bits(data: bytes) -> str:
    return ''.join(f'{byte:08b}' for byte in data)

def xor_bits(a: str, b: str) -> str:
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))

def crc_remainder(data_bits: str, generator: str) -> str:
    degree = len(generator) - 1
    padded = data_bits + '0' * degree
    padded = list(padded)

    for i in range(len(data_bits)):
        if padded[i] == '1':
            part = ''.join(padded[i:i + len(generator)])
            result = xor_bits(part, generator)
            padded[i:i + len(generator)] = list(result)

    return ''.join(padded[-degree:])

def check_crc(encoded_bits: str, generator: str) -> bool:
    data_len = len(encoded_bits) - (len(generator) - 1)
    remainder = crc_remainder(encoded_bits[:data_len], generator)
    return remainder == encoded_bits[data_len:]

def flip_bit(bits: str, index: int) -> str:
    bits = list(bits)
    bits[index] = '1' if bits[index] == '0' else '0'
    return ''.join(bits)

def split_into_packets(data: bytes, size: int = 5):
    return [data[i:i + size] for i in range(0, len(data), size)]

def main():
    generator = "100000111"

    text = input("Введите текст: ")
    data = text.encode("utf-8")

    packets = split_into_packets(data, 5)

    errors = {
        1: [3],
        3: [5, 12]
    }

    print("\nРезультат проверки пакетов:\n")

    for i, packet in enumerate(packets):
        data_bits = bytes_to_bits(packet)
        crc = crc_remainder(data_bits, generator)
        encoded = data_bits + crc

        transmitted = encoded

        if i in errors:
            for bit_index in errors[i]:
                if bit_index < len(transmitted):
                    transmitted = flip_bit(transmitted, bit_index)

        ok = check_crc(transmitted, generator)

        try:
            payload_text = packet.decode("utf-8")
        except UnicodeDecodeError:
            payload_text = str(packet)

        print(f"Пакет №{i + 1}")
        print(f"Полезные данные: {packet} ({payload_text})")
        print(f"Закодированный пакет: {encoded}")
        print(f"Контрольный код CRC: {crc}")
        print(f"Переданный пакет:    {transmitted}")
        print(f"Ошибка обнаружена: {'нет' if ok else 'да'}")
        print("-" * 80)

if __name__ == "__main__":
    main()