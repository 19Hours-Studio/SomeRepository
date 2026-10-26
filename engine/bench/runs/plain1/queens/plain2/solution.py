import numpy as np

N = 15
BLOCKED = [(0, 0), (0, 2), (1, 5), (3, 0), (3, 13), (4, 14), (5, 3), (5, 4), (5, 12), (6, 3), (6, 4), (7, 1), (7, 9), (7, 11), (8, 11), (9, 7), (10, 2), (11, 8), (12, 5), (13, 6), (13, 11), (14, 3), (14, 12), (14, 13)]
M = (1 << N) - 1


def relevance(blk, r, shift0):
    """Tables over the set of free columns: which ld / rd bits (projected onto
    the current row) can still meet a free cell in a free column in rows > r."""
    rem = np.arange(M + 1, dtype=np.int64)
    rl = np.zeros(M + 1, dtype=np.int64)
    rr = np.zeros(M + 1, dtype=np.int64)
    for k in range(N - 1 - r):
        avail = rem & ~blk[r + 1 + k]
        s = k + shift0
        rl |= avail >> s
        rr |= (avail << s) & M
    return rl, rr


def half(blk, nrows, project_last):
    """Row-by-row DP over the first nrows rows of blk.  Returns sorted unique
    keys rd | ld<<N | cols<<2N with counts.  ld/rd are diagonal attacks
    projected onto the next row (or the last placed row if project_last),
    pruned of bits that cannot matter."""
    S = 2 * N
    m = np.int64(M)
    keys = np.zeros(1, dtype=np.int64)
    cnts = np.ones(1, dtype=np.int64)
    for r in range(nrows):
        last = project_last and r == nrows - 1
        rlt, rrt = relevance(blk, r, 1 if last else 0)
        cols = keys >> S
        ld = (keys >> N) & m
        rd = keys & m
        occ = cols | ld | rd | blk[r]
        nk = []
        nc = []
        for c in range(N):
            b = 1 << c
            sel = (occ & b) == 0
            if not sel.any():
                continue
            cc = cols[sel] | b
            l2 = ld[sel] | b
            r2 = rd[sel] | b
            if not last:
                l2 = (l2 << 1) & m
                r2 = r2 >> 1
            rem = cc ^ m
            nk.append((cc << S) | ((l2 & rlt[rem]) << N) | (r2 & rrt[rem]))
            nc.append(cnts[sel])
        k = np.concatenate(nk)
        cn = np.concatenate(nc)
        o = np.argsort(k)
        k = k[o]
        cn = cn[o]
        st = np.flatnonzero(np.concatenate(([True], k[1:] != k[:-1])))
        keys = k[st]
        cnts = np.add.reduceat(cn, st)
    return keys, cnts


def main():
    blk = [0] * N
    for r, c in BLOCKED:
        blk[r] |= 1 << c
    kt = 8  # top rows 0..kt-1
    tk, tc = half(blk, kt, True)
    # bottom: flipped board, rows N-1..kt, projected onto real row kt-1
    bk, bc = half(blk[::-1], N - kt, False)
    m = np.int64(M)
    S = 2 * N
    # top: X = rd | ld<<N ; bottom (flipped, diagonals swap): Y = ld | rd<<N
    tcol = tk >> S
    tx = (tk & ((1 << S) - 1)).astype(np.int32)
    bcol = bk >> S
    by = (((bk >> N) & m) | ((bk & m) << N)).astype(np.int32)
    # per-group sums stay far below 2**24, so float32 is exact
    tc = tc.astype(np.float32)
    bc = bc.astype(np.float32)
    g = np.arange(M + 2)
    ts = np.searchsorted(tcol, g).tolist()
    bs = np.searchsorted(bcol, g).tolist()
    total = 0.0
    band = np.bitwise_and.outer
    for c in range(M + 1):
        a0 = ts[c]
        a1 = ts[c + 1]
        if a0 == a1:
            continue
        b0 = bs[M - c]
        b1 = bs[M - c + 1]
        if b0 == b1:
            continue
        z = band(tx[a0:a1], by[b0:b1]) == 0
        total += float(tc[a0:a1] @ (z @ bc[b0:b1]))
    print(int(round(total)))


main()
