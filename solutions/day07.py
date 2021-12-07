import numpy as np

def sum_n(n):
    return (abs(n)+1)*abs(n)//2

if __name__ == "__main__":
    with open("day07.input") as f:
        pos = np.array(list(map(int, f.readline().split(","))))
    
    print(int(abs(pos - np.median(pos)).sum()))

    f = np.vectorize(sum_n)
    print(f(pos - pos.reshape(-1,1)).sum(axis=1).min())