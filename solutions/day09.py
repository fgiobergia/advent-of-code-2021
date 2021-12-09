import numpy as np
from scipy.signal import convolve2d
from functools import reduce

def fill(hmap, mask, x, y):
    if not (0 <= x < hmap.shape[1]) or not(0 <= y < hmap.shape[0]) or hmap[y,x] == 9 or mask[y,x] == 1:
        return

    mask[y,x] = 1
    fill(hmap, mask, x-1, y)
    fill(hmap, mask, x+1, y)
    fill(hmap, mask, x, y-1)
    fill(hmap, mask, x, y+1)

if __name__ == "__main__":
    with open("day09.input") as f:
        hmap = np.array([ list(map(int, list(l.strip()))) for l in f.readlines() ])

    masks = [
        (np.array([[-1,1]]),   (0, hmap.shape[0], 1, hmap.shape[1]+1)),
        (np.array([[1,-1]]),   (0, hmap.shape[0], 0, -1)),
        (np.array([[-1],[1]]), (1, hmap.shape[0]+1, 0, hmap.shape[1])),
        (np.array([[1],[-1]]), (0, -1, 0, hmap.shape[1])),
    ]
    m = [ convolve2d(hmap, mask, mode="full", boundary="fill", fillvalue=9)[y1:y2, x1:x2]<0 for mask, (y1, y2, x1, x2) in masks ]
    fmask = reduce(lambda a, b: a & b, m)
    print(hmap[fmask].sum() + fmask.sum())

    basin_sizes = []
    for y, x in zip(*np.nonzero(fmask)):
        mask = np.zeros(hmap.shape)
        fill(hmap, mask, x, y)
        basin_sizes.append(mask.sum())
    
    print(int(np.product(np.partition(basin_sizes, kth=-3)[-3:])))