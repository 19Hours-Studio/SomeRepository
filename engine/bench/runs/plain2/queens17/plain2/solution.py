import numpy as np

N = 17
BLOCKED = [(0, 7), (0, 12), (0, 13), (1, 8), (2, 8), (2, 9), (4, 1), (4, 6), (4, 13), (6, 4), (6, 7), (7, 3), (8, 3), (8, 9), (8, 16), (9, 5), (9, 11), (10, 3), (10, 12), (11, 1), (11, 10), (12, 13), (13, 2), (15, 11), (16, 10), (16, 11), (16, 13), (16, 15)]
M = (1 << N) - 1
MID = 8  # middle row, placed during the join


def half(blk, nrows):
    """Enumerate all placements in the first nrows rows of blk (no merging).
    Returns cols, ld, rd with diagonals projected onto row nrows."""
    cols = np.zeros(1, dtype=np.int64)
    ld = np.zeros(1, dtype=np.int64)
    rd = np.zeros(1, dtype=np.int64)
    for r in range(nrows):
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
    return cols, ld, rd


def main():
    blk = [0] * N
    for r, c in BLOCKED:
        blk[r] |= 1 << c
    # top rows 0..MID-1 projected onto row MID
    tcol, tld, trd = half(blk, MID)
    tx = trd | (tld << N)
    # bottom rows N-1..MID+1 (flipped) projected onto row MID; diagonals swap
    bcol, bld, brd = half(blk[::-1], N - 1 - MID)
    by = bld | (brd << N)
    del tld, trd, bld, brd
    # place the middle queen in each column c: extends bottom states
    bocc = bcol | by | (by >> N)
    ys, gs = [], []
    for c in range(N):
        b = 1 << c
        if blk[MID] & b:
            continue
        sel = np.flatnonzero((bocc & b) == 0)
        ys.append(by[sel] | (b | (b << N)))
        gs.append(M ^ (bcol[sel] | b))  # top column set needed
    by = np.concatenate(ys)
    bg = np.concatenate(gs)
    del ys, gs, bocc, bcol

    # rank 8-subsets of columns
    pc = np.bitwise_count(np.arange(M + 1))
    rank = np.full(M + 1, -1, dtype=np.int64)
    sub = np.flatnonzero(pc == MID)
    rank[sub] = np.arange(len(sub))
    ng = len(sub)
    tr = rank[tcol].astype(np.int16)
    o = np.argsort(tr, kind='stable')
    tx = tx[o]
    ts = np.searchsorted(tr[o], np.arange(ng + 1)).tolist()
    br = rank[bg].astype(np.int16)
    o = np.argsort(br, kind='stable')
    by = by[o]
    bs = np.searchsorted(br[o], np.arange(ng + 1)).tolist()
    del o, tr, br, bg, tcol

    shifts = np.arange(35, dtype=np.int64)[:, None]
    csh = np.array([0, 7, 14, 21, 28], dtype=np.int64)
    coff = np.arange(5, dtype=np.int64) * 128
    total = 0
    for g in range(ng):
        a0, a1 = ts[g], ts[g + 1]
        b0, b1 = bs[g], bs[g + 1]
        if a0 == a1 or b0 == b1:
            continue
        X = tx[a0:a1]
        na = a1 - a0
        w = (na + 63) >> 6
        nb = ((X[None, :] >> shifts) & 1) == 0
        pk = np.zeros((36, w * 8), dtype=np.uint8)
        pk[:35, :(na + 7) >> 3] = np.packbits(nb, axis=1, bitorder='little')
        pk[35, :(na + 7) >> 3] = np.packbits(np.ones(na, dtype=bool), bitorder='little')
        pk = pk.view(np.uint64)
        T = np.broadcast_to(pk[35], (5, 1, w))
        nbr = pk[:35].reshape(5, 7, w)
        for j in range(7):
            T = np.concatenate((T, T & nbr[:, j:j + 1, :]), axis=1)
        T = T.reshape(640, w)
        Y = by[b0:b1]
        idx = ((Y[:, None] >> csh) & 127) + coff
        R = T[idx[:, 0]]
        for k in range(1, 5):
            R &= T[idx[:, k]]
        total += int(np.bitwise_count(R).sum())
    print(total)


main()
