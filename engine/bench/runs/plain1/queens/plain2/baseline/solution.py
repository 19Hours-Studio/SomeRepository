N = 15
BLOCKED = {(0, 0), (0, 2), (1, 5), (3, 0), (3, 13), (4, 14), (5, 3), (5, 4), (5, 12), (6, 3), (6, 4), (7, 1), (7, 9), (7, 11), (8, 11), (9, 7), (10, 2), (11, 8), (12, 5), (13, 6), (13, 11), (14, 3), (14, 12), (14, 13)}


def solve(r, cols, d1, d2):
    if r == N:
        return 1
    total = 0
    for c in range(N):
        if c in cols or (r - c) in d1 or (r + c) in d2 or (r, c) in BLOCKED:
            continue
        cols.add(c); d1.add(r - c); d2.add(r + c)
        total += solve(r + 1, cols, d1, d2)
        cols.remove(c); d1.remove(r - c); d2.remove(r + c)
    return total


print(solve(0, set(), set(), set()))
