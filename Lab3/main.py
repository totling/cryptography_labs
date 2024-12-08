import random
import time
from math import ceil
from sympy import mod_inverse


def check_timeout(start_time, timeout):
    if time.time() - start_time > timeout:
        raise TimeoutException("Время выполнения превышено")


class TimeoutException(Exception):
    pass


def miller_rabin(n, k=16):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # a^d % n
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def generate_prime(bits, k=16):
    while True:
        num = random.getrandbits(bits)
        num |= (1 << bits - 1) | 1
        if miller_rabin(num, k):
            return num


def generate_keys(bits):
    if bits < 32:
        bits = 32
    start_time = time.time()
    p = generate_prime(bits)
    check_timeout(start_time, timeout=60)
    q = generate_prime(bits)
    check_timeout(start_time, timeout=60)
    n = p * q
    phi = (p - 1) * (q - 1)

    while True:
        check_timeout(start_time, timeout=60)
        e = random.randrange(2, phi)
        if gcd(e, phi) == 1:
            break

    d = mod_inverse(e, phi)
    check_timeout(start_time, timeout=60)

    return (e, n), (d, n)


def encode_decode(message, flag=True):
    if flag:
        message_bytes = message.encode('windows-1251')
        message_int = int.from_bytes(message_bytes, byteorder='big')
        return message_int
    else:
        decrypted_bytes = message.to_bytes((message.bit_length() + 7) // 8, byteorder='big')
        decrypted_message = decrypted_bytes.decode('windows-1251')
        return decrypted_message


def encrypt_decrypt(message, key):
    start_time = time.time()
    e_d, n = key

    trans_message = pow(message, e_d, n)
    check_timeout(start_time, timeout=10)
    return trans_message


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def main():
    try:
        message = input("Введите текст для шифрования:\n")
        encoded_message = encode_decode(message)

        public_key, private_key = generate_keys(ceil(encoded_message.bit_length()*1.4))

        print("Public Key:", public_key)
        print("Private Key:", private_key)

        encrypted_message = encrypt_decrypt(encoded_message, public_key)
        print("Зашифрованное сообщение:\n", encrypted_message)

        decrypted_message = encode_decode(encrypt_decrypt(encrypted_message, private_key), False)
        print("Расшифрованное сообщение:\n", decrypted_message)
    except TimeoutException as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()
