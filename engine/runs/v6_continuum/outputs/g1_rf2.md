# Continuum: SRAM-byte chiplet dataflow on organic packages

**Target and metrics.** The target is LLM inference serving. Two numbers define "best", and they only count together: $/Mtok and tok/s/user, read as a Pareto frontier.

- GB300 NVL72 is reported at about $0.06/Mtok at about 50 tok/s/user.
- Cerebras and Groq reach 300 to 2,500 tok/s/user, but no $/Mtok is sourced for them.
- Continuum aims at **500 to 1,500 tok/s/user at GB300-class $/Mtok**, for contexts of 8k tokens or less.
- Only Archetype C (SRAM-resident serving) leaves room for a 3x gain: silicon is 60% of its cost, so the ceiling is 16.7x.
- Continuum loses on long context (32k and above) and on training, where GB300 and TPUs remain better.

**Facts vs. my assumptions** ([bg] marks background knowledge that I have not verified):
- Fact [bg]: the SRAM bitcell shrank only about 20% from N7 to N3, while wafer price roughly doubled (about $10k to $20k).
- Assumption: about 2 MB/mm² of usable SRAM on N6.
- Assumption: about 70 mJ per token for a 70B model.
- Assumption: system bill of materials about $60k.

## Candidates

| # | Candidate | P |
|---|---|---|
| 1 | Bigger HBM4 GPU on CoWoS-L | 0.45 |
| 2 | Decode-only chip with right-sized compute and HBM | 0.15 |
| 3 | Wafer-scale SRAM with external weight streaming | 0.20 |
| 4 | FP4/FP3 numerics push | 0.25 |
| 5 | SRAM chiplets on N6 with organic package and pipeline dataflow | 0.07 |
| 6 | SRAM-resident MoE expert farm on N6 chiplets | 0.05 |
| 7 | Package schedules compiled from per-die test data, with spare dies | 0.03 |
| 8 | EMIB-T HBM packages outside the CoWoS pool | 0.09 |

## Arithmetic check for candidate 5

**Capacity**
- 70B FP8 weights: 70 GB.
- KV cache for a 70B model with GQA: 80 layers × 8 heads × 128 dims × 2 ≈ 160 KB/token. At 8k context that is 1.3 GB per sequence.
- 32 concurrent sequences need about 42 GB of KV.
- Total: about 112 GB of SRAM, which is about 56,000 mm² at 2 MB/mm². With logic added, that is about 1.2 N6 wafers, or about $15k of silicon.

**Throughput and cost**
- 32 sequences × 1,000 tok/s = 32k tok/s, or about 115 Mtok/hr.
- At about $8/hr all-in, that gives **$0.07/Mtok**.

**Power**
- 70 mJ/token × 32k tok/s ≈ 2.3 kW, spread across 16 packages of about 250 W each. These can be air-cooled.

**Links**
- Activations crossing a pipeline stage are about 8 KB/token per layer. Organic UCIe links handle that easily; weights never leave their die.

## Falsification plan

Before any tape-out, build two things:
1. A cycle-level simulation of the 70B model on 16 packages, using measured organic-link latency.
2. A cost model.

Kill the design if either result appears:
- fewer than 600 tok/s/user at 32 concurrent sequences, or
- more than $0.15/Mtok.

Software: the PyTorch/XLA graph goes to an ahead-of-time scheduler. Existing checkpoints run unchanged.

=== IDEAS ===
IDEA 1
NAME: N6 SRAM-chiplet pipeline packages
MECHANISM: Weights and KV cache live in about 112 GB of SRAM spread over many dies of about 100 mm² on N6. That node is chosen because SRAM stopped shrinking, so SRAM bytes cost about half as much there as on N3. Thirty-two dies sit on each organic package, and 16 packages hold one 70B model. A compiler pipelines the layers so that only about 8 KB of activations per token crosses the organic links. Closest earlier attempt is the Groq LPU, where 576 chips on 14 nm cards made capacity cost too high. Here SRAM is bought at roughly $0.1/MB on dense, cheap packages instead. The deciding quantity is delivered system cost per GB of SRAM, which must stay at or below about $1.5k/GB.
VALUE: It serves a 70B model at about 1,000 tok/s/user for about $0.07/Mtok, which is GB300's cost at 20x the speed, using no HBM and no CoWoS.

IDEA 2
NAME: SRAM-resident MoE expert farm
MECHANISM: All experts of a model with about 230B total and 10B active parameters stay resident in about 300 GB of N6 SRAM chiplets, roughly 2.5 to 3 wafers. A deterministic all-to-all over organic links moves only a few tens of KB per token per layer. The compiler replicates hot experts based on measured routing statistics. Closest earlier attempt is Cerebras streaming weights from MemoryX, which was bandwidth-bound off-wafer. Here nothing streams. The deciding quantity is the capacity needed to replicate hot experts, which must stay under 30%.
VALUE: It runs frontier MoE models at more than 500 tok/s/user near GB300's $/Mtok.

IDEA 3
NAME: Test-data-compiled spare-die packages
MECHANISM: Each package of 32 dies carries 4 spare dies. After assembly, each die's measured Fmax, minimum Vdd and defects are fed to the scheduler. The scheduler compiles a per-package timing-exact schedule that maps around bad dies and runs every die at its own voltage with no guard band. Closest earlier attempt is Cerebras' fixed row redundancy, which needs a whole wafer and does not adapt per die. The deciding quantity is the post-assembly die and bond failure rate, which must stay below 4 per 36.
VALUE: Large organic multi-die packages reach near-100% package yield and save about 15 to 25% power without CoWoS.