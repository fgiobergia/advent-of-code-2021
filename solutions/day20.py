import numpy as np

def apply_algo(grid, algo, iter=0):
    # this switch only works for inputs that have 
    # algo[0] = "#" (i.e. turn on if all are off) 
    # and algo[511] = "." (i.e. turn off if all are on).
    # Since this appears to be the case for the "real"
    # input (not the example one), this part of code is left here.
    if iter % 2 == 1:
        new_grid = np.zeros(grid.shape, dtype=bool)
    else:
        new_grid = np.ones(grid.shape, dtype=bool)
    for i in range(1, grid.shape[0]-1):
        for j in range(1, grid.shape[1]-1):
            new_grid[i,j] = algo[(2**np.arange(8, -1, -1)[grid[i-1:i+2, j-1:j+2].flatten()]).sum()]
    return new_grid

if __name__ == "__main__":
    with open("day20.input") as f:
        algo = np.array(list(f.readline())) == "#"
        f.readline()
        
        grid = []
        for line in f:
            grid.append(list(line.strip()))
        grid = np.array(grid) == "#"

        n_iters = 50
        padding = 4 * n_iters
        big_grid = np.zeros((grid.shape[0] + padding, grid.shape[1] + padding), dtype=bool)
        big_grid[padding//2:-padding//2, padding//2:-padding//2] = grid

        for i in range(2):
            big_grid = apply_algo(big_grid, algo, i)
        print(big_grid.sum())

        for i in range(48):
            big_grid = apply_algo(big_grid, algo, i)
        print(big_grid.sum())