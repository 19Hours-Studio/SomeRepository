# Idea 2: memory-light (LPDDR-only) prefill die. DeepSeek-V3.2 (DSA, 671B/37B active, 61 layers, 58 MoE layers, d=7168, expert ffn 2048).
import math
NL, NMOE, D, F = 61, 58, 7168, 2048
W = 671e9*0.5625; WL = W/NL                                   # NVFP4 weights per layer ~6.2 GB
def flops_per_token(L):
    dense = 2*37e9/NL                                         # active params incl. attn proj + shared expert
    idx = 64*128*2*(L/2)                                      # lightning indexer, avg causal position (FP8)
    att = 128*min(L/2,2048)*(576+512)*2                       # sparse MLA over top-2048
    return dense, idx, att
def prefill(L, S, pf_fp4, mem_bw, sram, mfu=0.6, a2a_bw=None, ep=1, mem_cap=None):
    """L prompt length, S tokens per pass (batch of prompts). Returns tok/s, binding term."""
    d,i,a = flops_per_token(L)
    t_comp = NL*(d/pf_fp4 + (i+a)/(pf_fp4/2))/mfu              # indexer/attention at FP8 = half FP4 rate
    per_tok_sram = D*(2+4)                                     # BF16 residual + FP32 layer accumulator
    T = max(1,(sram-100e6)/per_tok_sram)
    passes = math.ceil(S/T)
    w_bytes = (WL/ep)*passes*NL/S                              # weight bytes per token (re-streamed per resident tile)
    act = NL*D*(1+2)                                           # hidden in FP8, out BF16 per layer
    kv = NL*788*(1 + max(0,passes-1)/2)                        # write KV + re-read prefix keys per tile
    t_mem = (w_bytes+act+kv)/mem_bw
    t_net = 0
    if a2a_bw: t_net = NMOE*8*D*3*(ep-1)/ep/a2a_bw             # EP dispatch FP8 + combine BF16
    t = max(t_comp, t_mem, t_net)
    b = {t_comp:'compute', t_mem:'memory', t_net:'network'}[t]
    return 1/t, b, T
cfgs = {
 # name: (PF dense FP4, mem BW, on-die/stacked SRAM, a2a BW, EP)
 'Continuum-P (1 die, 8xLPDDR6 1.4TB/s, 256MB SRAM)': (17.5e15, 1.4e12, 256e6, None, 1),
 'Continuum-P (1 die, 1.4TB/s, +1.2GB SoIC SRAM)':    (17.5e15, 1.4e12, 1.45e9, None, 1),
 'Continuum-P2 (2 dies, 2.8TB/s, 2x1.45GB SRAM)':     (35e15,   2.8e12, 2.9e9, None, 1),
 'Rubin (35PF dense, 22TB/s, EP2 over NVLink6 1.8TB/s/dir)': (35e15, 22e12, 400e6, 1.8e12, 2),
 'CPX-like (30PF, 1.8TB/s GDDR7, EP3, 200GB/s NIC)':  (30e15, 1.8e12, 300e6, 0.2e12, 3),
 'Ironwood (4.6PF FP8 => FP4 n/a, 7.4TB/s, EP2 ICI ~0.6TB/s/dir)': (4.6e15*1.0, 7.4e12, 300e6, 0.6e12, 2),
}
for L in [8192, 32768, 131072, 1048576]:
    S = max(L, 131072)                                         # pack shorter prompts to >=128K tokens per pass
    print(f"\nL={L}, tokens/pass={S}")
    for n,(pf,bw,sr,a2a,ep) in cfgs.items():
        if n.startswith('Ironwood'):   # FP8 only: FP4 rate = FP8 rate
            d,i,a = flops_per_token(L); tc = NL*(d+i+a)/pf/0.6
            r,b,T = prefill(L,S,pf*2,bw,sr,a2a_bw=a2a,ep=ep); r = min(r, 1/tc); b = 'compute' if 1/tc<=r else b
        else:
            r,b,T = prefill(L,S,pf,bw,sr,a2a_bw=a2a,ep=ep)
        print(f"  {n:62s} {r/1e3:8.1f} ktok/s  bind={b:8s} tile={T/1e3:6.1f}k")
d,i,a = flops_per_token(131072); print("\nGFLOP/token @128K: dense %.0f indexer %.0f attn %.0f"%(NL*d/1e9,NL*i/1e9,NL*a/1e9))
# ridge and the idea's own threshold
print("ridge Continuum-P = %.0f FLOP/B (idea claimed 300)"%(17.5e15/1.4e12))
print("MoE expert-stationary activation intensity ~2F = %d FLOP/B (fixed, below ridge -> must keep token tile on-die)"%(2*F))
# KV handoff to decode tier
r,_,_ = prefill(131072,131072,17.5e15,1.4e12,1.45e9)
print("KV handoff per die @128K: %.1f GB/s"%(r*NL*788/1e9))
