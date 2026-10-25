# Gain check of answer.md

The scripts in round1/ reproduce byte-for-byte (costs, tiers, replay2).
Sensitivity script: scratchpad check.py (results below).

Baseline used here as "best current practice": an append-only prompt (Manus guidance; coding agents),
plus CPU-DRAM KV offload (LMCache / vLLM OffloadingConnector / SGLang HiCache) on own stacks.

| Claim | Against which baseline | Against best practice (this check) |
|---|---|---|
| Hit rate ~100% on re-sent tokens | in-place | append_full already gets 1.0000; total hit 96.27% vs 96.30%, so no gain |
| Idea 1 errata -35.8% | in-place (strawman) | -11.0% at 50 turns (only the diff=200 vs 2000-token re-read); -3% to -7% for long sessions; about 0 if the agent already appends diff-sized edit results |
| Idea 2 span ops -25% vs append_full | fixed shallow retention 195k->140k | gain shrinks as clearing gets deeper: -24.5/-12.2/-5.2% at 140k/100k/40k targets. Over a wider grid the cheapest setting for every policy is a 10k target: punch -1.0%, patch -5.4% vs append_full, and patch is no better than client errata (-5.6%). Approximate KV, quality untested |
| Idea 4 DRAM parking 1.4-9.5x | HBM pinning, with HBM priced at rental and DRAM at capex (mixed bases) | same basis (rental): 1.28/2.24/3.57x vs HBM pinning. DRAM offload is already standard (Continuum's own baseline is vLLM+LMCache CPU offload), so the gain is none |
| Quality | - | nothing measured on a real model; errata have a published interference risk (PI-LLM) |
