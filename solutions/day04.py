import numpy as np

if __name__ == "__main__":
    with open("day04.input") as f:
        num = list(map(int, f.readline().split(",")))
        boards = []
        lines = f.readlines()
        while lines:
            lines.pop(0)
            b = [ list(map(int, [ x for x in lines.pop(0).split(" ") if x.strip()] )) for _ in range(5) ]
            boards.append(b)
    
    boards = np.array(boards)
    masks = np.zeros(boards.shape).astype(bool)
    sol1 = False # only print 1st board that solves the 1st problem
    for n in num:
        masks[boards == n] = 1 # update drawn numbers
        # check for winners (vertically and horizontally)
        vert = masks.sum(axis=1) == 5
        horiz = masks.sum(axis=2) == 5

        # if there are winners, and they are the first (sol1==False)
        if (vert.any() or horiz.any()) and not sol1:
            pos, _ = vert.nonzero() if vert.any() else horiz.nonzero() # find the winning board
            print(boards[pos[0]][~masks[pos[0]]].sum() * n)
            sol1 = True

        # if all boards have at least 1 winning row-column
        if (vert.any(axis=1)|horiz.any(axis=1)).all():
            masks[boards == n] = 0 # "un-draw" the latest number 
            vert = masks.sum(axis=1) == 5
            horiz = masks.sum(axis=2) == 5
            # and get the only board that has no winning row/col (i.e. the
            # board that wins when adding the current n)
            pos = (~(vert.any(axis=1)|horiz.any(axis=1))).nonzero()
            print((boards[pos[0]][~masks[pos[0]]].sum() - n) * n)
            break
