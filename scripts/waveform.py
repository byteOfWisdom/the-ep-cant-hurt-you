#!python3
import numpy as np
from sys import argv
from matplotlib import pyplot as plt
from glob import glob


def load_csv(fname):
    with open(fname, "r") as file:
        raw = file.readlines()
        parse_line = lambda l: float(l.strip().strip(","))
        if raw[11].split(",")[0] == "Waveform Last Dot Address":
            data = np.array(list(map(parse_line, raw[17:17 + int(raw[11].split(",")[1])])))
        else:
            data = np.array(list(map(parse_line, raw[16:])))

        metadata = {}
        metadata["vdiff"] = float(raw[5].split(",")[1])
        if raw[11].split(",")[0] == "Waveform Last Dot Address":
            metadata["tdiff"] = float(raw[12].split(",")[1])
        else:
            metadata["tdiff"] = float(raw[11].split(",")[1])
        metadata["v_offset"] = float(raw[6].split(",")[1])

        return data, metadata["vdiff"], metadata["tdiff"], metadata["v_offset"]


def find_unit(interval):
    # leaving this function here as a joke.
    # maybe at some point it'll get a proper implementation
    if interval < 1e-5 and interval >= 1e-8:
        return r"$\mu s$", 1e6
    elif interval < 1e-2 and interval >= 1e-5:
        return r"$ms$", 1e3
    elif interval >= 1e-2:
        return r"$s$", 1.0
    return r"$s$", 1.0


def plot_single(fname, fout):
    data, vstep, tstep, offset = load_csv(fname)
    cal_factor = 10 / 255 # this is a best guess for a signed 8 bit integer value and 5 divs per side, 10 divs total
    time = np.arange(0, len(data)) * tstep
    unit, unit_value = find_unit(tstep)
    amplitude = data * vstep * cal_factor
    if dn != 0.0:
        amplitude = denoise(amplitude, dn)

    scaled_time = time * unit_value
    plt.plot(scaled_time, amplitude)
    plt.xlabel(unit)
    plt.ylabel("V")
    plt.xlim([scaled_time[0], scaled_time[-1]])
    #offset = - sum(amplitude) / len(amplitude)
    #print(f"average voltage = {sum(amplitude) / len(amplitude)}V")
    plt.ylim([-4.5 * vstep - offset, 4.5 * vstep + offset])
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()

    if fout[-4:] == ".pdf":
        plt.savefig(fout)
    else:
        plt.show()

def plot_dual(fname1, fname2, fout):
    global dn
    data1, vstep1, tstep1, offset_1 = load_csv(fname1)
    data2, vstep2, tstep2, offset_2 = load_csv(fname2)
    cal_factor = 10 / 255 # this is a best guess for a signed 8 bit integer value and 5 divs per side, 10 divs total
    time = np.arange(0, len(data1)) * tstep1
    unit, unit_value = find_unit(tstep1)
    amplitude1 = data1 * vstep1 * cal_factor
    amplitude2 = data2 * vstep2 * cal_factor
    if dn != 0.0:
        amplitude1 = denoise(amplitude1, dn)
        amplitude2 = denoise(amplitude2, dn)

    scaled_time = time * unit_value

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    #famp1 = np.fft.fft(amplitude1)
    #famp1[np.abs(famp1) < 0.1 * max(np.abs(famp1))] = 0.0
    #amplitude1 = np.fft.ifft(famp1)

    #famp2 = np.fft.fft(amplitude2)
    #famp2[np.abs(famp2) < 0.1 * max(np.abs(famp2))] = 0.0
    #amplitude2 = np.fft.ifft(famp2)

    p1 = ax1.plot(scaled_time, amplitude1 + offset_1, label="CH1", color="tab:blue")
    p2 = ax2.plot(scaled_time, amplitude2 + offset_2, label="CH2", color="tab:orange")

    ax1.set_ylim(-4.5 * vstep1 - offset_1, 4.5 * vstep1 + offset_1)
    ax2.set_ylim(-4.5 * vstep2 - offset_2, 4.5 * vstep2 + offset_2)

    ax1.set_xlabel(unit)
    ax1.set_ylabel("V", color="tab:blue")
    ax1.set_xlim(scaled_time[0], scaled_time[-1])

    ax1.grid(which="major")
    ax1.grid(which="minor", linestyle=":", linewidth=0.5)
    ax1.minorticks_on()
    ax2.set_ylabel("V", color="tab:orange")
    ax2.tick_params(axis="y",labelcolor="tab:orange")
    ax1.tick_params(axis="y",labelcolor="tab:blue")
    ax1.legend(p1 + p2, [l.get_label() for l in p1 + p2])

    if fout[-4:] == ".pdf":
        plt.savefig(fout)
    else:
        plt.show()


def pad(n):
    s = str(n)
    while len(s) < 4:
        s = "0" + s

    return s


if __name__ == "__main__":
    global dn
    path = argv[1][:-4]
    num = int(argv[1][-4:])

    fout =  argv[2] if len(argv) > 2 and argv[2][-4:] == ".pdf" else "/dev/zero"
    dn = float(argv[3]) if len(argv) > 3 else 0.0

    if len(glob(argv[1] + "/*.CSV")) > 1:
        plot_dual(argv[1] + f"/A{pad(num)}CH1.CSV", argv[1] + f"/A{pad(num)}CH2.CSV", fout)
    else:
        plot_single(glob(argv[1] + "/*.CSV")[0], fout)
