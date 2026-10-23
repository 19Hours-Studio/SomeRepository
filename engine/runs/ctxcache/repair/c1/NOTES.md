# Repair notes c1

Scripts: `idea1_calc.py`, `idea2_calc.py` (run with python3). No real-model run was possible because Hugging Face is blocked. Every quality number below is a published measurement or an assumption, and each one is marked as such.

## Idea 1: audit-calibrated chunk-KV fusion
Anchor: a closed-loop guarantee. A small sample of requests is shadow-audited against full recompute, and the results tune the recompute threshold to a measured quality budget for each workload.

Model: Llama-70B-class, FP8 KV at 160 KiB/token. One 8×H100 node at 50% MFU. Prefill costs 0.141 GPU-ms/token and decode 0.684 GPU-ms/token (4.8×, which matches the 5× API output/input price ratio). Each request has a 1k system prompt, 6×1k chunks, a 100-token query and 200 output tokens.

| scheme | GPU-ms/request | × vs exact prefix |
|---|---|---|
| full recompute | 1141 | 0.88 |
| exact prefix (system prompt only) | 1003 | 1.00 |
| ContextPilot reorder+dedup, h=0.34 / 0.60 (exact, no quality loss) | 720 / 503 | 1.39 / 1.99 |
| CacheBlend open-loop r=0.15 | 295 | 3.39 |
| AgentKVShift r=0.10 | 254 | 3.95 |
| IDEA r*=0.10, a=2% | 271 | 3.69 |
| IDEA + ContextPilot h=0.34, r*=0.10 | 237 | 4.22 |

Consistency checks:

| limit | value | check |
|---|---|---|
| KV load bandwidth, node | needs 24–39 GB/s | 1 NVMe at 7–14 GB/s FAILS. 4×NVMe RAID or a DRAM tier passes. PCIe5 at about 50 GB/s per GPU passes |
| storage economics, per 1k-token chunk (0.164 GB) | NVMe ≈ $2.2e-5/h, DRAM ≈ $6.7e-4/h; each reuse saves ≈ $8.8e-5 | admit to NVMe if ≥0.25 reuses/h, to DRAM if ≥7.6/h |
| audit power | ε=2%: 148 audits, i.e. 7.4k requests per window at a=2% | small tenants cannot be certified, so they get the exact-prefix fallback |
| decode floor | 137 of 271 GPU-ms is output | the whole-request gain is capped at about 2× more even at r=0 |
| quality at r=0 | Musique F1 0.35→0.15 (CacheBlend paper) | ~100% reuse with exact quality is impossible |
| selector at 10% | CacheBlend −47.5%, AgentKVShift −5.9% (AMem) | a correcting selector is needed to reach r*≤0.1 |

## Idea 2: context-length-gated turn collapsing
Anchor: the decision to stop and observe is gated on the price of one more full-context read, which grows with C. Late, expensive turns are therefore collapsed into multi-step scripts.

Results (Anthropic pricing: 5-minute write 1.25×, read 0.1×, output 5×):

| session | baseline $ | read share | gated | gated + in-script filter 50% |
|---|---|---|---|---|
| 40 turns, 8k system, 1.2k obs | 0.925 | 47% | 1.48× | 1.81× (1.92× at 30%) |
| 150 turns, 20k system, 0.6k obs | 4.41 | 75% | 2.02× | 2.42× |

For comparison: uniform 2× turn cut 1.41×; CodeAct's 30% fewer turns 1.20×; observation masking with cache rewrites 0.83× (my model).

Consistency checks:

| limit | check |
|---|---|
| 5-minute TTL | a longer script means a longer wall-clock gap between reads. If a folded batch runs >5 min, use the 1-hour TTL (write 2×) or a keep-alive. Not modelled in the ratios |
| irreversible actions | never fold steps that write, delete or deploy. Fold only read-only or idempotent tools |
| output tokens | scripts raise output (AIMultiple measured +120% output with −78% input). My model keeps action tokens constant, so this is a hazard |
| success-drop tolerance | the saving is $0.41/task, so the success drop has to be ≈0 for any task worth more than about $10 |
| test power | 1,307 paired tasks to detect a 3-point drop; 470 for 5 points |
