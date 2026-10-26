import numpy as np

X, M = 10**10, 1_000_000_007
r = int(X**0.5) + 1
small = np.ones(r + 1, bool); small[:2] = False
for i in range(2, int(r**0.5) + 1):
    if small[i]:
        small[i * i::i] = False
ps = np.nonzero(small)[0]
total, seg = 0, 10**8
for lo in range(0, X + 1, seg):
    hi = min(lo + seg, X + 1)
    s = np.ones(hi - lo, bool)
    if lo == 0:
        s[:2] = False
    for p in ps:
        p = int(p)
        if p * p >= hi:
            break
        st = max(p * p, (lo + p - 1) // p * p)
        s[st - lo::p] = False
    q = (np.nonzero(s)[0].astype(np.int64) + lo) % M
    total = (total + int(((q * q) % M).sum()) % M) % M
print(total)
