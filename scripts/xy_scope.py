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


def plot_xy(x_file, y_file, y_scale):
    x, x_vstep, _ = load_csv(x_file)
    y, y_vstep, _ = load_csv(y_file)
    cal_factor = 10 / 255 # this is a best guess for a signed 8 bit integer value and 5 divs per side, 10 divs total
    x_amp = x * x_vstep * cal_factor
    y_amp = y * y_vstep * cal_factor * y_scale
    plt.scatter(x_amp, y_amp, marker=".")
    plt.xlabel("Spannung [V]")
    plt.ylabel("Strom [mA]")
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    plt.show()


if __name__ == "__main__":
    num = argv[1][-4:]
    x_file = argv[1] + "/A" + num + "CH1.CSV"
    y_file = argv[1] + "/A" + num + "CH2.CSV"
    y_scale = 1000 / 100
    plot_xy(x_file, y_file, y_scale)
