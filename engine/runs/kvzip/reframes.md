**ASSUMPTIONS:**
- One architecture can be "best" across all workloads. (contradicted: A is prefill-bound and KV is about 4% of GPU time; in B, KV reads are about 50%)
- Smaller KV makes serving broadly cheaper. (contradicted: in A it mainly buys capacity; in B a 10× cut gives only 1.82×, because weight reads are 36%)
- FP16 is the right baseline. (contradicted: the bar is NVFP4, about 4× with <1% loss claimed, plus FP8 and the prefix-cache/offload stack)
- Nominal bit-width equals the real ratio. (contradicted: "2-bit" KIVI lands at 2.6× once metadata and the FP16 window are counted)
- Plain quantization can go far below 4 bits with almost no loss. (contradicted: below about 3 bits, AIME drops 13 points and GSM8K falls from 0.90 to 0.72)
- Perplexity and LongBench reveal "almost no loss." (contradicted: they hide long-CoT collapse)
- Token eviction is a safe compression axis. (contradicted: it fails query-agnostic reuse, multi-turn and long outputs beyond 3–4×)
- Heads and layers carry large redundancy. (contradicted: gains shrink on GQA, to 1.67×, and on MLA)
- Lossless entropy coding adds a lot. (contradicted: about 25–30% on BF16, and the slack shrinks at low bit-width)
- Storage format alone sets quality. (contradicted: the FP8 needle-in-a-haystack collapse came from accumulation precision)
- Compression becomes speed. (contradicted: an independent TurboQuant test gave +3% decode)
- One design transfers across GQA and MLA. (contradicted in part: MLA latents are low-rank and RoPE is decoupled)
- "No retraining" excludes calibration. (unclear)

**REFRAME 1:** Which sub-3-bit errors actually break long chain-of-thought reasoning, and can a calibration-free signal computed online flag them before they compound?
- CHANGES: It attacks the hardest sub-question first: where the loss comes from (which tokens, heads, channels, steps), before any format is chosen.
- IMPORTANCE: high
- POSSIBILITY: high
- WHY: Every attempt below 3 bits fails in the same place, long-CoT. A cheap diagnostic on one 8B R1-distill model with AIME/MATH decides which axis can go further. It also answers the calibration question.

**REFRAME 2:** What all-in format (≤2 bits per value including scales, indices, codebooks and residual window, about 2× better than NVFP4) keeps a ≤1% relative drop on AIME/MATH long-CoT and RULER-128k for GQA reasoning models? It must also have a fused decode kernel that turns the bytes saved into measured throughput.
- CHANGES: It sets a number for the target, the baseline (NVFP4/FP8, not FP16), the accounting, the scope (decode-heavy archetype B) and the success metric (tokens/s and batch size).
- IMPORTANCE: high
- POSSIBILITY: medium
- WHY: It makes "much stronger, almost no loss" testable where the payoff actually exists.

**REFRAME 3:** Can the cache be split into a small low-bit copy that stays on the GPU and residuals stored off-GPU or entropy-coded, where attention fetches the residuals only when needed? Nothing is dropped, and quality can be restored to near FP8 on demand.
- CHANGES: The means move from a single lossy format to progressive, recoverable storage.
- IMPORTANCE: high
- POSSIBILITY: medium
- WHY: It avoids the failure of eviction on reuse and of plain quantization on CoT. It also fits the existing LMCache/HiCache tiers.

**REFRAME 4:** For each archetype, what HBM bytes per request, cache hit rate and decode-step bandwidth must a KV format achieve to move cost or capacity by a stated factor? Which archetype justifies more than 4×?
- CHANGES: The unit becomes cost or capacity per request instead of bits per value.
- IMPORTANCE: medium
- POSSIBILITY: high
- WHY: The ceilings show the gain is concentrated in B. This reframe prevents optimizing a term that is worth 3%.

**REFRAME 5:** Should the storage format and the attention numeric path (accumulation precision, dequantize-in-register, sink and outlier handling) be designed together, so that compression does not create accuracy cliffs at long context?
- CHANGES: The scope widens from storage to the kernel.
- IMPORTANCE: medium
- POSSIBILITY: medium
- WHY: The FP8 needle-in-a-haystack cliff and the +3% TurboQuant speedup both came from the kernel, not the format.

**REFRAME 6:** What compression applies on top of MLA latents (DeepSeek-V3-class) that are already low-rank, without breaking the decoupled RoPE part?
- CHANGES: The target model class changes to MLA.
- IMPORTANCE: medium
- POSSIBILITY: low
- WHY: The ceiling reads NO ROOM, and the material has no MLA-specific quantization data.

**KEEP:** 1, 2
