#!python3
from glob import glob
from sys import argv
from os import system

if __name__ == "__main__":
    script = "/".join(argv[0].split("/")[:-1]) + "/waveform.py"
    for file in glob(argv[1] + "/**/*.CSV"):
        out = (file[:-4] + ".pdf").split("/")[-1]
        system("python " + script + " " + file + " ./" + out)
