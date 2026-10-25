**Deciding numbers** (Archetype A ledger; assumed Llama-70B-class GQA, 80 layers, 8 KV heads):

- **Cache write share.** Writes are 8.2% of input tokens: write volume 0.47/3.75 versus read volume 0.42/0.30. With about 50 turns of linear growth, genuinely new tokens are only about 2/N ≈ 4%. About half of all writes are therefore rewrites of content already seen, worth about 23% of the bill.
- **KV fetch versus recompute.** KV is about 320 KB per token in BF16, so a 100k context is 32 GB. Fetching it over 50 GB/s takes 0.64 s, or 0.32 s in FP8. Recomputing it takes about 35 s. Fetching wins by about 50×.
- **Ceiling.** Suppose all rewrites are removed, the write premium is dropped and reads become 5× cheaper. The bill falls to 0.19 + 0.08 + 0.01 + 0.10 = 0.38, about 2.6× cheaper. That is below the 3× target.
- **Who gets the saving.** On a hosted API all of this is provider-side, and the client sees it only if prices change.
- **What stays below about 100%.** Middle edits, reordering and early tool-output changes are matching problems, not placement problems. Under these constraints they stay well below 100%.

**Candidates**

1. Prefix-aware or session-sticky routing | P 0.60
2. CPU/SSD KV tier (LMCache, Mooncake) | P 0.55
3. FP8 or 4-bit KV in the store | P 0.40
4. Layer-wise streaming fetch that overlaps compute | P 0.15
5. Register decode-time KV so assistant turns are never rewritten | P 0.08. Rejected: output is only about 5% of written tokens, so it saves about 2.5% of the bill.
6. Provider-signed public-prefix pool | P 0.09
7. Attention computed at the KV store | P 0.07
8. Erasure-coded pooled KV | P 0.05

=== IDEAS ===
IDEA 1
NAME: Attention at the KV store
MECHANISM: On each agent turn, only the new suffix is prefilled. The suffix's queries go to the node that already holds the session's prefix KV, and that node returns partial attention outputs with log-sum-exp values. These merge exactly with local attention over the suffix, so the KV never moves and the output matches full recomputation bit-for-bit up to floating-point order. Closest earlier work: Lamina (2024) offloads decode attention only; this applies the same split to suffix prefill. The deciding quantity is traffic, n·Hq/(L·Hkv) = 8n/L. It wins whenever the n new tokens are fewer than L/8, for example 2k new tokens over a 100k context gives about 6× less traffic than a BF16 fetch. Costs: 80 per-layer round trips per turn, and compute on the store node. It runs on your own stack or provider-side.
VALUE: Hits on 100k+ contexts become cheap from any replica without moving the KV. This lowers the provider's cost of cache reads (42% of the bill), but it does nothing for middle edits.

IDEA 2
NAME: Erasure-coded pooled KV memory
MECHANISM: Each content-addressed KV chunk, keyed by its prefix hash, is striped in FP8 across the CPU DRAM of a replica group using a k-of-n erasure code (for example 8+2). This replaces full replication, so the pooled memory holds about 2.4× more sessions than 3× replication at the same capacity. Any replica can rebuild a chunk from any k stripes. Closest earlier work: Mooncake Store replicates chunks, and its capacity limit causes the evictions that lead to rewrites. The deciding quantity is the share of rewrites caused by eviction or placement rather than by expiry. Losing a stripe costs one decode, not a recompute. Output quality is unchanged because the stored values are exact FP8.
VALUE: It cuts the roughly 23%-of-bill rewrite term wherever capacity misses drive it, on your own stack or provider-side.

IDEA 3
NAME: Signed public-prefix KV pool
MECHANISM: Agent harnesses publish signed, version-pinned system prompts and tool schemas, assumed to be about 15–20k tokens. Their KV is precomputed once and pinned on every replica. Requests whose prefix hash matches a signed entry get a hit without a per-organisation write. Closest earlier work: per-organisation prompt caching, which isolates organisations because shared caches leak through timing side channels. Sharing only public signed content removes that leak. The deciding quantity is the harness-prefix share of all writes, including writes repeated after expiry. The estimate is a 5–9% bill cut, with no change in quality. It runs provider-side only.
VALUE: Session starts and cross-replica first turns stop paying the write premium for content that is identical across all users.