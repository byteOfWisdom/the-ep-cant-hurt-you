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
    return max(voltages) - min(voltages)


def extract_data(fname1, fname2):
    t1, u1, dt1, dv1 = get_SI_values(fname1)
    t2, u2, dt2, dv2 = get_SI_values(fname2)
    f = 0.5 * (get_freq(t1, u1) + get_freq(t2, u2))
    v = ev(get_Upp(u2), dv2) / ev(get_Upp(u1), dv1)
    return f, v, ev(get_Upp(u1), dv1), ev(get_Upp(u2), dv2)


def pad(n):
    s = str(n)
    while len(s) < 4:
        s = "0" + s

    return s


def say(start):
    path = start[:-4]
    start_num = int(start[-4:])

    f_ch1 = path + pad(start_num) + f"/A{pad(start_num)}CH1.CSV"
    f_ch2 = path + pad(start_num) + f"/A{pad(start_num)}CH2.CSV"

    f, v, upp1, upp2 = extract_data(f_ch1, f_ch2)

    print(f"estimated freq: f = {f} Hz")
    print(f"estimated amp: v = {v}")
    print(f"U_pp_ch1 = {upp1}")
    print(f"U_pp_ch2 = {upp2}")


if __name__ == "__main__":
    say(argv[1])
