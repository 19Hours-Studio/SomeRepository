# Exact KV arithmetic + ledger-D chain for the 4 prefix-reuse ideas.
def kv_bytes(L, kvh, hd, b): return 2*L*kvh*hd*b
# known-answer checks: Llama-3.1-8B BF16 = 128 KiB/token; 70B = 320 KiB (=327.7 KB, ledger)
assert kv_bytes(32,8,128,2)==131072; assert kv_bytes(80,8,128,2)==327680
n, P, d, L = 20_000, 8.03e9, 4096, 32
flops = 2*P*n + 2*n*n*d*L                      # linear + causal attention (QK,PV)
t_pre = flops/500e12; us_tok = t_pre/n*1e6
bf, f8 = kv_bytes(32,8,128,2), kv_bytes(32,8,128,1)
print(f"prefill 20K: {flops:.3g} FLOP, {t_pre:.2f}s, {us_tok:.1f} us/token")
print(f"KV 20K BF16 {n*bf/1e9:.2f} GB, FP8 {n*f8/1e9:.2f} GB")
for name,bw in [("PCIe4 x16 ~25GB/s",25e9),("PCIe5 x16 ~50GB/s",50e9),("NVMe Gen4 ~7GB/s",7e9)]:
    print(f"  {name}: BF16 load {n*bf/bw:.3f}s, FP8 load {n*f8/bw:.3f}s")
print(f"required BW to hide load: BF16 {bf/(us_tok*1e-6)/1e9:.2f} GB/s, FP8 {f8/(us_tok*1e-6)/1e9:.2f} GB/s")
g = lambda h,pre=0.66: 1/(1-pre*h)
print("gain vs no-reuse: h=0.342 %.3f, h=0.374 %.3f, h=0.5 %.3f"%(g(.342),g(.374),g(.5)))
# idea 2 falsifier at h=0.5 with un-overlapped PCIe4 BF16 load (ledger D: 1.15 GPU-s, 0.76 prefill)
load=n*bf/25e9; print("idea2 h=0.5 with load: %.3f"%(1.15/(1.15-0.5*0.76+0.5*load)))
# idea 4: LRU vs better policy, Mooncake conv trace token-hit (16M tok cap 34.2%, 4M 18.5%, ceiling 37.4%)
c = lambda h: 1-0.66*h
for hl in (0.185,0.342):
    print(f"idea4 LRU h={hl}: +15% -> ratio {c(hl)/c(hl*1.15):.3f}; to ceiling -> {c(hl)/c(0.374):.3f}")
print("16M tokens FP8 8B = %.2f TB; 4M = %.2f TB"%(16e6*f8/1e12, 4e6*f8/1e12))
print("max hit headroom over LRU at 16M cap: %.1f%%"%((0.374/0.342-1)*100))
