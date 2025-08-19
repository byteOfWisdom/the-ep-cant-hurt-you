#!python3
import numpy as np
from sys import argv
from matplotlib import pyplot as plt


def load_csv(fname):
    with open(fname, "r") as file:
        raw = file.readlines()
        parse_line = lambda l: float(l.strip().strip(","))
        data = np.array(list(map(parse_line, raw[16:])))

        metadata = {}
        metadata["vdiff"] = float(raw[5].split(",")[1])
        metadata["tdiff"] = float(raw[11].split(",")[1])

        return data, metadata["vdiff"], metadata["tdiff"]


def find_unit(interval):
    # leaving this function here as a joke.
    # maybe at some point it'll get a proper implementation
    return r"$\mu s$", 1e6


def plot_single(fname, fout):
    data, vstep, tstep = load_csv(fname)
    cal_factor = 10 / 255 # this is a best guess for a signed 8 bit integer value and 5 divs per side, 10 divs total
    time = np.arange(0, len(data)) * tstep
    unit, unit_value = find_unit(tstep)
    amplitude = data * vstep * cal_factor
    scaled_time = time * unit_value
    plt.plot(scaled_time, amplitude)
    plt.xlabel(unit)
    plt.ylabel("V")
    plt.xlim([scaled_time[0], scaled_time[-1]])
    plt.grid()
    #plt.show()
    plt.savefig(fout)

def plot_dual(fname1, fname2, fout):
    data1, vstep1, tstep1 = load_csv(fname1)
    data2, vstep2, tstep2 = load_csv(fname2)
    cal_factor = 10 / 255 # this is a best guess for a signed 8 bit integer value and 5 divs per side, 10 divs total
    time = np.arange(0, len(data1)) * tstep1
    unit, unit_value = find_unit(tstep1)
    amplitude1 = data1 * vstep1 * cal_factor
    amplitude2 = data2 * vstep2 * cal_factor
    scaled_time = time * unit_value
    plt.plot(scaled_time, amplitude1)
    plt.plot(scaled_time, amplitude2)
    plt.xlabel(unit)
    plt.ylabel("V")
    plt.xlim([scaled_time[0], scaled_time[-1]])
    plt.grid()
    #plt.show()
    plt.savefig(fout)


if __name__ == "__main__":
    fname = argv[1]
    fout = fname[0:-4] + ".pdf"
    if len(argv) > 2:
        fout = argv[-1]
    if len(argv) > 3:
        plot_dual(argv[1], argv[2], fout)
    else:
        plot_single(fname, fout)
