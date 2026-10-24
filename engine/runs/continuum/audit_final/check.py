"""Adversarial recomputation of the 4 Continuum ideas. All units SI unless noted."""
GB = 1e9; TB = 1e12; PF = 1e15
# ---- DeepSeek-V3 shape (public config.json) ----
H, I_moe, L, L_moe, E, k = 7168, 2048, 61, 58, 256, 8
p_exp = 3 * H * I_moe                      # params per routed expert
B4 = 4.5 / 8                               # NVFP4 bytes/param incl. scales
W_tot = 671e9 * B4
print("== IDEA 1 ==")
print(f"NVFP4 weights {W_tot/GB:.0f} GB; per die /8 {W_tot/8/GB:.1f} GB")
print(f"LPDDR5X 1024b @10.7Gbps = {1024*10.7e9/8/TB:.2f} TB/s")
print(f"tokens/expert at 8K pass = {8192*k/E:.0f}; FLOP/B = {8192*k/E*2/B4:.0f}")
bal = 20 * PF / 1.37e12
print(f"die balance {bal:.0f} FLOP/B")
tok_exp_needed = bal * B4 / 2
print(f"routed-expert compute-bound needs {tok_exp_needed:.0f} tok/expert -> {tok_exp_needed*E/k/1e3:.0f}K tok/pass")
# aggregate (all weights read once, all FLOPs incl. causal attention)
att_per_tok_layer = lambda ctx: 2 * ctx * 128 * (192 + 128)   # MLA prefill, non-absorbed
for name, ctx in [("causal avg 4K", 4096), ("full 8K", 8192)]:
    f = 2 * 37e9 + L * att_per_tok_layer(ctx)
    print(f"  {name}: {f/1e9:.0f} GFLOP/tok -> aggregate break-even {bal*W_tot/f/1e3:.0f}K tok/pass")
# activation round-trip intensity for routed experts (mega-batch can't live in SRAM)
fl = 2 * p_exp
for nm, by in [("FP8 in+FP8 out", 2 * H), ("FP8 in+BF16 out", 3 * H)]:
    ai = fl / by
    print(f"  activation-only intensity ({nm}) {ai:.0f} FLOP/B -> caps routed experts at {ai*1.37e12/PF:.1f} PF = {ai/bal*100:.0f}% of 20 PF")
megabatch = 45e3 * H * 1        # FP8 hidden state per layer
print(f"  45K mega-batch hidden state per layer FP8 {megabatch/1e6:.0f} MB, BF16 {2*megabatch/1e6:.0f} MB (on-chip SRAM not budgeted)")
# TTFT
f4 = 2 * 37e9 + L * att_per_tok_layer(4096)
for mfu in (1.0, 0.4, 0.3):
    t = 45e3 * f4 / (8 * 20 * PF * mfu) * 8   # batch traverses 8 dies serially
    print(f"  TTFT for one 45K mega-batch through 8 dies @MFU {mfu}: {t:.2f} s")
thr = 8 * 20 * PF * 0.4 / f4
print(f"  system prefill @0.4 MFU {thr/1e3:.0f}K tok/s; activation crossing BF16 {thr*H*2/GB:.1f} GB/s; KV egress/die FP8 {thr*576*L/8/GB:.1f} GB/s")
print(f"  W/mm2 die {1180/800:.2f}; Rubin 2300W over ~1600mm2 {2300/1600:.2f}")
# memory $ per PF at 2026 prices
for lp in (10, 20):
    print(f"  LPDDR ${lp}/GB: 64GB={64*lp}$ per 20PF -> ${64*lp/20:.0f}/PF ; Rubin HBM 288GB*$15.3={288*15.3:.0f}$ -> ${288*15.3/50:.0f}/PF(50) ${288*15.3/35:.0f}/PF(35 dense)")

print("== IDEA 2 ==")
kv_tok = 80 * 8 * 128 * 2 * 1               # Llama-70B-class GQA FP8 KV bytes/token
kv_user = kv_tok * 128 * 1024
print(f"KV/user 128K {kv_user/GB:.1f} GB; 2 users {2*kv_user/GB:.1f} GB of 48")
rate = 2.5 * TB / kv_user
print(f"stack-limited tok/s total {rate:.0f}; 2x49={98} -> BW eff {98/rate*100:.0f}%")
link = 80 * (64 * 128 * 2 * 2 + 64 * 2 * 4)  # q + partial out BF16 + (m,l) stats
print(f"link bytes/token {link/1e6:.2f} MB; ratio {kv_user/link:.0f}; link rate {98*link/GB:.2f} GB/s")
for st in (400, 600, 760):
    print(f"  {st} stacks -> GPU-side link {st*98*link/GB:.0f} GB/s (CX-9 1.6Tb/s = 200 GB/s)")
