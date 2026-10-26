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
    gk = np.arange(M + 1, dtype=np.int64) << (S + CB)
    tv = half(blk, kt, True)
    # replicate states by multiplicity so every state has weight 1
    tc = tv & CM
    if int(tc.max()) > 1:
        tv = np.repeat(tv, tc)
    del tc
    ts = np.append(np.searchsorted(tv, gk), len(tv))
    # Diagonal bits 1..31 are the only ones both halves can use: 4 chunks
    # of 8 bits.  Top states are laid out per column group, padded to whole
    # 64-bit words; TP[j, w] has bit i set iff top state 64w+i lacks
    # diagonal bit j+1 (i.e. does not conflict through it).
    nt_g = np.diff(ts)
    W_g = (nt_g + 63) >> 6
    wo = np.concatenate(([0], np.cumsum(W_g)))
    tot_w = int(wo[-1])
    pos = np.arange(len(tv), dtype=np.int64)
    pos += np.repeat(wo[:-1] * 64 - ts[:-1], nt_g)
    txp = np.zeros(tot_w * 64, dtype=np.int64)
    txp[pos] = (tv >> (CB + 1)) & ((1 << 32) - 1)
    del pos, tv
    TP = np.empty((32, tot_w), dtype=np.uint64)
    step = 1 << 14  # words per conversion step
    for w in range(0, tot_w, step):
        x = txp[w * 64:(w + step) * 64].view(np.uint8).reshape(-1, 8)
        bits = np.unpackbits(x, axis=1, count=32, bitorder='little')
        pk = np.packbits(bits.T, axis=1, bitorder='little')
        TP[:, w:w + step] = ~np.ascontiguousarray(pk).view(np.uint64)
    del txp, bits, pk
    # bottom: flipped board, rows N-1..kt, projected onto real row kt-1
    bv = half(blk[::-1], N - kt, False)
    bc = bv & CM
    if int(bc.max()) > 1:
        bv = np.repeat(bv, bc)
    del bc
    bs = np.searchsorted(bv, gk).tolist() + [len(bv)]
    nb_all = len(bv)
    B8 = np.empty((4, nb_all), dtype=np.uint8)
    step = 1 << 18
    for i in range(0, nb_all, step):
        x = bv[i:i + step] >> CB
        # flipped board swaps the diagonals
        y = ((x >> N) & m) | ((x & m) << N)
        y >>= 1
        for k in range(4):
            B8[k, i:i + step] = (y >> (8 * k)) & 255
    del bv, x, y
    ts = ts.tolist()
    wo = wo.tolist()
    full = ~np.uint64(0)
    lo16 = np.uint64(0x00FF00FF00FF00FF)
    lo32 = np.uint64(0x0000FFFF0000FFFF)
    total = 0
    for c in range(M + 1):
        a0 = ts[c]
        nt = ts[c + 1] - a0
        if nt == 0:
            continue
        b0 = bs[M - c]
        b1 = bs[M - c + 1]
        if b0 == b1:
            continue
        w0 = wo[c]
        W = wo[c + 1] - w0
        P = TP[:, w0:w0 + W].reshape(4, 8, W)
        # T[k, v]: top states compatible with bottom bits v of chunk k;
        # chunk 0 starts from the valid-state mask so padding never counts
        T = np.full((4, 1, W), full, dtype=np.uint64)
        if nt & 63:
            T[0, 0, -1] = np.uint64((1 << (nt & 63)) - 1)
        for j in range(8):
            T = np.concatenate((T, T & P[:, j:j + 1]), axis=1)
        idx = B8[:, b0:b1].astype(np.intp)
        acc = np.take(T[0], idx[0], axis=0)
        for k in range(1, 4):
            acc &= np.take(T[k], idx[k], axis=0)
        # popcount, summing the byte counts eight at a time
        pc = np.bitwise_count(acc).reshape(-1)
        n8 = len(pc) >> 3
        q = pc[:n8 * 8].view(np.uint64)
        q = (q & lo16) + ((q >> 8) & lo16)
        q = (q & lo32) + ((q >> 16) & lo32)
        s = int(q.sum())
        total += (s & 0xFFFFFFFF) + (s >> 32) + int(pc[n8 * 8:].sum())
    print(total)


main()
