import os
from math import gcd
import numpy as np
from random import randint
from sympy import Matrix


default_alp = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ "
mixed_alp = "ИПЕЙЭЯУХЁЛЫВТОЩЮЬФЖГАБШМДЦЗЪЧНРСК "
alphabet_path = "E://Cripta/Lab1/alphabet.txt"
text_path = "E://Cripta/Lab1/in.txt"
key_path = "E://Cripta/Lab1/key.txt"
matrix = "ГВЕЖ"


def checkout_load_alphabet():
    if os.path.isfile(alphabet_path):
        with open("alphabet.txt", encoding="utf-8") as file:
            alphabet = ""
            lines = file.readlines()

            for line in lines:
                alphabet += line.replace("\n", "")

            temp_alph = alphabet
            for char in alphabet:
                if temp_alph.count(char) == 1:
                    temp_alph = temp_alph.strip(char)
                else:
                    print("Incorrect alphabet in file, set the default value")
                    return default_alp.lower()

            return alphabet.lower()
    else:
        print("Can't find alphabet.txt, set the default value")
        return default_alp.lower()


def checkout_load_text(alphabet):
    if os.path.isfile(text_path):
        with open("in.txt", encoding="utf-8") as file:
            text = ""
            lines = file.readlines()

            for line in lines:
                text += line.replace("\n", "")

            text = text.lower()

            for char in text:
                if char not in alphabet:
                    print("Incorrect in.txt, change it")
                    exit()

            return text
    else:
        print("Can't find in.txt, try creating it")
        exit()


def checkout_load_key():
    if os.path.isfile(key_path):
        with open("key.txt", encoding="utf-8") as file:
            key = ""
            lines = file.readlines()

            for line in lines:
                key += line.replace("\n", "")

            return key.lower()
    else:
        print("Can't find key.txt, try creating it")
        exit()


def save_encrypt(msg):
    with open("crypt.txt", "w") as file:
        file.write(msg)


def save_decrypt(msg):
    with open("decrypt.txt", "w") as file:
        file.write(msg)


