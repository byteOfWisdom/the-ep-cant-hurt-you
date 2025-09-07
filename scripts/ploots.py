import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from labtools.perror import ev, value, error
from sys import argv


def show_or_save():
    if len(argv) > 2:
        plt.savefig(argv[2])
    else:
        plt.show()


def opamp_noninverting():
    f = np.linspace(0, 1e5, 1000000)
    R = 100e3
    C = 100e-9
    v = 1. + 2. * np.pi * R * C * f
    plt.loglog()
    plt.plot(f, v)
    plt.xlabel("Frequenz [Hz]")
    plt.ylabel("Verstärkung")
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    show_or_save()


def gleichrichter():
    x = np.linspace(0, 10 * np.pi, 10000)
    y1 = np.sin(x)
    y1[y1 < 0] = 0
    y2 = np.abs(np.sin(x))
    var = "a"

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


def tex(v):
    s = str(v)
    if "^" in s:
        s = s.replace("^", "^{")
        s += "}"
    s = s.replace("+-", r"\pm").replace("*", r"\cdot ")
    return s


def voltage_sin_gen():
    us = np.array([2.1, 4.0, 8.1, 15.7, 11.1, 6.0, 3.0])
    ts = np.array([15.5e-3 - 12.3e-3, 172e-6 - 130e-6, 90e-6 - 69e-6, 49e-6 - 34e-6, 53e-6 - 34e-6, 99e-6 - 69e-6, 245e-6 - 173e-6])
    dts = np.array([1e-3, 2e-6, 2e-6, 2e-6, 2e-6, 2e-6, 2e-6])
    fs = value(1 / ev(ts, dts))#np.array([32.5e1, 25.0e3, 43.7e3, 7.5e4, 5.0e4, 31.2e3, 12.5e3])
    dfs = error(1 / ev(ts, dts))#np.array([2.5e1, 2.5e3, 6.3e3, 1.2e4, 1.2e4, 6.2e3, 2.5e3])
    log_line = lambda x, a, b: np.exp(a * np.log(x) + b)
    params, cov = curve_fit(log_line, us[1:], fs[1:], sigma=dfs[1:], maxfev=99999)
    errs = np.sqrt(np.diag(cov))
    print(f"a={str(ev(params[0], errs[0]))}")
    print(f"b={str(ev(params[1], errs[1]))}")

    for i in range(len(us)):
        print(f"${tex(ev(us[i], 0.1))}$ & ${tex(ev(ts[i], dts[i]))}$ & ${tex(ev(fs[i], dfs[i]))}$ \\\\")

    plt.errorbar(us[1:], fs[1:], fmt=" ", yerr=dfs[1:], xerr=dts[1:], label="", elinewidth=0.75, capsize=2)
    plt.plot(np.linspace(min(us), max(us), 1000), log_line(np.linspace(min(us), max(us), 1000), *params))
    plt.loglog()
    plt.xlabel("Spannung [V]")
    plt.ylabel("Frequenz [Hz]")
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    show_or_save()


def bandpass_expected():
    x = np.exp(np.linspace(np.log(1), np.log(1e3), 10000))
    varsin = lambda x, f: np.sin(x * f(x))
    lin = lambda x: 1 * x
    f0 = 3e1
    bandpass = lambda f: f * f0 / (f**2 + f0**2)

    plt.semilogx()
#    plt.plot(x, bandpass(lin(x)), label="Bandpass Erwartung")
    plt.plot(x, varsin(x, lin) * bandpass(lin(x)))
    plt.ylabel("Oszilloskop Y-Achse U [V], normiert")
    plt.xlabel("Oszilloskop X-Achse U [V] ~ f [Hz] (jeweils logarithmisch)")
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    plt.show()


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
    elif argv[1] == "h":
        opamp_noninverting()
    elif argv[1] == "i":
        voltage_sin_gen()
    elif argv[1] == "j":
        bandpass_expected()
