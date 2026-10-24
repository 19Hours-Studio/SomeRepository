**Target and metrics.** Continuum targets data-center decode of long-context MoE models (128K context, GLM- or Qwen-class GQA, FP4 weights) at a floor of **≥50 tok/s/user**. It is judged on **J/token and $/token per rack at that floor**, compared against GB300 NVL72 (vendor figures: ~576 TB/s HBM, ~130 kW), Ironwood (vendor: 192 GB and 7.4 TB/s per chip) and Groq/Cerebras (230 MB per chip; 44 GB per wafer).

This target is where the cost ledger leaves room for gains:
- HBM traffic is roughly 50% of decode energy (estimate).
- HBM plus packaging is about 62% of chip BOM.

Training is out of scope. Staff cost caps how much any chip can save there. "Best" is claimed only on this metric, and only if the tests below pass.

**Deciding arithmetic** (facts are vendor or paper figures; the rest are my estimates):
- **KV traffic.** GQA KV at 128K is about 4–5 GB per user. At 50 tok/s that is about 230 GB/s per user, or about 0.14 J/token at about 3.9 pJ/bit for HBM.
- **MLA is excluded.** Absorbed MLA is compute-bound at about 480 FLOP/B, so moving it near memory gains nothing.
- **Weights versus KV.** A 355B model at FP4 is 178 GB, read every step at large batch. At 64 users per rack, KV is about 62% of bytes moved and weights about 38%.
- **Realistic total gain.** About **1.5–2.5× J/token**, not 10×. Bandwidth utilization may fall below roofline; one study measured 27% on H100.

**Falsification plan:**
1. Run a cycle-level simulation (e.g., Ramulator2 plus a custom NoC model) on real 128K traces.
2. Build a test chip with one bonded SRAM stack and one HBM4 custom base die.
3. **Kill the design if** it shows <1.3× J/token at matched tok/s/user, or if base-die junction temperature exceeds the DRAM retention limit.

**Software.** Continuum is a PyTorch/vLLM backend. Prefill stays on GPUs (disaggregated serving). Decode attention and expert GEMMs lower to two compiler ops, so models run unmodified. The risk is the Gaudi pattern: a backend that loses to CUDA kernels.

=== IDEAS ===
IDEA 1
NAME: Attention in HBM4 base die
MECHANISM: Each HBM4 stack's custom logic base die runs GQA decode attention (QKᵀ, softmax, AV at FP8) on KV read through the TSVs, skipping the PHY and interposer, and sends only the partial outputs to the main die. The closest attempt, HBM-PIM, stalled on general programmability. Here a single fixed compiler op with a small vector unit avoids that. The deciding quantity is attention intensity × in-stack bandwidth against the base-die thermal budget: about 16 FLOP/B × 2 TB/s ≈ 32 TFLOPS ≈ 16 W per stack, which I estimate is tolerable. MLA, at about 480 FLOP/B, falls outside it.
VALUE: Cuts KV-movement energy about 2× (est. ~1.5 vs ~3.9 pJ/bit) for long-context GQA decode, the largest term in decode energy.

IDEA 2
NAME: Expert-stationary stacked SRAM
MECHANISM: Four-high hybrid-bonded SRAM layers (V-Cache-style; est. ~7 GB per chip) hold all MoE expert weights resident across a 64-chip rack. Each step therefore reads weights at about 0.2 pJ/bit instead of streaming them from HBM, and HBM is left serving only KV. The closest attempts, Groq (230 MB) and Cerebras (44 GB), failed on capacity because they tried to fit KV too. Here 3D stacking gives about 30× Groq's per-chip capacity, and KV stays off-SRAM. The deciding quantity is SRAM $/GB: about $170/GB (est.) × 178 GB ≈ $30k per rack, negligible next to rack cost.
VALUE: Gives about 1.4–1.6× lower J/token and about 1.6× more users per rack at 50 tok/s/user, because all HBM bandwidth goes to KV.

IDEA 3
NAME: HBM-free air-cooled decode rack
MECHANISM: Organic-substrate accelerators (no CoWoS) are each paired with 16 GDDR7 devices, giving about 2 TB/s and 32 GB per chip. That holds about 7 users at 128K and 230 GB/s each, so capacity and bandwidth are balanced. Racks are capped at 40 kW so they fit existing air-cooled halls. The closest attempt, CXL memory pooling, offered capacity without bandwidth. Here every KV byte is local at full rate. The deciding quantity is decode bandwidth per dollar against GB300, which must beat it about 2×; this holds only if GDDR7 supply and its ~5 pJ/bit energy do not erase the saving.
VALUE: Lowers $/token by removing HBM and packaging (about 62% of BOM) and the 120 kW facility requirement, though it loses roughly 1.3× on J/token.