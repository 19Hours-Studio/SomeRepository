import numpy as np

N = 17
BLOCKED = [(0, 7), (0, 12), (0, 13), (1, 8), (2, 8), (2, 9), (4, 1), (4, 6), (4, 13), (6, 4), (6, 7), (7, 3), (8, 3), (8, 9), (8, 16), (9, 5), (9, 11), (10, 3), (10, 12), (11, 1), (11, 10), (12, 13), (13, 2), (15, 11), (16, 10), (16, 11), (16, 13), (16, 15)]
M = (1 << N) - 1
MID = 8  # the middle row's queen is placed during the join


def half(blk, nrows, bottom):
    """All placements in the first nrows rows of blk.  Returns cols and the
    diagonal mask projected onto row nrows: rd | ld<<N (top) or ld | rd<<N
    (bottom, flipped board, so its diagonals line up with the top's)."""
    cols = np.zeros(1, dtype=np.int32)
    ld = np.zeros(1, dtype=np.int32)
    rd = np.zeros(1, dtype=np.int32)
    for r in range(nrows - 1):
        occ = cols | ld | rd | blk[r]
        nc, nl, nr = [], [], []
        for c in range(N):
            b = 1 << c
            sel = np.flatnonzero((occ & b) == 0)
            if not len(sel):
                continue
            nc.append(cols[sel] | b)
            nl.append(((ld[sel] | b) << 1) & M)
            nr.append((rd[sel] | b) >> 1)
        cols = np.concatenate(nc)
        ld = np.concatenate(nl)
        rd = np.concatenate(nr)
    occ = cols | ld | rd | blk[nrows - 1]
    ld = ld.astype(np.int64)
    rd = rd.astype(np.int64)
    sl, sr = (0, N) if bottom else (N, 0)
    nc, nx = [], []
    for c in range(N):
        b = 1 << c
        sel = np.flatnonzero((occ & b) == 0)
        if not len(sel):
            continue
        nc.append(cols[sel] | b)
        nx.append(((((ld[sel] | b) << 1) & M) << sl) | (((rd[sel] | b) >> 1) << sr))
    return np.concatenate(nc), np.concatenate(nx)


def main():
    blk = [0] * N
    for r, c in BLOCKED:
        blk[r] |= 1 << c
    pc = np.bitwise_count(np.arange(M + 1))
    rank = np.zeros(M + 1, dtype=np.uint16)
    sub = np.flatnonzero(pc == MID)
    rank[sub] = np.arange(len(sub))
    ng = len(sub)

    # top rows 0..MID-1, grouped by column set, each group padded to a
    # multiple of 64 with dummies that conflict with everything
    tcol, tx = half(blk, MID, False)
    tr = rank[tcol]
    del tcol
    cnt = np.bincount(tr, minlength=ng)
    start = np.concatenate(([0], np.cumsum(cnt)))
    nw = (cnt + 63) >> 6
    wst = np.concatenate(([0], np.cumsum(nw)))
    NB = 35  # 34 diagonal bits + bit 34, set only in the dummies
    pad = (nw << 6) - cnt
    full = (1 << NB) - 1
    txp = np.concatenate(((tr.astype(np.int64) << NB) | tx,
                          (np.repeat(np.arange(ng, dtype=np.int64), pad) << NB) | full))
    txp.sort()
    txp &= full
    del tr, tx
    by8 = txp.view(np.uint8).reshape(-1, 8)
    pk = np.empty((NB, int(wst[-1])), dtype=np.uint64)
    for k in range(5):
        col = np.ascontiguousarray(by8[:, k])
        for j in range(8):
            b = 8 * k + j
            if b >= NB:
                break
            pk[b].view(np.uint8)[:] = np.packbits((col & (1 << j)) == 0, bitorder='little')

    del txp, by8, col
    ts = start.tolist()
    ws = wst.tolist()

    bcol, by = half(blk[::-1], N - 1 - MID, True)
    br = rank[bcol]
    by |= br.astype(np.int64) << (2 * N)
    by.sort()
    by &= (1 << (2 * N)) - 1
    bs = [0] + np.cumsum(np.bincount(br, minlength=ng)).tolist()
    del br, bcol
    sub = sub.tolist()
    rankl = rank.tolist()
    midfree = M & ~blk[MID]

    csh = np.array([0, 7, 14, 21, 28], dtype=np.int64)
    coff = np.arange(5, dtype=np.int64) * 128
    total = 0
    for g in range(ng):
        if ts[g] == ts[g + 1]:
            continue
        rem = M ^ sub[g]
        parts = []
        dv = []
        dn = []
        m = rem & midfree
        while m:
            b = m & -m
            m ^= b
            h = rankl[rem ^ b]
            b0, b1 = bs[h], bs[h + 1]
            if b0 != b1:
                parts.append(by[b0:b1])
                dv.append(b | (b << N))
                dn.append(b1 - b0)
        if not parts:
            continue
        Y = np.concatenate(parts)
        D = np.repeat(np.array(dv, dtype=np.int64), dn)
        ok = (Y & D) == 0
        Y = Y[ok] | D[ok]
        if not len(Y):
            continue
        w0, w1 = ws[g], ws[g + 1]
        w = w1 - w0
        T = np.empty((5, 128, w), dtype=np.uint64)
        T[:, 0] = pk[34, w0:w1]
        nbr = pk[:, w0:w1].reshape(5, 7, w)
        for j in range(7):
            h = 1 << j
            np.bitwise_and(T[:, :h], nbr[:, j:j + 1], out=T[:, h:2 * h])
        T = T.reshape(640, w)
        idx = ((Y[:, None] >> csh) & 127) + coff
        R = T[idx[:, 0]]
        for k in range(1, 5):
            R &= T[idx[:, k]]
        total += int(np.bitwise_count(R).sum())
    print(total)


main()
