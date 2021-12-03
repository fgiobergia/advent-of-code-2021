import numpy as np

def to_bin(v):
    return (2**np.arange(v.shape[0]-1, -1, -1))[v].sum()

# bit_criteria: true => most common, false: least common
def find_report(report, bit_criteria):
    i = 0
    while report.shape[0] > 1:
        chosen_bit = not ((report[:, i].sum() >= report.shape[0]/2) ^ bit_criteria)
        report = report[report[:,i] == chosen_bit]
        i += 1
    return to_bin(report[0].astype(bool))


if __name__ == "__main__":
    with open("day03.input") as f:
        report = np.array([ list(l.strip()) for l in f.readlines() ], dtype=int)
    
    ndx = report.sum(axis=0) > report.shape[0]/2
    gamma = to_bin(ndx)
    eps = 2 ** report.shape[1] - 1 - gamma
    print(gamma * eps)

    print(find_report(report[::], True) * find_report(report[::], False))