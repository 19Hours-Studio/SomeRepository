import numpy as np

N = 15
BLOCKED = [(0, 0), (0, 2), (1, 5), (3, 0), (3, 13), (4, 14), (5, 3), (5, 4), (5, 12), (6, 3), (6, 4), (7, 1), (7, 9), (7, 11), (8, 11), (9, 7), (10, 2), (11, 8), (12, 5), (13, 6), (13, 11), (14, 3), (14, 12), (14, 13)]
SPLIT = 7  # top half: rows [0, SPLIT); bottom half: rows [SPLIT, N)

FULL = (1 << N) - 1
# Packed state: columns in bits 0..14, r-c diagonals in bits 16..30,
# r+c diagonals in bits 32..46, each diagonal set projected onto one row.
SA, SR = 16, 32
MC, MA, MR = FULL, FULL << SA, FULL << SR


def place(states, r, blocked):
    out = []
    for c in range(N):
        if (r, c) in blocked:
            continue
        b = 1 << c
        m = np.int64(b | (b << SA) | (b << SR))
        out.append(states[(states & m) == 0] | m)
    return np.concatenate(out)


def halves():
    blocked = set(BLOCKED)
    # Top: rows 0..SPLIT-1 going down, diagonals projected onto row SPLIT.
    s = np.zeros(1, dtype=np.int64)
    for r in range(SPLIT):
        s = place(s, r, blocked)
        s = (s & MC) | ((s << 1) & MA) | ((s >> 1) & MR)
    top = s
    # Bottom: rows N-1..SPLIT going up, diagonals projected onto row SPLIT.
    s = np.zeros(1, dtype=np.int64)
    for r in range(N - 1, SPLIT - 1, -1):
        if r != N - 1:
            s = (s & MC) | ((s >> 1) & MA) | ((s << 1) & MR)
        s = place(s, r, blocked)
    return top, s


def main():
    top, bot = halves()
    tc = (top & MC).astype(np.int16)
    bc = (FULL ^ (bot & MC)).astype(np.int16)
    td = (top >> SA).astype(np.int32)
    bd = (bot >> SA).astype(np.int32)
    to = np.argsort(tc, kind="stable")
    bo = np.argsort(bc, kind="stable")
    tc, td = tc[to], td[to]
    bc, bd = bc[bo], bd[bo]
    tkeys, tstart = np.unique(tc, return_index=True)
    tend = np.append(tstart[1:], len(tc))
    bkeys, bstart = np.unique(bc, return_index=True)
    bend = np.append(bstart[1:], len(bc))
    pos = np.searchsorted(bkeys, tkeys)
    pos[pos >= len(bkeys)] = 0
    total = 0
    for i in np.flatnonzero(bkeys[pos] == tkeys):
        j = pos[i]
        A = td[tstart[i]:tend[i]]
        B = bd[bstart[j]:bend[j]]
        total += np.count_nonzero((A[:, None] & B[None, :]) == 0)
    print(int(total))


main()
