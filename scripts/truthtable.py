#!python
from sys import argv
func = None


def parse_expr(expr):
    vars = expr.replace("|", " ").replace("^", " ").replace("~", " ").replace("(", " ").replace(")", " ").replace("/", " ").split()
    vars = sorted(list(set(vars)))
    fstring = "func = lambda " + ", ".join(vars) + ": int(" + expr.replace("|", " or ").replace("^", " and ").replace("~", " not ").replace("/", " ^ ") + ")"
    exec("global func; " + fstring)
    return vars, func


def gen_values(f, num_vars):
    res = []
    for i in range(2 ** num_vars):
        bits = list(reversed([(i & (1 << x)) >> x for x in range(num_vars)]))
        res.append(bits + [f(*bits)])
    return res


def print_header(num_vars):
    print(r"\begin{table}[H]")
    print(r"\centering")
    format_spec = "{" + "".join(("c" for _ in range(num_vars))) + "|c}"
    print(r"\begin{tabular}" + format_spec)


def print_footer():
    print(r"\end{tabular}")
    print(r"\caption{Eine Wahrheitstabelle!}")
    print(r"\label{tab:truths}")
    print(r"\end{table}")


if __name__ == "__main__":
    expr = " ".join(filter(lambda x: not x.startswith("-"), argv[1:]))
    args = list(filter(lambda x: x.startswith("-"), argv[1:]))

    vars, func = parse_expr(expr)
    valuetable = gen_values(func, len(vars))

    if "-t" in args:
        print_header(len(vars))
        print("&".join(vars) + "&$=$\\\\\\hline")
        for line in valuetable:
            print("&".join(map(str, line)) + "\\\\")
        print_footer()

    else:
        print(" ".join(vars) + " =")
        for line in valuetable:
            print(" ".join(map(str, line)))
