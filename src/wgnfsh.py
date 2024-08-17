import numpy as np

# Wagner-Fischer algorithm
# https://en.wikipedia.org/wiki/Wagner%E2%80%93Fischer_algorithm

# returns a list of the same length as sequence
# element i = % distance between suffix of sequence of length i/last i elements and cmp
def match(sequence: list, cmp: list, tolerance: float) -> np.array:
    m, n = len(sequence), len(cmp)
    sequence.insert(0, 0)
    cmp.insert(0, 0)

    d = np.zeros((m + 1, n + 1))
    for i in range(1, m + 1):
        d[i][0] = i
    for i in range(1, n + 1):
        d[0][i] = i
    
    for j in range(1, n + 1):
        for i in range(1, m + 1):
            if sequence[m - i + 1] == cmp[n - j + 1]:
                cost = 0
            else:
                cost = abs(sequence[m - i + 1] - cmp[n - j + 1])
            d[i][j] = min(
                d[i - 1][j] + 1,
                d[i][j - 1] + 1,
                d[i - 1][j - 1] + cost
            )
    
    del sequence[0]
    del cmp[0]

    dists = d[n:, n] / n
    min_dist = np.min(dists)
    return (np.argmin(dists) + n, min_dist) if min_dist <= tolerance else (-1, 0)

# print(match(list("00000000001100AA03000A0400CCBEEEFFFFF"), list("CCCCEEEEFFFF"), 0.16))