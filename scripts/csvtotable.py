from sys import argv

with open(argv[1]) as file:
    for line in file.readlines()[1:]:
        print(r"$ \num{" + line.split(", ")[0] + r"(1)} $ & $ \num{" + line.split(", ")[1].strip() + r"(1)} $ \\")
