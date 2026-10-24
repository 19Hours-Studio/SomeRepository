# Screening arithmetic for the 4 Continuum ideas. All inputs are labelled with their source.
GB=1e9
# ---- known-answer check: Llama-3-70B KV/token BF16 (widely quoted ~320 KB = 80L*8kv*128*2*2B)
L,kvh,hd=80,8,128
kv_tok_bf16=L*kvh*hd*2*2
assert kv_tok_bf16==327680, kv_tok_bf16
# DeepSeek-V3 MLA latent: 61 layers * 576 elems -> 70,272 B/token BF16 (published ~70 KB)
assert 61*576*2==70272
print("known-answer checks OK: Llama70B KV/token",kv_tok_bf16/1024,"KiB; DSV3 MLA",61*576*2/1024,"KiB")

# ---- IDEA 1: $/(GB/s)
hbm3e=350/1229      # SK hynix 12-hi ~$350 (Notebookcheck), 1.2 TB/s per stack (B200 8 TB/s / 8... ~1 TB/s; use 1.2 for 12-hi spec)
hbm3e_b200=350/1000 # at B200's delivered 1 TB/s per stack
pkg=1100/8/1000     # CoWoS share per GB/s (ledger D: $1,100 / 8 stacks / ~1 TB/s)
gddr_lo,gddr_hi=10*2/128,15*2/128   # $10-15/GB card-level (Implicator), 2GB @32Gbps x32 = 128 GB/s
def energy_cost(pj):  # 4yr, 100% util, $0.13/kWh, PUE 1.3, per GB/s
    W=8e9*pj*1e-12; return W*4*8760/1000*0.13*1.3
hbm_all=hbm3e_b200+pkg+energy_cost(3.9)     # HBM ~3.4-3.97 pJ/bit (RPU 3.44; FGDRAM 3.97)
g_all_lo=gddr_lo+energy_cost(5.5); g_all_hi=gddr_hi+energy_cost(5.5)  # GDDR7 ~5-6 pJ/bit est.
print(f"IDEA1 $/(GB/s): HBM3E dev {hbm3e_b200:.3f} +CoWoS {pkg:.3f} +energy -> {hbm_all:.3f}; GDDR7 {g_all_lo:.3f}-{g_all_hi:.3f}; ratio {hbm_all/g_all_hi:.2f}-{hbm_all/g_all_lo:.2f}")
# product level: B200-class BOM $6.4k/8TB/s vs attention card BOM (die $100 + 32GB GDDR7 $320-480 + board $150) / 1.79 TB/s
print(f"  BOM/(GB/s): GPU {6400/8000:.2f}; GDDR7 attention card {(100+320+150)/1792:.2f}-{(100+480+150)/1792:.2f}")
for f in (0.5,0.6,0.7):
    for r in (1.5,2.0,2.5):
        print(f"  KV share of decode cost f={f} cheaper by r={r}: $/token ratio {1/(1-f+f/r):.2f}")

# ---- IDEAS 2/4: removable energy
# Llama-70B-class GQA, FP8 weights 70 GB, FP8 KV, per-GPU batch B
W=70*GB; kv_fp8=kv_tok_bf16/2
for ctx in (16384,32768,131072):
    for B in (8,32):
        kv=B*ctx*kv_fp8; share=kv/(kv+W)
        print(f"IDEA2 ctx {ctx} B {B}: KV share of bytes {share:.2f}")
# GQA intensity: g=8 q heads per kv head, QK+PV = 2*2*g flops per (K,V) element pair ... per byte
g=8
for bytes_per in (2,1):
    print(f"  GQA flop/B at {bytes_per}B KV: {2*g/bytes_per:.0f}")
# per-bit energy: HBM3E 3.44 pJ/bit of which I/O 0.25 (RPU model); GPU-side PHY+NoC+L2 est 0.5-1.0 pJ/bit
for io,gpu_side in ((0.25,0.5),(0.25,1.0),(1.0,1.0)):
    removable=(io+gpu_side)/(3.44+gpu_side)
    for hbm_share,kvs in ((0.5,0.7),(0.6,0.8)):
        saved=hbm_share*kvs*removable
        print(f"  io {io} gpu {gpu_side}: removable/bit {removable:.2f}; HBM share {hbm_share} KV {kvs}: token energy saved {saved:.2f} -> ratio {1/(1-saved):.2f}; margin vs 50% {saved/0.5:.2f}")
print("  even with 100% of KV movement energy removed (0.5*0.7):", round(1/(1-0.35),2),"x  -> halving impossible unless HBM share >= ~70%")

# ---- IDEA 3: DeepSeek-V3 671B FP4 MoE on 72 GB200-class GPUs, MLA KV FP8
cap=671e9*4.5/8/96; print(f"IDEA3 SRAM need/package {cap/GB:.2f} GB vs 4 GB")
sram_area=4096/1.6; print(f"  SRAM area {sram_area:.0f} mm2 = {sram_area/3:.0f} mm2/layer (reticle ~858); N7 cost at $10k/60k mm2 usable, 80% yld: ${sram_area*10000/60000/0.8:.0f}")
PF=5e15; BW=8e12   # GB200 FP8 dense ~5 PF, 8 TB/s per GPU
Wg=671e9*4.5/8/72; act=37e9
for ctx in (8192,32768,131072):
    kvt=61*576*ctx           # FP8 latent bytes per sequence
    attf=ctx*61*128*2*(576+512)
    for B in (4,16,32,64):
        comp=B*(2*act+attf)/PF; mem=(Wg+B*kvt)/BW; mem2=B*kvt/BW
        t0=max(comp,mem); t1=max(comp,mem2)
        print(f"  ctx {ctx} B/gpu {B}: weight share {Wg/(Wg+B*kvt):.2f} comp {comp*1e3:.1f}ms mem {mem*1e3:.1f}ms -> speedup {t0/t1:.2f}")
print(f"  MLA absorbed attn intensity {128*2*(576+512)/576:.0f} FLOP/B vs ridge {PF/BW:.0f}")
