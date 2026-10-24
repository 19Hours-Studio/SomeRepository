# Continuum: three candidate architectures

**Scope.** All three target the data center. Vendor figures are marked (v), my estimates are marked (est.), and nothing here has been simulated. Archetype A, owned NVL72 inference, has no room for a 3x gain: the vendor's margin is the largest term and no architecture changes it. So each variant aims at a term with room under its ceiling. "Best" here means the best result on the metric chosen, not the best on every metric.

**Reference points (v):**
- Rubin: about 288 GB HBM4, about 20 TB/s.
- Ironwood: 192 GB HBM3E, 7.4 TB/s, 4.6 PF FP8.
- WSE-3: 44 GB SRAM.
- Groq: 230 MB per chip.

## A1: Stacked-SRAM decode (metric: mJ/token, tok/s/user)

**Design (est.):**
- One logic die (N3, 1 FP8 PF).
- Four hybrid-bonded SRAM dies at about 3 MB/mm², giving about 7 GB at 0.15 pJ/bit. HBM is about 3–4 pJ/bit.
- Two HBM stacks hold the KV cache.

**Sizing.** A 1T-parameter MoE in FP4 is about 500 GB, so one replica needs about 72 packages. Groq needs 576 chips for a 70B model.

**Costs and limits.**
- SRAM costs about $190/GB versus about $20/GB for HBM (est.), roughly 10x more.
- This only pays where weight traffic dominates. At 32K context the KV cache dominates, so the gain falls back toward HBM-bound.

**Expected result.** Energy per token improves about 1.5–1.8x, against a ceiling of 1.82x.

**Loses to:** Rubin on $/GB and on long context.

## A2: CoWoS-free training (metric: $ per trained token at equal loss)

**Design (est.):**
- Organic-substrate chiplets with 512 MB SRAM and 2 FP8 PF.
- 16 LPDDR6 packages: about 1 TB/s and 512 GB per package, at about $3k.

**Roofline check.** 2 PF ÷ 1 TB/s = 2,000 FLOP/B. GEMMs reach this with 512 MB tiles. Attention backward passes, norms and MoE all-to-all do not. B200 sits near 280 FLOP/B.

**Software.** A torch.compile → Triton backend, so existing PyTorch models run unmodified.

**Expected result.** About 1.4–1.7x lower hardware cost, mainly from removing CoWoS and HBM, which are scarce. Staff cost (33%) is unaffected.

**Loses to:** GPUs on bandwidth-bound kernels.

## A3: Attention in the HBM4 base die (metric: long-context mJ/token)

**Design.**
- The HBM4 base die is already a logic process (established).
- A fixed GQA attention engine sits in it, so KV data never crosses the interposer.

**Power check (est.).** About 15 W per stack at 0.3 pJ/FLOP gives about 50 TFLOP/s. With GQA group 8 (16 FLOP/B), that covers about 3 TB/s of KV per stack.

**Programmability.** The engine runs one fixed operation, which avoids the programmability problem that stalled PIM.

**Expected result.** KV movement energy falls about 3–4x, giving about 1.4x per token.

## Falsification and risks

**Tests that could prove these designs wrong.**
- Run cycle-level simulation (e.g. Timeloop/ASTRA-sim) on DeepSeek-class traces. Validate it first against measured H100 numbers: 107 and 242 mJ/token.
- If A2 sustains less than 60% of its GEMM-bound throughput over an MoE step, it fails.

**Risks:**
- Hybrid-bond yield.
- Base-die thermals.
- NVFP4 training beyond 12B is unproven.
- LPDDR6 supply.

=== IDEAS ===
IDEA 1
NAME: Stacked-SRAM weight-resident decode
MECHANISM: Four hybrid-bonded SRAM dies (about 7 GB at 0.15 pJ/bit) hold FP4 MoE weights, sharded across about 72 packages, while HBM holds only the KV cache. Groq stalled at 230 MB per chip; vertical stacking gives about 30x more capacity per package. The deciding quantity is the weight share of decode bytes at the target context length.
VALUE: Up to about 1.8x lower decode energy per token at short to medium context.

IDEA 2
NAME: CoWoS-free LPDDR training chiplets
MECHANISM: Organic-substrate chiplets pair 512 MB SRAM tiles with LPDDR6 (1 TB/s, 512 GB), and need GEMM tiling at about 2,000 FLOP/B. They avoid the HBM/CoWoS shortage, and an unmodified PyTorch Triton backend avoids the Gaudi software failure. The deciding quantity is the fraction of step time below 2,000 FLOP/B.
VALUE: About 1.5x cheaper training hardware without scarce HBM or CoWoS.

IDEA 3
NAME: Base-die GQA attention engine
MECHANISM: A fixed-function attention unit in the HBM4 logic base die reads KV over TSVs, stays within a 15 W power budget, and returns only attention outputs. Because it runs a single fixed operation, it sidesteps the programmability failure of PIM. The deciding quantity is sustained attention bandwidth per stack inside the thermal limit.
VALUE: About 1.4x lower long-context decode energy per token.