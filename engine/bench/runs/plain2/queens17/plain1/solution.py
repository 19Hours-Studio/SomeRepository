import numpy as np

N = 17
BLOCKED = [(0, 7), (0, 12), (0, 13), (1, 8), (2, 8), (2, 9), (4, 1), (4, 6), (4, 13), (6, 4), (6, 7), (7, 3), (8, 3), (8, 9), (8, 16), (9, 5), (9, 11), (10, 3), (10, 12), (11, 1), (11, 10), (12, 13), (13, 2), (15, 11), (16, 10), (16, 11), (16, 13), (16, 15)]
M = (1 << N) - 1
CB = 63 - 3 * N  # bits left for a packed count


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
        del nk, nc
        if int(cn.max()) < (1 << CB):
            # pack counts into the low bits: a plain sort is much faster
            # than argsort + gathers
            v = np.sort((k << CB) | cn)
            del k, cn
            k = v >> CB
            cn = v & ((1 << CB) - 1)
            del v
        else:
            o = np.argsort(k)
            k = k[o]
            cn = cn[o]
            del o
        st = np.flatnonzero(np.concatenate(([True], k[1:] != k[:-1])))
        keys = k[st]
        cnts = np.add.reduceat(cn, st)
        del k, cn, st
    return keys, cnts


def main():
    blk = [0] * N
    for r, c in BLOCKED:
        blk[r] |= 1 << c
    kt = 8
    m = np.int64(M)
    S = 2 * N
    tk, tc = half(blk, kt, True)
    tcol = tk >> S
    tx = tk & ((1 << S) - 1)
    del tk
    # replicate top states by multiplicity so packed bits carry weight 1
    if tc.max() > 1:
        rep = np.repeat(np.arange(len(tx)), tc)
        tcol = tcol[rep]
        tx = tx[rep]
        del rep
    del tc
    bk, bc = half(blk[::-1], N - kt, False)
    bcol = bk >> S
    by = ((bk >> N) & m) | ((bk & m) << N)
    del bk
    CH = 7
    nch = (S + CH - 1) // CH
    bidx = [((by >> (CH * k)) & ((1 << CH) - 1)) for k in range(nch)]
    del by
    bc = bc.astype(np.int64)
    g = np.arange(M + 2)
    ts = np.searchsorted(tcol, g).tolist()
    bs = np.searchsorted(bcol, g).tolist()
    del tcol, bcol
    shifts = np.arange(S, dtype=np.int64)[:, None]
    ones = np.full((1, 1), ~np.uint64(0), dtype=np.uint64)
    total = 0
    for c in range(M + 1):
        a0 = ts[c]
        a1 = ts[c + 1]
        if a0 == a1:
            continue
        b0 = bs[M - c]
        b1 = bs[M - c + 1]
        if b0 == b1:
            continue
        nt = a1 - a0
        W = (nt + 63) >> 6
        bm = ((tx[a0:a1][None, :] >> shifts) & 1).astype(np.bool_)
        pk = np.packbits(bm, axis=1, bitorder='little')
        if pk.shape[1] != W * 8:
            pk = np.pad(pk, ((0, 0), (0, W * 8 - pk.shape[1])))
        pk = ~pk.view(np.uint64)
        acc = None
        for k in range(nch):
            T = np.broadcast_to(ones, (1, W))
            for j in range(CH * k, min(S, CH * (k + 1))):
                T = np.concatenate((T, T & pk[j]))
            r = T[bidx[k][b0:b1]]
            if acc is None:
                acc = r
            else:
                acc &= r
        rem = nt & 63
        if rem:
            acc[:, -1] &= np.uint64((1 << rem) - 1)
        total += int(np.bitwise_count(acc).sum(axis=1, dtype=np.int64) @ bc[b0:b1])
    print(total)


main()
