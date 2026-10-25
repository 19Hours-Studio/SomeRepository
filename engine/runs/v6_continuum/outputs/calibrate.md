=== CALIBRATION ===

P | 1 | 34% | The most complete and physically argued architecture, with no FATAL in either review. Its headline 2.2–2.7× tokens/kW, however, applies to GQA models, while its own named 1T/32B target class is MLA (only 1.08–1.29×). It also loses at 100 tok/s/user (0.65×) and gives no cost figure.

P | 2 | 24% | Highest tournament score, honest about where it loses, and its numbers reproduce. But it is sized only for 32 users at 8K, its 1 µs 32-die all-reduce is unsourced, and it costs 2–4× more per token than GB300 bulk serving.

P | 3 | 8% | An unanswered FATAL: the 2.8× capex gain compares a part priced at cost with a street price carrying about 75% margin. At equal margin the gain is about 1.0–1.3×.

P | 4 | 3% | Two unanswered FATALs. Its SRAM density exceeds any measured die and leaves no room for logic. Its "$0.07/Mtok, 20× speed" claim is contradicted by Idea 2's repaired version of the same design.

P | none | 31% | Every survivor's whole-chain ratio is about 1.0–1.5×, and none credibly earns "best in the world." Closely related designs already exist (d-Matrix Raptor, Groq 3 LPX), so a better answer could still be written.

WEAKEST LINK: Idea 1 assumes 160 GB at 64 TB/s and ≤1 pJ/bit of hybrid-bonded DRAM sitting under ~1–1.5 W/mm² logic. That is about 2–5× the capacity of any shown part. It also needs the DRAM to stay cool enough to avoid heavy refresh or throttling, which imec measured at 141.7 °C unmitigated.

FLIP TEST: A measured logic-on-DRAM stack, or a validated thermal and electrical simulation, run at full logic power. | The ranking flips if it shows any of these:
- under ~20 GB per stack;
- under ~8 TB/s per stack at ≤95 °C;
- refresh or frequency throttling that cuts usable bandwidth or FP8 by more than ~40%.

Any one of these pulls Idea 1's GQA gain below ~1.4×. Idea 2, or "none", would then lead.

UNKNOWN: Even if Idea 1 is right, it may not be best on cost per token. Composite wafer-on-wafer yield is about 34%, package capex is unknown, and energy is only about 10% of TCO. It is also unclear whether frontier models will stay GQA (where Continuum wins) or move to MLA (where it barely wins).