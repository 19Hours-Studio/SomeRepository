# round1/fix: files and how to reproduce

All scripts use only the Python standard library. Run them from this directory.

| File | What it does | Output |
|---|---|---|
| `fetch_traces.py` | Downloads a fixed random sample (seed 0) of 200 of the 500 SWE-agent / Claude Sonnet 4 SWE-bench Verified trajectories from the public `swe-bench-submissions` S3 bucket. It keeps only the message history. | `data/traces.jsonl` (sha256 in `data/traces.sha256`) |
| `traces.py` | Replays the traces under several context policies (append-only, sliding last-5 elision, batch clearing, ski-rental, offline DP optimum, server-side splice, delta re-views) with exact prefix-cache billing. | `traces.out` |
| `rule.py` | Tests the price-derived online "horizon" clearing rule, and checks that each request's context is a superset of what the sliding window shows. Set `KEEP=10` for the sensitivity run. | `rule.out`, `rule_keep10.out` |
| `diffstat.py` | Measures real file re-view statistics, which set the size of a diff erratum. | `diffstat.out` |
| `replay_v1.py` | Synthetic edit replay. Billing is corrected as in check0, and it adds the hybrid erratum-or-rewrite chooser. | `replay_v1.out` |
| `idea4.py` | Per-model break-even reuse interval: each model's own recompute cost (including attention) against its own KV storage cost. | `idea4.out` |

```
python3 -I fetch_traces.py data/ids_all.txt data/traces.jsonl 200
python3 -I traces.py data/traces.jsonl > traces.out
python3 -I rule.py data/traces.jsonl > rule.out; KEEP=10 python3 -I rule.py data/traces.jsonl > rule_keep10.out
python3 -I diffstat.py data/traces.jsonl > diffstat.out
python3 -I replay_v1.py > replay_v1.out; python3 -I idea4.py > idea4.out
```

Assumptions:
- Tokens are estimated as chars/3.5, because no tokenizer could be downloaded here.
- A tool-schema prefix of 2,500 tokens is assumed.
- The elision placeholder is 12 tokens.
- Each request can hit the cache of the previous request (the 5-minute TTL is assumed never to expire inside a trace).
- The replays hold the agent's actions fixed. They measure prompt cost, not how the agent's behaviour would change under a different context.
