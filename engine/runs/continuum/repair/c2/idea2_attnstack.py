# Idea 2: GQA decode attention in HBM4 base die. Round 1 = GPU-attached (original); Round 2 = detached SPHBM4 attention stacks.
# Energy (pJ/bit). HBM side from FACT 6/7 (3.44 total; I/O 0.25). GPU-side movement are ESTIMATES (flagged):
hbm_total=3.44; hbm_io=0.25
gpu_phy=0.25           # host-side PHY, assume symmetric with DRAM-side I/O (est.)
noc_mm=0.08; dist=15   # ~80 fJ/bit/mm on-chip wire (Dally-class figure), PHY->L2->SM ~15 mm (est.)
sram_rw=0.15*3         # L2 write+read, SMEM write/read ~0.15 pJ/b each (est.)
base_local=0.08*3+0.15 # TSV landing -> local buffer -> MAC, ~3 mm + one SRAM pass (est.)
gpu_path=hbm_total+gpu_phy+noc_mm*dist+sram_rw
stack_path=hbm_total-hbm_io+base_local
print(f"KV bit to MAC: GPU-attached {gpu_path:.2f} pJ/b, in-base-die {stack_path:.2f} pJ/b, saving {1-stack_path/gpu_path:.0%} (claim was ~2x)")

# Workload: Llama-3.1-70B-class GQA (80 layers, 64 q heads, 8 kv heads, hd 128), 128K context
Lyr=80; qh=64; kvh=8; hd=128; ctx=131072
for name,bpe in (("FP8",1.0),("NVFP4 KV",0.5625)):
    kv_tok=2*Lyr*kvh*hd*bpe
    print(f"{name}: KV/token {kv_tok/1e3:.0f} KB, per user @128K {kv_tok*ctx/1e9:.1f} GB, attention FLOP/B {2*2*qh/kvh*hd*kvh*Lyr/ (kv_tok):.1f}")
# base-die power: intensity x bandwidth; pJ/FLOP at FP8 incl local SRAM on N5/N4 logic (est. 0.4-0.6)
BW=2.0e12  # HBM4 2048-bit @ 8 Gb/s; SPHBM4 same bandwidth via 512 x 4:1
for I,lab in ((16,"FP8 KV"),(28.4,"FP4 KV->FP8 math")):
    for pj in (0.4,0.6):
        print(f"  {lab}: {I*BW/1e12:.0f} TFLOPS/stack, {I*BW*pj*1e-12:.0f} W @ {pj} pJ/FLOP")
mla_I=2*128*(576+512)/576
print(f"MLA absorbed decode intensity {mla_I:.0f} FLOP/B -> {mla_I*BW*0.4e-12:.0f} W/stack: excluded")
dsa_I=2*64*128/128
print(f"DSA lightning-indexer scan {dsa_I:.0f} FLOP/B -> {dsa_I*BW*0.4e-12:.0f} W/stack: excluded")
dram_W=(hbm_total-hbm_io)*BW*8e-12
print(f"DRAM core power at full BW {dram_W:.0f} W/stack; base logic +{16*BW*0.5e-12:.0f} W; PHY removed -{hbm_io*BW*8e-12:.0f} W")

# Link bytes per stack: q in + partial (o, m, l) out per user-shard per layer
def link(users_on_stack, step_s, frac_ctx=1.0):
    per=Lyr*(qh*hd*2 + qh*hd*2 + qh*8)
    return users_on_stack*per/step_s
cap=48e9  # 16-high 24Gb HBM4 = 48 GB
for name,bpe in (("FP8",1.0),("FP4",0.5625)):
    kvu=2*Lyr*kvh*hd*bpe*ctx; u=cap*0.9/kvu; step=cap*0.9/(BW*0.85)
    print(f"stack {name}: {u:.1f} users@128K, step {step*1e3:.1f} ms -> {1/step:.0f} tok/s/user, link {link(u,step)/1e9:.2f} GB/s, ratio KV/link {cap*0.9/step/link(u,step):.0f}x")
# per-layer round-trip latency budget
rt=2e-6; print(f"latency: {Lyr} layers x {rt*1e6:.0f} us RT = {Lyr*rt*1e3:.2f} ms/step (hidden by 2-microbatch ping-pong)")
