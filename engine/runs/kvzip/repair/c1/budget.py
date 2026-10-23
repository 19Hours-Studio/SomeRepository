import numpy as np
d=128
def eff_bits(body_bits, L, sinks=4, window=128, hi_bits=16, meta_per_vec_bits=8, basis_bits=0, n_basis=0):
    # bits per stored value averaged over context L (per head), metadata included
    body=L-sinks-window
    tot=body*(d*body_bits+meta_per_vec_bits)+(sinks+window)*d*hi_bits+n_basis*basis_bits
    return tot/(L*d)
print("== Idea1 repaired: band-E8 keys 3.0b (4x4b,8x3b,4x2b groups of 8), values E8 2b, FP8 scale/token/head, FP16 sinks+window")
for L in (4096,32768,131072):
    k=eff_bits(3.0,L); v=eff_bits(2.0,L); kb=k+ (16*1/ (L*d))  # +16-bit band permutation table per head (64 pair ids*6b=384b) negligible
    perm=64*6/(L*d)
    m=(k+v)/2+perm; print(f" L={L:6d} K={k:.3f} V={v:.3f} mean={m:.3f} b/value  ratio vs FP16={16/m:.2f}x  vs FP8={8/m:.2f}x")
print("== Idea2 repaired: KLT keys (post-RoPE) ~2.5b avg, values KLT 2.5b, FP8 norm/token, FP16 basis 128x128 + 128 mean per segment")
for L,seg in ((4096,1),(32768,2),(131072,4)):
    bb=(d*d+d)*16
    k=eff_bits(2.5,L,basis_bits=bb,n_basis=seg); v=eff_bits(2.5,L,basis_bits=bb,n_basis=seg)
    print(f" L={L:6d} segs={seg} basis overhead={seg*bb/(L*d):.3f} b  mean={(k+v)/2:.3f} b/value ratio={32/(k+v):.2f}x")
print(" claimed '<0.01 b' basis overhead check at 32k, 1 basis FP16:", (d*d*16)/(32768*d))

# ---- decode roofline / serving cost: Llama-3.1-8B (32L, 8 KV heads, hd128), H100 SXM 3.35TB/s, 80GB
BW=3.35e12; HBM=80e9; W=16.06e9  # BF16 weights bytes
per_tok_vals=32*8*128*2  # K+V values per token
price=2.99  # $/GPU-hr (Lambda on-demand H100 SXM list, 2025)
def serve(bits, L=32768, acc=None, name=""):
    kv_seq=per_tok_vals*L*bits/8
    B=int((HBM*0.9-W)//kv_seq)
    t_step=(W+B*kv_seq)/BW          # memory-bound decode step
    tps=B/t_step; cost=price/3600/tps*1e6
    s=f" {name:34s} {bits:5.2f}b batch={B:4d} tok/s={tps:7.0f} $/Mtok={cost:6.3f}"
    if acc: s+=f"  AIME24 acc={acc:.1f}% -> $ per 1k correct answers (12k tok each)={cost*12e-3/(acc/100)*1000:7.2f}"
    print(s); return cost
print("== serving cost at 32k context (decode, memory-bound model; quality numbers: R1-Distill-Qwen-7B AIME24, Block-GTQ paper)")
serve(16,acc=54.2,name="BF16 KV")
serve(8.06,acc=54.2,name="FP8 KV (assume lossless)")
serve(4.5,acc=None,name="NVFP4 KV (quality on AIME unmeasured)")
serve(2.6,acc=51.7,name="Block-GTQ K3V2 (~2.5b+meta)")
serve(2.2,acc=54.2-3.5,name="KITTY ~2.x b (-3..4 pts, Kitty paper)")
serve(2.13,acc=41.0,name="KIVI K2V2 (~-13 pts AIME)")
serve(2.57,acc=54.2-2.0,name="Idea1 band-E8 K3V2 (PREDICTED <=2pt)")
serve(2.6,acc=54.2-2.0,name="Idea2 KLT 2.5b (PREDICTED)")
# ---- kernel arithmetic intensity, Idea1 decode on H100 (CUDA-core ridge = 67e12/3.35e12 = 20 op/B)
for g in (1,4,8):
    bytes_tok=128*(3.06+2.06)/8
    ops_decode=128*2*4          # LUT+sign+scale per value, K and V, decoded once per KV head
    ops_dot_cuda=128*2*2*g      # if dot on CUDA cores
    print(f" GQA g={g}: decode-only {ops_decode/bytes_tok:.1f} op/B ; decode+dot on CUDA cores {(ops_decode+ops_dot_cuda)/bytes_tok:.1f} op/B (ridge 20) ")
# Idea2: per-step basis transforms vs attention FLOPs
for L in (4096,32768,131072):
    segs=max(1,L//32768); extra=2*2*128*128*segs; att=2*2*128*L
    print(f" Idea2 L={L}: q/o basis transforms {extra:.2e} FLOP vs attention {att:.2e} per q-head -> +{100*extra/att:.2f}%")
# killer from kill-test (pre-RoPE reconstruct): 2*128*128 FLOP per key per KV head = 32768 FLOP per 40B
print(" original Idea2 (reconstruct each key):",2*128*128/40,"FLOP/B vs H100 dense BF16 TC ridge 989e12/3.35e12=",989e12/3.35e12)
# prefill overheads, 70B-class (80L, 8KV, 64Q), L=32k
L=32768; cov=80*(8*2+64)*2*128*128*L; pf=2*70e9*L
print(f" Idea2 prefill covariance accumulation {cov:.2e} FLOP vs prefill matmul {pf:.2e} -> +{100*cov/pf:.2f}%")
enc=80*8*2*128*60*L   # E8 closest-point (Conway-Sloane D8 + coset) ~60 ops / value incl. RVQ second stage
print(f" Idea1 prefill E8 encode {enc:.2e} op vs {pf:.2e} -> +{100*enc/pf:.3f}%")
