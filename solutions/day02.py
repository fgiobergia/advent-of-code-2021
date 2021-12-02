from functools import reduce

def update(state, cmd):
    hor, ver, aim = state
    op, val = cmd
    if op == "forward":
        return hor + val, ver + val * aim, aim
    return hor, ver, aim + val * (2 * (op == "down") -1)

if __name__ == "__main__":
    with open("day02.input") as f:
        cmds = list(map(lambda x: (x[0],int(x[1])), [ l.strip().split() for l in f.readlines() ]))

    hor = sum(c[1] for c in cmds if c[0] == "forward")
    ver = sum(c[1] * (2 * (c[0] == "down") -1) * (c[0] != "forward") for c in cmds)
    print(hor * ver)

    hor, ver, _ = reduce(update, cmds, (0, 0, 0))
    print(hor * ver)
