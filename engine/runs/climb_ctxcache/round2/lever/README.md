# round2/lever: files and how to reproduce

New in this round: a real model. Qwen3-0.6B weights came from Docker Hub's `ai/qwen3:0.6b-safetensors`
OCI artifact (registry-1.docker.io is reachable here; huggingface.co is not). Every blob was checked
against its OCI sha256 digest. `fetch_model.sh` downloads it.

| File | What it does | Output |
|---|---|---|
| `fetch_model.sh` | Downloads Qwen3-0.6B (config, tokenizer, safetensors) from Docker Hub and verifies digests | `$QWEN_DIR` (default `/tmp/claude-0/w/qwen3`) |
| `qwen.py` | Minimal Qwen3 forward with an explicit, editable KV cache (post-RoPE keys, key re-rotation). Matches `transformers` 5.2 logits to 7e-5 in fp32 (argmax 100%). | — |
| `spliceq.py` | Real-model quality of server-side KV splicing on real SWE-agent traces (sliding last-5 clearing): exact recompute vs splice (re-rotate), splice (position gap), splice + 16/128-token boundary repair; plus the clearing effect itself (append-only vs sliding) and a bf16 chunking floor | `spliceq_s0.jsonl`, `spliceq_s1.jsonl` |
| `analyze.py` | Summary with bootstrap CIs over traces | `analyze.out` |
| `bp2.py` | Anthropic 20-block lookback billing with written-prefix cache entries: 1 breakpoint, +window breakpoint (check1's fix), 4-breakpoint layout | `bp2.out` |
| `ownstack.py` | Own-stack GPU time per policy (Llama-3-70B shape, H100 roofline, decode batch 8/32/128) instead of API multipliers | `ownstack.out` |
| `traces.py`, `rule.py`, `fetch_traces.py`, `data/` | Unchanged from round1/fix (sha256 of `data/traces.jsonl` matches) | — |

```
sh fetch_model.sh
CAP=8000 NTR=8 MAXEV=6 TMPD=/tmp/claude-0/t0 python3 -I spliceq.py data/traces.jsonl spliceq_s0.jsonl 0 2
CAP=8000 NTR=8 MAXEV=6 TMPD=/tmp/claude-0/t1 python3 -I spliceq.py data/traces.jsonl spliceq_s1.jsonl 1 2
python3 -I analyze.py spliceq_s0.jsonl spliceq_s1.jsonl > analyze.out
python3 -I bp2.py data/traces.jsonl > bp2.out
for b in 32 8 128; do echo "== decode batch $b"; BATCH=$b python3 -I ownstack.py data/traces.jsonl; done > ownstack.out
```

Notes:
- `spliceq.py` runs in bf16 and single-threaded (the CPU is shared). Each shard took about 2 h with ~2 GB anonymous RSS.
- Bf16 is not bit-deterministic across chunkings. `floor` in the output measures the KL between one-shot and two-chunk exact prefill of the same prompt; that is the noise any bf16 server already has.
- Selection: traces whose first 4+ clearing events happen while the append-only prompt is at most 8,000 Qwen tokens (seed 0, 8 traces, up to 6 evaluation requests each). These are early turns, so at most a few accumulated splices are tested.
- Qwen3 tokenizer: 3.51 chars/token on these traces, so round1's chars/3.5 estimate holds for this tokenizer.
