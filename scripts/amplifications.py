#!python3
import numpy as np
from sys import argv

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
    return scaled_time, amplitude


def get_freq(times, values):
    fft_values = np.abs(np.fft.fft(values))
    freqs = np.fft.fftfreq(values.size(), d = times[1] - times[0])
    return freqs[max(fft_values)]


def extract_data(fname):
    t, u = get_SI_values(fname)
    f = get_freq(t, u)
    return f


def pad(n):
    s = str(n)
    while len(s) > 4:
        s = "0" + s
    return s


if __name__ == "__main__":
    start = argv[1]
    path = start[:-4]
    start_num = int(start[-4:])
    count = int(argv[2])

    for i in range(start_num, start_num + count):
        f_ch1 = path + pad(i) + f"/A{pad(i)}CH1.CSV"
        f_ch2 = path + pad(i) + f"/A{pad(i)}CH2.CSV"

        print(extract_data(f_ch1))
        print(extract_data(f_ch2))
