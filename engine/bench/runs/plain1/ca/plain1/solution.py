import hashlib
import numpy as np

N, STEPS = 4096, 1000
W = N // 64
P = W + 2  # row pitch: [wrap-left, 64 words, wrap-right]
H = N // 2
B = 128  # row pairs per strip
g = (np.random.default_rng(2026).random((N, N)) < 0.35).astype(np.uint8)

# Bit-sliced: word k of a row holds columns k, k+64, ..., k+64*63 (bit b = column b*64+k).
# Even and odd rows live in separate arrays, so a pair of rows (2k, 2k+1) is index k in both.
sh = np.arange(64, dtype=np.uint64)
u1, u63 = np.uint64(1), np.uint64(63)
GE = np.zeros(H * P + 2, np.uint64)
GO = np.zeros(H * P + 2, np.uint64)
G2 = [a[1:1 + H * P].reshape(H, P) for a in (GE, GO)]
Gw = [a[:, 1:W + 1] for a in G2]
for p in (0, 1):
    gp = g[p::2]
    Gw[p][:] = gp[:, 0:W]
    for b in range(1, 64):
        Gw[p] |= gp[:, b * W:(b + 1) * W].astype(np.uint64) << sh[b]
del g, gp

# column sums (2 bits). SE: even rows 0..H (row H = copy of row 0); SO: odd rows -1..H-1
SE0 = np.empty((H + 1) * P, np.uint64)
SE1 = np.empty((H + 1) * P, np.uint64)
SO0 = np.empty((H + 1) * P, np.uint64)
SO1 = np.empty((H + 1) * P, np.uint64)
M = B * P
d0, d1, d2, c, x, y, t0, t1, t2 = (np.empty(M, np.uint64) for _ in range(9))
tmp = np.empty(H, np.uint64)
band, bxor, bor = np.bitwise_and, np.bitwise_xor, np.bitwise_or
lsh, rsh = np.left_shift, np.right_shift


def sl(a, row):
    return a[row * P:row * P + M]


strips = []
for k in range(0, H, B):
    o = 1 + k * P
    strips.append(((GE[o - 1:o - 1 + M], GE[o:o + M], GE[o + 1:o + 1 + M], sl(SE0, k), sl(SE1, k)),
                   (GO[o - 1:o - 1 + M], GO[o:o + M], GO[o + 1:o + 1 + M], sl(SO0, k + 1), sl(SO1, k + 1)),
                   sl(SO0, k), sl(SO1, k), sl(SE0, k + 1), sl(SE1, k + 1)))
NS = len(strips)


def hsum(h):
    L, G, R, s0, s1 = h
    bxor(L, R, x)
    band(L, R, s1)
    bxor(x, G, s0)
    band(x, G, x)
    bor(s1, x, s1)


def finish(G, m0, m1):
    # T = D + m (9-cell total incl. self); new = T==3 | (T==4 & g) | (T==6 & ~g)
    bxor(d0, m0, t0)
    band(d0, m0, c)
    bxor(d1, m1, x)
    bxor(x, c, t1)
    band(c, x, c)
    band(d1, m1, y)
    bor(c, y, c)
    bxor(d2, c, t2)
    band(G, t2, y)
    bxor(y, t1, y)
    bxor(t0, t2, x)
    band(x, y, G)


wraps = [(a[:, 1], a[:, W], a[:, 0], a[:, W + 1]) for a in G2]
last = (H - 1) * P
for _ in range(STEPS):
    for cw0, cw1, cl, cr in wraps:
        lsh(cw1, u1, cl)
        rsh(cw1, u63, tmp)
        bor(cl, tmp, cl)
        rsh(cw0, u1, cr)
        lsh(cw0, u63, tmp)
        bor(cr, tmp, cr)
    for i in (0, NS - 1):
        hsum(strips[i][0]); hsum(strips[i][1])
    SE0[H * P:] = SE0[0:P]; SE1[H * P:] = SE1[0:P]
    SO0[0:P] = SO0[H * P:]; SO1[0:P] = SO1[H * P:]
    for i in range(NS):
        if i + 1 < NS - 1:
            st = strips[i + 1]
            hsum(st[0]); hsum(st[1])
        (_, GEs, _, e0, e1), (_, GOs, _, o0, o1), m0, m1, p0, p1 = strips[i]
        # D = E + O (0..6)
        bxor(e0, o0, d0)
        band(e0, o0, c)
        bxor(e1, o1, x)
        bxor(x, c, d1)
        band(c, x, c)
        band(e1, o1, y)
        bor(c, y, d2)
        finish(GEs, m0, m1)
        finish(GOs, p0, p1)

g = np.empty((N, N), np.uint8)
for p in (0, 1):
    gp = g[p::2]
    for b in range(64):
        gp[:, b * W:(b + 1) * W] = (Gw[p] >> sh[b]) & u1
print(hashlib.sha256(np.packbits(g).tobytes()).hexdigest())
