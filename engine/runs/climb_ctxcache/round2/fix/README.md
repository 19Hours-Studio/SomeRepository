# round2/fix: files and how to reproduce

Round-1 files copied unchanged: `traces.py`, `rule.py`, `data/` (same sha256 as round 1).
`probe_check1.py` is check1's probe (SWE-agent `polling`, 20-block lookback), copied for reference.

| File | What it does | Output |
|---|---|---|
| `billing2.py` | (a) Anthropic breakpoint billing: entries only at earlier breakpoints, 20-block lookback; 1 end breakpoint vs the 4-breakpoint placement. (b) Every clearing family (SWE-agent polling, fixed batch, horizon, DP) swept over window KEEP=3/5/7/10, as cost vs mean prompt. (c) Own-stack cost (Llama-3-70B shape, H100): prefill FLOPs incl. splice key re-rotation, decode KV bytes read, GPU-hours, KV residency. | `billing2.out` |
| `decode_dilute.py` | Adds the policy-independent decode weight compute (2·NP per output token, at 45% and 15% MFU) that (c) leaves out, so the own-stack GPU-hour percentages are not overstated. | `decode_dilute.out` |
| `get_model.sh` | Fetches SmolLM2-135M-Instruct (GGUF Q4_1) from the PyPI wheel `llm-smollm2==0.1.2` (sha256 checked); huggingface.co is blocked here. | `model/` |
| `smol.py` | Minimal exact Llama forward pass in torch (weights dequantized to fp32) with an editable KV cache: `splice` (cut span, RoPE-shift later keys) and `insert_at`. | |
| `sanity.py` | Tokenizer round-trip, RoPE convention (right one: NLL 3.24 vs 4.74), chunked = unchunked, splice+reinsert of the same tokens = original cache bit-exactly. | `sanity.out` |
| `spliceq.py` | Splice quality on real traces vs full recompute (KL, top-1, dNLL), with no-shift, keep+1 and numerical-noise references. | `out/spliceq.*.jsonl` |
| `spliceq_sum.py` | Summary with bootstrap CIs over traces. | `spliceq_sum.out`, `poll4_sum.out` (splices batched 4 at a time, POLL=4) |
| `clearq.py` | Exact clearing (keep-5, keep-3) vs the append-only prompt the agent ran, same metrics. | `out/clearq.jsonl`, `clearq_sum.out` |

```
python3 -I billing2.py data/traces.jsonl > billing2.out            # ~10 min, stdlib only
python3 -I decode_dilute.py data/traces.jsonl billing2.out > decode_dilute.out
sh get_model.sh                                                    # needs pip, torch, gguf, tokenizers
python3 sanity.py model/llm_smollm2/SmolLM2-135M-Instruct.Q4_1.gguf data/traces.jsonl > sanity.out
for s in 0 1; do python3 -u spliceq.py model/llm_smollm2/SmolLM2-135M-Instruct.Q4_1.gguf data/traces.jsonl $s 2 > out/spliceq.$s.jsonl & done; wait
python3 -I spliceq_sum.py out/spliceq.*.jsonl > spliceq_sum.out
POLL=4 NTR=12 EVERY=2 python3 -u spliceq.py model/llm_smollm2/SmolLM2-135M-Instruct.Q4_1.gguf data/traces.jsonl 0 1 > out/poll4.jsonl
python3 -I spliceq_sum.py out/poll4.jsonl > poll4_sum.out      # keep+1 is 0 here: under polling it is often the same prompt
python3 -u clearq.py model/llm_smollm2/SmolLM2-135M-Instruct.Q4_1.gguf data/traces.jsonl > out/clearq.jsonl
python3 -I clearq_sum.py out/clearq.jsonl > clearq_sum.out
```

Torch runs single-threaded by default (`THREADS=1`): the machine was shared and 4 threads were slower.
The splice runs are deterministic on one machine (fp32, fixed sample seed 0); across CPUs the last digits of KL can differ.

`out_old/` holds partial output of an earlier, larger configuration that was stopped (OOM on the shared machine); it is not used.
