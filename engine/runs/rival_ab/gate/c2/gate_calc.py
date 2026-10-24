# Known-answer check: B200 ridge = 4.5 PF FP8 dense / 8 TB/s = ~562 FLOP/B (idea 3 quotes ~560)
print("B200 ridge", 4.5e15/8e12)
# HBM4 4 stacks @ 2 TB/s (JEDEC-class 2048b x 8 Gb/s) -> ridge with 4.5 PF
print("4xHBM4 ridge", 4.5e15/(4*2.0e12), " 4xHBM3E ridge", 4.5e15/(4*1.0e12))
# ---- per-bit energy path (pJ/bit) ----
dev=3.44        # HBM3E device total, arXiv 2602.18568
dev_io=0.25     # device I/O share in same model
host_phy=0.3    # host PHY + interposer (est.)
host_noc=1.0    # PHY->L2->SM on ~800mm2 die, ~0.1 pJ/bit/mm x ~10mm (est.)
gpu_path=dev+host_phy+host_noc
base_logic=0.22*2+0.1   # GQA g=8, FP8: 2 FLOP/bit x 0.22 pJ/FLOP (B200 1000W/4.5PF) + SRAM
base_path=dev-dev_io+0.2+base_logic
r=gpu_path/base_path
print(f"gpu path {gpu_path:.2f}  base path {base_path:.2f}  ratio {r:.2f}")
print("base logic pJ/bit", base_logic, " MLA g=128:", 0.22*32+0.1)
print("base-die extra W/stack @2TB/s:", 16e12*base_logic*1e-12)
# measured differential (arXiv 2605.11999): 107 mJ @4K, 242 @16K
kv16=(242-107)*16/12
print("KV-attributable mJ @16K", kv16)
# idea4 needs 242->150: save 92 mJ of kv16
print("idea4 requires KV energy cut to", (kv16-92)/kv16)
# energy saved per KV bit vs effective all-in cost
for name,kvshare in [("ledger C (HBM 50%, KV~60% of bytes)",0.30),("measured differential",kv16/242*3.44/10.7)]:
    save=(gpu_path-base_path)/gpu_path
    print(name, "token energy ratio", 1/(1-kvshare*save))
# idea 2: bandwidth - standard core dies, TSV BW ~= PHY BW
print("idea2 BW margin", 1.0/2.0, " energy margin", (1-1/r)/0.5)
print("idea1 energy/bit margin", r/1.5)
# idea 3 chain: training cost
bom_old=6400; bom_new=6400-1450-300
print("BOM ratio", bom_old/bom_new)
acc_share=33  # accelerator part of 44 hardware pts (est.)
for passthru in [1.0]:
    print("training RATIO", 100/(100-acc_share*(1-bom_new/bom_old)))
print("idea3 margin (dense, non-GEMM/FA 6%)", 15/6)
