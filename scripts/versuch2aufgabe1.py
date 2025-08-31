import numpy as np
import matplotlib
from sys import argv

from matplotlib import pyplot as plt
from labtools.perror import ev

def tex(v):
    s = str(v)
    if "^" in s:
        s = s.replace("^", "^{")
        s += "}"
    s = s.replace("+-", r"\pm").replace("*", r"\cdot ")
    return s


def unpackdata(filename, polarity):
    U = []
    I = []
    filehandle = open(filename)
    lines = filehandle.readlines()[1:]

    for line in lines:
        U += [polarity * float(line.split(",")[0])]
        I += [polarity * float(line.split(",")[1])]
    filehandle.close()
    return U, I

Ud1_sperr, Id1_sperr = unpackdata(argv[1] + "/d1_sperr.csv", -1)
Ud1_durchlass, Id1_durchlass = unpackdata(argv[1] + "/d1_durchlass.csv", 1)

Id1_sperr =list(0.5 * np.array(Id1_sperr))
Ud1_durchlass = list(0.025 * np.array(Ud1_durchlass))

Ud1, Id1 = Ud1_sperr + Ud1_durchlass, Id1_sperr + Id1_durchlass
err_U1 = [0.01 for _ in Ud1_sperr] + [0.025 for _ in Ud1_durchlass]
err_I1 = [0.5 for _ in Ud1_sperr] + [0.1 for _ in Ud1_durchlass]

Ud2_sperr, Id2_sperr = unpackdata(argv[1] + "/d2_sperr.csv", -1)
Ud2_durchlass, Id2_durchlass = unpackdata(argv[1] + "/d2_durchlass.csv", 1)

Id2_sperr =list(0.0025 * np.array(Id2_sperr))
Ud2_durchlass =list(0.005 * np.array(Ud2_durchlass))
err_U2 = [0.01 for _ in Ud2_sperr] + [0.025 for _ in Ud2_durchlass]
err_I2 = [0.5 for _ in Ud2_sperr] + [0.1 for _ in Ud2_durchlass]



Ud2, Id2 = Ud2_sperr + Ud2_durchlass, Id2_sperr + Id2_durchlass

for i in range(max([len(Ud1), len(Ud2)])):
    line = ""
    if i < len(Ud1):
        line += f"${tex(ev(Ud1[i], err_U1[i]))}$ "
    line += " & "
    if i < len(Id1):
        line += f"${tex(ev(Id1[i], err_I1[i]))}$"
    line += " & "
    if i < len(Ud2):
        line += f"${tex(ev(Ud2[i], err_U2[i]))}$"
    line += " & "
    if i < len(Id2):
        line += f"${tex(ev(Id2[i], err_I2[i]))}$"
    line += "\\\\"

    print(line)

#plt.xlabel(r"U [V]")
#plt.ylabel(r"I [mA]")

#plt.plot(Ud1, Id1)
#plt.errorbar(Ud1, Id1, xerr=err_U1, yerr=err_I1, fmt="x")
#plt.grid()
#plt.show()
#plt.savefig("d1kennlinie.pdf")
#plt.cla()

#plt.xlabel(r"U [V]")
#plt.ylabel(r"I [mA]")



#plt.plot(Ud2, Id2)
#plt.errorbar(Ud2, Id2, xerr=err_U2, yerr=err_I2, fmt="x")
#plt.grid()
#plt.show()
#plt.savefig("d2kennlinie.pdf")
