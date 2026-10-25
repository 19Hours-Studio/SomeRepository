# Integrated answer (synthesis of Parts 1–3)

Model: `combine.py` in this folder (python3, run 2026-10-25). Inputs are the facts ledger, the blind-review corrections and stated assumptions marked in the code.

=== IDEAS ===
IDEA 1
NAME: Gated diesel bridge plus pooled spares
MECHANISM: (1) Norilsk, starting now: a single spares registry for the Western-built underground fleet. Spares are pooled across 6 mines and ranked by Ni-eq lost per machine-hour (6.3 t on rich ore against 1.2 t on Norilsk-1). Domestic reverse-engineering and casting start with the worst part families. The programme ends as the BelAZ/MoAZ JV fleet (Sosnovoborsk, about 150 machines/yr) replaces those machines. The corrected effect is +8 to +29 kt Ni-eq/yr (central +15 kt) at about $5.4k per added tonne. (2) Baimskaya, decided at a gate in Q4 2027: if the first two RITM-200S floating units are not at mooring trials by then, they cannot power line 1 when it is ready in Q1 2029. In that case Baimskaya leases about 80 MW of domestic gensets and runs line 1 at about 65 MW average. Each such genset fleet is roughly 6 Kolomna plants or UDMZ 1.5–2.5 MW units. That gives 12.2 Mt/y of ore (not 15), 48 kt Cu and 77 koz Au a year, on 146 kt/y of diesel at 0.225 kg/kWh, and about $0.31/kWh. Diesel arrives from Far East refineries through the Bering Strait in 7–8 tanker calls into Pevek. That route avoids the Kara Sea icebreakers that Part 2 needs. It is held in about 173k m³ of tankage costing about $173m, built on cooled piles to bedrock with full secondary containment, which is the Ambarnaya lesson. Concentrate (about 222 kt wet a year, 5–6 ships of 40 kt) is stockpiled at Nagleynyn for the 3–4 month shipping season. The gensets leave when the units arrive. (3) Oil and gas: no change. Both Part 2 ideas only reproduce current practice: Vankor oil south through Vankor–Purpe, Payakha north as far as the hulls allow, and Yamal LNG's Kildin STS plus summer cargoes east.
VALUE: Copper: the expected value is +$185m (+$66m at $8k Cu/$2.8k Au), and the bridge breaks even if the floating units slip 0.44 years. Life-of-mine full cost is 0.98× the no-bridge case for a 1-year slip and 0.955× for 2 years. First metal is expected 1.05 years earlier, with a 35% chance that it is not earlier at all. Nickel-equivalent: group full cost goes from about $10.05k to $9.97k/t Ni-eq (−0.85%, range −0.1 to −2.5%) within 6–18 months, and the gain fades over about 3–5 years. LNG and oil: 1.00× current practice.

IDEA 2 (alternative: when the all-season road is late)
NAME: Half bridge on the winter road
MECHANISM: Same Q4 2027 gate, but with 40 MW average. That gives 7.5 Mt/y of ore, 30 kt Cu, 48 koz Au and 90 kt/y of diesel, using 106k m³ of tankage at about $106m. About 6,600 road loads a year, roughly 51 a day over a 130-day winter road, is a quarter below the TCWR record daily rate (about 158 a day). So it does not depend on the 800 km Baimskaya–Nagleynyn all-season road, which was only 250 km built at last report. Line 1 is commissioned and run in on diesel. Norilsk and oil and gas are as in IDEA 1.
VALUE: Expected value is +$102m (+$29m at low prices), with break-even at 0.50 years of slip. Net cash cost is $2.0k/t Cu at base prices and $3.0k/t at low prices. The life-of-mine cost gain is about half that of IDEA 1. It is the version that can still be done if the road slips along with the floating units.

## NOTES

**Parts used.**
- Part 1 Idea 1 (no FATAL defect): used, with all four MAJOR defects fixed.
  - Fuel rate set to 0.225 kg/kWh. This gives 146 kt/y of fuel at 65 MW average, or 180 kt at 80 MW.
  - Throughput cut from 15 to 12.2 Mt/y.
  - Separate loads at 38 t: 10,800 a year, including consumables and mine-fleet diesel.
  - Recovery 83.6% (design 87.6% minus 4 points). Head grade 0.476%, derived from the PFS figure of 250 kt Cu at 60 Mt/y, instead of the unsourced 0.51%.
  - The bridge window becomes a gate decision with a probability-weighted slip, rather than an assumption.
- Part 3 Idea 1 (no FATAL defect): used at the corrected size.
  - Pooled service level is about 95%, not 99.5%.
  - Mines are the limit 30–60% of the time.
  - Change-out downtime is counted.
  - The gain fades as the BelAZ JV fleet replaces the Western machines.
  - The 9-month lead time, the 7-point availability gain and the Talnakh hoisting and backfill ceiling are unmeasured; they are carried as risks.
- Left out:
  - Part 1 Idea 2: FATAL. Kekura already has its own mill and grid power. The fix (a mill-less satellite under a 0.4 Mt/y cap) leaves a ratio of about 0.95 at best, and the sorter loses more value than it saves.
  - Part 3 Idea 2: FATAL. It describes current Nornickel practice; ratio 1.00.
  - Part 2 Ideas 1 and 2: no FATAL defect, but both rate 1.00 against current practice. Idea 2's direct-only Arctic LNG 2 shipping delivers about 40% less than 2026 practice (1.96 against about 3.2 Mt/y).

