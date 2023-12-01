from copy import deepcopy

def move(burrows, corridor, curr_cost, known_states={}):

    key = f"{burrows}|{corridor}"
    if key in known_states:
        return curr_cost + known_states[key]
        
    costs = {
        "A": 1, "B": 10, "C": 100, "D": 1000
    }
    addresses = {
        "A": 2, "B": 4, "C": 6, "D": 8
    }
    # end conditions
    if all([ burrows[c] == [c] * len(burrows[c]) for c in "ABCD" ]):
        # aa,bb,cc,dd => finished
        return curr_cost

    # try moving everything that can be moved

    all_scores = []

    # first, everything in the corridor:
    pos = 0
    while pos < len(corridor):
        am = corridor[pos]
        if am == " ":
            pos += 1
            continue # nothing there to move

        # something to move, check if it can go to
        # its burrow (if not, it cannot move)

        if all([ c == am or c == " " for c in burrows[am]]):
            # burrow is open for business, see if there's a path there
            
            # here, we assume that addresses[AM] will be empty
            # (if AMs can stop in front of burrows, something changes here)
            start = min(pos+1, addresses[am]+1) # using pos+1 to exclude the AM itself
            stop = max(pos, addresses[am]) # no need to exclude AM since it would be a :stop

            if all([ c==" " for c in corridor[start : stop] ]):
                # empty corridor, can go!

                # not burrows[am] => if empty, 1 extra step needs to be taken
                new_steps = (stop - start + 1)
                burrow_steps = sum([ c == ' ' for c in burrows[am] ])# walk down the burrow
                new_steps += burrow_steps
                
                new_cost = new_steps * costs[am]

                new_burrows = deepcopy(burrows)
                new_burrows[am][burrow_steps-1] = am
                new_corridor = corridor[:]
                new_corridor[pos] = " "

                score = move(new_burrows, new_corridor, curr_cost + new_cost, known_states)
                all_scores.append(score)
        pos += 1
    
    # then, try to move the first available AM in each burrow
    for bur in "ABCD":
        # if burrows[bur] == [' ', ' '] or burrows[bur] == [' ', bur] or burrows[bur] == [bur] * 2:
        if all([ c == ' ' or c == bur for c in burrows[bur]]):
            # edge cases where
            # 1. no one is home (can't move anyone)
            # 2. an AM is at the bottom of the correct burrow, no point in moving them
            # 3. the burrow is filled with the right people, leave them there!
            continue
        pos = sum(c == ' ' for c in burrows[bur])
        am = burrows[bur][pos]
        out_steps = 1 + pos # num of steps to get out of burrow
        start_pos = addresses[bur] # now that AM is out, they belong to the corridor! they must move left or right
        # try left

        for step in [-1, +1]:
            new_pos = start_pos+step
            new_steps = 1
            new_burrows = deepcopy(burrows)
            new_burrows[bur][pos] = " "
            while new_pos >= 0 and new_pos < len(corridor) and corridor[new_pos] == " ":
                # AM can move there! what would happen?!

                if new_pos not in addresses.values():
                    new_corridor = corridor[:]
                    new_corridor[new_pos] = am

                    score = move(new_burrows, new_corridor, curr_cost + (out_steps + new_steps) * costs[am], known_states)
                    all_scores.append(score)

                new_steps += 1
                new_pos += step
    
    # 1e100 as a flag value for "unsolvable" problems
    score = 1e100 if not all_scores else min(all_scores)
    known_states[key] = score - curr_cost
    return score


if __name__ == "__main__":
    with open("input23") as f:
        lines = f.readlines()

    burrows = { # pop from 0
        "A": [lines[2][3], lines[3][3]], 
        "B": [lines[2][5], lines[3][5]],
        "C": [lines[2][7], lines[3][7]],
        "D": [lines[2][9], lines[3][9]]
    }

    corridor = [" "] * 11
    print(move(burrows, corridor, 0))

    burrows = { # pop from 0
        "A": [lines[2][3], "D", "D", lines[3][3]], 
        "B": [lines[2][5], "C", "B", lines[3][5]],
        "C": [lines[2][7], "B", "A", lines[3][7]],
        "D": [lines[2][9], "A", "C", lines[3][9]]
    }
    print(move(burrows, corridor, 0))
