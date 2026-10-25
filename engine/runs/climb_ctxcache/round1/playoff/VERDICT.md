# Playoff verdict: C1 > C2 > C4 > C3

## Reproduction (all re-run in this session)
| Answer | Script(s) re-run | Result |
|---|---|---|
| C1 (fix) | `rule.py` on 200 Sonnet-4 SWE-agent traces (sha256 matches) | identical to `rule.out` |
| C2 (lever) | `replay.py` on 63 Claude-3.5 SWE-agent 0.x traces | identical to `replay.out` |
| C3 (reframe) | `levers.py`, `op_cost.py`, `combo.py`, `noedit.py` | identical (combo/noedit need to be run without `-I`) |
| C4 (fresh) | `rag.py`; read `experiments.out` | identical |

## Independent check: do C2's lossless "delta views" hold up on a modern harness?
C2's only lossless gain (−19.4% vs append-only) comes from replacing already-seen line runs with back-references.
I applied the same rule (runs of ≥3 lines, same path, same line number and content, 12-token reference) to C1's
200 newer traces, including `str_replace` edit snippets (scratchpad `linedelta.py`):
**saving = 2.5%** (C1's narrower whole-view diff gives 0.2%). The 19% comes from SWE-agent 0.x's
windowed viewer, which shows the same 100 lines again after every edit. C2 does not flag that it depends on the harness.

## Why this order
- **C1**: largest and newest real-trace replay. Cost-timed batch clearing gives −24% to −26% vs append-only and
  −45% vs sliding-window clearing, with 0 superset violations in 24,442 requests. It reports honestly that deltas and
  errata add almost nothing on modern agents. It puts a dollar value on the server-side splice and gives per-model
  storage-tier break-even times. Weak point: the −45% headline is measured against a baseline that breaks the cache
  on every turn.
- **C2**: same core finding on real traces (−19% from batch masking alone, −30% combined). It has the best cost
  decomposition and an honest comparison with tuned thresholds. But its headline lossless lever mostly disappears
  on current harnesses, and its sample is smaller and older.
- **C4**: same masking idea, with a nice closed-form K* and a cost rule for pinning RAG documents. But it is
  measured on synthetic data and on 19 short demos resampled into sessions (0% on the recorded traces). Its
  −47.9% headline compares lossy masking with lossless in-place edits.
- **C3**: a useful reframe (reads, not misses, dominate the bill) and a sound physical-cost analysis of reads.
  But its −63% stacks an assumed batching factor k≈1.5–2, taken from one demo trajectory, on a read price that API
  users cannot change. All of its workloads are synthetic.
