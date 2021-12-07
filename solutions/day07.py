import numpy as np

def sum_n(n):
    return (n+1)*n//2

if __name__ == "__main__":
    with open("day07.input") as f:
        pos = np.array(list(map(int, f.readline().split(","))))
    
    print(int(abs(pos - np.median(pos)).sum()))

    print(np.min([ sum([ sum_n(abs(pos[i] - k)) for i in range(len(pos)) ]) for k in range(pos.max()) ]))