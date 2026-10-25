# Cost-scheduled observation masking (EOQ / ski-rental) — reproduction

python3 experiments.py > experiments.out   # ~3.5 min; W1 = baseline's synthetic workload, W2 = real SWE-agent steps
python3 rag.py > rag.out                   # multi-turn RAG: rebuild vs pin vs pin+evict

data/swea_steps.json: per-step (assistant_tokens, observation_tokens) = chars/4 from the 19 unique public
SWE-agent demo trajectories (git clone https://github.com/SWE-agent/SWE-agent, trajectories/ and tests/test_data/).
Billing: longest prefix identical to the previous request at R, rest at W. Anthropic W=1.25,R=0.1; OpenAI W=1.0,R=0.1.
Output tokens not counted. TTL expiry not modelled. All quality claims need a real-model A/B (not run here).
Differences from check0/replay_fixed.py: each entry is two segments (assistant output, tool result), errata are maskable;
this gives in-place 751k vs errata 548k units (-27.0%); the check reports -28.0% for full-size (2300-token) errata.
