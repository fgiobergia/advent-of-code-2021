from functools import reduce

def first_error(line):
    closer = { "{": "}", "(": ")", "[": "]", "<": ">"}
    stack = []
    for i, ch in enumerate(line):
        if ch in "([{<":
            stack.append(ch)
        else:
            el = stack.pop()
            if ch != closer[el]:
                return i, ch
    return "".join(map(closer.get, stack[::-1]))

def score_seq(seq):
    score_table = {")": 1, "]": 2, "}": 3, ">": 4}
    return reduce(lambda a,b: 5 * a + score_table[b], seq, 0)
    

if __name__ == "__main__":
    with open("day10.input") as f:
        lines = [ l.strip() for l in f.readlines() ]
    
    score_table = {")": 3, "]": 57, "}": 1197, ">": 25137}
    fe = [ first_error(line) for line in lines ]
    score = sum( score_table[e[1]] for e in fe if isinstance(e,tuple) )
    print(score)

    score = sorted([ score_seq(e) for e in fe if isinstance(e,str) ])
    print(score[len(score)//2])
