import numpy as np

def fold(dots, fold_info):
    axis, coord = fold_info
    for i in range(len(dots)):
        x,y = dots[i]
        if axis == "y" and y > coord:
            dots[i] = (x, 2 * coord - y)
        elif axis == "x" and x > coord:
            dots[i] = (2 * coord - x, y)
    return list(set(dots))



if __name__ == "__main__":
    with open("day13.input") as f:
        dots, folds = f.read().split("\n\n")
        dots = [ tuple(map(int, line.split(","))) for line in dots.split("\n")  ]
        folds = [ (w.split("=")[0][-1], int(w.split("=")[1])) for w in folds.split("\n") ]

        print(len(fold(dots, folds[0])))

        for f in folds:
            dots = fold(dots, f)
        
        dots = np.array(dots)
        origami = np.full((dots[:,1].max()+1, dots[:,0].max()+1), " ")
        origami[dots[:,1], dots[:,0]] = "█"
        print("\n".join( "".join(x) for x in origami))