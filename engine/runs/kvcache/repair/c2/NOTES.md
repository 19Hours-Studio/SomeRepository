# NOTES — repair c2

Scripts (all in this folder): `idea1_budget.py`, `sim_evict.py`, `sim_chain.py` (+ `sim_admit.py`, which is the flawed per-block version that is kept for the record), `idea2_econ.py`.
Outputs: `sim_evict_out2.txt`, `sim_chain_out.txt`.
Traces: Mooncake FAST25 `conversation_trace.jsonl` (12,031 requests) and `toolagent_trace.jsonl` (23,608 requests), 512-token hashed blocks, 1 h (github.com/kvcache-ai/Mooncake).
No real-model run was possible (HF blocked). Every quality claim below is either sourced or listed as an open unknown.

## Idea 1: Turn-granular reversible eviction
Anchor: query-agnostic (KVzip-style) residency, with evicted pages kept in CPU memory and recallable instead of deleted. Kept.

Change: recall moves from every decode step to once per user turn, with a small per-step valve.

Consistency table (Llama-3.1-8B, FP8 64 KiB/token, H100 80 GB, PCIe 25 GB/s effective, 32K context):

| limit | value used | computed | margin |
|---|---|---|---|
| HBM for KV (80 − 16 − 8 GB reserve) | 56 GB | 64 users × 0.41 × 32K × 64 KiB | fits by construction |
| PCIe per step, per-turn recall | 25 GB/s × 20.8 ms | 0.08 of the step | 12× |
| PCIe per step, valve | ≤ 0.36 % of context per step | — | hard cap |
| output tokens per turn | ≥ 26 needed | trace mean 343 | 13× |
| recall burst at turn start | 210 MB → 8.4 ms | overlapped with prefill | OK |
| host DRAM, 2 TB node | 954 sessions at 32K (238 at 128K) | 8 GPUs × 64 active = 512 | OK at 32K; at 128K, needs an SSD/LMCache tier |
| KVzip ratio window | near-lossless at 30 % (FACT 2) | 30 % resident + 10 % recalled | in window |
| FP8 kernel | needs the FP32-accumulation fix (FACT 6); skip SWA layers | — | config |
| scoring overhead | must be ≤ 0.29 × prefill at 7.6K new tokens per turn | KVzip ≈ prefill-scale (unverified) | **binding** |

## Idea 2: Cost-per-byte value density at the bounded tier
Anchor: (expected reuses × recompute FLOPs) ÷ bytes, with exact reuse only. Kept.

Change: the score is applied only where capacity or writes are bounded. Admission works on whole prefix chains, because a deep block is worthless without its ancestors (found in the replay). The eviction half-life is 180 s.

Consistency table:

| limit | value | check |
|---|---|---|
| HBM-tier capacity where the anchor pays | 0.26–2.56 M tokens | 8B FP8 on H100: ~0.2–0.9 M tokens free → in window |
| larger tiers | ≥ 5 M tokens | gain −5 % to +11 % → LRU is fine (kill test confirmed) |
| SSD write-all load | DSv3 2.26 GB/s per node = 196 TB/day = 25 × 7.68 TB 1-DWPD drives | exceeds a typical 8–16 drive node at 1 DWPD; fits at ≥ 3 DWPD |
| 70B BF16 | 10.5 GB/s = 912 TB/day = 119 drives of endurance | hard cap → admission required |
| break-even P(reuse), from the anchor's $ form | 0.04 (DSv3), 0.21 (8B) | sets the threshold |
| half-life | 600 s and GDSF lose up to 25 % at 5–10 M tokens | tune per tier |
