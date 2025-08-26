import numpy as np
from matplotlib import pyplot as plt
from sys import argv


def show_or_save():
    if len(argv) > 3:
        plt.savefig(argv[3])
    else:
        plt.show()

def show(U1, I1, U2, I2):
    plt.errorbar(I1, U1, xerr=0.01, yerr=0.1, fmt=".", label="nicht-stabilisiert")
    plt.errorbar(I2, U2, xerr=0.01, yerr=0.1, fmt=".", label="stabilisiert")
    plt.xlabel("Strom [mA]")
    plt.ylabel("Spannung [V]")
    plt.legend()
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    show_or_save()


if __name__ == "__main__":
    file_a = argv[1]
    file_b = argv[2]
    data_a = np.transpose(np.loadtxt(file_a, skiprows=1, delimiter=","))
    data_b = np.transpose(np.loadtxt(file_b, skiprows=1, delimiter=","))
    show(data_a[1], data_a[0], data_b[1], data_b[0])
    show_or_save()
