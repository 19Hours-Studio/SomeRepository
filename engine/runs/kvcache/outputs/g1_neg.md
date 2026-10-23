**Criteria.** I judge "best" by four things: GPU-seconds per request, accuracy change against an **FP8 baseline** (not FP16), whether outputs match exactly, and the per-model calibration cost. The ledger rules out targeting C, because the provider margin caps the gain at 3.3×. D has room, with prefill recompute at 66% of cost. A is tight: a 10× cut of the decode KV read gives at most 1.29×.

**The 8 standard answers:** FP8 KV, KIVI, KVQuant, SnapKV/H2O, StreamingLLM, DuoAttention, Quest, and prefix caching with LMCache. **Shared paradigm:** each one shrinks or drops one request's cache using a local guess about which bits matter. That makes them lossy whenever the guess is wrong, as in multi-turn chat, long outputs and reasoning. FP8 is the safe default only on GQA models it has been tested on. It is known to fail on DeepSeek-R1-Distill-Qwen-7B.

**Outside that paradigm,** every idea below either gives exact outputs or proves its error bound. None of the three has been run. The gains are hypotheses, each with a test that would kill it.

=== IDEAS ===
IDEA 1
NAME: Lossless-coded offload tier
MECHANISM: FP8 KV pages that are evicted to CPU or SSD are entropy-coded with per-layer, per-channel tables, and decoded on the GPU while they stream back, so restored caches are bit-identical. The closest earlier attempt is CacheGen, which is lossy, needs codec kernels and gains only 1.67–1.81× over 8-bit. Lossless coding avoids its accuracy risk, and it raises the prefix hit rate by fitting more prefixes into the same tier. The deciding quantity is the lossless ratio on FP8 KV. It can be falsified by measuring byte entropy on Llama-3.1-8B, Qwen and Gemma caches: below about 1.3×, or decode slower than PCIe (about 25 GB/s), and the idea is dead. It would then fail on models whose KV has near-uniform exponents.
VALUE: For RAG or chat with shared prefixes (D), it gives more cache hits per dollar of storage while keeping outputs exactly the same.

IDEA 2
NAME: Certified-bound page skipping
MECHANISM: Each KV page stores per-channel min/max key bounds. At decode, the method computes an upper bound on each page's softmax mass and skips a page only if all skipped pages together provably carry less than ε of the attention. Otherwise it reads the full page. The closest earlier attempt is Quest, whose top-k is heuristic and gives no guarantee. This design trades some speedup for a provable error bound. The deciding quantity is the fraction of pages that can be certified as skippable at ε=1e-3 on RULER at 128K. If it is under 50%, the gain is below about 1.15× and the idea fails. It also fails on diffuse-attention tasks such as aggregation and HTML-to-TSV.
VALUE: For long single requests (A), it cuts the decode KV read with a stated error bound and no calibration.

IDEA 3
NAME: Compressed-draft, full-cache verify
MECHANISM: Decoding drafts k tokens against a 2-bit or evicted copy of the cache. The full FP8 cache, kept in HBM or CPU, then verifies all k tokens in one pass, so the final output equals the full-cache output. The closest earlier attempts are TriForce and MagicDec, which target latency and keep the full cache on the GPU. This design moves the full cache to the verify path only, and spreads its read over the accepted tokens. The deciding quantity is the mean accepted length per verify, which must exceed about 3 to beat FP8. It can be falsified on long-reasoning traces, where acceptance falls once compressed drafts drift; that is where it stops working.
VALUE: It frees GPU KV memory and reduces KV reads while keeping outputs exactly the same on any model.