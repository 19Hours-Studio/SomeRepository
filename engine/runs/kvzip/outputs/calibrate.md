=== CALIBRATION ===

P | 1 | 38% | No fatal defect, and its bit, MSE and op/B numbers reproduce. But it is essentially Block-GTQ K3V2 plus published E8 (NexusQuant, Nedelkoski et al.), its claimed edge cannot be measured, and the per-band scale problem is unpriced.

P | 2 | 12% | It needs no calibration and its bit costs reproduce. But the linear error bound fails through exp() on sharp heads, precision fixed at prefill cannot be undone, and at 3.22–3.80 b it ties TurboQuant at 3.5 b.

P | 3 | 8% | FATAL, unanswered: absorbed-MLA decode is already compute-bound at FP8, so the claimed 1.2× throughput is about 1.0×. On its target stores, the basis overhead eats the gain, which is only simulated.

P | 4 | 3% | FATAL, unanswered: relative to a flat head's useful output, dithered 1-bit is 5–15× worse than 4-bit, so the gate is wrong. The 1-bit dequant is also compute-bound.

P | none | 39% | Every candidate's ratio is about 1.0 against TurboQuant or Block-GTQ, all are partly or fully known, and none reports measured LongBench, RULER or AIME numbers. The best real answer may simply be Block-GTQ K3V2 or TurboQuant at 3.5 b as published.

Candidate 1 leads the candidates but sits essentially tied with "none". Idea 1 is the least overstated candidate, not a demonstrated winner.

WEAKEST LINK: One FP8 scale per token and head is shared by 16 bands whose energies differ by up to about 30×. Proxy MSE rises from 0.118 to 0.76–3.19 at mismatched scales. Per-band scales would fix this but add about 0.25–1.0 b/value, which would push keys toward 3.5–4 b. Most of the edge over TurboQuant and KVTuner would then be gone.

FLIP TEST: On real post-RoPE keys from Llama-3.1-8B and Qwen2.5-7B, measure per-band relative MSE with the single scale and with per-band scales, then run RULER-32k and LongBench against Block-GTQ K3V2 and TurboQuant 3.5 b. | Idea 1 falls below "none" if either holds:
- the single-scale MSE on low-energy bands is above about 0.2, and fixing it pushes the total above about 3.3 b/value;
- it trails Block-GTQ by more than 1 point on RULER or LongBench.

UNKNOWN: Even if idea 1 is right, nobody knows whether any ~6× format keeps a ≤1% relative drop on long reasoning-model chains of thought (AIME, MATH at 32k+ generated tokens). The −2.5 AIME24 drop for Block-GTQ suggests the ceiling is nearer 5× than 6×. It is also still unclear whether offline calibration is allowed.