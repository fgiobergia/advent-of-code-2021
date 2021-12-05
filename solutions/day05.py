import numpy as np
import re

if __name__ == "__main__":
    with open("day05.input") as f:
        pts = []
        for line in f.readlines():
            m = re.match(r"^(\d+),(\d+) -> (\d+),(\d+)$", line.strip())
            pts.append([ int(m.group(i)) for i in range(1,5)])
    pts = np.array(pts)

    field = np.zeros((pts[:,[1,3]].max()+1, pts[:,[0,2]].max()+1))
    diag =  np.zeros((pts[:,[1,3]].max()+1, pts[:,[0,2]].max()+1))

    for x1,y1, x2, y2 in pts:
        offx = 2 * int(x1 < x2) -1
        offy = 2 * int(y1 < y2) -1
        rx = np.arange(x1, x2+offx, offx)
        ry = np.arange(y1, y2+offy, offy)
        if x1 == x2 or y1 == y2:
            field[ry,rx] += 1
        else:
            diag[ry,rx] += 1
    
    print((field>=2).sum())
    print((field+diag>=2).sum())