**How they combine.** The Baimskaya and Norilsk pieces share no plant, port or capital, so their gains are reported per product and not added together. The shared resources are:
- **Icebreakers:** the bridge adds about 13 eastern-sector calls a year (7–8 tankers plus 5–6 concentrate ships), mostly in open water from July to October and supplied from the east. That leaves the four 22220s on the Ob Gulf, the Yenisei and Dudinka. Chukotka (2027) covers late-season Pevek calls.
- **Northern-delivery capacity:** this is a real conflict. The bridge's diesel equals 0.92× Chukotka's entire 2025 seaborne northern delivery (159.2 kt). Its tanker calls must be booked with Rosatom Arktika, the single operator, alongside community supply. This is a stated risk.
- **Port:** 222 kt/y of concentrate is 12% of Nagleynyn's 1.842 Mt/y design. 148 kt of seasonal stockpile is well under Red Dog's 950 kt store.
- **People:** about 400–600 drivers plus 60–80 genset crew at Chukotka's 100% northern allowance. This is in the haul cost of $0.18/t-km.

**Order.** Norilsk spares in 2027 (fastest, no gate). Baimskaya gate in Q4 2027, because tankage has to be built in the summer-2028 season. Fuel arrives in the 2028 navigation, and line 1 starts in Q1 2029 on whichever power source is ready.

**Combined numbers (basis: `combine.py`).**

| | Value |
|---|---|
| Baimskaya bridge, 65 MW, base prices Cu $9.5k / Au $3.5k | 12.2 Mt/y ore, 48.5 kt Cu, 77 koz Au |
| Net cash cost | $2.0k/t Cu ($3.0k at low prices) |
| Margin | $303m/y ($190m/y at low prices) |
| Bridge-specific outlay | $134m (tankage at $1,000/m³ with 40% later reuse, plus $30m genset mobilisation) |
| Slip distribution (assumed) | 0 / 1 / 2 / 3 years at 0.35 / 0.35 / 0.20 / 0.10 |
| Expected value | +$185m |
| Levelised full cost | $8.88k → $8.73k/t Cu (1-year slip), $9.79k → $9.35k/t Cu (2-year slip), net of the Au credit, at 12% discount, including the $8bn capex |
| Norilsk group full cost | $10.05k/t Ni-eq: cash opex $5.1bn plus capex $3.0bn as a proxy for the capital charge, over 806 kt |
| Norilsk effect | −0.85% central |

Effectiveness:
- Baimskaya: recovery is −4 points while the bridge runs. Days worked per year are unchanged. Infrastructure life depends on the tank-farm foundation design.
- Norilsk: LHD availability +3.5 to +7 points. Recovery and structure life are unchanged.

**Benchmarks.** For years from decision to first output, Kupol, Meliadine and Natalka took about 2.5–4 years. Baimskaya, with its BFS in 2021 and line 1 in 2029, takes about 7.5 years; the bridge removes only the power-driven part of that delay. Raglan and Diavik offset only about 10% of their diesel with wind, so diesel at $0.28–0.34/kWh is the cold-region norm, not a penalty. The Norilsk comparison is current practice, the Talnakh expansion at $7.3–8.1k per added tonne of capacity, but that buys 20 or more years of capacity, while the spares gain lasts 3–5 years.

**Which part carries the value.** Part 1 does: Baimskaya, at about $185m expected and up to about $0.6bn over a 2-year slip. Part 3 adds roughly $80m/y at most. Part 2 adds nothing. Its honest output is a constraint: oil and gas output is set by hull numbers. There is one Arc6 hull at Bukhta Sever, and Russian-built Arc7s for Arctic LNG 2 arrive at about 1–2 a year. No change to shipping, product form or field order beats current practice within the legal limits.

**Deciding unknown and its cheapest test.** The decisive unknown is the date the first two floating units energise at Nagleynyn, compared with line 1's Q1 2029 readiness. RAEX (Apr 2026) puts the plant start at Q1 2029 for line 1 and Q1 2030 for line 2; the Chukotka governor says 2 units in 2028 and 2 more by 2030. If the slip is under 0.44 years, the bridge loses money. The cheapest test is a free schedule check in mid-2027: are FPU-1 and FPU-2 at Baltiysky Zavod at mooring trials with fuel loaded? Akademik Lomonosov took about 1.3 years from fuel loading to first power plus a summer tow. If they are not, the bridge pays at better than 2:1 odds. The second decider is the all-season road; it decides between IDEA 1 and IDEA 2.

**Main risks.**
- Genset supply: domestic output of large units is small. Chinese units (Weichai, Jichai) are not restricted, but carry secondary-sanction withdrawal risk, as in the Wison case.
- Domestic spare parts may last less than 0.6–0.8× as long as the originals.
- Arctic tank-farm cost is assumed at $1,000/m³.
- Payability and freight terms for concentrate going to China.
- The Talnakh hoisting ceiling may stop extra LHD hours becoming extra ore.

Sources checked this session: [RAEX 24.04.2026](https://raexpert.ru/releases/2026/apr24a), [eastrussia: all-season road](https://www.eastrussia.ru/news/vsesezonnuyu-dorogu-ot-baimskogo-goka-postroyat-na-chukotke/), [eastrussia: ice roads](https://www.eastrussia.ru/news/ledovye-dorogi-dlya-gdk-baimskaya-postroyat-na-chukotke/), [Mining Weekly 2020](https://www.miningweekly.com/article/russia-infrastructure-plans-raise-risk-for-baimskaya-copper-project-kaz-2020-11-18).
