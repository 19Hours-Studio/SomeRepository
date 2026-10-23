Both ideas can be repaired and both keep their anchors, but neither reaches "8× with almost no loss". After repair they land at **about 4.1–5.0× vs FP16 (3.2–3.95 bits per value, all metadata counted)**. That is 10–34% more requests served per GPU than uniform 4-bit, the best near-lossless option that needs no calibration. No quality number here was measured on a real model, because Hugging Face is blocked. All error figures come from synthetic simulations plus published results.

=== IDEAS ===
IDEA 1
NAME: Mass-gated dithered value codes
MECHANISM: The anchor stays: keys and values are treated differently. Keys are always deterministic 4-bit (per-channel, 128-token groups, 4.25 bits with scales), because key error is exponentiated in the softmax. Values carry a subtractive dither regenerated from a position hash, so it costs no stored bits. The repair is where the dither matters. It does not reduce error per value (0.50 relative RMS at 2 bits either way), and simple per-block mean-centering beats it on channel-offset data (0.49 vs 1.33). It is, however, the only one of the three schemes that makes errors on repeated content (repeated phrases, code, CoT loops) shrink as more tokens are averaged: at 60 copies, 0.065 vs 0.44–0.52 for the other schemes. That makes a provable gate possible. Each KV head's value precision is chosen from E_h = √Σp² over its quantized tokens: 4-bit above 0.31, 3-bit for 0.133–0.31, 2-bit for 0.046–0.133, and 1-bit dithered at or below 0.046 (about 470 or more tokens effectively attended). At that 1-bit setting the simulated error is 0.025–0.063, under the 0.10 that single-token 4-bit already gives, while deterministic 1-bit stays at 0.38–1.10. Values are Hadamard-rotated and mean-centered, 4 sink tokens plus the last 128 tokens stay FP16, and E_h is accumulated inside the attention kernel (the maximum over the GQA group, 99th percentile over queries).
VALUE: 3.46–3.95 bits (4.1–4.6×), with total attention-output error at most 1.2–1.43× that of uniform 4-bit. That is 55–60 vs 50 concurrent 32k requests on an H100 (+10–20% requests per GPU), with no calibration.

IDEA 2
NAME: Window-mass per-head precision gating
MECHANISM: The anchor stays: each KV head's precision is set per prompt from the prompt's own attention, measured during prefill, and no token is dropped. Four repairs remove the causes of death. First, 1-bit and 2-bit keys are banned; the menu is now K4V4, K4V3 or K3V2. Second, there is an error target instead of a fixed 2.1-bit budget. Third, ranking heads by entropy (which needed Spearman stability across prompts) is replaced by an absolute gate on m_q, the share of attention that falls outside the FP16 sink-plus-recent window. Fourth, every head gets per-block channel-mean centering (0.125 bit). Deterministic error can stay correlated across tokens, but it is still bounded by rel(b)·m_q, so the gate holds without dither. The thresholds are K3V2 if m_q ≤ 0.133, K4V3 if m_q ≤ 0.31, and K4V4 otherwise. A decode-time Σp² watchdog upgrades a head's new 128-token blocks if it turns sharp during chain-of-thought.
VALUE: 3.22–3.80 bits (4.2–5.0×), with error at most 1.2–1.67× that of uniform 4-bit. That is 57–67 vs 50 concurrent requests (+14–34%). It matches the calibrated KVTuner (about 3.5 bits) while needing no calibration, and it beats uniform K3V3 (3.31 bits, about 2.15× error) on error at the same size.

=== NOTES ===
**Idea 1**
- **Anchor kept?** Yes. Keys stay 4-bit, and dither stays as a zero-metadata feature of the value plane. The use of dither changed: it no longer comes with a fixed 2-bit setting. It now certifies an error bound that allows 1–2-bit values in broad heads.
- **Decisive numbers** (from `sim_*.py`):
  - The predicted error rel(b)·√Σp² matched the measured error within 20%.
  - Gate thresholds are 0.31, 0.133 and 0.046.
