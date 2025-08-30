from labtools.perror import ev as e
from labtools.perror import value as val
from labtools.perror import error as err

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
from sys import argv

table = False
save = False
do_plot = False
print_vals = False


if len(argv) > 1 and argv[1] == "table":
    table = True

if len(argv) > 1 and argv[1] == "print":
    print_vals = True

if len(argv) > 1 and argv[1] == "save":
    save = True
    do_plot = True

if len(argv) > 1 and argv[1] == "show":
    save = False
    do_plot = True


def plot_stuff(name = ""):
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    plt.legend()
    plt.show() if name == "" else plt.savefig(name)
    plt.cla()



R_d = 500 #Ohm
#offset_U = - 3.3 # find out # jay und co
#U_d = e([-3.2, -2.7, -1.8, -0.6, 0.6, 2.0, 3.4], 0.2) - offset_U #jay und co
#R = e(30.46, 0.1) * 1e3 #jay und co

offset_U = - 3.6 # find out # lena und co
U_d = e([-3.4, -2.9, -2.1, -1.2, -0.2, 0.8, 1.9, 3.0, 4.2], 0.2) - offset_U #lena und co
R = e(46.5, 0.1) * 1e3 #lena und co


I_d = U_d / R_d
n = (np.flip(np.arange(0, len(I_d))) - 16) * (-1)
U_gs = n * R * 6e-6 - I_d * 100
sqrt_I_d = np.sqrt(I_d)


def tex(v):
    s = str(v)
    if "^" in s:
        s = s.replace("^", "^{")
        s += "}"
    s = s.replace("+-", r"\pm").replace("*", r"\cdot ")
    return s




lin = lambda x, a, b: x * a + b
parab = lambda x, a, b: b * ((x - a) ** 2)
res2, cov2 = curve_fit(parab, val(U_gs), val(I_d), maxfev=10000)
fit_errs2 = np.sqrt(np.diag(cov2))
k2 = e(res2[1], fit_errs2[1])
U_thr2 = e(res2[0], fit_errs2[0])

res, cov = curve_fit(lin, val(U_gs), val(np.sqrt(I_d)), maxfev=10000)
fit_errs = np.sqrt(np.diag(cov))
a, b = e(res[0], fit_errs[0]), e(res[1], fit_errs[1])
k = a ** 2
U_thr = 0 - b / a


x_vals = np.linspace(U_gs[0].value - 0.05, U_gs[-1].value + 0.05, 1000)
fit_vals = a.value * x_vals + b.value
fit_vals_sq = k2.value * ((x_vals - U_thr2.value) ** 2)
#fit_vals_sq = fit_vals ** 2

delta_I_D = I_d[1:] - I_d[:-1]
delta_U_gs = U_gs[1:] - U_gs[:-1]
gm_measured = delta_I_D / delta_U_gs
U_gm_measured = 0.5 * (U_gs[1:] +  U_gs[:-1])

gm_cal = 2.0 * k2 * (x_vals - U_thr2)
gm_approx = 2.0 * np.sqrt(k2 * I_d)


if print_vals:
    print(f"a = {a}")
    print(f"b = {b}")
    print(f"k = {k}")
    print(f"U_thr = {U_thr}")
    print(f"k2 = {k2}")
    print(f"U_thr2 = {U_thr2}")



if do_plot:
    plt.errorbar(val(U_gs), val(sqrt_I_d), xerr = err(U_gs), yerr = err(sqrt_I_d), fmt=" ", elinewidth=0.75, capsize=2, label="Messwerte")
    plt.plot(x_vals, fit_vals, label="Fit")
    plt.xlabel(r"$U_{GS}$ [V]")
    plt.ylabel(r"$\sqrt{I_{d}}$ $[\sqrt{A}]$")
    plot_stuff("fet_U_sqrt_I.pdf" if save else "")

    plt.errorbar(val(U_gs), val(I_d * 1e3), xerr = err(U_gs), yerr = err(I_d * 1e3), fmt=" ", elinewidth=0.75, capsize=2, label="Messwerte")
    plt.plot(x_vals, fit_vals_sq * 1e3, label="Fit")
    plt.xlabel(r"$U_{GS}$ [V]")
    plt.ylabel(r"$I_{d}$ $[mA]$")
    plot_stuff("fet_U_I.pdf" if save else "")


    plt.plot(x_vals, val(gm_cal), label="$g_{m, berechnet}$", color="tab:grey")
    plt.errorbar(val(U_gm_measured), val(gm_measured), xerr = err(U_gm_measured), yerr = err(gm_measured), fmt=" ", elinewidth=0.75, capsize=2, label="$g_{m, gemessen}$")
    plt.errorbar(val(U_gs), val(gm_approx), xerr = err(U_gs), yerr = err(gm_approx), fmt=" ", elinewidth=0.75, capsize=2, label="$g_{m, näherung}$")
    plt.xlabel(r"$U_{GS}$ [V]")
    plt.ylabel(r"$gm$ $[\Omega]$")
    plot_stuff("fet_gm.pdf" if save else "")


if table:
    print(r"Linie & $U_d / \si{\V}$ & $I_d / \si{\ampere}$ & $U_{GS} / \si{\V}$&$ g_\mathrm{m, näherung} $\\")
    print(r"\hline")
    for i in range(len(n)):
        print(f"${n[i]}$ & ${tex(U_d[i])}$ & ${tex(I_d[i])}$ & ${tex(U_gs[i])}$ & ${tex(gm_approx[i])}$\\\\")

    print()
    print(r"$U_{GS, Mittel} / \si{\V}$ & $\Delta I_d / \si{\ampere}$ & $\Delta U_{GS} / \si{\V}$&$ g_\mathrm{m, gemessen} / \mathrm{\Omega}$\\")
    print(r"\hline")
    for i in range(len(gm_measured)):
        print(f"${tex(U_gm_measured[i])}$ & ${tex(delta_I_D[i])}$ & ${tex(delta_U_gs[i])}$ & ${tex(gm_measured[i])}$ \\\\")
