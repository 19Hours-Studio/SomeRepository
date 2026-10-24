"""Roofline + cost model for the two Continuum repair candidates.
All numbers tagged SRC (sourced, see NOTES.md) or EST (my assumption)."""
import math

# ---------------- models ----------------
# DeepSeek-V3/V3.2 (SRC: DeepSeek-V3 tech report / V3.2 config)
L = 61; MOE_L = 58; H = 7168; EXP_FF = 2048
N_EXP = 256; TOPK = 8; HEADS = 128
p_exp = 3 * H * EXP_FF                      # params per routed expert
P_EXPERTS = N_EXP * MOE_L * p_exp           # routed-expert params
P_TOTAL = 671e9; P_ACT = 37e9
B_FP4 = 4.5 / 8                             # NVFP4 incl. block scales (bytes/param)
KV_MLA = 656                                # B/token/layer, V3.2 FP8 latent cache (SRC)
KV_IDX = 132                                # B/token/layer, lightning-indexer key FP8+scale (SRC)
TOPK_TOK = 2048                             # DSA selected tokens (SRC)
F_ATT = HEADS * (576 + 512) * 2             # FLOP per attended token per layer (absorbed MLA)
F_IDX = 64 * 128 * 2                        # indexer FLOP per context token per layer

def per_token(ctx, sparse):
    """bytes of KV read and attention FLOP per generated token, KV footprint per user"""
    foot = ctx * L * (KV_MLA + (KV_IDX if sparse else 0))
    if sparse:
        att = min(ctx, TOPK_TOK)
        rd = L * (att * KV_MLA + ctx * KV_IDX)
        fl = L * (att * F_ATT + ctx * F_IDX)
    else:
        rd = L * ctx * KV_MLA
        fl = L * ctx * F_ATT
    return rd, fl + 2 * P_ACT, foot

W_BYTES = P_TOTAL * B_FP4
print(f"routed-expert params {P_EXPERTS/1e9:.0f}B, weights FP4 {W_BYTES/1e9:.0f} GB, expert {p_exp*B_FP4/1e6:.1f} MB")
for ctx, sp in [(32768, False), (32768, True), (131072, False), (131072, True)]:
    rd, fl, ft = per_token(ctx, sp)
    print(f"ctx {ctx//1024}K sparse={sp}: KV read/token {rd/1e9:.2f} GB, FLOP/token {fl/1e9:.0f} G, footprint {ft/1e9:.2f} GB, "
          f"drain time needed @100tok/s = {ft/(rd*100)*1e3:.0f} ms")

# ---------------- memory economics ----------------
HBM4_STACK_GB, HBM4_STACK_BW = 36, 2.75e12          # SRC FACT 15/18
for yr, price in [("2026", 575), ("2027", 1300)]:   # SRC FACT 18
    print(f"HBM4 {yr}: ${price/HBM4_STACK_GB:.1f}/GB, ${price/(HBM4_STACK_BW/1e12):.0f} per TB/s, drain {HBM4_STACK_GB*1e9/HBM4_STACK_BW*1e3:.0f} ms")
LP_PKG_BW = 128e9          # EST: LPDDR6 x96 package ~10.7 Gb/s (JEDEC LPDDR6 launch speed)
LP_PKG_GB = 8              # EST: smallest practical package capacity at volume
for price in (10, 21):     # SRC FACT 1/20
    n = 1e12 / LP_PKG_BW
    print(f"LPDDR @${price}/GB: {n:.0f} pkgs per TB/s, {n*LP_PKG_GB:.0f} GB, ${n*LP_PKG_GB*price:.0f} per TB/s, drain {LP_PKG_GB*1e9/LP_PKG_BW*1e3:.0f} ms")
