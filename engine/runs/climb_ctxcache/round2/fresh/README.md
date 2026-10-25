# round2/fresh: files and how to re-run them

Everything uses the Python standard library only. `sh scripts/fetch_data.sh` fetches the data and
checks its hashes; `sh scripts/run_all.sh` rewrites every file in `out/` (about 15–25 min on 4 cores).

## Data (sha256 in `data/SHA256SUMS`)

- **Bailian production traces.** `data/qwen_{traceA,traceB,coder,thinking}_blksz_16.jsonl`: 269,681
  anonymised requests to a Qwen serving cluster on Alibaba Cloud Bailian, covering a 2-hour window,
  from the KVCache-in-the-Wild paper (ATC'25). Each record has an arrival time, input and output lengths,
  a request type, the parent request in the session, and hashes of 16-token blocks. They are fetched from
  the Git LFS media host of `github.com/alibaba-edu/qwen-bailian-usagetraces-anon`.
  - `probe.py` shows that A and B hash each block's content, so non-prefix reuse is visible in them. Coder
    and thinking chain each hash to its prefix, so only prefix reuse is visible there.
- **SWE-agent traces.** `data/traces.jsonl` holds the same 200 trajectories as round1/fix (SWE-agent 1.1,
  Claude Sonnet 4, SWE-bench Verified, temperature 0).
  - `data/swe_stats.jsonl` (written by `fetch_stats.py`) adds the dollars SWE-agent recorded and each
    tool's measured execution time.

## Scripts and outputs

| Script | Question it answers | Output |
|---|---|---|
| `probe.py` | Are the block hashes per-content or prefix-chained? | `out/probe.txt` |
| `reuse.py` | Infinite cache: prefix hits vs. non-prefix content seen before | `out/reuse.txt` |
| `sessions.py` | Within sessions: how much re-sent context is lost to a mid-prompt change; gaps between turns | `out/sessions.txt` |
| `compose.py` | Input split into re-sent parent prompt, carried-over parent reply, and new tokens | `out/compose.txt` |
| `ttl.py` | Prefix-hit share under TTLs of 5 min to infinity | `out/ttl.txt` |
| `taxonomy.py` | Non-prefix reuse split into insertion/edit, reordering, and content from another request | `out/taxonomy.txt` |
| `retain.py` | Anthropic-style bill under fixed client policies: 5 min, 1 h, keep-alive pings | `out/retain_fixed.txt` |
| `policy.py` | Per-request choice between skipping the write, 5 min and 1 h: online rule (train/test split by session) and oracle | `out/policy.txt` |
| `exact_ceiling.py` | Exact-KV levers on the bill: reply carry-over, 1 h provider retention; with `W=1.0 ROWS=openai`, OpenAI's 24 h retention flag | `out/exact_ceiling.txt`, `out/openai_retention.txt` |
| `keep_cost.py` | Provider view: NVMe/DRAM storage cost of 1 h retention vs. the prefill it saves, for a dense and a MoE model | `out/keep_cost.txt` |
| `controller.py` | Provider-side cost-based keep time per (turn, type) category, trained on even sessions, scored on odd ones | `out/controller.txt` |
| `calibrate.py` | Round-1 replay bill vs. dollars actually recorded by SWE-agent | `out/calibrate.txt` |
| `carry_swe.py` | Reply-KV carry-over on the 200 agent sessions | `out/carry_swe.txt` |
| `swe_crossreuse.py` | Agent tool output already seen in an earlier trajectory, or earlier in the same one | `out/swe_crossreuse.txt` |
| `copyspec.py` | Lossless prompt-lookup speculation on the real agent outputs: tokens per verify pass | `out/copyspec.txt` |
| `agent_gpu.py` | Own-stack GPU time breakdown of the agent sessions with exact prefix caching | `out/agent_gpu.txt` |
| `agent_gpu_spec.py` | The same breakdown with copy-speculation (the τ, ρ values from `copyspec.py`) | `out/agent_gpu_spec.txt` |

`r1_traces.py` is round1/fix's `traces.py`, copied unchanged and used as a library for the agent traces.

## Assumptions (all in the script headers)

- **Prices.**
  - Anthropic: read 0.1, 5-min write 1.25, 1-h write 2.0, output 5× input.
  - OpenAI: no write premium, read 0.1, and the same price for 24 h retention.
  - Hardware: H100 at $2/h, 45% of 989 TFLOP/s, 70% of 3.35 TB/s.
  - Storage: DRAM $0.0066/GB-h; NVMe $0.00014/GB-h.
- **Token estimates.**
  - Agent-trace tokens are chars/3.5. `calibrate.py` shows the recorded dollars are 1.30× the replay, so
    absolute values are about 30% low; ratios are unaffected.
  - `copyspec.py` uses GPT-2 pre-tokenizer pieces as tokens. With a finer split, τ is higher (2.3–3.0).
- **Trace window.** The Bailian window is 2 h, so gaps longer than about 1 h are censored.
- **Cache scope.** The Bailian replays share one cache across all users. An API cache is scoped per
  organisation.
- **Not measured: output quality.** No model weights could be downloaded. Every mechanism counted as a
  saving here leaves the prompt and the KV exactly as a full recompute would, except where it is labelled
  "approximate".
