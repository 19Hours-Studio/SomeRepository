=== TRIAGE ===
IDEA 1 | I 4 | P 2 | DECIDES: achieved FLOP/byte ≥2,000 on attention and collectives | Repeats Dojo/Graphcore; 2 TB/s LPDDR starves optimizer and checkpoint traffic.
IDEA 2 | I 5 | P 5 | DECIDES: accuracy loss at ~2 bits/weight | 0.1 pJ decode is easy; whether 2-bit trellis holds on frontier models is the real test.
IDEA 3 | I 6 | P 3 | DECIDES: DRAM junction temperature over hot N3 logic | Retention vs a 1 ms sweep is fine; heat and row-activation energy are the real limits.
IDEA 4 | I 6 | P 6 | DECIDES: SRAM bond energy ≤0.12 pJ/bit at ~210 TB/s/die | Uses existing SoIC; modest 1.1–1.6× gain is credible and ~10–15% capex offsets part of it.
IDEA 5 | I 5 | P 5 | DECIDES: accuracy retained at 128K | MLA shows latents work; 3–4-bit plus outliers at long context is unproven.
IDEA 6 | I 6 | P 5 | DECIDES: gather efficiency ≥80% of HBM peak at 324 B | Win depends on sparse-attention models and on HBM row-activation overhead.
IDEA 7 | I 4 | P 3 | DECIDES: residual bits/weight ≤1.5 | Experts are trained to diverge, so a shared base is likely a poor predictor.
IDEA 8 | I 6 | P 7 | DECIDES: tokens/kW vs Rubin+CPX (~2× claimed) | Honest scoping; it adds system value without new physics.
IDEA 9 | I 3 | P 3 | DECIDES: all-to-all latency after OCS retune | Routing changes per token, and ms-scale OCS can't track it.
IDEA 10 | I 6 | P 3 | DECIDES: DRAM-to-coolant thermal resistance (DRAM ≤95 °C) | The 60 °C claim is doubtful; ~2.7 kA through DRAM TSVs is hard.
IDEA 11 | I 4 | P 8 | DECIDES: RULER-128K loss ≤1 point vs BF16 | Necessary enabler that is mostly proven, but it does not differentiate.
IDEA 12 | I 7 | P 2 | DECIDES: bonded-wafer yield after repair | Wafer-on-wafer compounding of DRAM and logic defects is untested at this scale.
IDEA 13 | I 4 | P 8 | DECIDES: measured prefill:decode mix utilization | Sensible cost hedge; parity, not best.
IDEA 14 | I 5 | P 4 | DECIDES: hit rate ≥85% at adequate lead time | 2 TB/s LPDDR still caps per-user speed for 32B-active models.
IDEA 15 | I 5 | P 4 | DECIDES: SRAM reuse ≥6 / $ per GB/s | 256 tok/s is not SRAM-class latency; 24 LPDDR packages per die is a routing burden.
IDEA 16 | I 5 | P 3 | DECIDES: p99 per-hop latency ≤12.5 µs/layer | Rests on co-packaged optics, which has not reached volume.
IDEA 17 | I 3 | P 4 | DECIDES: die/bond failures <4 per 36 | No-guard-band voltage risks aging failures; it saves little cost share.
IDEA 18 | I 6 | P 5 | DECIDES: system cost ≤$1.5k/GB SRAM | It beats Groq's 14 nm capacity cost; Archetype C has room, and organic-link power is the open question.
IDEA 19 | I 8 | P 4 | DECIDES: stacked DRAM ≤1 pJ/bit at 64 TB/s under 2 kW logic | Biggest upside; DRAM thermals and custom-DRAM supply are unproven.
IDEA 20 | I 5 | P 5 | DECIDES: hot-expert replication ≤30% capacity | SRAM cost scales with total parameters; it only helps mid-size MoE.
IDEA 21 | I 5 | P 4 | DECIDES: attention-node bandwidth/$ vs HBM | It moves the KV problem elsewhere; optics adds latency risk.
IDEA 22 | I 6 | P 4 | DECIDES: all-to-all ≤1.5 µs with dynamic MoE routing | Capacity padding and static schedules may erase the gain.
IDEA 23 | I 6 | P 5 | DECIDES: random 324 B fetch efficiency on stacked DRAM | Needed to keep the MLA lead; it overlaps Idea 6 and depends on DSA adoption.