- **Best baselines**, as requests per GPU (Llama-3.1-8B, 32k context):

  | Scheme | Requests per GPU | Quality |
  |---|---|---|
  | FP8 (cheapest) | 26 | |
  | NVFP4 | 47 | |
  | Uniform K4V4 | 50 | |
  | KVTuner (calibrated) | 61 | |
  | Kitty | 107 | loses 3–4 AIME points |
  | **Idea 1** | **55–60** | |

- **Consistency summary** (full table in `NOTES.md`):
  - Gate accuracy, metadata, the FP16 window and GQA handling all pass.
  - Dither costs about 0.08 ms of arithmetic per sequence per decode step, vs 0.30 ms to read the cache. That is 27% if the kernel does not overlap it.
  - MLA models can only be gated per layer.
- **Hazards:**
  - In multi-turn reuse, a later sharp query can land on a block stored at 1 bit. The worst case is 1.45 relative error on a single token.
  - Blocks already written at low precision cannot be upgraded.
  - The total error envelope assumes uniform 4-bit has headroom.
- **Deciding unknown:** the share of real heads with E_h ≤ 0.046 or ≤ 0.133.
- **Experiment:** dump FP16 attention for Llama-3.1-8B and Qwen3-8B on 50 RULER-32k prompts and 20 AIME traces (about 1 GPU-hour). The idea is falsified if fewer than 30% of heads pass 2-bit or below, or if the 99th-percentile exceedance rate during decode is above 5%. End-to-end confirmation would take AIME24 (30 problems × 16 paired samples), RULER-64k (1,300 samples) and GSM8K (1,319).
- **Closest work:** HyperQuant (dither as a uniform 4-bit codec), Kitty, KIVI.
- **Verdict: NICHE.** It is strongest for long contexts and repetitive content.

**Idea 2**
- **Anchor kept?** Yes: per-prompt, calibration-free, per-head precision, with no eviction. The statistic changed from entropy to m_q, and allocation changed from a fixed budget to a fixed error target.
- **Decisive numbers:**
  - The kill's 14% retrieval-head share comes from forcing a 2.1-bit budget; it no longer applies.
  - Simulated 2-bit value error, deterministic with centering: 0.44–0.49.
  - The m_q bound works without assuming independence between tokens.
- **Baseline:** 57–67 requests per GPU, vs 50 for uniform K4V4 and 61 for calibrated KVTuner.
- **Hazards:**
  - RateQuant reports that activation-based proxies allocate worse than gradient-based ones.
  - Short-prompt chain-of-thought depends on the decode watchdog.
  - MLA models can only be gated per layer.
- **Deciding unknown:** the distribution of m_q across heads, given a 128- or 512-token FP16 window. The same dump as Idea 1 measures it. The idea is falsified if fewer than 40% of heads have m_q ≤ 0.31.
- **Closest work:** RateQuant (calibrated, per-head), DuoAttention and RazorAttention (eviction), RDKV.
- **Verdict: NICHE, close to WORKS.** It is the better of the two for compression. The two ideas also stack: Idea 1's dithered 1-bit tier could be added as a fourth option in Idea 2.

Scripts, `LOG.md` and `NOTES.md` (with the full consistency table) are in `/home/user/SomeRepository/engine/runs/kvzip/repair/c2/`.

Sources: [KVTuner](https://arxiv.org/pdf/2502.04420), [HyperQuant](https://arxiv.org/pdf/2606.23406), [RateQuant](https://www.alphaxiv.org/abs/2605.06675), [RDKV](https://arxiv.org/pdf/2605.08317), [Kitty](https://arxiv.org/pdf/2511.18643), [MixKVQ](https://arxiv.org/pdf/2512.19206), [Quantized Keys Steal Attention](https://www.alphaxiv.org/abs/2605.26266v1), [vLLM quantized KV cache](https://docs.vllm.ai/features/quantization/quantized_kvcache.html)