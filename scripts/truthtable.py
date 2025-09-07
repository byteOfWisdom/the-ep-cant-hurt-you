#!python
from sys import argv
func = None


def parse_expr(expr):
    vars = expr.replace("|", " ").replace("^", " ").replace("~", " ").split()
    fstring = "func = lambda " + ", ".join(vars) + ": " + expr.replace("|", "|").replace("^", "&").replace("~", "!")
    exec("global func; " + fstring)
    return vars, func


def gen_values(f, num_vars):
    res = []
    for i in range(2 ** num_vars):
        bits = list(reversed([(i & (1 << x)) >> x for x in range(num_vars)]))
        res.append(bits + [f(*bits)])
    return res


if __name__ == "__main__":
    expr = " ".join(filter(lambda x: not x.startswith("-"), argv[1:]))
    args = list(filter(lambda x: x.startswith("-"), argv[1:]))

    vars, func = parse_expr(expr)
    valuetable = gen_values(func, len(vars))

    if "-t" in args:
        pass # print latex table
    else:
        print(" ".join(vars) + " =")
        for line in valuetable:
            print(" ".join(map(str, line)))
