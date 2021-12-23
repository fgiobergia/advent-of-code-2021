import re
from itertools import product
from tqdm import tqdm

def inters_axis(a1, a2, b1, b2):
    if b1 <= a1 <= b2 <= a2:
        return a1, b2
    
    if a1 <= b1 <= a2 <= b2:
        return b1, a2
    
    if a1 <= b1 <= b2 <= a2:
        return b1, b2
    
    if b1 <= a1 <= a2 <= b2:
        return a1, a2

def intersects(cube_a, cube_b):
    x1a, x2a, y1a, y2a, z1a, z2a = cube_a
    x1b, x2b, y1b, y2b, z1b, z2b = cube_b

    inters_x = inters_axis(x1a, x2a, x1b, x2b)
    inters_y = inters_axis(y1a, y2a, y1b, y2b)
    inters_z = inters_axis(z1a, z2a, z1b, z2b)

    if inters_x and inters_y and inters_z:
        return (*inters_x, *inters_y, *inters_z)

def switch(cmds):
    cubes = set()
    for op, cb in tqdm(cmds):
        all_cubes_b = { cb }

        new_cubes_a = set()

        cubes_a_stack = list(cubes)
        while cubes_a_stack:
            cube_a = cubes_a_stack.pop(0)

            a_has_intersected = False
            all_new_cubes_b = set()
            still_missing_b = all_cubes_b.copy()

            for cube_b in all_cubes_b:
            
                intersection = intersects(cube_a, cube_b)
                still_missing_b.remove(cube_b)

                if intersection is None:
                    # there is no intersection between cubes a and b -- try the next one
                    all_new_cubes_b.add(cube_b)
                    continue

                if cube_a in new_cubes_a:
                    # cube a was previously added to new_cubes_a, but now
                    # we matched it once again, so we need to remove it from new_cubes_a
                    new_cubes_a.remove(cube_a)
            
                a_has_intersected = True

                if intersection == cube_a:
                    # all of cube_a is contained in cube_b. 
                    # Instead of splitting everything, let's just
                    # (1) remove cube_a from new_cubes_a, 
                    # (2) add cube_b to all_new_cubes_b
                    all_new_cubes_b |= { cube_b } | still_missing_b
                    break
            
                x1a, x2a, y1a, y2a, z1a, z2a = cube_a
                x1b, x2b, y1b, y2b, z1b, z2b = cube_b
                x1c, x2c, y1c, y2c, z1c, z2c = intersection # c => intersection

                x_sections = [ (a,b) for a,b in [ (x1a, x1c-1), (x1c, x2c), (x2c+1, x2b), (x1b, x1c-1), (x2c+1, x2a) ] if a <= b ]
                y_sections = [ (a,b) for a,b in [ (y1a, y1c-1), (y1c, y2c), (y2c+1, y2b), (y1b, y1c-1), (y2c+1, y2a) ] if a <= b ]
                z_sections = [ (a,b) for a,b in [ (z1a, z1c-1), (z1c, z2c), (z2c+1, z2b), (z1b, z1c-1), (z2c+1, z2a) ] if a <= b ]

                all_sections = set([ (*a, *b, *c) for a,b,c in product(x_sections, y_sections, z_sections) ])

                cube_b_sections = { s for s in all_sections if intersects(cube_b, s) }
                cube_a_sections = { s for s in all_sections - cube_b_sections if intersects(cube_a, s) }

                new_cubes_a |= cube_a_sections
                all_new_cubes_b |= cube_b_sections | still_missing_b

                cubes_a_stack.extend(list(cube_a_sections)) # allow for further matches with a

                break
                
            if not a_has_intersected:
                new_cubes_a.add(cube_a) # add cube A as is, as it has not matched anything
            all_cubes_b = all_new_cubes_b


        cubes = new_cubes_a
        if op == "on":
            cubes |= all_cubes_b

    return cubes

def cube_size(c):
    return (c[1] - c[0] +1) * (c[3] - c[2] +1) * (c[5] - c[4] +1)

if __name__ == "__main__":
    with open("day22.input") as f:
        lines = [ re.match(r"^(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)$", line).groups() for line in f.readlines() ]
        cmds = [ (l[0], tuple(int(x) for x in l[1:])) for l in lines ]
    
    cmds_50 = [ (op, c) for op, c in cmds if -50 <= c[0] <= c[1] <= 50 and -50 <= c[2] <= c[3] <= 50 and -50 <= c[4] <= c[5] <= 50]

    print(sum(map(cube_size, switch(cmds_50))))
    # 23 mins for part 2 😅
    print(sum(map(cube_size, switch(cmds))))