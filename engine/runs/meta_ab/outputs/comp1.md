**Continuum: a long-context, decode-first inference accelerator**

*No CONTEXT block was attached, so the figures below are commonly reported 2025–26 numbers and should be read as approximate.*

**Target and metric.** Continuum is for data-center inference of frontier MoE models with contexts of 128K to over 1M tokens. The metric is **joules and dollars per million output tokens, at ≥150 tok/s per user, with 1M-token context**.

**Why existing designs plateau.** At long context, decode cost is dominated by reading the KV cache, not by weight FLOPs.
- **Rubin** (~288 GB HBM4, ~20+ TB/s) and **Ironwood** (192 GB HBM3e, ~7.4 TB/s, 9,216-chip OCS pods) still stream every KV byte to the compute die for each token.
- **WSE-3** (44 GB SRAM) and **Groq** (~230 MB per chip) have huge bandwidth but cannot hold a 1M-token KV cache economically. SRAM bit-cell area barely shrank from N5 to N3E.
- Off-chip access costs roughly 3–5 pJ/bit. Moving bytes, not doing math, is the energy limit.

**Architecture**
- **Compute:** two reticle-limited N2 dies (~800 mm² each) with FP4/FP6 tensor arrays and modest SRAM.
- **Memory:** 8 stacks of HBM4 with custom logic base dies. TSMC and SK hynix now offer logic-process base dies.
- **Packaging:** CoWoS-L, backside power, ~1.8 kW per package, liquid cooling.
- **Programming model:** a JAX/PyTorch front end that lowers to "attention contracts". Each contract states which top-k selection is allowed and an error budget, so the compiler can choose sparsity and precision legally.

**What must be true**
1. Top-k sparse attention keeps model quality. DeepSeek's DSA "lightning indexer" is early evidence.
2. HBM base-die logic fits a few watts per stack under thermal limits.
3. Co-packaged optics yield is acceptable.
4. CoWoS capacity is available.

**Failure mode.** If models abandon softmax attention (for example, moving to SSM hybrids), the first idea loses most of its value. The other two survive.

=== IDEAS ===
IDEA 1
NAME: Retrieval-native HBM base die
MECHANISM: Each HBM4 stack's logic base die stores a 1–2-bit sketch of every key. For each decode query it runs an approximate top-k search beside the DRAM. Only the selected K/V rows cross to the compute die. The value of k adapts per head from observed attention entropy.
VALUE: Long-context decode traffic falls by an estimated 10–50×, so million-token contexts cost roughly what short ones do today.

IDEA 2
NAME: Checksum-governed adaptive precision
MECHANISM: Each matmul tile carries algorithm-based fault-tolerance checksums computed at higher precision. Hardware compares the low-precision result against the checksum and uses the residual to step that tile's precision per token (ternary, FP4, FP6, or FP8), staying within a compiler-specified error budget. The same residuals flag silent data corruption.
VALUE: The chip runs each operation at the lowest precision that is provably safe, and it catches the silent hardware errors that plague large fleets.

IDEA 3
NAME: Softmax-merging optical switches
MECHANISM: The KV cache is sharded across chips over co-packaged optics. Fabric switches contain ALUs that combine partial attention results (running max, sum, and weighted output) using the online-softmax rule as packets pass through. A query reaches all shards and gets back one merged vector in a single round trip.
VALUE: One sequence's context can span hundreds of chips at near single-chip latency, with no all-gather of KV data.