#!python3
import numpy as np
from sys import argv
from matplotlib import pyplot as plt
from labtools.perror import ev, value, error

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
    return r"$s$", 1.0


def get_SI_values(fname):
    data, vstep, tstep, offset = load_csv(fname)
    cal_factor = 10 / 255 # this is a best guess for a signed 8 bit integer value and 5 divs per side, 10 divs total
    time = np.arange(0, len(data)) * tstep
    unit, unit_value = find_unit(tstep)
    amplitude = data * vstep * cal_factor
    scaled_time = time * unit_value
    dt = scaled_time[1] - scaled_time[0]
    dv = vstep * cal_factor
    return scaled_time, amplitude, dt, dv


def get_freq(times, values):
    fft_values = np.abs(np.fft.fft(values))
    freqs = np.fft.fftfreq(values.size, d = times[1] - times[0])
    return ev(abs(freqs[fft_values == max(fft_values)])[0], freqs[1] - freqs[0])


def get_Upp(voltages):
    #maybe add denoising here if single outliers are a problem
    return min(voltages) - max(voltages)


def extract_data(fname1, fname2):
    t1, u1, dt1, dv1 = get_SI_values(fname1)
    t2, u2, dt2, dv2 = get_SI_values(fname2)
    f = 0.5 * (get_freq(t1, u1) + get_freq(t2, u2))
    v = ev(get_Upp(u2), dv2) / ev(get_Upp(u1), dv1)
    return f, v


def pad(n):
    s = str(n)
    while len(s) < 4:
        s = "0" + s
    return s


def collate(start, count):
    path = start[:-4]
    start_num = int(start[-4:])

    amps = []
    damps = []
    freqs = []
    dfreqs = []

    for i in range(start_num, start_num + count):
        f_ch1 = path + pad(i) + f"/A{pad(i)}CH1.CSV"
        f_ch2 = path + pad(i) + f"/A{pad(i)}CH2.CSV"

        f, v = extract_data(f_ch1, f_ch2)
        freqs.append(f.value)
        dfreqs.append(f.error)
        amps.append(v.value)
        damps.append(v.error)

    plt.errorbar(freqs, amps, fmt=".", yerr=damps, xerr=dfreqs)


if __name__ == "__main__":
    collate(argv[1], int(argv[2]))
    if len(argv) > 3:
        collate(argv[3], int(argv[4]))

    plt.xlabel("ln(Frequenz) [ln(Hz)]")
    plt.ylabel("Verstärkung")
    plt.grid()
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    #plt.legend()
    plt.loglog()
    plt.show()
