=== CALIBRATION ===

P | 1 | 20% | It is the only candidate with an edge that survived review (MLA, write-capped last tier, ratio 1.05), but it was never compared with Marconi, GDSF or second-hit admission. Its dense-8B SSD-wear figure is about 9× too low, which reverses its "≤3% of node cost" conclusion.

P | 2 | 17% | Exact-prefix reuse in the native dtype is the strongest plug-and-play lossless design, but it is already HiCache, LMCache or Mooncake (ratio 0.99). Its 95% hit at 0.15–0.30 s is not derived and conflicts with the NVMe bandwidth available.

P | 3 | 15% | Calibrated FP8 KV is the realistic memory win, but this probe adds about nothing over fixed-kernel FP8 on every layer (0.97×). No model with a true few-layer failure has been verified, and 100 prompts cannot detect a 3–5 point loss.

P | 4 | 3% | The FATAL defect is unanswered: dropping about 60% of KV is lossy, which breaks "same outputs". It is also beaten by ArkVale and ShadowKV.

P | none | 45% | The best answer is probably a known stack that no candidate improves on: stock exact-prefix caching with tiered offload and selective write-back, plus calibrated FP8 KV. Each candidate is either already known or loses to that stack.

WEAKEST LINK: Idea 1's 43–207% (HBM) and 37–95% (SSD) gains are measured only against LRU and random admission. Cost-aware eviction (Marconi, GDSF) and second-hit admission probably capture most of that gain.

FLIP TEST: Replay the Mooncake traces for DeepSeek-V3 at a 0.5–1M-token HBM cache and a 10–35% SSD write budget, against two baselines: Marconi-style FLOP/byte eviction and HiCache `write_through_selective`. | If Idea 1 beats both by less than about 10% in saved prefill FLOPs per byte, it falls below "none" and Idea 2 or the plain stock stack leads. If it keeps more than 30% over both, it rises to about 35%.

UNKNOWN: Even if Idea 1 is right, it is unclear whether capacity-short, write-capped MLA last tiers are common enough in real deployments to matter. It is also untested whether the whole-chain score carries over to hybrid, SSM or sliding-window architectures, where prefix state is not per-token KV.