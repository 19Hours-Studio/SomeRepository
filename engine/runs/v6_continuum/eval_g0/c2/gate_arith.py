# Kill-test arithmetic for 4 Continuum ideas
# Known-answer check: DeepSeek-V3 MLA NVFP4 row = 576 dims*4.5b/8 = 324 B (idea 2's stated value); vLLM FP8 layout 656 B
L, ctx = 61, 131072
row = 576*4.5/8; assert row == 324.0
dense = row*L*ctx/1e9
idx = 128*4.5/8*L*ctx/1e9; sel = 2048*row*L/1e9
print(f"[I2] dense KV/token {dense:.2f} GB, sparse {idx+sel:.2f} GB (index {idx:.3f}, gather {sel:.3f}); gather share {sel/(idx+sel):.1%}")
# sparse FLOPs (absorbed MLA 128 heads, 576 QK + 512 PV; indexer 64 heads x 128)
f_attn = 2*(576+512)*128*2048*L; f_idx = 2*64*128*ctx*L
print(f"[I2] sparse attn FLOP/token {(f_attn+f_idx)/1e9:.0f} G, intensity {(f_attn+f_idx)/((idx+sel)*1e9):.0f} FLOP/B -> needs {(f_attn+f_idx)/((idx+sel)*1e9)*22e12/1e15:.1f} PF at 22 TB/s")
# energy of 10 PF FP8 in HBM base dies, B200: 4.5 PF dense FP8 @ ~1000 W -> 0.22 pJ/FLOP
pj = 1000/4.5e15*1e12; P = 10e15*pj*1e-12
print(f"[I2] {pj:.2f} pJ/FLOP -> 10 PF = {P:.0f} W total, {P/8:.0f} W per HBM stack base die (8 stacks)")
# base-die budget estimate: ~0.5 W/mm2 (imec: ~GPU density under DRAM -> 141C; needed freq halving) x ~120 mm2
avail = 0.5*120; print(f"[I2] est. base-die thermal budget {avail:.0f} W/stack -> MARGIN {avail/(P/8):.2f}")
# I1: KV compression vs NVFP4 best practice; Palu 30% rank cut + 3-bit (<~2% LongBench loss, 32K only)
bits = 3+0.25  # 3b + per-block scale
eff = bits*0.70 + 0.02*16*1   # 70% rank kept, ~1% outlier channels at FP16 (k and v)
cf = 16/eff; nv = 16/4.5
print(f"[I1] idea {cf:.1f}x vs FP16, NVFP4 {nv:.2f}x -> {cf/nv:.2f}x KV over best practice")
for kvshare in (0.25,0.35):
    print(f"[I1] KV share {kvshare}: step time ratio {1/(1-kvshare+kvshare*nv/cf):.2f}x")
# I3: capacity / bandwidth model (BW-bound, memory full): tokens/s/pkg -> BW/kvbytes as N grows
W = 1e12*4.5/8  # 1T params at 4.5 b
kv = 8*128*2*4.5/8*60*131072  # GQA 8 kv heads, 60 layers, 128K
def tps(C,BW,N): B=(N*C-W)/kv; step=(N*C)/(N*BW); return B/step/N
for N in (8,16,32):
    c=tps(160e9,64e12,N)/2.0; r=tps(288e9,22e12,N)/1.8
    print(f"[I3] N={N}: Continuum {c:.0f} tok/s/kW, Rubin {r:.0f} -> {c/r:.2f}x; step {160/64:.1f} ms vs {288/22:.1f} ms")
need_bw_per_gb = 64e12/1280/1e9; print(f"[I3] needs {need_bw_per_gb:.0f} GB/s/Gb vs SeDRAM 135 (VLSI'23); density {1280/(4*4*400):.2f} Gb/mm2 per DRAM die")
for pjb in (0.8,1.5,2.0): print(f"[I3] DRAM power @ {pjb} pJ/b = {64e12*8*pjb*1e-12:.0f} W of 2000 W")
# I4: SRAM saving on compute-bound SKU
for s in (0.10,0.15): print(f"[I4] saving {s:.0%} of pkg (45% share) -> cost ratio {1/(1-0.45*s):.3f}")
