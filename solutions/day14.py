from collections import defaultdict
from functools import reduce

def repls(s, m):
    new_combs = defaultdict(lambda: 0)
    for comb, coef in s.items():
        rule = m[comb]
        new_combs[comb[0] + rule] += coef
        new_combs[rule + comb[1]] += coef
    return new_combs

def count_el(s, seq):
    c = defaultdict(lambda: 0)
    for k,v in s.items():
        c[k[0]] += v
        c[k[1]] += v
    ret = { k: v // 2 for k,v in c.items() }
    ret[seq[0]] += 1 # 1st and last element appear only once!
    ret[seq[-1]] += 1
    return ret

if __name__ == "__main__":
    with open("day14.input") as f:
        seq = f.readline().strip()
        f.readline()
        mapper = { l[0]: l[1] for l in [ line.strip().split(" -> ") for line in f.readlines() ] }

        combs = defaultdict(lambda: 0)
        for i in range(len(seq)-1):
            combs[seq[i:i+2]] += 1

        combs = reduce(lambda c, _: repls(c, mapper), range(10), combs)
        c = count_el(combs, seq)
        print(max(c.values()) - min(c.values()))

        combs = reduce(lambda c, _: repls(c, mapper), range(30), combs)
        c = count_el(combs, seq)
        print(max(c.values()) - min(c.values()))
