=== TRIAGE ===
IDEA 1 | I 6 | P 4 | DECIDES: yielded hybrid-bonded SRAM $/GB (≲$250 vs HBM ~$24) | 4.8 GB per tile is dense but plausible at N5, and it says where KV lives (LPDDR). Inference cost ceiling is thin (A: NO ROOM), so the win is tok/J and tok/kW, not $/token.
IDEA 2 | I 5 | P 5 | DECIDES: base-die TSV pJ/B vs PHY+interposer path | Exact, one-op answer to PIM's programmability failure. Saves energy, but "2× bandwidth" is doubtful because TSV rate ≈ channel rate. Still needs HBM and CoWoS.
IDEA 3 | I 6 | P 4 | DECIDES: delivered pJ/bit at 1 W/mm² without throttling | The 53→9 mJ figure follows from 3→0.5 pJ/bit. 16 GB per die is conservative for DRAM density. Thermal and compound wafer yield are unproven.
IDEA 4 | I 6 | P 4 | DECIDES: KV GB/s per user (110) vs ~2 TB/s per HBM4 stack | The arithmetic checks out (192×36 GB, 384 TB/s, 3,500 users). It never says how about 3.5 GB of SRAM fits on each package, and it still uses CoWoS.
IDEA 5 | I 3 | P 5 | DECIDES: CPO $/Tb/s and FIT vs copper | 144 W per chip is consistent. A 1.1–1.2× gain is honest but small (B network term 1.13×).
IDEA 6 | I 5 | P 4 | DECIDES: end-to-end pJ/bit ≤2.5 with DRAM refresh above 90 °C | Same idea as 3 with a modest 1.5 pJ/bit target. It has the clearest falsifier of this group.
IDEA 7 | I 5 | P 5 | DECIDES: KV share of decode bytes ≥60% at ≥32K | Duplicates 2. The ~8 FLOP/B GQA intensity check is sound.
IDEA 8 | I 3 | P 5 | DECIDES: batched expert intensity ≥~900 FLOP/B | Works only for prefill. A 1.7× BOM cut gives little delivered gain because the silicon/HBM term is 1.08× in A.
IDEA 9 | I 5 | P 3 | DECIDES: LPDDR $/(TB/s) vs HBM | Logic-bearing LPDDR is not a commodity part. The plan wins on capacity, but per-module bandwidth is weak.
IDEA 10 | I 5 | P 5 | DECIDES: DRAM-core share of access energy ≤40% | Duplicates 2 and 7. It openly states the MLA exclusion.
IDEA 11 | I 3 | P 5 | DECIDES: DiLoCo extra-token penalty <10% beyond 70B | An honest 1.15–1.2× that targets a 1.13× term. The ideas are algorithmic rather than chip design.
IDEA 12 | I 4 | P 5 | DECIDES: 70B/1T-token FP4 loss within 1% of FP8 | Cheap to falsify on today's GPUs. The optics add nothing essential.
IDEA 13 | I 5 | P 4 | DECIDES: achieved FLOP per off-chip byte ≥~4,000 at production microbatch | The "d/1.4" derivation is wrong. Intensity scales with microbatch tokens, not d, because weights do not fit in 256 MB. Removing HBM/CoWoS attacks D's 1.68× term.
IDEA 14 | I 5 | P 4 | DECIDES: good-die stacked SRAM ≤$250/GB | It has no headroom: 336 GB holds exactly 335 GB, leaving none for replicating hot experts. KV placement is unstated. N3 is a poor node for SRAM. Weaker than 1.
IDEA 15 | I 6 | P 4 | DECIDES: retention and refresh overhead at logic hotspot temperature | 70 GB over three to four DRAM layers is density-plausible. The 1.7× per-token claim is honest. Wafer-on-wafer yield is the hidden risk.

Run first: 15/3/6 (one thermal test chip), 1 vs 14 (SRAM $/GB), 12 (FP4 simulation). Merge 2/7/10.