#!python3
import numpy as np
from sys import argv
from matplotlib import pyplot as plt
from labtools.perror import ev, value, error
from scipy.optimize import curve_fit

def c_iter():
    yield "tab:blue"
    yield "tab:cyan"
    yield "tab:orange"
    yield "tab:red"

colors = c_iter()

ref_fg = 0
ref_ft = 0


def tex(v):
    s = str(v)
    if "^" in s:
        s = s.replace("^", "^{")
        s += "}"
    s = s.replace("+-", r"\pm").replace("*", r"\cdot ")
    return s


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
    dv = 4 * vstep * cal_factor
    return scaled_time, amplitude, dt, dv


def denoise(data, emphasis = 0.1):
    famp = np.fft.fft(data)
    cutoff = sorted(famp)[int(1.0 - emphasis):]
    famp[np.abs(famp) < cutoff] = 0.0
    return np.real(np.fft.ifft(famp))


def get_freq(times, values, reject = 0):
    fft_values = np.abs(np.fft.fft(values))[reject:]
    freqs = np.fft.fftfreq(values.size, d = times[1] - times[0])[reject:]
    return ev(abs(freqs[fft_values == max(fft_values)])[0], freqs[1] - freqs[0])


def get_Upp(voltages, conf = 0.99):
    #maybe add denoising here if single outliers are a problem
    v_sorted = np.array(list(sorted(voltages)))
    avg = sum(voltages) / len(voltages)
    upper = max(v_sorted[v_sorted > avg][:int(conf * len(v_sorted[v_sorted > avg]))])
    lower = min(v_sorted[v_sorted < avg][int((1.0 - conf) * len(v_sorted[v_sorted < avg])):])

    #voltages = denoise(voltages, 1 - conf)
    #upper = max(voltages)
    #lower = min(voltages)

    #print(f"{lower} to {upper}")
    return upper - lower



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


def collate(start, count, name):
    global ref_ft, ref_fg
    path = start[:-4]
    start_num = int(start[-4:])

    amps = np.zeros(count)
    damps = np.zeros(count)
    freqs = np.zeros(count)
    dfreqs = np.zeros(count)
    print(name)

    for i in range(start_num, start_num + count):
        f_ch1 = path + pad(i) + f"/A{pad(i)}CH1.CSV"
        f_ch2 = path + pad(i) + f"/A{pad(i)}CH2.CSV"


        f, v, u1, u2 = extract_data(f_ch1, f_ch2)
        freqs[i - start_num] = f.value
        dfreqs[i - start_num] = f.error
        amps[i - start_num] = v.value
        damps[i - start_num] = v.error
        #print(r"$ " + tex(u1) + "$&$" + tex(u2) + "$&$" + tex(v) + "$&$" + tex(f) + r"$\\")


    # ensure frequencies vaguely in ascending order
    order = freqs.argsort()
    freqs = freqs[order]
    dfreqs = dfreqs[order]
    amps = amps[order]
    damps = damps[order]

    # find ft und fg
    fg, ft = 0, 0
    dfg, dft = 0, 0
    i = np.where(freqs == freqs[amps <= amps[0] / np.sqrt(2)][0])[0][0]
    fg = 0.5 * (freqs[i] + freqs[i - 1])
    dfg = 0.5 * (freqs[i] - freqs[i - 1])


    if min(amps) > 1:
        ft = freqs[-1]
        dft = 0.5 * (freqs[-1] - freqs[-2])
    else:
        i = np.where(freqs == freqs[amps <= 1.0][0])[0][0]
        ft = 0.5 * (freqs[i] + freqs[i - 1])
        dft = 0.5 * (freqs[i] - freqs[i - 1])

    dft = max(dft, dfreqs[-1])


    print(name)
    print(f"grenzfrequenz = {ev(fg, dfg)}")
    print(f"transitfrequezn = {ev(ft, dft)}")
    print()

    if ref_fg == 0:
        ref_fg = ev(fg, dfg)
        ref_ft = ev(ft, dft)
    else:
        print(f"verhältniss grenz = {ev(fg, dfg) / ref_fg}")
        print(f"verhältniss trans = {ev(ft, dft) / ref_ft}")

    fgc = next(colors)
    plt.hlines(amps[0] / np.sqrt(2), min(freqs), max(freqs) * 1.1, color=fgc, linestyle = "--")
    plt.vlines(fg, 0.9, max(amps), label="$f_\\text{g, " + name + "}$" if name != "" else "$f_g$", color = fgc, linestyle="--")
    plt.vlines(ft, 0.9, max(amps), label="$f_\\text{t, " + name + "}$" if name != "" else "$f_t$", color = next(colors), linestyle="--")

    plt.errorbar(freqs, amps, fmt=" ", yerr=damps, xerr=dfreqs, label=name, elinewidth=0.75, capsize=2, color = fgc)


if __name__ == "__main__":
    collate(argv[1], int(argv[2]), "ohne Kaskode" if len(argv) > 3 else "")
    if len(argv) > 3:
        collate(argv[3], int(argv[4]), "mit Kaskode" if len(argv) > 3 else "")

    plt.xlabel("Frequenz [Hz]")
    plt.ylabel("Verstärkung")
    plt.loglog()
    plt.grid()
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    plt.legend(loc="lower left")

    plt.show()
