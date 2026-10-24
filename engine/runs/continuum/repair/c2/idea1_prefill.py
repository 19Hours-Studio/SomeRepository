# Idea 1: memory-light (LPDDR-only) prefill die. Roofline + cost model.
# Model: DeepSeek-V3-class MoE (public config: 61 layers, 3 dense, d=7168, 256 routed experts top-8 + 1 shared,
# expert inter 2048, MLA q_lora 1536 kv_lora 512 rope 64, 128 heads, qk_nope 128, v 128). Llama-3.1-70B-class GQA dense.
import math
d=7168; L=61; Ldense=3; Lmoe=58
exp_p=3*d*2048
attn_p=d*1536+1536*128*192+d*576+512*128*256+128*128*d
dense_ffn_p=3*d*18432
routed_total=256*exp_p*Lmoe
nonexp=L*attn_p+Lmoe*exp_p+Ldense*dense_ffn_p
tot=routed_total+nonexp
act_per_tok=(L*attn_p+Lmoe*9*exp_p+Ldense*dense_ffn_p)
print(f"DSV3 params: routed {routed_total/1e9:.0f}B nonexpert(ex-embed) {nonexp/1e9:.1f}B total {tot/1e9:.0f}B active/tok {act_per_tok/1e9:.1f}B")
BPP=0.5625  # NVFP4: 4b + E4M3 scale per 16 -> 4.5 bit
W=tot*BPP
def attn_flops_tok(ctx):  # causal prefill, average over sequence: 2 matmuls * heads*(dqk+dv)/... per token per layer
    return L*2*128*(192+128)*ctx/2
flop_tok=lambda ctx: 2*act_per_tok+attn_flops_tok(ctx)
print(f"FP4 weights {W/1e9:.0f} GB; FLOP/token @8K {flop_tok(8192)/1e9:.0f} GF, @128K {flop_tok(131072)/1e9:.0f} GF")

# Kill-test claim: single die, 30 PF, 1 TB/s -> ridge 30,000 FLOP/B. Per-expert intensity = 2*tok_per_expert/BPP
for T in (8192, 65536, 262144, 1<<20):
    tpe=T*8/256
    print(f"  global tokens/pass {T:>8}: tokens/expert {tpe:7.0f}, expert FLOP/B {2*tpe/BPP:9.0f}")

# Repaired design: N-stage layer pipeline, each die = its layers' weights resident in LPDDR, layer-major mega-batch.
PF_peak=10e15; util=0.6; BW=1.37e12*0.8   # 1024-bit LPDDR5X-10.7 = 1.37 TB/s, 80% sustained
act_bytes_tok_layer=2*d*2*2   # BF16 hidden read+write, x2 for MoE dispatch/combine buffers
kv_tok_layer=576*1.0+576/16    # MLA latent FP8 + scales
def stage(N, T, ctx=8192):
    w=W/N; lay=L/N
    t_c=T*flop_tok(ctx)/N/(PF_peak*util)
    bytes_=w+T*lay*(act_bytes_tok_layer+kv_tok_layer*2)  # KV written then read for egress
    t_m=bytes_/BW
    return t_c,t_m,w
print("\nN  T/pass  stage_c(ms) stage_m(ms) bound  W/die(GB) TTFT(s)  tok/s/die  ridgeT")
for N in (4,8,16):
    for T in (8192,32768,65536):
        tc,tm,w=stage(N,T); ts=max(tc,tm)
        Tbal=(w/BW)/(flop_tok(8192)/N/(PF_peak*util))
        print(f"{N:<3}{T:>7}  {tc*1e3:9.1f} {tm*1e3:10.1f}  {'C' if tc>tm else 'M'}   {w/1e9:7.1f}  {N*ts:6.2f}  {T/ts/N:9.0f}  {Tbal:7.0f}")
N=8; T=32768
tc,tm,w=stage(N,T); ts=max(tc,tm); tps_die=T/ts/N
hop=T*2*d*2/ts   # BF16 hidden across a stage boundary
kv_egress=T*(L/N)*kv_tok_layer/ts
print(f"\nchosen N={N},T={T}: per-die {tps_die:.0f} tok/s, inter-stage {hop/1e9:.1f} GB/s, KV egress/die {kv_egress/1e9:.2f} GB/s, LPDDR util {min(1,tm/ts):.2f}")
# GQA 70B dense: KV 160 KB/token FP8 egress check
kv70=2*80*8*128*1.0; tps70=PF_peak*util/(2*70e9)
print(f"70B GQA on one die: {tps70:.0f} tok/s, KV egress {kv70*tps70/1e9:.1f} GB/s = {kv70*tps70*8/1e9:.0f} Gb/s; weights {70e9*BPP/1e9:.0f} GB")
# all-to-all EP alternative (what the pipeline avoids): bytes per token per MoE layer, 8 experts FP8 dispatch + BF16 combine
a2a=tps_die*N*(8*d*1+8*d*2)*Lmoe/N
print(f"EP alternative would need all-to-all {a2a/1e12:.2f} TB/s per die (vs pipeline {hop/1e9:.0f} GB/s)")

