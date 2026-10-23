# Task: the ledger of earlier attempts - what has been tried, and why the problem is still unsolved

QUESTION the ledger serves: Hosted LLM APIs (Anthropic, OpenAI and others) offer prompt caching. The provider stores the computed intermediate state (the attention key/value, or KV, cache) for a request's token prefix. A later request is served from that state only if its prefix is token-for-token identical, and the cached portion is billed at a discount. An edit in the middle of a prompt, an insertion, a changed tool output, or a different document order breaks the match from the first differing token onward. Everything after that point is recomputed and billed at full price. The asker wants a way to make cached context much cheaper and to reach a cache-hit rate close to 100%. This must include requests that differ from earlier ones in the middle, by insertions, tool outputs or reordered documents, and it must work without retraining or fine-tuning the model. The question does not say whether the asker runs their own serving stack or uses a third-party API, or whether the solution may sit on the client side, the server side, or both. What is the best way to do this?
A good answer: A good answer proposes one or more concrete, new or non-obvious approaches. Each must state three things:
- which request-change cases it covers: middle edit, insertion, tool output, document reordering;
- its expected hit rate and cost change, with the reasoning or a quantitative estimate;
- its effect on output quality compared with full recomputation, and how that effect could be tested.
Each approach must also say where it can run (client only, own serving stack, or provider-side) and what it costs in memory, storage and latency. It must be checked against existing prior art and say what it adds. It must state honestly which cases cannot reach about 100% under the stated constraints.
Constraints: 
- No retraining or fine-tuning of the model.
- Target hit rate close to 100% across non-identical prefixes.
- Much lower cost than current prefix caching.
- Nothing else was stated.

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
