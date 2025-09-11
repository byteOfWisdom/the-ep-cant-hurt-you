#!python3
from sys import argv


def convert(num):
    value = -420
    if num[:2] == '0b':
        value = int(num, 2)
    elif num[:2] == '0x':
        value = int(num, 16)
    else:
        value = int(num)

    return value, hex(value), bin(value)


def bin_add(a, b):
    a, _, _ = convert(a)
    b, _, _ = convert(b)
    return bin(a + b)


def from_tc(bin):
    bits = len(bin) - 2
    comp = 2 ** (bits - 1)
    if bin[2] == '1':
        bin = '0b0' + bin[3:]
        return int(bin, 2) - comp
    else:
        return int(bin, 2)


def to_tc(dec, bits = 8):
    comp = 2 ** (bits - 1)
    if dec < 0:
        bin_rep = bin(dec + comp)
        bin_rep = '0b1' + bin_rep[3:]
        return bin_rep
    else:
        return bin(dec)

"""
if __name__ == "__main__":
    if len(argv) == 2:
        d, b, h  = convert(argv[1])
        print(f"{d} = {b} = {h}")
    if len(argv) == 3:
        print(bin_add(argv[1], argv[2]))
"""
