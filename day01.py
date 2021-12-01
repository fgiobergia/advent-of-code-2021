with open("day01.input") as f:
    depths = list(map(int, f.readlines()))

print(sum(depths[i] > depths[i-1] for i in range(1, len(depths))))

print(sum(sum(depths[i:i+3]) < sum(depths[i+1:i+4]) for i in range(len(depths)-3)))
