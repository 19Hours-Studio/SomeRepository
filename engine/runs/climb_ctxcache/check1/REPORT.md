# check1: review of round1/fix

What was done
- rerun/: copied all of the answer's scripts and re-ran them on data/traces.jsonl (sha256 matches 7dc0a031...).
  All six .out files are byte-identical to the answer's.
- exp/probe.py -> exp/probe.out: SWE-agent LastNObservations(polling=P) baseline, size-selective batch clearing,
  Anthropic ~20-block cache lookback with a single end breakpoint, and bootstrap CIs over the 200 traces.
- exp/chsens.py -> exp/chsens.out: chars/token at 2.8 / 3.5 / 4.2.

Key results (Anthropic prices, billed-input units)
| policy | vs sliding | vs append | mean prompt |
|---|---|---|---|
| horizon (answer) | -45.4% (CI -46.4..-44.3) | -23.7% | 14,030 |
| batch5k (answer) | -47.1% (CI -47.8..-46.3) | -26.0% | 15,156 |
| SWE-agent polling=10 (prior art, not in answer) | -45.0% (CI -45.7..-44.3) | -23.2% | 15,724 |
| polling=5 / 20 | -42.0% / -43.2% | -18.9% / -20.6% | 14,396 / 18,411 |
| size-selective (>=500 tok, 3k batch) | -42.4% | -19.5% | 17,402 |

With only an end-of-prompt breakpoint and a ~20-block lookback, the clearing policies lose part of the hit:
horizon +31.6% (-45.4% falls to -28.1% vs sliding), batch5k +12.1%, polling10 +19.2%. Sliding and append are unaffected.
Fix: write and keep a second breakpoint at the start of the kept window at each clear (costs nothing extra).

Ratios move by <=1 point across chars/token 2.8-4.2.
