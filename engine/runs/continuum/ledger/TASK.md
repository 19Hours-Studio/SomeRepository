# Task: the value ledger - where the cost actually goes today

QUESTION the ledger serves: Propose a new architecture for an AI accelerator chip, named "Continuum", that could credibly be called the best in the world. The asker has not said which workloads count: training, inference, or both. They have not said what "best" is measured by, or which kind of target (data center, edge, or other) the chip is for. A good answer therefore has to state its own target workloads and metrics, then defend the architecture against the current leading designs. Those designs include GPUs such as the Nvidia Rubin class, Google TPUs such as Ironwood, and SRAM-centric dataflow chips such as Cerebras WSE-3 and Groq LPU. The architecture should cover compute, memory hierarchy, interconnect, numerics, programming model, packaging and power. It should cite known physical, economic and manufacturing limits, and say what would need to be true for it to work. Reported 2026 reference points are listed in CONTEXT. Many are vendor or blog figures, and the sources disagree on some numbers.
A good answer: 
- The answer states explicit target workloads and a metric set. Examples are tokens/s per user, tokens per joule, cost per token, and training throughput. It says why those metrics define "best".
- It describes a coherent architecture with named blocks and quantified estimates. Estimates cover compute, on-chip and off-chip memory capacity and bandwidth, interconnect, power and die or package size. They are sanity-checked against roofline or bandwidth arithmetic.
- It compares quantitatively against at least three current designs (GPU, TPU, SRAM/wafer-scale) and says where Continuum wins, where it loses, and by how much.
- It names the main risks and the physical, process or supply limits (HBM supply, CoWoS packaging, power density, yield). It gives a falsifiable test or simulation plan that could prove the design wrong.
- It covers the software stack and programming model, and says what happens to existing models and frameworks.
- It separates established facts from the design's own assumptions and estimates.
- "Best in the world" is not asserted without evidence. Trade-offs are stated honestly.
Constraints: 
- The name is "Continuum".
- The answer is an architecture for an AI chip.
- Nothing else was specified. The answer must be a real, physically plausible design, not marketing text.

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
