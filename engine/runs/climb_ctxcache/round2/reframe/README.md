# round2/reframe: own-stack KV splicing, priced on 200 real traces and quality-tested on a real model

Run everything from this directory. `data/traces.jsonl` is the round1 file, and its sha256 is in `data/traces.sha256`.

## Real model, obtained without Hugging Face
`pip download --no-deps llm-smollm2` (PyPI) contains `SmolLM2-135M-Instruct.Q4_1.gguf`. That is a Llama-architecture model with RoPE and GQA (30 layers, 9 query heads / 3 KV heads, 8k context). Its sha256 is
`b179c9523d0e6a0f98a330c7562b682750a6f8c8c15e5bc70ea373728110db53`.
```
mkdir -p dl && cd dl && pip download --no-deps llm-smollm2 -d . && mkdir x && cd x && python3 -m zipfile -e ../llm_smollm2-0.1.2-py3-none-any.whl . && cd ../..
pip install gguf tokenizers     # torch 2.x already present
```

| File | What it does | Output |
|---|---|---|
| `smol.py` | Pure-torch forward pass for that model. The tokenizer is built from the GGUF vocab and merges, and the KV cache is explicit and editable (post-RoPE keys plus positions). `python3 smol.py` generates "The capital of France is Paris." and checks incremental against full logits (max diff 2e-5). | stdout |
| `test_rope.py` | Checks that re-rotating cached keys by +d equals recomputing at positions shifted by d, across all layers. Max relative error is 1e-6. | stdout |
| `exp_edit.py`, `run_edit.sh` | Real-model test of non-prefix KV reuse on real SWE-agent contexts. Edit cases: clear, replace, insert, reorder. Reuse variants: gap, shift, shift+boundary-recompute, tail. Each is compared with exact recompute. | `out/edit_*.jsonl` |
| `analyze.py` | Summary with bootstrap CIs. | `edit.out` |
| `cost.py` (imports `traces.py` from round1, unchanged) | Replays the 200 traces. It bills own-stack splicing (with the repair recompute measured in `exp_edit.py`, a re-rotation charge, and optional decode-KV reuse) against append-only, SWE-agent `polling=10`, batch5k and the round1 DP. Part 2 gives operator GPU-seconds for a 70B-class model. | `cost.out` |

```
python3 smol.py; python3 test_rope.py
./run_edit.sh          # 4 single-thread shards; ~1 h here (multi-threading is badly contended on this VM)
python3 -I analyze.py out/edit_*.jsonl > edit.out
python3 -I cost.py data/traces.jsonl > cost.out
```

Assumptions and limits:
- The quality model is a 135M model at Q4_1. Contexts are capped at 4,000 tokens, with each message truncated to 800 tokens, so the `clear` case uses KEEP=2.
- The cost replay uses chars/3.5 tokens, as in round1. The SmolLM tokenizer measures 3.05 chars/token on these traces, and the check showed the ratios move by 1 point or less across 2.8–4.2.
- The GPU model is roofline arithmetic, not a measurement.
