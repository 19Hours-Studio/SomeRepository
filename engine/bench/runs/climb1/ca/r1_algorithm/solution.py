import hashlib
import numpy as np

N, STEPS = 4096, 1000
W = N // 64
S = W + 2  # row stride: pad word, W data words, pad word
BR = 128  # rows per block
NB = N // BR
BL = BR * S
HL = BL + 2 * S

g8 = (np.random.default_rng(2026).random((N, N)) < 0.35).astype(np.uint8)
# Interleaved packing: bit k of word w in a row = column k*W + w, so the
# horizontal neighbours of a word are just the adjacent words.  Each row is
# stored as [left pad, W words, right pad]; the pads hold rotated wrap copies.
# Rows -1 and N are wrap copies of rows N-1 and 0.  Buffers are flat with one
# spare word at each end so that the neighbour slices of a whole block stay
# contiguous; pad slots compute garbage that is overwritten before use.
bufs = [np.zeros((N + 2) * S + 2, np.uint64) for _ in range(2)]
bufs[0][1 + S:1 + S + N * S].reshape(N, S)[:, 1:W + 1] = np.packbits(
    g8.reshape(N, 64, W).transpose(0, 2, 1), axis=2,
    bitorder='little').reshape(N, W * 8).view('<u8')
del g8

one = np.uint64(1)
s63 = np.uint64(63)
XOR, AND, OR = np.bitwise_xor, np.bitwise_and, np.bitwise_or
SHL, SHR = np.left_shift, np.right_shift

# block-local horizontal sums h = L+g+R and m = L+R, rows r0-1 .. r0+BR
H0 = np.empty(HL, np.uint64)
H1 = np.empty(HL, np.uint64)
M0 = np.empty(HL, np.uint64)
M1 = np.empty(HL, np.uint64)
m0 = M0[S:S + BL]
m1 = M1[S:S + BL]
a0 = H0[:BL]; a1 = H1[:BL]
b0 = H0[2 * S:]; b1 = H1[2 * S:]

T = np.empty(BL, np.uint64)
X0 = np.empty(BL, np.uint64)
X1 = np.empty(BL, np.uint64)
C0 = np.empty(BL, np.uint64)
P = np.empty(BL, np.uint64)
pl = np.empty(N, np.uint64)
pr = np.empty(N, np.uint64)


def build(G, NG):
    """Flat list of (ufunc, x, y, out) for one step from G into NG."""
    ops = []
    Gv = G[1:-1].reshape(N + 2, S)
    rows = Gv[1:N + 1]
    # wrap pads: left of word 0 is word W-1 rotated up one bit, etc.
    ops += [(SHL, rows[:, W], one, pl), (SHR, rows[:, W], s63, pr),
            (OR, pl, pr, rows[:, 0]),
            (SHR, rows[:, 1], one, pl), (SHL, rows[:, 1], s63, pr),
            (OR, pl, pr, rows[:, W + 1]),
            (OR, Gv[N], Gv[N], Gv[0]), (OR, Gv[1], Gv[1], Gv[N + 1])]
    for k in range(NB):
        a = 1 + k * BL  # start of row r0-1
        L = G[a - 1:a - 1 + HL]; g = G[a:a + HL]; R = G[a + 1:a + 1 + HL]
        gc = G[a + S:a + S + BL]
        out = NG[a + S:a + S + BL]
        ops += [
            (XOR, L, R, M0), (AND, L, R, M1),
            (XOR, M0, g, H0), (AND, M0, g, H1), (OR, H1, M1, H1),
            # bit0 of n and its carry
            (XOR, a0, b0, T), (XOR, T, m0, X0), (AND, T, m0, C0),
            (AND, a0, b0, T), (OR, C0, T, C0),
            # bits 1 and 2: s1 = parity of (a1, b1, m1, C0); s2 is only
            # needed where s1 is set, i.e. the count is 1 or 3, and there it
            # is 1 iff one of the pairs is fully set
            (XOR, a1, b1, P), (XOR, m1, C0, X1), (XOR, P, X1, P),    # s1
            (AND, m1, C0, C0), (AND, a1, b1, T), (OR, T, C0, T),     # s2
            # alive = s1 & (s2 ^ (s0 | g))
            (OR, X0, gc, X0), (XOR, X0, T, X0), (AND, X0, P, out)]
    return ops


plans = [build(bufs[0], bufs[1]), build(bufs[1], bufs[0])]
for step in range(STEPS):
    for f, x, y, o in plans[step & 1]:
        f(x, y, o)
G = bufs[STEPS & 1]

words = np.ascontiguousarray(G[1 + S:1 + S + N * S].reshape(N, S)[:, 1:W + 1])
g = np.unpackbits(words.view(np.uint8).reshape(N, W, 8), axis=2, bitorder='little')
g = g.transpose(0, 2, 1).reshape(N, N)
print(hashlib.sha256(np.packbits(g).tobytes()).hexdigest())
