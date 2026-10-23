# Task: the value ledger - where the cost actually goes today

QUESTION the ledger serves: Which KV-cache design (storage layout, compression, eviction, quantization, offloading or reuse) can be swapped into an existing pretrained transformer LLM with no retraining and no fine-tuning, so that the same model gives the same outputs with a smaller, faster or cheaper cache? The asker wants to take any model and replace one component with another. This design should be the best across memory, speed and quality. "Best" is not defined. The answer should say which metric or workload it is best for, and where it stops working. Plausible workloads are long-context single requests, multi-user serving, multi-turn chat and prefix reuse. The asker did not give a model family, hardware, context length or serving stack. The answer may be a ranking of existing approaches, a new combination of them, or a new idea. Each claim must be checkable against published benchmarks or an experiment that can be run.
A good answer: 
- It names the criteria that define "best" (memory saved, throughput or latency, accuracy loss, calibration cost) and the workload each applies to.
- It checks "no training, any model" against published evidence: which models and architectures it was tested on, and what happens on an architecture it was not tested on.
- It gives numbers (compression ratio, accuracy change on benchmarks such as RULER, LongBench or multi-turn tasks, throughput) with sources.
- It states the conditions under which it fails, including a compression level, a task type and a model type.
- If it proposes something new, it gives a test that could show the idea is wrong.
Constraints: 
- No retraining and no fine-tuning of the model weights.
- It should be near plug-and-play and work on "any" model. See ASSUMPTIONS on whether that is possible.

You are a cost researcher. Build the ledger that tells inventors WHERE THE COST IS today, with sourced numbers, for the
3-5 archetypes (a concrete use case + the way a competent practitioner does it today, best current practice) most
relevant to the question. "Cost" is what the question asks to reduce or improve - money, energy, memory, time,
bandwidth, error - per unit of the final product or service. Tools: WebSearch (WebFetch does not reach hosts here; use
excerpts) and Bash with python3. At most 15 searches. Write files only in the current directory; do not commit.

For each archetype give: best current practice in one line; the cost per unit of final product or service; the cost
split in % that sums to 100 across 4-8 terms natural to this domain (for physical goods use exactly: energy | labour |
inbound logistics | outbound logistics | processing | capital | other), always ending with "other" = the part that no
answer to this question could change (for goods: taxes, royalties, fees, margins); the largest term.

Final answer (text only), exactly this shape, at most 700 words:
=== LEDGER ===
ARCHETYPE A: <best practice> | cost <number unit per unit of product or service> | <price or target, if any>
SHARES: <term> x% | <term> y% | ... | other t%
LARGEST: <term> - a 10x cut of it removes <p>% of the cost
(same for B, C, ...)
SOURCES: short list of URLs.
