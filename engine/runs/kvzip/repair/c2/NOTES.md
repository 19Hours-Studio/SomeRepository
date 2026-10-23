# NOTES — repair c2 (scripts: sim_dither.py, sim_dither2.py, sim_round3.py, sim_1bit.py, accounting.py, final_calc.py)

## Core finding used by both ideas
The attention output error from independent per-token errors is rel_rms(b)·E_h·|v|, with E_h = sqrt(Σ_{quantized i} p_i²),
so it scales with E_h = 1/√N_eff. The measured value matched the prediction within ~20% (sim_round3 b).
This only holds if the errors are uncorrelated across tokens:
- RTN errors on offset-type data stay coherent. Fix: centering, or dither.
- RTN errors on duplicated content stay coherent. Only dither fixes this.

When the errors are coherent, the error is bounded by rel(b)·m_q, where m_q is the attention mass on the quantized tokens.
Measured relative RMS (Hadamard-rotated, min-max, g128): 1b 1.45 / 2b 0.50 / 3b 0.215 / 4b 0.10. The 4-bit figure agrees with FACT 3 (0.097).

## Consistency table (every window the designs rely on)
| tolerance / window | value used | checked against | status |
|---|---|---|---|
| gate bound accuracy | pred vs meas within 20% | safety factor 1.5 | OK |
| Idea1 V1 gate | E_h ≤ 0.046 (N_eff_q ≥ 470) | sim: ctr+dith1 0.025–0.063 at N_eff ≥ 512, target 0.10 | OK in sim; real share of heads unknown |
| aggregate error across heads | quadrature sum | ≤ 1.20–1.43× (I1), 1.20–1.67× (I2) of uniform K4V4; uniform K3V3 ≈ 2.15× | conditional: needs K4V4 headroom |
| decode drift | gate is measured on prefill queries | head turns sharp in decode, old blocks cannot be upgraded | HAZARD: run an in-kernel Σp² watchdog, upgrade new blocks, flag |
| short prompt + 32k CoT | prompt stays FP16 (window) | CoT blocks gated from running decode statistics, per 128-token block | OK by design; still unmeasured |
| FP16 sink+recent overhead | 132 tok: 0.064 b @32k, 0.016 b @128k; win 512: 0.25 b @32k | included in all bit counts | OK |
| metadata | scale+zero FP16/128 = 0.25 b; channel mean 0.125 b | included | OK |
| dither ALU | 0.08 ms vs 0.30 ms KV-read per seq-step (27% if not overlapped) | memory-bound kernel; H100 INT32 ~33.5 TOPS | OK if overlapped; needs a kernel to verify |
| prefill Σp² | 2 FLOP per score vs 512 tensor FLOP | ≤ +10% attention time if every query; ~0 if only the last 1k queries | OK |
| GQA | E_h, m_q = max over the 4 query heads in a group, p99 over queries | stops a sharp query head from hiding inside a broad group | OK |
| MLA (DeepSeek) | a single latent shared by all heads | per-head gating is impossible; falls back to per-layer gating | LIMIT |
| multi-turn reuse | a later query can be sharp on a block tagged V1/V2 | I1: error bound is √Σp² of that query; worst single token V1 → 1.45 rel error | HAZARD (I1 > I2) |

## Baselines, per request served (Llama-3.1-8B, H100-80GB, 32k ctx, bandwidth-bound decode; accounting.py)
| scheme | bits | concurrent seqs | tok/s |
|---|---|---|---|
| FP8 (cheapest) | 8 | 26 | 1211 |
| NVFP4 | 4.5 | 47 | 2162 |
| K4V4 g128 | 4.31 | 50 | 2265 |
| KVTuner (calibrated) | ~3.5 | 61 | 2785 |
| Kitty | ~2 | 107 | 4877 (but −3–4 AIME) |
| Idea1 mid | 3.71 | 58 | 2630 |
| Idea2 mid | 3.46 | 62 | 2817 |

## Novelty check
- Dither on the KV cache already exists: HyperQuant (arXiv 2606.23406) uses a per-call dither with a rotation, at about 3.79× near-lossless at 4 bps. The new part here is using dither as the certificate that allows mass-gated sub-2-bit (1-bit) values in broad heads, while keys stay deterministic 4-bit. Dither as a uniform 4-bit codec is not new.
- Per-head bit allocation via reverse water-filling also exists: RateQuant (arXiv 2605.06675) is calibrated and gradient-based. RDKV (2605.08317) allocates per token. The new part here is an online, per-prompt, calibration-free gate on m_q that keeps every token. Caveat: RateQuant reports that activation-based proxies are worse than gradient-based ones.