# ---------------- cost per million prefill tokens ----------------
def die_cost(area_mm2, wafer=20000, D0=0.10):
    r=150; dpw=math.pi*r*r/area_mm2 - math.pi*2*r/math.sqrt(2*area_mm2)
    y=((1-math.exp(-D0*area_mm2/100))/(D0*area_mm2/100))**2  # Murphy
    return wafer/(dpw*y)
amort_yr=4; hrs=amort_yr*8766; elec=0.08; pue=1.25; sys_overhead=0.35  # rack/net/host as fraction of accel COGS
def cpm(cogs, watts, tps, markup=1.0):
    capex=cogs*(1+sys_overhead)*markup
    per_hr=capex/hrs + watts*pue/1000*elec
    return per_hr/(tps*3600)*1e6
lp_price=10.0
c_die=die_cost(800)
rows=[]
for lp in (7.8,10,21):
    cont_cogs=c_die+64*lp+250+400    # die + 64 GB LPDDR5X (8 pkgs) + organic pkg + board/VRM/cold plate share
    cont_w=750+25
    rows.append(("Continuum-P (8-stage) LPDDR $%.1f/GB"%lp, cont_cogs, cont_w, tps_die))
fl=flop_tok(8192)
# Baselines, same util, same model; compute-bound prefill (competent operator: PP or EP on NVLink, FP4)
hbm4=16.0; hbm3e=12.4
rubin_cogs=2*die_cost(800)+288*hbm4+1800+600   # 2 N3 dies + 288 GB HBM4 + CoWoS-L + substrate/board
b200_cogs=2*die_cost(800,wafer=17000)+192*hbm3e+1200+500
cpx_cogs=die_cost(800)+168*hbm4+1500+500      # revived CPX: 168 GB HBM4 (Kuo, Aug 2026)
rows+= [("Rubin (35 PF dense FP4, 288GB HBM4)", rubin_cogs, 2000, 35e15*util/fl),
        ("Rubin CPX-HBM4 (30 PF, 168GB)", cpx_cogs, 2300*0.8, 30e15*util/fl),
        ("B200 (9 PF dense FP4)", b200_cogs, 1000, 9e15*util/fl),
        ("H100 FP8 (2 PF), cheapest fleet", 3300, 700, 1.98e15*util/fl)]
print(f"\nN3 800mm2 die cost ${c_die:.0f}")
print(f"{'design':42s} {'COGS$':>7} {'W':>5} {'tok/s':>8} {'$/PF':>6} {'$/Mtok(COGS)':>12}")
for n,c,wt,t in rows:
    pf=t*fl/util/1e15
    print(f"{n:42s} {c:7.0f} {wt:5.0f} {t:8.0f} {c/pf:6.0f} {cpm(c,wt,t):12.4f}")
# market-price view: rented B200 $4.5/h, H100 $2.2/h; Rubin $55K/GPU (MS via Wccftech) ; Continuum at 70% GM
print("\nprice view:")
print(f" B200 rent $4.5/h: ${4.5/(9e15*util/fl*3600)*1e6:.4f}/Mtok; H100 rent $2.2/h: ${2.2/(1.98e15*util/fl*3600)*1e6:.4f}/Mtok")
print(f" Rubin @ $55K: ${cpm(55000/(1+sys_overhead),2000,35e15*util/fl):.4f}/Mtok ; Continuum-P @70%GM: ${cpm(rows[1][1]/0.3,775,tps_die):.4f}/Mtok")
# HBM demand: share of fleet HBM bits in prefill when P:D GPU ratio = 1:1 (Dynamo DSV3.2 recipe, 2P+2D)
print("HBM-bits removed per served token if prefill share of GPUs = 0.5 -> 50% (only if decode tier unchanged)")
# power density
print(f"power density {775/800:.2f} W/mm2 (B200 ~1000W/1600mm2 = {1000/1600:.2f})")