print(f"  per-layer time budget at 49 tok/s: {1/49/80*1e6:.0f} us (80 serial GPU<->stack round-trips/token)")
pj = 3.58e-12
print(f"  DRAM+path energy at 2.5TB/s, 3.58pJ/b: {2.5*TB*8*pj:.0f} W per stack (+13-19 W base die)")
att_fl = 4 * 128 * 1024 * 64 * 128 * 80
print(f"  attention FLOP/tok {att_fl/1e9:.0f} G -> {att_fl*98/1e12:.0f} TFLOP/s FP8 per base die")
# HBM bits per delivered token/s
users = 1500; tps = users * 49
hbm_idea = users / 2 * 48
print(f"  HBM per tok/s: idea {hbm_idea/tps:.3f} GB vs Rubin-only {288/ (22e12/kv_user*0.9):.3f} GB  (Rubin {22e12/kv_user*0.9:.0f} tok/s, {int((288-35)/ (kv_user/GB))} users)")
for p in (15.3, 36, 53):
    print(f"  HBM $/GB {p}: KV tier HBM cost {hbm_idea*p/1e6:.2f} M$ per Rubin; per Mtok over 4y {hbm_idea*p/(tps*4*3.156e7/1e6):.3f}")
# DSA-style sparse attention (top-2048) cuts per-token KV read
print(f"  sparse-attn top-2048 reads {2048/(128*1024)*100:.1f}% of dense 128K KV -> {128*1024/2048:.0f}x fewer KV bytes")

print("== IDEA 3 ==")
lay = 6.9 / 4
print(f"SRAM layer {lay:.3f} GB -> {lay*1e3/2.29:.0f} mm2 at 2.29 MB/mm2; rack {72*2*6.9:.0f} GB")
print(f"DSV3 2 layers rack {72*2*2*lay:.0f} GB vs {W_tot/GB:.0f}; Kimi-K2 1.04T NVFP4 {1.04e12*B4/GB:.0f} GB vs 3 layers {72*2*3*lay:.0f}")
print(f"claimed savings $10-14k/4 stacks -> ${10e3/4:.0f}-{14e3/4:.0f}/stack = ${10e3/144:.0f}-{14e3/144:.0f}/GB")
for s in (550, 600, 1300, 1900):
    print(f"  stack ${s}: saved {4*s} - added 4300 = net {4*s-4300:+d} $/package")
mla_ai = 2 * 128 * (576 + 512) / 576
print(f"MLA absorbed decode intensity DSV3 {mla_ai:.0f} FLOP/B (FP8 KV); Kimi-K2 64 heads {mla_ai/2:.0f}; GQA-8 (Llama-70B) {2*2*64*128/(8*128*2):.0f}")
for fp8 in (17.5, 25):
    print(f"  Rubin FP8 {fp8} PF / 22 TB/s = {fp8*PF/22e12:.0f}; /11 TB/s = {fp8*PF/11e12:.0f} FLOP/B")
# DSV3 32K decode per token on Rubin
ctx = 32768
f_att = L * 2 * 128 * (576 + 512) * ctx
kv_read = L * 576 * ctx
for mfu in (0.35, 0.67):
    c = 17.5 * PF * mfu / (2 * 37e9 + f_att)
    for bw in (22, 11):
        m = bw * TB / kv_read
        print(f"  MFU {mfu} BW {bw}: compute-cap {c:.0f}, KV-BW-cap {m:.0f} tok/s/GPU -> {min(c,m):.0f}")
print("  (FlashMLA reports ~660 TFLOPS BF16 on H800 = 67% of peak)")

print("== IDEA 4 ==")
Mib = 1.25e9 * 8 / 2**20
print(f"1.25 GB SRAM = {Mib:.0f} Mib -> {Mib/31.8/0.7:.0f} mm2; total {333*1.25:.0f} GB")
print(f"LPDDR6 26 x24 @14.4 = {26*24*14.4e9/8/TB:.2f} TB/s ; total LPDDR {333*48/1e3:.1f} TB")
kv4 = L * 576 * B4 * ctx
print(f"KV/user 32K NVFP4 {kv4/GB:.2f} GB; LPDDR-BW cap {333*TB/kv4/1e3:.0f}K tok/s")
print(f"J/token 117kW/414k = {117e3/414e3:.3f} (claimed 0.19-0.20)")
print(f"hop floor 1/85us = {1/85e-6:.0f} tok/s; per-group {85/61:.2f} us")
print(f"concurrent users at 414k tok/s and 1000 tok/s/user = {414e3/1000:.0f}; KV in use {414*kv4/GB:.0f} GB of {333*48/2:.0f} GB (after replica)")
for lp in (10, 20):
    print(f"  LPDDR6 {333*48:.0f} GB x ${lp} = ${333*48*lp/1e6:.2f}M vs BOM $0.81M")
toks = 414e3 * 4 * 3.156e7 / 1e6
for capex in (2.44e6, 2.44e6 + 333 * 48 * 20 * 3):
    print(f"  capex {capex/1e6:.2f}M /4y -> {capex/toks:.3f} $/Mtok (excl power/DC)")
print(f"SRAM $/GB: 333 dies x ~$700 / 416 GB = ${333*700/416:.0f}/GB")
# failure blast radius: Llama-3 405B 16K H100, 54 days: 148 GPU + 72 HBM faults
afr = (148 + 72) / 16384 / 54 * 365
print(f"accel AFR (Llama3 data) {afr*100:.1f}%/yr -> {333*afr:.0f} die faults/yr, one per {365/(333*afr):.0f} days; spare SRAM {(416-377)/1.25:.0f} dies")
