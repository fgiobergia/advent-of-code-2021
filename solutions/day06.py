from collections import Counter

def run(ages, days):
    c = Counter(ages)
    for i in range(1, days+1):
        nz = c[0]
        c[0] = 0
        for j in range(1,9):
            c[j-1] = c[j]
        c[6] += nz
        c[8] = nz
    return sum(c.values())
    

if __name__ == "__main__":
    with open("day06.input") as f:
        ages = list(map(int, f.readline().split(",")))

    print(run(ages, 80))
    print(run(ages, 256))