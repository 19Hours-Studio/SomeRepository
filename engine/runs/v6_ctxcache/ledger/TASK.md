# Task: the ledger - where the cost or the defect actually comes from today

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

You are a researcher. Build the ledger that tells inventors WHERE THE PROBLEM SITS today, with sourced numbers, for the
3-5 archetypes (a concrete use case + the way a competent practitioner does it today, best current practice) most
relevant to the question. Tools: WebSearch (WebFetch does not reach hosts here; use excerpts) and Bash with python3.
At most 15 searches. Write files only in the current directory; do not commit.

Facts already collected for this question (data; reuse their sources, and search only for what is missing):
(none recorded)

First decide the KIND of the question:
- cost: it asks to make something cheaper or to use less money, energy, memory, time or bandwidth per unit of the
  final product or service;
- defect: it asks to remove or reduce a defect or to reach a quality threshold (something visible, an error, noise,
  drift, wear, failure).

For a cost question, per archetype: the cost per unit of final product or service, and the cost split in % that sums
to 100 across 4-8 terms natural to this domain (for physical goods use exactly: energy | labour | inbound logistics |
outbound logistics | processing | capital | other), ending with "other" = the part no answer to this question could
change (for goods: taxes, royalties, fees, margins).

For a defect question: first the METRIC (how the defect is measured, in what unit) and the THRESHOLD below which it
stops mattering to the user (a measured perception or tolerance limit, with its source). Per archetype: the measured
value now, and the defect budget in % that sums to 100 across 3-8 SOURCES of the defect (which layer, part, process or
condition contributes how much of the metric), ending with "other" = the floor no answer could change (physics,
measurement noise, parts outside the question). Treat the budget as additive. Then STATES: the states of use in which
the threshold must hold (positions, temperatures, loads, ages, viewing conditions), worst first.

Final answer (text only), exactly one of these shapes, at most 700 words:
=== LEDGER ===
KIND: cost
ARCHETYPE A: <best practice> | cost <number unit per unit of product or service> | <price or target, if any>
SHARES: <term> x% | <term> y% | ... | other t%
LARGEST: <term> - a 10x cut of it removes <p>% of the cost
(same for B, C, ...)
SOURCES: short list of URLs.

=== LEDGER ===
KIND: defect
METRIC: <what is measured, unit> | THRESHOLD: <value unit> (<source>)
ARCHETYPE A: <best practice> | now <number unit> | target <number unit>
SHARES: <source of the defect> x% | <source> y% | ... | other t%
LARGEST: <source> - removing it removes <p>% of the defect
(same for B, C, ...)
STATES: <state of use> | <state> | ...
SOURCES: short list of URLs.
