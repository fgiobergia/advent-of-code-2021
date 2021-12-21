import re

def throw_die(pos_a, pos_b, cumul_a, cumul_b, score_a, score_b, table, curr_throw):
    if (pos_a, pos_b, cumul_a, cumul_b, score_a, score_b, curr_throw % 6) in table:
        return table[(pos_a, pos_b, cumul_a, cumul_b, score_a, score_b, curr_throw % 6)]

    if curr_throw % 6 == 3: 
        # a finished playing -- sum values in cumul_a, compute new position and add to score
        pos_a = (pos_a + sum(cumul_a)) % 10
        score_a = score_a + pos_a + 1
        cumul_a = ()

        if score_a >= 21:
            # finished!
            return (1,0)
    
    if curr_throw and curr_throw % 6 == 0: # avoid case curr_throw = 0
        pos_b = (pos_b + sum(cumul_b)) % 10
        score_b = score_b + pos_b + 1
        cumul_b = ()

        if score_b >= 21:
            return (0,1)

    if curr_throw % 6 < 3:
        # a throws
        wins_ab = [ throw_die(pos_a, pos_b, cumul_a + (i,), cumul_b, score_a, score_b, table, curr_throw + 1) for i in [1,2,3] ]

    else:
        wins_ab = [ throw_die(pos_a, pos_b, cumul_a, cumul_b +(i,), score_a, score_b, table, curr_throw + 1) for i in [1,2,3] ]

    wins_a = sum([ w_a for w_a,_ in wins_ab ])
    wins_b = sum([ w_b for _, w_b in wins_ab ])

    table[(pos_a, pos_b, cumul_a, cumul_b, score_a, score_b, curr_throw % 6)] = (wins_a, wins_b)
    
    return wins_a, wins_b

def roll(die):
    return die + 1 if die < 100 else 1

if __name__ == "__main__":

    with open("day21.input") as f:
        init_pos_a = int(re.match(r".+position: (\d)$", f.readline()).group(1)) - 1
        init_pos_b = int(re.match(r".+position: (\d)$", f.readline()).group(1)) - 1

    die = 0
    rolls = 0
    pos = [init_pos_a, init_pos_b]
    scores = [0, 0]

    i = 0
    while True:
        d1 = roll(die)
        d2 = roll(d1)
        d3 = roll(d2)

        pos[i] = (pos[i] + d1 + d2 + d3) % 10
        scores[i] += pos[i] + 1 # counting from 0 for positions
        rolls += 3
        die = d3
        if scores[i] >= 1000:
            break
        
        i = (i+1) % 2


    print((scores[1] if scores[0] >= 1000 else scores[0]) * rolls)
    print(max(throw_die(init_pos_a, init_pos_b, (), (), 0, 0, {}, 0)))