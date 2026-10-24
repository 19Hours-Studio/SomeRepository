**Scope and metrics.** Continuum targets data-center inference of large MoE models (DeepSeek, Kimi or GLM class) at 100–500 tok/s/user, with training as a secondary target. The question is reformulated as delivered throughput per scarce input. "Best" is scored on four numbers:

- tokens/J
- tokens/s per facility kW
- tokens per HBM stack
- cost per token at a fixed tok/s/user

**Ceilings (from the context ledger).**
- Removing HBM streaming energy entirely caps the decode tokens/J gain at about 1.8–2×.
- Facility cost is about 20% of inference TCO, so facility savings cap at about 1.2×.
- No chip can remove vendor margin or staff cost.
- "Several times cheaper" is possible only in chip BOM, through HBM and CoWoS (D, which has room).

**Established facts (sourced in context):**
- Groq used 576 chips of 230 MB each for a 70B model.
- Cerebras has 44 GB on-wafer and roughly 150 GB/s off-wafer.
- NVL72 racks draw 120–130 kW.
- HBM is about 45% of the B200 BOM.

**My estimates, not facts:**
- About 1.2 GB per 600 mm² N5 SRAM die, extrapolated from AMD V-Cache at roughly 1.5 MB/mm² on N7.
- Stacked SRAM costs about $150–250/GB, versus about $20/GB for HBM3E.

**Where Continuum wins and loses.**
- **Training:** loses to Rubin and Ironwood.
- **Single-stream speed:** likely loses to Cerebras.
- **Chip count:** beats Groq by about 30–70× fewer chips per model.
- **Efficiency:** targets 1.5–1.8× tokens/J and roughly 3× tok/s per kW over GB300, with no HBM at all.

**Software.** Continuum ships as a PyTorch `torch.compile` and Triton backend with MX/NVFP4 checkpoints. vLLM and SGLang plug in as the serving layer. Models run unmodified, with one attention op swapped.

**Kill tests.**
- Run a cycle-accurate simulation on DeepSeek-V3 decode traces. Abandon the design if tokens/J falls below 1.4× GB300 at equal tok/s/user.
- Abandon it if stacked-SRAM yield pushes cost above $250/GB.
- Abandon it if the 8-hop pipeline adds more than 2 ms per token.

=== IDEAS ===
IDEA 1
NAME: Weight-stationary stacked-SRAM tiles
MECHANISM: Each tile is an 800 mm² N3 logic die (~2 PFLOPS FP4, est.) with four hybrid-bonded N5 SRAM dies on top (~4.8 GB at ~40 TB/s, est.). The tile also carries 128 GB of LPDDR6 for KV cache, on an organic substrate with no HBM or CoWoS. About 80 tiles (~32 kW, est.) hold a 671B FP4 model, so expert weights never move; tokens move between tiles instead, and KV bandwidth caps aggregate throughput at roughly 10⁵ tok/s at 8K context. The closest earlier attempt is the Groq LPU, which needed 576 chips because it had only 230 MB of SRAM each; 3D stacking gives about 20× the capacity per chip. The deciding quantity is the cost per GB of yielded stacked SRAM, where SoIC capacity is the supply risk.
VALUE: It serves frontier MoE decode with zero HBM stacks, at an estimated 1.5–1.8× the tokens/J of GB300 and about 3× the tokens per facility kW.

IDEA 2
NAME: Attention-only near-memory KV engine
MECHANISM: A logic base die under the LPDDR or HBM stacks runs only the fused QK-softmax-V reduction for GQA decode. It returns a vector per head instead of streaming the whole KV cache across the PHY, and appears to software as a single FlashAttention-compatible kernel. The closest earlier attempt is HBM-PIM, which failed on general programmability; here, one fixed op hides all address and coherence issues. The deciding quantity is DRAM-core energy as a share of total access energy (assumed ≤40%), which sets the gain. It gives no gain on compute-bound absorbed-MLA decode.
VALUE: It roughly halves energy per token for long-context GQA decode, where energy grows 2.26× from 4K to 16K context.

IDEA 3
NAME: Optical scale-up, low-density racks
MECHANISM: HBM4 training chips use co-packaged optics (~5 pJ/bit, est.; about 150 W per chip at 3.6 TB/s) to form 512-chip scale-up domains spread across 40 kW racks instead of 120 kW copper racks. NVFP4 compute is paired with BF16 fallback layers. The closest earlier attempts are Google's TPU optical circuit switching (captive, and still CoWoS-bound) and NVL72 copper (which limits deployment by facility density). The deciding quantity is CPO cost and failure rate per Tb/s relative to copper.
VALUE: It runs frontier pretraining in existing air-assisted facilities, at about 1.1–1.2× lower cost, honestly capped by the facility share of cost.