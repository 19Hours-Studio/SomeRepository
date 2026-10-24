"""Exact-arithmetic margins for the 4 gate ideas (idea 3 measured in idea3_escalation.py)."""
# ---- Idea 1: FeFET CAM capacity for 4-bit keys
layers, kv_heads, dh = 80, 8, 128          # Llama-3-70B GQA config
ctx, batch = 1_000_000, 32                 # million-token decode, batch-limited serving
cells_user = layers * kv_heads * dh * ctx  # one 4-bit key element per multi-level cell
cell_um2 = 0.01                            # generous: < 1/10 of 28nm 6T SRAM (0.12 um2, GF/TU Dresden)
reticle_mm2 = 858
area_user = cells_user * cell_um2 / 1e6
print(f"I1 cells/user {cells_user:.3g}, key bytes/user {cells_user/2/1e9:.1f} GB, area/user {area_user:.0f} mm2")
print(f"I1 margin (one reticle / batch {batch}) = {reticle_mm2/(area_user*batch):.3f}")
# chain vs DeepSeek DSA at 128K: indexer key 128 B/token/layer FP8, top-2048 x 656 B MLA
L = 128_000
idx = L * 128; topk = 2048 * 656; w = 37e9 / 61 / 32  # active weights per layer per user, batch 32
now, new = idx + topk + w, topk + w
hbm_ratio = now / new
print(f"I1 HBM traffic ratio {hbm_ratio:.2f}, system ratio (HBM 50%) {1/(0.5+0.5/hbm_ratio):.2f}")

# ---- Idea 2: PIM compute throughput
gpu_tok_s = 4130                            # GB200 NVL72, DeepSeek R1 FP4 @125 tok/s/user (InferenceX)
flop_tok = 2 * 37e9
req = gpu_tok_s * flop_tok / 1e12
pim_stack, stacks = 1.2, 8                  # Samsung HBM-PIM 1.2 TFLOPS (ISSCC'21); 8 stacks/package
avail = pim_stack * stacks
print(f"I2 required {req:.0f} TFLOP/s/package, available {avail:.1f} -> margin {avail/req:.3f}; x4 for FP4 units {4*avail/req:.3f}")
gb200_cost = 1.86 / (gpu_tok_s * 3600) * 1e6
pim_tok_s = avail * 1e12 / flop_tok
pim_cost = 0.25 / (pim_tok_s * 3600) * 1e6  # $0.25/package-hr all-in, no vendor margin (generous)
print(f"I2 $/Mtok now {gb200_cost:.3f}, with idea {pim_cost:.3f}, ratio {gb200_cost/pim_cost:.2f}")

# ---- Idea 3: break-even escalation fraction vs NVFP4 (2x FP8 throughput on Blackwell)
t8, t4, t3 = 1.0, 0.5, 0.375
print(f"I3 max escalation to beat NVFP4 f<{t4-t3:.3f}; measured f=1.0 -> margin {(t4-t3)/1.0:.3f}")
print(f"I3 matmul ratio vs FP8 at f=1: {t8/(t3+1):.2f}; vs NVFP4 {t4/(t3+1):.2f}; ceiling at f=0 vs NVFP4 {t4/t3:.2f}")

# ---- Idea 4: optical ingress per chip vs HBM it must beat
rubin_hbm_tbps = 22 * 8                     # Rubin HBM4 ~22 TB/s
b200_hbm_tbps = 8 * 8
cpo = 8 * 4.4                               # 8 chiplets x 4.4 Tb/s (Celestial PF, HOTI'25)
print(f"I4 ingress {cpo:.0f} Tb/s vs Rubin {rubin_hbm_tbps} -> {cpo/rubin_hbm_tbps:.2f}; vs B200 {b200_hbm_tbps} -> {cpo/b200_hbm_tbps:.2f}")
# weight-read share at the InferenceX operating point (EP32, ~70 steps/s with MTP)
w_gpu_gb = 671e9 * 0.5625 / 32 / 1e9 + 8   # expert shard FP4+scales + replicated dense/attn (est.)
wt_tbs = w_gpu_gb * 70 / 1e3
hbm_w = wt_tbs * 8e12 * 3.9e-12            # ~3.9 pJ/bit HBM3E
print(f"I4 weight stream {wt_tbs:.2f} TB/s/GPU ({wt_tbs/8:.0%} of HBM), HBM weight power {hbm_w:.0f} W of ~1200 W")
saved = hbm_w * (15 / 16) / 1200            # fraction of GPU power saved, before optical Rx cost
sys = 1 / (1 - saved * 0.35)                # power-linked cost share (electricity 15 + facility 20)
print(f"I4 system ratio upper bound {sys:.3f}")
