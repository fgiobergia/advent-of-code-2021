import re
import numpy as np
from itertools import permutations
from scipy.spatial.distance import cdist, pdist
from collections import Counter

if __name__ == "__main__":

    with open("day19.input") as f:
        reads = []

        new_scanner = True
        scans = {}
        for line in f:
            line = line.strip()
            if not line:
                new_scanner = True
                continue
            if new_scanner:
                sid = int(re.match(r"--- scanner (\d+) ---", line).group(1))
                scans[sid] = []
                new_scanner = False
            else:
                scans[sid].append(list(map(int,line.split(","))))
        
    scans = { k: np.array(v) for k,v in scans.items() }

    eye = np.eye(3)
    mats = [ eye[list(i)] * f for i in list(permutations([0,1,2])) for f in [(1,1,1), (-1,1,1), (1,1,-1), (1,-1,1), (1,-1,-1), (-1,-1,1), (-1,1,-1), (-1,-1,-1)] ]

    j = 0
    merged = []
    scanners = [[0,0,0]]
    
    while len(merged) < len(scans)-1:
        j += 1
        if j % len(scans) == 0:
            j = 1
        if j in merged:
            continue
        
        for cmat in mats:
            prod = scans[j] @ cmat
            dists = cdist(scans[0], prod, metric="euclidean")
            dst, freq = Counter(dists.flatten()).most_common(1)[0]
            if freq >= 12:
                a, b = (dists==dst).nonzero()
                delta = (scans[0][a] - prod[b])[0]
                scanners.append(delta)
                scans[0] = np.unique(np.vstack([scans[0], prod + delta]), axis=0)
                merged.append(j)
    print(scans[0].shape[0])
    print(int(pdist(scanners, metric="cityblock").max()))