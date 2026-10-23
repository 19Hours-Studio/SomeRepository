# Final repaired designs: bits incl. ALL metadata, aggregate error vs uniform K4V4, both contexts.
import numpy as np
rel = {1: 1.45, 2: 0.50, 3: 0.215, 4: 0.10}; s = 1.5
OV, CTR = 0.25, 0.125                        # scale+zero per 128; FP16 channel mean per 128-token block
def side(ctx, win): return (4 + win) * 16 / ctx
print("Idea1 gates on E_h=sqrt(sum_q p^2):", {b: round(rel[4]/(rel[b]*s),3) for b in (1,2,3)})
for ctx in (32768, 131072):
    for name, f in {"cons": (0.5,0.2,0.3,0.0), "mid": (0.3,0.2,0.3,0.2), "long/opt": (0.3,0.1,0.2,0.4)}.items():
        V = f[0]*(4+OV) + f[1]*(3+OV+CTR) + f[2]*(2+OV+CTR) + f[3]*(1+OV+CTR)
        b = (4+OV+V)/2 + side(ctx,128)
        nb = f[1]+f[2]+f[3]; agg = np.sqrt(1 + (nb/f[0])*(1/s**2))   # quadrature vs K4V4 (low tiers sit at <= target/s)
        print(f"Idea1 ctx={ctx//1024}k {name:9s} bits={b:.2f} x{16/b:.2f}  agg err <= {agg:.2f}x K4V4")
print("Idea2 gates on m_q (mass on quantized tokens):", {b: round(rel[4]/(rel[b]*s),3) for b in (2,3)})
for ctx in (32768, 131072):
    for win in (128, 512):
        for name, f in {"cons": (0.5,0.2,0.3), "mid": (0.3,0.2,0.5), "opt": (0.2,0.1,0.7)}.items():
            b = f[0]*(4+OV) + f[1]*(3.5+OV+CTR/2) + f[2]*(2.5+OV+CTR/2) + side(ctx,win)
            agg = np.sqrt(1 + ((f[1]+f[2])/f[0])/s**2)
            print(f"Idea2 ctx={ctx//1024}k win={win} {name:5s} bits={b:.2f} x{16/b:.2f} agg<= {agg:.2f}x K4V4")
