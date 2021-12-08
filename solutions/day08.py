from collections import Counter
    
def find_mapping(obs):
    cnt = Counter("".join(obs))

    b = [ k for k,v in cnt.items() if v == 6][0]
    e = [ k for k,v in cnt.items() if v == 4][0]
    f = [ k for k,v in cnt.items() if v == 9][0]

    ac = [ k for k,v in cnt.items() if v == 8]
    dg = [ k for k,v in cnt.items() if v == 7] 

    one = set([ o for o in obs if len(o) == 2 ][0])
    seven = set([ o for o in obs if len(o) == 3 ][0])
    four = set([ o for o in obs if len(o) == 4 ][0])

    a = seven - one
    c = list(set(ac) - a)[0]
    a = list(a)[0]

    d253 = [ set(o) for o in obs if len(o) == 5 ]
    three = set(d253[0] if len(d253[1] | d253[2]) == 7 else d253[1] if len(d253[0] | d253[2]) == 7 else d253[2])

    d = (three - seven) & four
    g = list(set(dg) - d)[0]
    d = list(d)[0]

    return g,f,e,d,c,b,a


if __name__ == "__main__":
    with open("day08.input") as f:
        lines = [ [ v.strip().split(" ") for v in line.split(" | ") ] for line in f.readlines() ]
    
    print(sum(sum(len(v) in [2,4,3,7] for v in l[1]) for l in lines))

    vals = [
        0b1110111,
        0b0010010,
        0b1011101,
        0b1011011,
        0b0111010,
        0b1101011,
        0b1101111,
        0b1010010,
        0b1111111,
        0b1111011
    ]

    csum = 0
    for obs, reading in lines:
        mapping = find_mapping(obs)
        csum += sum( 10**(3-i) * vals.index(sum( 2**mapping.index(x) for x in r )) for i, r in enumerate(reading) )
    print(csum)