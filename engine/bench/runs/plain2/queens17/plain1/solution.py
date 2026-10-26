import numpy as np

N = 17
BLOCKED = [(0, 7), (0, 12), (0, 13), (1, 8), (2, 8), (2, 9), (4, 1), (4, 6), (4, 13), (6, 4), (6, 7), (7, 3), (8, 3), (8, 9), (8, 16), (9, 5), (9, 11), (10, 3), (10, 12), (11, 1), (11, 10), (12, 13), (13, 2), (15, 11), (16, 10), (16, 11), (16, 13), (16, 15)]
M = (1 << N) - 1
S = 2 * N
CB = 63 - 3 * N  # low bits of a packed state that hold its count
CM = (1 << CB) - 1
CHUNK = 1 << 17  # parents per expansion step (keeps temporaries in cache)


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
    """Row-by-row DP over the first nrows rows of blk.  Returns sorted packed
    states (cols<<2N | ld<<N | rd) << CB | count.  ld/rd are diagonal attacks
    projected onto the next row (or the last placed row if project_last),
    pruned of bits that cannot matter.  Equal states are merged except after
    the last row, where merging hardly ever happens."""
    m = np.int64(M)
    v = np.ones(1, dtype=np.int64)
    for r in range(nrows):
        final = r == nrows - 1
        last = project_last and final
        rlt, rrt = relevance(blk, r, 1 if last else 0)
        out = []
        for i in range(0, len(v), CHUNK):
            vv = v[i:i + CHUNK]
            cn = vv & CM
            kk = vv >> CB
            cols = kk >> S
            ld = (kk >> N) & m
            rd = kk & m
            occ = cols | ld | rd | blk[r]
            for c in range(N):
                b = 1 << c
                if blk[r] & b:
                    continue
                sel = (occ & b) == 0
                cc = cols[sel] | b
                if len(cc) == 0:
                    continue
                l2 = ld[sel] | b
                r2 = rd[sel] | b
                if not last:
                    l2 <<= 1
                    l2 &= m
                    r2 >>= 1
                rem = cc ^ m
                l2 &= rlt[rem]
                r2 &= rrt[rem]
                cc <<= S
                l2 <<= N
                cc |= l2
                cc |= r2
                cc <<= CB
                cc |= cn[sel]
                out.append(cc)
        v = np.concatenate(out)
        del out
        v.sort()
        if final:
            return v
        k = v >> CB
        st = np.flatnonzero(np.concatenate(([True], k[1:] != k[:-1])))
        cnt = np.add.reduceat(v & CM, st)
        assert int(cnt.max()) <= CM
        v = (k[st] << CB) | cnt
        del k, st, cnt


def main():
    blk = [0] * N
    for r, c in BLOCKED:
        blk[r] |= 1 << c
    m = np.int64(M)
    kt = 8  # top rows 0..kt-1
    tv = half(blk, kt, True)
    tc = tv & CM
    # replicate top states by multiplicity so every packed bit has weight 1
    if int(tc.max()) > 1:
        tv = np.repeat(tv, tc)
    del tc
    tv >>= CB
    tcol = tv >> S
    tx = tv & ((1 << S) - 1)
    del tv
    # bottom: flipped board, rows N-1..kt, projected onto real row kt-1
    bv = half(blk[::-1], N - kt, False)
    CH = 7
    nch = (S + CH - 1) // CH
    nb_all = len(bv)
    # bidx[i, k] = 128 * k + (chunk k of the bottom state's diagonal bits)
    bidx = np.empty((nb_all, nch), dtype=np.int16)
    bc = np.empty(nb_all, dtype=np.int64)
    bcol = np.empty(nb_all, dtype=np.int32)
    off = np.arange(nch, dtype=np.int64) << CH
    sh = np.arange(nch, dtype=np.int64) * CH
    step = 1 << 18
    for i in range(0, nb_all, step):
        x = bv[i:i + step]
        bc[i:i + step] = x & CM
        x = x >> CB
        bcol[i:i + step] = x >> S
        # flipped board swaps the diagonals
        y = ((x >> N) & m) | ((x & m) << N)
        bidx[i:i + step] = ((y[:, None] >> sh) & ((1 << CH) - 1)) + off
    del bv
    g = np.arange(M + 2)
    ts = np.searchsorted(tcol, g).tolist()
    bs = np.searchsorted(bcol, g).tolist()
    del tcol, bcol
    txb = tx.view(np.uint8).reshape(-1, 8)
    ones = np.full((nch, 1, 1), ~np.uint64(0), dtype=np.uint64)
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
        # pk[j]: bitset over this group's top states having diagonal bit j
        bits = np.unpackbits(txb[a0:a1], axis=1, count=nch * CH, bitorder='little')
        pk = np.zeros((nch * CH, W * 8), dtype=np.uint8)
        pk[:, :(nt + 7) >> 3] = np.packbits(bits.T, axis=1, bitorder='little')
        P = (~pk.view(np.uint64)).reshape(nch, CH, W)
        # T[k, v]: top states compatible with bottom bits v in chunk k
        T = np.broadcast_to(ones, (nch, 1, W))
        for j in range(CH):
            T = np.concatenate((T, T & P[:, j:j + 1]), axis=1)
        acc = np.bitwise_and.reduce(T.reshape(-1, W)[bidx[b0:b1]], axis=1)
        rem = nt & 63
        if rem:
            acc[:, -1] &= np.uint64((1 << rem) - 1)
        total += int(np.bitwise_count(acc).sum(axis=1, dtype=np.int64) @ bc[b0:b1])
    print(total)


main()
