import numpy as np
from matplotlib import pyplot as plt
from sys import argv
from labtools import perror


data = np.transpose(np.loadtxt(argv[1], skiprows = 1, delimiter = ","))
freqs = perror.ev(data[0], 0)
amps = perror.ev(data[1], 0.3)
u0 = 20

def crazy_log10(x):
    #log a (x) = log b (x) / log b (a)
    # -> log 10 (x) = ln(x) / ln(10)
    return np.log(x) / np.log(10.0)

dB = 20 * crazy_log10(amps / u0)

freq_grenz = 15.92 # 10nF and 1k Ohm

plt.errorbar(perror.value(freqs), perror.value(dB), perror.error(dB), fmt="x")
plt.grid()
plt.xlabel("Frequenz [kHz]")
plt.ylabel(r"Amplitudenverhältniss $20 log(\frac{U_0}{U_{ausgang}})$ [dB]")
plt.vlines(freq_grenz, 0, -7, linestyles="dashed", label = r"$f_{gr} = 15.92kHz$", color="green")
plt.legend()
plt.title("Dämpfung am Tiefpassfilter")
#plt.show()
plt.savefig(argv[1][:-4] + ".pdf")
