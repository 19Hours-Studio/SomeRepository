# Archetype B roofline: 8B dense GQA (128 KB/token @FP16), 32k generated tokens, H100 80GB, 3.35 TB/s
BW=3.35e12; W=16e9; KVB=60e9; ctx=32768; tok16=128*1024
def per_tok(bits, extra_step_s=0.0, hbm_bits=None):
    hb=hbm_bits or bits
    peak=tok16*ctx*hb/16; B=int(KVB//peak)
    t_step=W/BW + B*(tok16*ctx/2*bits/16)/BW + extra_step_s   # avg ctx = 16k
    return t_step/B*1.10, B   # +10% kernel/launch/sampling overhead
base,Bb=per_tok(4.5)   # NVFP4: 4b E2M1 + FP8 scale per 16 = 4.5 b
print(f"NVFP4 4.5b: batch {Bb}, {base*1e3:.3f} ms/token")
for name,b in [("Idea1 HadE8 2.57b",2.57),("Idea2 dither 2.65b",2.65),("Idea3 E8 2b 2.13b",2.13)]:
    t,B=per_tok(b); print(f"{name}: batch {B}, {t*1e3:.3f} ms/tok, RATIO {base/t:.2f}")
# Idea 4: base 2.25b hot; residual 2b for top 5% pages, refetched per step
# (a) residual in HBM: held 4.25 b
t,B=per_tok(2.25+0.05*2, hbm_bits=4.25); print(f"Idea4 resid-in-HBM: batch {B}, {t*1e3:.3f} ms/tok, RATIO {base/t:.2f}")
# (b) residual in CPU over PCIe Gen5 x16 (~55 GB/s achievable of 64 GB/s)
PCIe=55e9; Bc=int(KVB//(tok16*ctx*2.25/16))
pcie_bytes=Bc*0.05*(ctx/2)*tok16*2/16
t,B=per_tok(2.25, extra_step_s=pcie_bytes/PCIe, hbm_bits=2.25)
hbm_step=W/BW+Bc*(tok16*ctx/2*2.25/16)/BW
print(f"Idea4 resid-on-CPU: batch {B}, PCIe {pcie_bytes/1e9:.2f} GB/step = {pcie_bytes/PCIe*1e3:.1f} ms vs HBM step {hbm_step*1e3:.1f} ms; {t*1e3:.3f} ms/tok RATIO {base/t:.2f}")
print(f"  PCIe budget margin (time to fetch must be <= HBM step to hide): {hbm_step/(pcie_bytes/PCIe):.2f}")
for b,n in [(2.57,1),(2.65,2),(2.13,3),(2.25,4)]: print(f"idea{n}: {16/b:.2f}x vs FP16, {4.5/b:.2f}x vs NVFP4")
