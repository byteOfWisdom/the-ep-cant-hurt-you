from labtools.perror import ev as e
from labtools.perror import value as val
from labtools.perror import error as err

import numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

I_d = e([3.4, 3.8, 4.2, 4.8, 5.3, 5.9, 6.5, 7.0, 7.7, 8.3], 0.1) * 1e-3
n = np.arange(1, len(I_d) + 1)
R = e(0.491, 0.01) * 1e6 #from key.txt
U_gs = n * R * 6e-6 - I_d * 100
sqrt_I_d = np.sqrt(I_d)

lin = lambda x, a, b: x * a + b
parab = lambda x, a, b: b * ((x - a) ** 2)
res, cov = curve_fit(parab, val(U_gs), val(I_d))
k = res[1]
U_thr = res[0]
fit_vals = np.sqrt(k * ((val(U_gs) - U_thr) ** 2))
fit_vals_sq = k * ((val(U_gs) - U_thr) ** 2)

print(f"k = {k}")
print(f"U_thr = {U_thr}")

version_a = False
if version_a:
    plt.errorbar(val(U_gs), val(sqrt_I_d), xerr = err(U_gs), yerr = err(sqrt_I_d), fmt=".")
    plt.plot(val(U_gs), fit_vals)
    plt.xlabel(r"$U_{GS}$ [V]")
    plt.ylabel(r"$\sqrt{I_{d}}$ $[\sqrt{mA}]$")
else:
    plt.errorbar(val(U_gs), val(I_d), xerr = err(U_gs), yerr = err(I_d), fmt=".")
    plt.plot(val(U_gs), fit_vals_sq)
    plt.xlabel(r"$U_{GS}$ [V]")
    plt.ylabel(r"$\sqrt{I_{d}}$ $[\sqrt{mA}]$")

plt.grid(which="major")
plt.grid(which="minor", linestyle=":", linewidth=0.5)
plt.gca().minorticks_on()
plt.show()
#plt.savefig(fout)
