with open("day01.input") as f:
    depths = list(map(int, f.readlines()))

print(sum(1 for i in range(1, len(depths)) if depths[i] > depths[i-1]))

# reaching len(depths) instead of len(depths)-N b/c "overflowing" sums
# will never be larger than the final "full" sum (since all values are > 0
print(sum(1 for i in range(len(depths)) if sum(depths[i:i+3]) < sum(depths[i+1:i+4])))
