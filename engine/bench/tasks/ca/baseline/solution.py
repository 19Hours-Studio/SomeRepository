import hashlib
import numpy as np

N, STEPS = 4096, 1000
g = (np.random.default_rng(2026).random((N, N)) < 0.35).astype(np.uint8)
for _ in range(STEPS):
    n = sum(np.roll(np.roll(g, i, 0), j, 1) for i in (-1, 0, 1) for j in (-1, 0, 1) if i or j)
    born = (g == 0) & ((n == 3) | (n == 6))
    stay = (g == 1) & ((n == 2) | (n == 3))
    g = (born | stay).astype(np.uint8)
print(hashlib.sha256(np.packbits(g).tobytes()).hexdigest())
