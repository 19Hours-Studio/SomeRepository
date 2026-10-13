# Research log (one line per experiment). Screening = 1000 steps seed 0 unless noted. Base = r0_blindB_1 architecture (tpl.py knobs).
| file | steps | seed | bpc | tested | conclusion |
|---|---|---|---|---|---|
| e01_base.py | 1000 | 0 | 2.0191 | reference: r0_blindB_1 copy-head transformer, unchanged | 1000-step reference |
| e02_lr2.py | 1000 | 0 | 1.9895 | effective lr x2 via reparam W=2*W' (all params) | -0.030: harness lr is too low for this budget |
| e03_lr4.py | 1000 | 0 | 2.0018 | effective lr x4 | better than base, worse than x2: optimum near 2-3 |
| e04_rep2.py | 1000 | 0 | 2.0104 | apply both blocks twice (4-layer depth, same params, 2x time) | -0.009 for 2x compute: depth is not the limit |
| e05_canon.py | 1000 | 0 | - | canon convs (first try 150720 params, over budget) | rerun with HID 156 |
| e05_canon.py | 1000 | 0 | 1.9872 | "canon" causal depthwise conv k=4 residual mixers (before attn, on qkv, before MLP), HID 156 | -0.032: local token mixing inside blocks helps |
| e06_canon_lr2.py | 1000 | 0 | 1.9213 | canon + lr x2 | -0.098: the two effects stack super-additively |
| e07_lr3.py | 1000 | 0 | 1.9841 | lr x3 | ~ x2 (1.990); optimum lr x2-3 |
| e08_zo_lr2.py | 1000 | 0 | 1.9649 | zero-init attn-out and fc2 + lr x2 | -0.025 vs lr2: zero-init residual branches helps |
| e09_ngram_lr2.py | 1000 | 0 | 1.9973 | trainable hashed bigram+trigram input tables (8 dims), HID 96, lr x2 | +0.008 vs lr2: sparse n-gram tables do not pay for the MLP they displace |
| e10_c_zo_lr2.py | 1000 | 0 | 1.8839 | canon + zero-init residual outs + lr x2 | -0.135 vs base: all three stack |
| e11_c_zo_lr3.py | 1000 | 0 | 1.8724 | same with lr x3 | slightly better than x2 at 1000 steps |
| e12_c8_zo_lr2.py | 1000 | 0 | 1.8923 | canon kernel 8 instead of 4 (HID 148) | +0.008 vs k=4: wider local conv no better |
| e13_c_zo_lr2_nocopy.py | 1000 | 0 | 1.9894 | e10 with all heads RoPE (no shifted-key copy heads) | +0.105: copy heads remain essential; canon complements, does not replace them |
| e14_cabcd_zo_lr2.py | 1000 | 0 | 1.9021 | add canon conv on MLP hidden too (HID 152) | +0.018 vs e10: no gain from conv inside MLP |
| e15_cb_zo_lr2.py | 1000 | 0 | 1.9330 | canon only on qkv (no residual-stream convs) | +0.049 vs e10: residual-stream convs (pre-attn, pre-MLP) carry most of the canon gain |
| e16_c_zo_lr2_copy3.py | 1000 | 0 | 1.9327 | 3 of 4 heads shifted-key copy heads | +0.049 vs e10: need positional heads too; keep 2/2 |
| e17_c_zo_lr2_nh6.py | 1000 | 0 | 1.9105 | 6 heads of dim 16 | +0.027 vs e10: keep 4 heads of dim 24 |
| e10_c_zo_lr2.py | 3000 | 0 | 1.7209 | confirm canon+zero-init+lr x2 at full budget | beats plateau 1.781 by 0.060 |
| e11_c_zo_lr3.py | 3000 | 0 | 1.7110 | confirm canon+zero-init+lr x3 at full budget | 1.711, best so far (-0.070) |
| e18_c_zo_lr4.py | 1000 | 0 | 1.9081 | canon+zero-init with lr x4 | worse than x3 (1.872) and x2 (1.884): lr optimum ~x3 |
| e05_canon.py | 3000 | 0 | 1.7563 | ablation: canon convs only (no lr change, no zero-init) | -0.024 vs 1.780 |
| e07_lr3.py | 3000 | 0 | 1.7429 | ablation: lr x3 only on original r0_blindB_1 | -0.037 vs 1.780: the old plateau was partly under-optimisation |
| e11_c_zo_lr3.py | 3000 | 1 | 1.7022 | seed 1 of best | mean of 2 seeds 1.7066 |
| e20_c_zo_lr3_d80.py | 1000 | 0 | 1.8641 | d=80, MLP 264 (more MLP, less attention) | -0.008 vs e11 at 1k: within noise, maybe slightly better |
| e21_c_zo_lr3_3L.py | 1000 | 0 | 1.8829 | 3 layers at d=80 (MLP 116), 1.2x time | +0.011 vs e11: depth does not help |
| e23_c_zo_lr3_emb6.py | 1000 | 0 | 1.8983 | embedding lr x6, rest x3 | worse than uniform x3 |
| e24_c_zo_lr3_emb1.py | 1000 | 0 | 1.9160 | embedding lr x1, rest x3 | worse: embedding needs the raised lr as much as matrices |
| e11_c_zo_lr3.py | 1000 | 0/1 | 1.8724/1.8943 | noise check (seed 0 rerun identical; seed 1) | runs are deterministic; seed noise at 1000 steps ~0.02, so 1k differences <0.02 are not reliable |
| e25_c_zo_lr3_qkn.py | 1000 | 0 | 1.8995 | cosine (QK-norm) attention, learned temperature init 10 | no gain at 128 (within noise); 2x-context bpc much better (1.79) |
| e20_c_zo_lr3_d80.py | 3000 | 0 | 1.6884 | d=80, MLP 264, canon+zero-init+lr x3 | -0.023 vs e11: trading attention width for MLP width helps; new best |
| e26_c_zo_lr3_d64.py | 3000 | 0 | 1.6906 | d=64, MLP 416 | same as d=80 (1.6884): MLP-width gain saturates; 2x context 1.678 |
| e28_d80_only.py | 3000 | 0 | 1.7739 | ablation: d=80/MLP 264 on original r0_blindB_1 (no canon, no zero-init, lr x1) | -0.006 only: wider MLP pays only once learning is fast |
| e20_c_zo_lr3_d80.py | 3000 | 1 | 1.6941 | seed 1 of d80 best | mean 2 seeds 1.6913 |
| e27_c_zo_lr3_d72.py | 3000 | 0 | 1.6985 | d=72, MLP 332 | same plateau ~1.69 for d in 64..80 |
| e29_c_zo_lr3_d96qk8.py | 3000 | 0 | 1.7189 | query/key dim 8 per head (d=96, MLP 220) | +0.03 vs d80: copy matching needs wide keys; (2x-context 1.603, best extrapolation) |
| e30_c_zo_lr3_d80qk8.py | 3000 | 0 | 1.7194 | query/key dim 8 per head (d=80, MLP 318) | same: narrow QK hurts at 128 |
| e31_d80_c_zo_lr1.py | 3000 | 0 | 1.7273 | ablation of e20: lr x1 | +0.039: raised step size is half of the gain |
| e32_d80_zo_lr3_nocanon.py | 3000 | 0 | 1.7232 | ablation of e20: no canon convs (MLP 276) | +0.035: canon convs are the other half; each alone ~1.72-1.74 |
| e33_d80_c_lr3_nozo.py | 3000 | 0 | 1.6809 | ablation of e20: no zero-init of residual outputs | -0.008 (noise level): zero-init is unnecessary; drop it |
| e34_d80_c_zo_lr3_glu.py | 3000 | 0 | 1.6871 | GEGLU MLP (hidden 176) instead of GELU 264 | same as e20 (1.6884): MLP form irrelevant |
| e35_d80_c_zo_lr3_nh2.py | 3000 | 0 | 1.6915 | 2 heads of dim 40 (1 positional + 1 copy) | same at 128; 2x-context 1.589 |
| e36_d80_c_zo_lr3_untie.py | 3000 | 0 | 1.6812 | untied output head (MLP 240) | -0.007, noise level |
| e33_d80_c_lr3_nozo.py | 3000 | 1 | 1.6817 | seed 1 of e33 | mean 2 seeds 1.6813 (vs 1.781 plateau) |
| e37_d80_c_lr4.py | 3000 | 0 | 1.6895 | e33 with lr x4 | +0.009: x3 is about the optimum at full length too |
| e38_d80_c_lr3_untie.py | 3000 | 0/1 | 1.6945/1.6972 | e33 + untied output head (MLP 240) | worse than tied (e33): keep tied |
| best.py | 3000 | 0/1 | 1.6809/1.6817 | final = e33 (canon convs + lr x3 + d80/MLP264 on copy-head transformer) | new plateau ~1.68-1.69: width, heads, GLU, untie, zero-init, lr x4 all within +-0.01 |
