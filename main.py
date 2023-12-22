#!/usr/bin/python3

import math
import argparse
import json


def parse_arguments():
    parser = argparse.ArgumentParser(description='Optional app description')
    parser.add_argument('--type', type=str,
                        help='Type of usage')
    parser.add_argument('--message_file_name', type=str,
                        help='Message file name for encrypt of decrypt')
    parser.add_argument('--alphabet_file_name', type=str,
                        help='Alphabet file name for encrypt of decrypt')

    args = parser.parse_args()
    return args


def get_dict_key(value: int, dictionary: dict) -> int:
    for k, v in dictionary.items():
        if v == value:
            return k


def extended_euqlid(a: int, b: int) -> int:
    old_r = a
    r = b
    old_s = 1
    s = 0
    old_t = 0
    t = 1

    while r != 0:
        q = math.floor(old_r / r)

        temp = r
        r = old_r - q * r
        old_r = temp

        temp = s
        s = old_s - q * s
        old_s = temp

        temp = r
        t = old_t - q * t
        old_t = temp
    return old_s if old_s > 0 else old_s + b


def init_keys() -> (tuple, tuple):
    p = 67
    q = 197
    n = p * q
    euler_func = (p - 1) * (q - 1)
    e = 13
    d = extended_euqlid(e, euler_func)
    public_key = tuple([e, n])
    private_key = tuple([d, n])

    return public_key, private_key


def get_bigramms(text: str) -> list:
    bigramms_list = []
    if len(text) % 2 != 0:
        text += ' '
    for i in range(0, len(text), 2):
        ch1, ch2 = text[i], text[i + 1]
        bigramm = ch1 + ch2
        bigramms_list.append(bigramm)
    return bigramms_list


def get_trigramms(text: str) -> list:
    trigramms_list = []
    if len(text) % 3 != 0:
        while len(text) % 3 != 0:
            text += ' '
    for i in range(0, len(text), 3):
        ch1, ch2, ch3 = text[i], text[i + 1], text[i + 2]
        trigramm = ch1 + ch2 + ch3
        trigramms_list.append(trigramm)
    return trigramms_list


def convert_bigramm_to_num(bigramm: str, alphabet: dict, e: int, n: int) -> int:
    bigramm_in_num = alphabet.get(bigramm[0]) * len(alphabet) + alphabet.get(bigramm[1])
    return (bigramm_in_num ** e) % n


def convert_num_to_trigramm(num: int, alphabet: dict) -> (str, str, str):
    ch3 = get_dict_key(num % len(alphabet), alphabet)
    ch2 = get_dict_key(num // len(alphabet) % len(alphabet), alphabet)
    ch1 = get_dict_key(num // len(alphabet) ** 2, alphabet)
    trigramm = ch1 + ch2 + ch3
    return trigramm


def convert_trigramm_to_num(trigramm: str, alphabet: dict, d: int, n: int) -> int:
    trigramm1 = alphabet.get(trigramm[0]) * (len(alphabet) ** 2)
    trigramm2 = alphabet.get(trigramm[1]) * len(alphabet)
    trigramm3 = alphabet.get(trigramm[2])
    trigramm_in_num = trigramm1 + trigramm2 + trigramm3
    return (trigramm_in_num ** d) % n


def convert_num_to_bigramm(num: int, alphabet: dict) -> (str, str):
    ch1 = get_dict_key(int(num / len(alphabet)), alphabet)
    ch2 = get_dict_key(num % len(alphabet), alphabet)
    bigramm = ch1 + ch2
    return bigramm


def encrypt(text: str, public_key: tuple, alphabet: dict) -> str:
    result_str = ''
    bigramms_list = get_bigramms(text)
    for bigramm in bigramms_list:
        bigramm_in_num = convert_bigramm_to_num(bigramm, alphabet, public_key[0], public_key[1])
        trigramm = convert_num_to_trigramm(bigramm_in_num, alphabet)
        result_str += trigramm

    return result_str


def decrypt(text: str, private_key: tuple, alphabet: dict) -> str:
    result_str = ''
    trigramms_list = get_trigramms(text)
    for trigramm in trigramms_list:
        trigramm_in_num = convert_trigramm_to_num(trigramm, alphabet, private_key[0], private_key[1])
        bigramm = convert_num_to_bigramm(trigramm_in_num, alphabet)
        result_str += bigramm

    return result_str


def main() -> int:
    args = parse_arguments()
    public_key, private_key = init_keys()
    message_file = open(args.message_file_name, 'r')
    alphabet_file = open(args.alphabet_file_name, 'r')
    alphabet = json.load(alphabet_file)

    print(public_key, private_key)

    if args.type == 'encrypt':
        encrypt_text = encrypt(message_file.read(), public_key, alphabet)
        print(encrypt_text)
    elif args.type == 'decrypt':
        decrypt_text = decrypt(message_file.read(), private_key, alphabet)
        print(decrypt_text)
    else:
        print('Wrong type of usage!')
        print('Type of usage can be <encrypt> or <decrypt>')
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
