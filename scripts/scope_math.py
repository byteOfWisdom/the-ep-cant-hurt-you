#!python3
import numpy as np
from sys import argv


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
    return list(v_amp)

if __name__ == "__main__":
    if len(argv) > 2:
        u1 = load_voltages(argv[1])
        u2 = load_voltages(argv[2])
        print(f"v_avg_1 = {sum(u1) / len(u1)}V")
        print(f"v_avg_2 = {sum(u2) / len(u2)}V")
        print(f"V_pp_1 = {max(u1) - min(u1)}")
        print(f"V_pp_2 = {max(u2) - min(u2)}")
        print(f"v_diff = {sum(np.array(u1) - np.array(u2)) / len(u1)}V")
    else:
        u1 = load_voltages(argv[1])
        print(f"v_avg_1 = {sum(u1) / len(u1)}V")
