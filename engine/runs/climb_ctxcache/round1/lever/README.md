# Lever round 1: real-trace replay of cache-aware context management

- `extract.py`: downloads a 1-in-8 sample (63 of 500) of the SWE-agent + Claude 3.5 Sonnet SWE-bench Verified
  trajectories from the public bucket `s3://swe-bench-submissions` (listed in SWE-bench/experiments `metadata.yaml`).
  It reduces them to `traces.json`, which holds message sizes and per-line hashes of file views.
- `replay.py` → `replay.out`: prefix-cache billing replay of 2,068 real API calls under 8 context policies and 3 price
  schedules, plus the exact offline-optimal masking schedule (DP).
- `robust.py` → `robust.out`: per-trace spread, bootstrap CI, placeholder-size and run-length sensitivity, and the
  context-window check.

Calibration: SWE-agent ran with LastNObservations(5). A 3.45 chars/token rate, with a tight spread (IQR 3.36–3.50),
reproduces the recorded `tokens_sent` only under that masking (raw append would need 4.9, with a wide spread). So each
trace is converted at its own calibrated rate, and its masked total matches `tokens_sent` exactly.

Not measured here: task success (quality). That needs a real-model A/B run on SWE-bench (see the answer).

Added in this round (all standard library, run from this directory with `python3 -I <script> > <script>.out`):
- `terms.py` → `terms.out`: splits each policy's bill into static-prefix reads, history reads, first writes, re-writes.
- `thresh.py` → `thresh.out`: ski-rental trigger vs fixed `clear_at_least`-style thresholds (best chosen in hindsight),
  and cross-task sharing of the 7.1k-token system+demo prefix. Needs the `thresh` policy added to `replay.py`.
- `superset.py` → `superset.out`: at all 4,136 (call, variant) points, the batch mask hides only observations that the
  shipped roll-5 policy also hid.
- `phys.py` → `phys.out`: physical cost of a cache read on your own stack (70B, H100) relative to recompute.
