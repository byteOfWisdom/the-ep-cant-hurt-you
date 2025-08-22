import numpy as np
from matplotlib import pyplot as plt
from sys import argv


def show_or_save():
    if len(argv) > 2:
        plt.savefig(argv[2])
    else:
        plt.show()


def gleichrichter():
    x = np.linspace(0, 10 * np.pi, 10000)
    y1 = np.sin(x)
    y1[y1 < 0] = 0
    y2 = np.abs(np.sin(x))

    if var == "a":
        plt.plot(x, y1, label= "Einwege-Wechselrichter")
    elif var == "b":
        plt.plot(x, y2, label= "Zweiwege-Wechselrichter")
    else:
        print("nope")

    plt.xlabel("Zeit [arbiträre Einheit]")
    plt.ylabel("Relative Spannung")
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    show_or_save()


def belastung():
    rl = np.linspace(0, 1000, 10000)
    u0 = 1.0
    r = 100
    u_ = u0 * rl / (rl + r)
    plt.plot(rl, u_)
    plt.xlabel(r"$R_L [\Omega]$")
    plt.ylabel(r"$U' / U_0$")
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    show_or_save()


def r_min_max():
    uz = 8.2
    rls = [200, np.infty]
    i_s = [0.002, 0.1]
    u0s = [16, 22]
    r = lambda rl, I, u0: (u0 - uz) / (I + (uz / rl))
    print(rls[0], i_s[1], u0s[0], r(rls[0], i_s[0], u0s[1]))
    print(rls[1], i_s[1], u0s[0], r(rls[1], i_s[0], u0s[1]))
    print(rls[0], i_s[1], u0s[1], r(rls[0], i_s[1], u0s[1]))
    print(rls[1], i_s[1], u0s[1], r(rls[1], i_s[1], u0s[1]))
    print(rls[0], i_s[0], u0s[0], r(rls[0], i_s[0], u0s[0]))
    print(rls[1], i_s[0], u0s[0], r(rls[1], i_s[0], u0s[0]))
    print(rls[0], i_s[0], u0s[1], r(rls[0], i_s[1], u0s[0]))
    print(rls[1], i_s[0], u0s[1], r(rls[1], i_s[1], u0s[0]))


def zero_line():
    x = np.linspace(0, 10 * np.pi, 10000)
    y = x - x

    plt.plot(x, y)
    plt.xlabel("Zeit [arbiträre Einheit]")
    plt.ylabel("Relative Spannung")
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    show_or_save()

def diode_line(u):
    a = 1.5
    return 0.001 * (np.exp(a * u) - 1) if u >= 0 else - 0.0001 * (np.exp(a * (np.abs(u) + 3.5)) - 1)


def kennlinie(f):
    u = np.linspace(-10, 10, 10000)
    i = list(map(lambda x: f(x) * 1000, u))
    #plt.plot(u[i**2 <= 1e4], i[i**2 <= 1e4])
    plt.plot([], [])
    plt.ylabel(r"$I [mA]$")
    plt.xlabel(r"$U [V]$")
    plt.xlim([-10, 10])
    plt.ylim([-10, 10])
    #plt.vlines(0, -1, 1, color="grey")
    #plt.hlines(0, -10, 10, color="grey")
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    plt.gca().tick_params(labelbottom=False)
    plt.gca().tick_params(labelleft=False)
    plt.gca().set_aspect("equal")
    show_or_save()


def kennlinie_a():
    kennlinie(lambda x: x / 100)

def kennlinie_b():
    kennlinie(diode_line)


if __name__ == "__main__":
    if argv[1] == "a" or argv[1] == "b":
        gleichrichter()
    elif argv[1] == "c":
        belastung()
    elif argv[1] == "d":
        r_min_max()
    elif argv[1] == "e":
        zero_line()
    elif argv[1] == "f":
        kennlinie_a()
    elif argv[1] == "g":
        kennlinie_b()
