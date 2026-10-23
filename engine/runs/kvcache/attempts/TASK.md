# Task: the ledger of earlier attempts - what has been tried, and why the problem is still unsolved

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

An unsolved problem means every earlier attempt stopped short for a reason that a re-invention would inherit. Build
the ledger of earlier attempts with sourced facts. Tools: WebSearch (WebFetch does not reach hosts here; use excerpts)
and Bash with python3. At most 15 searches. Write files only in the current directory; do not commit.

Cover methods in standard use (and what they still leave expensive), methods that stayed niche, pilots that were
dropped, and ideas that were costed and rejected, in any country, industry or period. For each: the binding reason it
did not solve the problem, with the number that shows it.

Final answer (text only), at most 1,000 words:
=== ATTEMPTS ===
ATTEMPT 1: <mechanism> | <where, who, when> | <standard / niche / dropped / rejected> | WHY IT DID NOT SOLVE IT: <reason with number> | <source>
(12-20 attempts, the most important first)
LESSONS: 3-6 lines - the limits any new answer must get past.
