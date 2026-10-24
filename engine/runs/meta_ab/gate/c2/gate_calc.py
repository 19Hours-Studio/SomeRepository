# Ideas 1-3: share of HBM access energy saved by keeping data on-stack (only off-stack I/O avoided)
tot, io = 3.44, 0.25            # pJ/bit, HBM3e total and I/O (arXiv 2602.18568)
gain_io = 1/(1-io/tot)          # max attention-movement gain vs same top-k algorithm on GPU
print("I/O share %.3f -> max gain %.3fx; margin vs 10x %.3f" % (io/tot, gain_io, gain_io/10))
kaist = 1.104                   # measured PIM-HBM energy-eff gain vs GPU-HBM (KAIST)
print("KAIST margin %.3f" % (kaist/10))
hbm_share = 0.50                # ledger C est.
print("system ratio (I/O) %.3f, (KAIST) %.3f" % (1/(1-hbm_share*(1-1/gain_io)), 1/(1-hbm_share*(1-1/kaist))))
# Idea 4: optical ingress per package to receive 15/16 of all weights every decode step
W = 671e9                       # bytes, DeepSeek-V3/R1 FP8
for tps in (50, 85):
    req = 15/16*W*tps
    print("tok/s/user %d: required ingress %.1f TB/s; NVLink6 per-direction 1.8 TB/s; margin %.3f" % (tps, req/1e12, 1.8e12/req))
import math; print("1:16 split loss %.1f dB" % (10*math.log10(16)))
