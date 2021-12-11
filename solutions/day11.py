import numpy as np

def run_epoch(emap):
    emap += 1
    fired = emap > 9
    fired_list = list(zip(*np.nonzero(fired)))
    grid = np.indices(emap.shape)

    i = 0
    while i < len(fired_list):
        a,b = fired_list[i]

        a_from = max(0, a-1)
        a_to = min(emap.shape[0], a+2)
        b_from = max(0, b-1)
        b_to = min(emap.shape[1], b+2)
        neighbors = grid[0, a_from:a_to, b_from:b_to], grid[1, a_from:a_to, b_from:b_to]

        emap[neighbors] += 1 
        new_fired = (emap > 9) & ~fired
        fired_list.extend(list(zip(*np.nonzero(new_fired))))
        fired = fired | new_fired

        i += 1
    emap[fired] = 0
    return fired.sum()

if __name__ == "__main__":
    with open("day11.input") as f:
        emap = np.array([ list(map(int, line.strip())) for line in f.readlines() ])
    emap_copy = emap.copy()

    print(sum(run_epoch(emap) for _ in range(100)))

    i = 1
    while run_epoch(emap_copy) != np.product(emap_copy.shape):
        i += 1
    print(i)