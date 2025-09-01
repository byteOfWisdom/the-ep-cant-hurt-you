#!python3
import numpy as np
from sys import argv
from matplotlib import pyplot as plt
from labtools.perror import ev, value, error
from scipy.optimize import curve_fit


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
    dv = 2 * vstep * cal_factor
    return scaled_time, amplitude, dt, dv


def get_freq(times, values, reject = 0):
    fft_values = np.abs(np.fft.fft(values))[reject:]
    freqs = np.fft.fftfreq(values.size, d = times[1] - times[0])[reject:]
    return ev(abs(freqs[fft_values == max(fft_values)])[0], freqs[1] - freqs[0])


def denoise(data, emphasis = 0.1):
    famp = np.fft.fft(data)
    famp[np.abs(famp) < emphasis * max(np.abs(famp))] = 0.0
    return np.real(np.fft.ifft(famp))


def get_Upp(voltages, conf = 0.99):
    #maybe add denoising here if single outliers are a problem
    v_sorted = np.array(list(sorted(voltages)))
    avg = sum(voltages) / len(voltages)
    upper = max(v_sorted[v_sorted > avg][:int(conf * len(v_sorted[v_sorted > avg]))])
    lower = min(v_sorted[v_sorted < avg][int((1.0 - conf) * len(v_sorted[v_sorted < avg])):])

    #voltages = denoise(voltages, 1 - conf)
    #upper = max(voltages)
    #lower = min(voltages)

    return upper - lower


def extract_data(fname1, fname2):
    t1, u1, dt1, dv1 = get_SI_values(fname1)
    t2, u2, dt2, dv2 = get_SI_values(fname2)
    f = 0.5 * (get_freq(t1, u1, 1) + get_freq(t2, u2, 1))
    v = ev(get_Upp(u2, 0.95), dv2) / ev(get_Upp(u1, 0.95), dv1)
    return f, v, ev(get_Upp(u1), dv1), ev(get_Upp(u2), dv2)


def pad(n):
    s = str(n)
    while len(s) < 4:
        s = "0" + s

    return s


def plot_stuff(name = ""):
    plt.grid(which="major")
    plt.grid(which="minor", linestyle=":", linewidth=0.5)
    plt.gca().minorticks_on()
    plt.legend()
    plt.show() if name == "" else plt.savefig(name)
    plt.cla()



def get(start):
    path = start[:-4]
    start_num = int(start[-4:])

    f_ch1 = path + pad(start_num) + f"/A{pad(start_num)}CH1.CSV"
    f_ch2 = path + pad(start_num) + f"/A{pad(start_num)}CH2.CSV"

    f, v, upp1, upp2 = extract_data(f_ch1, f_ch2)

    return upp1, upp2, v


linear = lambda x, a, b : a * x + b


if __name__ == "__main__":
    tbl = argv[1]
    files, rcs, res = [], [], []
    with open(tbl) as f:
        for line in f.readlines():
            files.append(line.split()[0])
            rcs.append(float(line.split()[1]))
            res.append(float(line.split()[2]))

    rcs, res = iter(rcs), iter(res)


    table_row = lambda rc, re, u1, u2, v, vtheo: f"${tex(rc)}$ & ${tex(re)}$ & $ {tex(u1)}$ & $ {tex(u2)}$ & $ {tex(v)} $ & $ {tex(vtheo)}$\\\\"
    Rc, Re, V = [], [], []
    for input in files:
        u1, u2, v = get(input)
        rc, re = next(rcs), next(res)
        Rc.append(rc)
        Re.append(re)
        V.append(0 - v)
        #print(table_row(rc, re, u1, u2, 0 - v, - round(rc / re, 2)))

    Rc = np.array(Rc)
    Re = np.array(Re)
    V = np.array(V)

    plt.errorbar(Re[Rc == 390], value(1 / V)[Rc == 390], yerr = error(1 / V)[Rc == 390], fmt=".", elinewidth=0.75, capsize=2, label=r"$R_c = \mathrm{const}$")
    plt.xlabel(r"$R_E$ [$\Omega$]")
    plt.ylabel("$v^{-1}$")

    fit, cov = curve_fit(linear, Re[Rc == 390], value(1 / V)[Rc == 390], sigma = error(1 / V)[Rc == 390])
    errs = np.sqrt(np.diag(cov))
    a = ev(fit[0], errs[0])
    b = ev(fit[1], errs[1])

    Rc_fit = - 1 / a
    v0 = 1 / b
    print(f"a1 = {a}")
    print(f"b1 = {b}")
    print(f"gefittet: Rc = {Rc_fit}")
    print(f"gefittet: v0 = {v0}")
    plt.plot(np.linspace(min(Re), max(Re), 1000), linear(np.linspace(min(Re), max(Re), 1000), a.value, b.value), label="Fitgrade")
    plot_stuff("res_amps_Rc_const.pdf")

    plt.errorbar(Rc[Re == 390], value(V)[Re == 390], yerr = error(V)[Re == 390], fmt=".", elinewidth=0.75, capsize=2, label=r"$R_e = \mathrm{const}$")
    plt.legend()
    plt.xlabel(r"$R_C$ [$\Omega$]")
    plt.ylabel("v")

    fit, cov = curve_fit(linear, Rc[Re == 390], value(V)[Re == 390], sigma = error(V)[Re == 390])
    errs = np.sqrt(np.diag(cov))
    a = ev(fit[0], errs[0])
    b = ev(fit[1], errs[1])

    beta = ev(-171.0, 6.0)
    v0_theo = ev(148, 6)
    rbe = 0 - beta * 390 / v0_theo
    print(f"rbe = {rbe}")

    a_theo = beta / (rbe + (beta + 1) * 390)

    print(f"a2 = {a}")
    print(f"a_t = {a_theo}")
    print(f"b2 = {b}")
    plt.plot(np.linspace(min(Re), max(Re), 1000), linear(np.linspace(min(Re), max(Re), 1000), a.value, b.value), label="Fitgrade")

    plot_stuff("res_amps_Re_const.pdf")
