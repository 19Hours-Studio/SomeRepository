# Review of answer.md (Continuum-10)

Every Continuum number in the answer, and the Rubin baseline at >=1,000 tok/s/user, is output from the author's own analytic model.

## Reproduction
`check_v3.py` → `check_v3.txt` imports the author's `model10.py`.
- The base case matches the answer: 60.0 against 36.6 tok/s/W, a ratio of 1.27 / 1.40 / **1.64** / 1.92 / 2.90.

## My perturbations at 128K (ratio against Rubin trimmed by 150 W; tiers ≥200 / ≥500 / ≥1,000 / ≥1,500 / ≥2,000)
| Case | Ratio |
|---|---|
| Base | 1.27 / 1.40 / 1.64 / 1.92 / 2.90 |
| Continuum zero-skip ×1.43 → ×1 (Rubin keeps its vendor 50 PF) | 1.07 / 1.18 / **1.34** / 1.58 / 2.37 |
| Draft positions pick their own CSA top-1024 (union u = 0.5, both systems) | 1.27 / 1.40 / 1.69 / 2.09 / 3.21 (hurts Rubin more) |
| No zero-skip + same node + u = 0.5 | 0.97 / 1.07 / **1.23** / 1.54 / 2.36 |

## Main points
- About 1.19× of the 1.64× comes from the assumed N2 vs N3P process node. It is not from the architecture. On the same node the ratio is 1.48 (the author's own run).
- The ×1.43 zero-skip on Continuum is an assumption. My estimate for NVFP4 weights is that only about 6% of block-scaled weights round to zero, which would mean roughly ×1.06. Without the ×1.43, the ratio is 1.34.
- The ≥1,000 tok/s/user tier on V4-Pro has never been measured on any hardware. The best InferenceX GB300 points peak at roughly 190 tok/s/user, about 500 tok/s/GPU. The model has Rubin at 57k tok/s/GPU. The headline therefore depends entirely on ρ_C = ρ_G at a tier where neither has been measured.
- Continuum is a 2028 part. Against same-date peers it does not clearly win: about 1.24× a 4-die Ultra (worst pair 0.88), and 1.02–1.13× a Feynman proxy.
- At the bulk tier (≥200) it shows no meaningful gain: 0.95–1.27×.
- The answer is candid about most of this. Its own §0.3 and §7 already state these limits.
