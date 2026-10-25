# Reframe: the bill is re-reads, not misses

Run with `python3 <file>` from this directory. Outputs are saved next to each script as `.out`.

- `trace_bound.py` replays the Mooncake FAST'25 public traces (toolagent, conversation, synthetic) with an infinite exact prefix cache. Download them from raw.githubusercontent.com/kvcache-ai/Mooncake/main/FAST25-release/traces/ and pass the paths as arguments. The script reports the hit rate, the read/write split of the input bill, and the most a perfect 100% hit rate could save. The hashes are chained, so non-prefix reuse cannot be measured; the trace check confirms 0 of 183,300 missed blocks had been seen before.
- `levers.py` is the corrected-billing agent session from check0/replay_fixed.py: errata, k-way batching of tool calls, and digest side-calls.
- `op_cost.py` estimates the operator's real cost of a cache read compared with a recompute: attention plus residency in HBM, DRAM or NVMe. The hardware prices are assumptions.
- `combo.py` combines the client-side levers with read prices of 0.1x, 0.05x and 0.03x.
- `noedit.py` runs the same levers on a workload with no edits, and shows how the saving grows with session length.

Nothing here was measured on a real model, because huggingface.co is blocked in this environment. All quality claims are untested.