def main():
    print("Enter the type of crypto-system:\n")

    print("Enter the number")
    print("""1.Caesar's Cipher
2.Affine cipher
3.A simple replacement cipher
4.Hill's Cipher
5.The permutation cipher
6.The Vigener cipher""")
    while True:
        value = input()
        if value != "1" and value != "2" and value != "3" and value != "4" and value != "5" and value != "6":
            print("Oops, wrong input, try again")
        else:
            break

    print("Select mode:")
    print("1.Encrypt")
    print("2.Decrypt")

    while True:
        mode = input()
        if mode != "1" and mode != "2":
            print("Oops, wrong input, try again")
        else:
            break

    alphabet = checkout_load_alphabet()
    text = checkout_load_text(alphabet)
    key = checkout_load_key()

    if value == "1":
        if len(key) == 1 and key in alphabet:
            if mode == "1":
                num = alphabet.index(key) + 1
                encrypted_msg = ""

                len_alphabet = len(alphabet)
                for char in text:
                    index = alphabet.index(char) + num
                    if index >= len_alphabet:
                        index = index % len_alphabet
                    encrypted_msg += alphabet[index]

                save_encrypt(encrypted_msg)
                print("Text encrypted successfully!")
            elif value == "2":
                num = alphabet.index(key) + 1
                decrypted_msg = ""

                len_alphabet = len(alphabet)
                for char in text:
                    index = alphabet.index(char) - num
                    decrypted_msg += alphabet[index]

                save_decrypt(decrypted_msg)
                print("Text decrypted successfully!")
        else:
            print("Invalid key.txt, try changing it")
    elif value == "2":
        if len(key) == 2 and key[0] in alphabet and key[1] in alphabet and gcd(alphabet.index(key[0]) + 1, len(alphabet)) == 1:
            if mode == "1":
                a = alphabet.index(key[0]) + 1
                b = alphabet.index(key[1]) + 1
                encrypted_msg = ""

                len_alphabet = len(alphabet)
                for char in text:
                    index = (a*alphabet.index(char) + b) % len_alphabet
                    encrypted_msg += alphabet[index]

                save_encrypt(encrypted_msg)
                print("Text encrypted successfully!")
            elif mode == "2":
                len_alphabet = len(alphabet)
                a = pow(alphabet.index(key[0]) + 1, -1, len_alphabet)
                b = alphabet.index(key[1]) + 1
                decrypted_msg = ""

                for char in text:
                    index = ((alphabet.index(char) - b)*a) % len_alphabet
                    decrypted_msg += alphabet[int(index)]

                save_decrypt(decrypted_msg)
                print("Text decrypted successfully!")
        else:
            print("Invalid key.txt, try changing it")
    elif value == "3":
        validity_key = True
        for char in key:
            if char not in alphabet or key.count(char) != 1 or len(key) != len(alphabet):
                validity_key = False
                break
        if validity_key:
            if mode == "1":
                encrypted_msg = ""

                for char in text:
                    encrypted_msg += key[alphabet.index(char)]

                save_encrypt(encrypted_msg)
                print("Text encrypted successfully!")
            elif mode == "2":
                decrypted_msg = ""

                for char in text:
                    decrypted_msg += alphabet[key.index(char)]

                save_decrypt(decrypted_msg)
                print("Text decrypted successfully!")
        else:
            print("Invalid key.txt, try changing it")
    elif value == "4":
        first_validity_key = True
        second_validity_key = True

        for char in key:
            if char not in alphabet:
                first_validity_key = False
                break

        if len(key) != 4:
            first_validity_key = False

        if first_validity_key:
            test_matrix = np.array([[alphabet.index(key[0]), alphabet.index(key[1])],
                               [alphabet.index(key[2]), alphabet.index(key[3])]])
            if test_matrix[0][1] * test_matrix[1][1] - test_matrix[1][0] * test_matrix[0][1] == 0:
                second_validity_key = False
        else:
            print("Invalid key.txt, try changing it")

        if second_validity_key:
            current_matrix = np.array([[alphabet.index(key[0]), alphabet.index(key[1])],
                                   [alphabet.index(key[2]), alphabet.index(key[3])]])

            if mode == "1":
                encrypted_msg = ""
                len_of_text = len(text)
                len_alphabet = len(alphabet)

                rand_letter = ""
                if len_of_text % 2 != 0:
                    rand_letter += alphabet[randint(0, len(alphabet) - 1)]
                    text += rand_letter
                    with open("hill.txt", "w") as file:
                        file.write(rand_letter)

                for num in range(0, len(text), 2):
                    index = np.dot([alphabet.index(text[num]), alphabet.index(text[num+1])],
                                   current_matrix) % len_alphabet
                    encrypted_msg += alphabet[index[0]]
                    encrypted_msg += alphabet[index[1]]

                save_encrypt(encrypted_msg)
                print("Text encrypted successfully!")
            elif mode == "2":
                decrypted_msg = ""
                len_alphabet = len(alphabet)

                sy_matrix = Matrix(current_matrix)
                inverse_mod_matrix = sy_matrix.inv_mod(len_alphabet)
                for num in range(0, len(text), 2):
                    index = np.dot([alphabet.index(text[num]), alphabet.index(text[num+1])], inverse_mod_matrix) % len_alphabet
                    decrypted_msg += alphabet[index[0]]
                    decrypted_msg += alphabet[index[1]]

                if os.path.isfile("E://Cripta/Lab1/hill.txt"):
                    decrypted_msg = decrypted_msg[:-1]
                    os.remove("E://Cripta/Lab1/hill.txt")

                save_decrypt(decrypted_msg)
                print("Text decrypted successfully!")
        else:
            print("Invalid key.txt, try changing it")
    elif value == "5":
        validity_key = True
        if len(key) > len(alphabet):
            validity_key = False
        for char in key:
            if char not in alphabet or key.count(char) != 1:
                validity_key = False
                break
        if validity_key:
            if mode == "1":
                encrypted_msg = ""
                len_of_text = len(text)

                temp_var = ""
                if len_of_text % len(key) != 0:
                    while len(text) % len(key) != 0:
                        rand_letter = alphabet[randint(0, len(alphabet) - 1)]
                        text += rand_letter
                        temp_var += rand_letter

                    with open("permut.txt", "w") as file:
                        file.write(temp_var)

                num_key = []
                for char in key:
                    num_key.append(alphabet.index(char))

                sorted_num_key = sorted(num_key)
                iterator = 1
                for num in sorted_num_key:
                    num_key[num_key.index(num)] = iterator
                    iterator += 1

                key_length = len(key)
                for num in range(0, len(text), key_length):
                    zipped_list = list(zip(text[num:num+key_length], num_key))
                    zipped_list.sort(key=lambda x: x[1])
                    sorted_char_string = "".join([char for char, num in zipped_list])
                    encrypted_msg += sorted_char_string

                save_encrypt(encrypted_msg)
                print("Text encrypted successfully!")
            elif mode == "2":
                decrypted_msg = ""

                num_key = []
                for char in key:
                    num_key.append(alphabet.index(char))

                sorted_key = sorted(num_key)
                iterator = 1
                for num in sorted_key:
                    num_key[num_key.index(num)] = iterator
                    iterator += 1

                key_length = len(key)
                for num in range(0, len(text), key_length):
                    decrypted_msg += ''.join([text[num:num+key_length][i-1] for i in num_key])

                if os.path.isfile("E://Cripta/Lab1/permut.txt"):
                    with open("permut.txt") as file:
                        temp = file.read()
                        decrypted_msg = decrypted_msg[:-len(temp)]

                    os.remove("permut.txt")

                save_decrypt(decrypted_msg)
                print("Text decrypted successfully!")
        else:
            print("Invalid key.txt, try changing it")
    elif value == "6":
        validity_key = True
        for char in key:
            if char not in alphabet:
                validity_key = False
                break
        if validity_key:
            if mode == "1":
                encrypted_msg = ""
                enlarged_key = ""
                len_alphabet = len(alphabet)

                while len(enlarged_key) < len(text):
                    enlarged_key += key

                for num in range(len(text)):
                    index = alphabet.index(text[num]) + alphabet.index(enlarged_key[num])
                    if index >= len_alphabet:
                        index = index % len_alphabet
                    encrypted_msg += alphabet[index]

                save_encrypt(encrypted_msg)
                print("Text encrypted successfully!")
            elif value == "2":
                decrypted_msg = ""
                enlarged_key = ""

                while len(enlarged_key) < len(text):
                    enlarged_key += key

                for num in range(len(text)):
                    index = alphabet.index(text[num]) - alphabet.index(enlarged_key[num])
                    decrypted_msg += alphabet[index]

                save_decrypt(decrypted_msg)
                print("Text decrypted successfully!")
        else:
            print("Invalid key.txt, try changing it")
    else:
        print("Unknown data, try again")


if __name__ == "__main__":
    main()
