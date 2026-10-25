# Continuum: 3D hybrid-bonded memory on logic

**Targets and metrics.** The target is data-center batch-1 to batch-8 decode on 70B to 1T-parameter models. The metrics are tok/s per user and cost per Mtok. I chose the SRAM-dataflow archetype because it is the only one with room: its ceiling is 16.7x, and silicon is 60% of its cost. Energy is about 10% of TCO, so tokens per joule is secondary.

## Candidate answers

| # | Candidate | P |
|---|---|---|
| 1 | Custom HBM4 base die carrying logic | 0.5 |
| 2 | SRAM stacked on compute, V-Cache style | 0.6 |
| 3 | Generic DRAM-on-logic stack with a mesh NoC | 0.3 |
| 4 | Bigger SRAM wafer | 0.3 |
| 5 | DRAM bank directly above each MAC tile | 0.2 |
| 6 | Stacked weight DRAM that is refreshed by being read | 0.05 |
| 7 | Full DRAM wafer bonded onto a wafer-scale compute wafer | 0.08 |
| 8 | Inverted stack: compute against the cold plate, power fed up through the DRAM | 0.08 |

Candidates 1 to 5 share one paradigm: put more memory closer to the same thermal stack-up.

## Established facts and my estimates

**Facts (from CONTEXT):**
- Cerebras WSE-3: 44 GB SRAM on 46,225 mm².
- Groq needed 576 chips for 70B.
- Rubin: about 22 TB/s, which bounds 70 GB at batch 1 to about 300 tok/s.

**My estimates (unverified):**
- DRAM density is about 0.3 Gb/mm² per layer, extrapolated from 16 to 24 Gb DDR5 dies of about 70 mm².
- That is about 10x SRAM's roughly 4 MB/mm², on a wafer that costs roughly 1/3 as much. So capacity costs about 30x less per byte.
- Bonding at 3 µm pitch gives about 100k bonds/mm²; at 1 Gb/s per bond that is ≥1 TB/s/mm².

**Sanity check.** Take an 800 mm² die with 4 DRAM layers. It holds about 120 GB. If the DRAM banks limit it to about 100 TB/s, a 70 GB FP8 model at batch 1 runs at about 1,400 tok/s/user on one chip. Groq needed 576 chips for this model size.

- **Win:** cost per byte of SRAM-class bandwidth.
- **Lose:** prefill FLOPs per mm² are the same as a GPU's, because the compute die is unchanged.

**Software.** The compiler is a dataflow compiler that places each layer's weights in the DRAM banks above that layer's tiles. Models enter through PyTorch/XLA graph capture, so existing models run unmodified.

## Falsification test

A thermal test chip with 1β DRAM bonded on an N3 heater, run at 1.0 W/mm². Measure two things:
- The distribution of worst-case cell retention.
- The bond bit-error rate at operating temperature.

=== IDEAS ===
IDEA 1
NAME: Read-refreshed stacked weight DRAM
MECHANISM: Commodity-density DRAM layers are hybrid-bonded over an N3 compute die and hold only the model weights. Every decode token streams all weights in about 1 ms, and each read restores the cell. That makes refresh unnecessary even at about 105 °C, where cells lose charge too fast for normal refresh. The closest earlier attempts are HBM-PIM and AiM, which were stopped by DRAM-process logic. Here the logic stays on a logic wafer. The deciding quantity is worst-cell retention at junction temperature versus the weight sweep period. Idle chips fall back to normal refresh.
VALUE: About 120 GB at about 100 TB/s on one die, so a 70B model decodes at more than 1,000 tok/s/user without a 576-chip SRAM farm.

IDEA 2
NAME: DRAM-wafer on wafer-scale engine
MECHANISM: A full DRAM wafer is bonded wafer-on-wafer onto a wafer-scale dataflow compute wafer. Each layer adds about 1.7 TB, against 44 GB of SRAM on Cerebras WSE-3. Defects are repaired through DRAM row and column redundancy plus spare compute tiles. The closest earlier attempt is Cerebras, which was stopped by capacity and needed external MemoryX streaming. The estimated power density of about 0.5 W/mm² is gentle enough for DRAM. The deciding quantity is the yield of the bonded stack after repair.
VALUE: A trillion-parameter FP8 model resident on one wafer at PB/s-class bandwidth, cutting the dominant 60% silicon cost.

IDEA 3
NAME: Inverted stack, power through DRAM
MECHANISM: The compute die is flipped so it faces the cold plate. Four DRAM layers sit beneath it, and power is fed up through roughly 100 Cu TSVs/mm², which take less than 1% of the DRAM area. The DRAM then stays near 60 °C even with the logic at 1.5 W/mm². The closest earlier attempt is AMD 3D V-Cache, which was stopped by heat trapped under the cache and by SRAM-only capacity. The deciding quantity is the thermal resistance from DRAM to coolant through the logic die.
VALUE: Data-center-power compute with 100 GB-class bonded DRAM and no HBM, CoWoS interposer or PHY.