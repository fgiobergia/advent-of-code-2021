import re 
from math import copysign

def launch(vx, vy, x1, x2, y1, y2):
    x = 0
    y = 0
    found = False
    y_max = y
    while True:
        y_max = max(y_max, y)

        if y < min(y1, y2) and vy < 0:
            break

        if x1 <= x <= x2 and y1 <= y <= y2:
            found = True
            break
        x += vx
        y += vy
        vx += -copysign(1, vx) * (vx != 0)
        vy -= 1

    return found, y_max

if __name__ == "__main__":
    with open("day17.input") as f:
        inp = f.read()

    m = re.match(r".+x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", inp)
    x1, x2, y1, y2 = [ int(m.group(i)) for i in range(1,5) ]

    y_max = 0
    pairs = 0
    # forgive me father for I have brute force'd
    for vx in range(0, max(abs(x1), abs(x2))+1, 2 * (x1>0) - 1 ):
        for vy in range(-max(abs(y1), abs(y2))-1, max(abs(y1), abs(y2))+1):
            found, m = launch(vx, vy, x1, x2, y1, y2)
            if found:
                pairs += 1
                y_max = max(y_max, m)
    print(y_max)
    print(pairs)