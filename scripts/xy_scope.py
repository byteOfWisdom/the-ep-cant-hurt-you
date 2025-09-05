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


def load_voltages(fname):
    v, vstep, _ = load_csv(fname)
    cal_factor = 10 / 255 # this is a best guess for a signed 8 bit integer value and 5 divs per side, 10 divs total
    v_amp = v * vstep * cal_factor
    plt.xlim(- 10 * vstep, 10 * vstep)
    plt.ylim(- 10 * vstep, 10 * vstep)
    return list(v_amp)


def chop_with_adjacency(xs, ys):
    xs = np.array(xs)
    ys = np.array(ys)
    dists = np.append((xs[1:] - xs[:-1]) ** 2 + (ys[1:] - ys[:-1]) ** 2, [0])
    avg_dist = sum(dists) / len(dists)
    value_chunks = []
    yacc, xacc = [], []
    for i in range(len(xs)):
        xacc.append(xs[i])
        yacc.append(ys[i])
        if dists[i] > 2 * avg_dist:
            value_chunks.append((xacc, yacc))
            xacc, yacc = [], []
    value_chunks.append((xacc, yacc))
    return value_chunks



def plot_xy(xdata, ydata, y_scale):
#    x, x_vstep, _ = load_csv(x_file)
#    y, y_vstep, _ = load_csv(y_file)
#    cal_factor = 10 / 255 # this is a best guess for a signed 8 bit integer value and 5 divs per side, 10 divs total
#    x_amp = x * x_vstep * cal_factor
#    y_amp = y * y_vstep * cal_factor * y_scale
    default = False
    if default:
        plt.scatter(xdata, np.array(ydata) * y_scale, marker=".", s =0.5)
    else:
        for x_chunk, y_chunk in chop_with_adjacency(xdata, ydata):
            plt.plot(x_chunk, np.array(y_chunk) * y_scale, color="tab:blue")
    plt.xlabel("Spannung [V]")
    plt.ylabel("Strom [mA]")
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
    #plt.savefig(argv[1] + ".pdf")


if __name__ == "__main__":
    xdata, ydata = [], []
    for file in argv[1:]:
        num = file[-4:]
        x_file = file + "/A" + num + "CH1.CSV"
        y_file = file + "/A" + num + "CH2.CSV"
        xdata += load_voltages(x_file)
        ydata += load_voltages(y_file)
    y_scale = 1000 / 500
    plot_xy(xdata, ydata, y_scale)
