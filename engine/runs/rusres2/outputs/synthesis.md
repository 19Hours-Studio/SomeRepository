=== IDEAS ===
IDEA 1
NAME: Gated diesel bridge plus pooled spares
MECHANISM: (1) Norilsk, starting now: build one spares registry for the Western-built underground fleet. Spares are pooled across 6 mines and ranked by Ni-eq lost per machine-hour (6.3 t on rich ore, 1.2 t on Norilsk-1). Domestic reverse-engineering and casting start with the worst part families. The programme winds down as the BelAZ/MoAZ JV fleet (Sosnovoborsk, about 150 machines/yr) replaces those machines. The corrected effect is +8 to +29 kt Ni-eq/yr (central +15 kt) at about $5.4k per added tonne. (2) Baimskaya, decided at a gate in Q4 2027: if the first two RITM-200S floating units are not at mooring trials by then, they cannot power line 1 when it is ready in Q1 2029 (RAEX, Apr 2026). In that case Baimskaya leases about 80 MW of domestic gensets (Kolomna or UDMZ 1.5–2.5 MW units) and runs line 1 at about 65 MW average. That gives 12.2 Mt/y of ore (not 15), 48 kt Cu and 77 koz Au a year. It burns 146 kt/y of diesel at 0.225 kg/kWh, which costs about $0.31/kWh. Diesel comes from Far East refineries through the Bering Strait in 7–8 tanker calls into Pevek. That route keeps clear of the Kara Sea icebreakers Part 2 needs. The fuel is held in about 173k m³ of tankage (about $173m), built on cooled piles to bedrock with full secondary containment, which is the Ambarnaya lesson. Concentrate (222 kt wet a year, 5–6 ships of 40 kt) is stockpiled at Nagleynyn for the 3–4 month shipping season. The gensets leave when the floating units arrive. (3) Oil and gas: no change. Both Part 2 ideas only reproduce current practice: Vankor oil goes south on Vankor–Purpe, Payakha oil goes north as far as the hulls allow, and Yamal LNG uses Kildin ship-to-ship transfer plus summer cargoes east.
VALUE: Copper: expected value is +$185m (+$66m at $8k Cu / $2.8k Au), and the bridge breaks even if the floating units slip 0.44 years. Life-of-mine full cost is 0.98× the no-bridge case for a 1-year slip and 0.955× for a 2-year slip. First metal comes 1.05 years earlier on expectation, with a 35% chance of no gain. Nickel-equivalent: group full cost goes from about $10.05k to $9.97k/t Ni-eq (−0.85%, range −0.1% to −2.5%) within 6–18 months, and the gain fades over 3–5 years. LNG and oil: 1.00× current practice.

IDEA 2 (alternative, if the all-season road is late)
NAME: Half bridge on the winter road
MECHANISM: Same Q4 2027 gate, but at 40 MW average: 7.5 Mt/y of ore, 30 kt Cu, 48 koz Au, 90 kt/y of diesel and about 106k m³ of tankage (about $106m). That needs about 6,600 road loads a year, or about 51 a day on a 130-day winter road. That is about a third of the record daily rate on Canada's Tibbitt–Contwoyto winter road (about 158 a day). So it does not depend on the 800 km Baimskaya–Nagleynyn all-season road, of which only 250 km was built at last report. Line 1 is commissioned and run in on diesel. Norilsk and oil and gas are handled as in IDEA 1.
VALUE: Expected value is +$102m (+$29m at low prices), with break-even at 0.50 years of slip. Net cash cost is $2.0k/t Cu at base prices and $3.0k/t at low prices. The life-of-mine cost gain is about half of IDEA 1's, but this version still works if the road slips along with the floating units.

**NOTES**

- **Parts used.**
  - **Part 1 Idea 1** (no FATAL defect), with all four MAJOR defects fixed:
    - Fuel rate set to 0.225 kg/kWh, giving 146 kt/y of fuel.
    - Throughput cut from 15 to 12.2 Mt/y.
    - Fuel, concentrate and consumables counted as separate loads: 10,800 a year at 38 t each.
    - Recovery set at 83.6% (design 87.6% minus 4 points). Head grade 0.476%, taken from the pre-feasibility study (250 kt Cu at 60 Mt/y), replaces the unsourced 0.51%.
    - The uncertain bridge window becomes a gate decision with a probability-weighted slip.
  - **Part 3 Idea 1** (no FATAL defect), at its corrected size:
    - Pooled service level is about 95%, not 99.5%.
    - Mines are the limit 30–60% of the time.
    - Change-out downtime is counted.
    - The gain fades as the BelAZ JV fleet arrives.
    - The lead time, the +7-point availability gain and the Talnakh hoisting ceiling are unmeasured, so they are carried as risks.
- **Left out.**
  - Part 1 Idea 2: FATAL, because Kekura already has its own mill and grid power. Even the repaired version scores about 0.95 at best, and the sorter loses more than it saves.
  - Part 3 Idea 2: FATAL, because it describes what Nornickel already does (score 1.00).
  - Part 2 Ideas 1 and 2: no FATAL defect, but both score 1.00 against current practice. Shipping Arctic LNG 2 only direct would deliver 1.96 Mt/y, against about 3.2 Mt/y in 2026.
- **How the parts combine.** Baimskaya and Norilsk share no plant, port or capital, so their gains are reported per product and not added together.
  - **Icebreakers:** the bridge adds about 13 eastern-sector calls a year, mostly in open water from July to October and supplied from the east. The four 22220s stay on the Ob Gulf, Yenisei and Dudinka, and Chukotka (2027) covers late-season calls.
  - **Northern delivery (a real conflict):** the bridge needs 0.92× Chukotka's entire 2025 seaborne northern delivery (159.2 kt). Those calls must be booked with Rosatom Arktika, the single sea operator, alongside supply to the towns.
  - **Port:** 222 kt/y is 12% of Nagleynyn's 1.842 Mt/y design. The 148 kt seasonal stockpile is far below Red Dog's 950 kt store.
  - **People:** about 400–600 drivers and 60–80 genset crew at Chukotka's 100% northern allowance.
  - **Order:** Norilsk spares in 2027. The Baimskaya gate comes in Q4 2027, because the tankage must be built in the summer-2028 season and fuel delivered in the 2028 navigation. Line 1 starts in Q1 2029 on whichever power source is ready.
- **Combined numbers** (from `combine.py`):
  - **Slip distribution (assumed):** 0, 1, 2 or 3 years with probabilities 0.35, 0.35, 0.20 and 0.10.
  - **Bridge at 65 MW:** margin is $303m/y ($190m/y at low prices). Upfront outlay is $134m: tankage at $1,000/m³ (assumed), 40% of it reused later, plus $30m to bring in the gensets.
  - **Levelised full cost** (net of gold credit, 12% discount, including the $8bn capex): $8.88k → $8.73k/t Cu for a 1-year slip, and $9.79k → $9.35k/t Cu for a 2-year slip.
  - **Norilsk:** full cost is $10.05k/t Ni-eq, taken as cash opex $5.1bn plus capex $3.0bn (as a proxy for the capital charge) over 806 kt.
  - **Effectiveness:** at Baimskaya, recovery is 4 points lower while the bridge runs, days worked are unchanged, and tank-farm life rests on the foundation design. At Norilsk, LHD availability rises 3.5–7 points; recovery and structure life are unchanged.
  - **Benchmarks, years from decision to first output:** Kupol, Meliadine and Natalka took about 2.5–4 years. Baimskaya takes about 7.5 years (bankable feasibility study 2021, line 1 in 2029), and the bridge removes only the delay caused by power.
  - **Benchmarks, power and capacity:** Raglan and Diavik offset only about 10% of their diesel with wind, so diesel power is normal practice in cold regions. Talnakh expansion at $7.3–8.1k per added tonne buys capacity for 20 years or more; the spares gain lasts 3–5 years.
- **Which part carries the value:** Part 1, at about +$185m expected and up to about $0.6bn over a 2-year slip. Part 3 adds at most about $80m/y. Part 2 adds nothing: oil and gas output is limited by hulls (one Arc6 at Bukhta Sever, and Russian-built Arc7s arriving at about 1–2 a year).
- **Deciding unknown and its test:** the deciding unknown is when the first two floating units start delivering power at Nagleynyn, compared with line 1 being ready in Q1 2029. The Chukotka governor says 2 units in 2028. Below 0.44 years of slip the bridge loses money. The cheapest test costs nothing: in mid-2027, check whether floating units 1 and 2 are at mooring trials with fuel loaded at Baltiysky Zavod. Akademik Lomonosov took about 1.3 years from fuel loading to first power, plus a summer tow. Whether the all-season road is open decides between IDEA 1 and IDEA 2.
- **Main risks:**
  - Genset supply. Chinese units (Weichai, Jichai) are not restricted, but suppliers could pull out over secondary-sanction risk, as Wison did.
  - Domestic spare parts may last less than 0.6–0.8× as long as the originals.
  - The $1,000/m³ tank-farm cost is assumed.
  - Payment terms for concentrate sold to China.
  - Hoisting limits at the Talnakh shafts may stop extra loader hours from becoming extra ore.

I used 4 of the 6 searches. The model and the full write-up are in the synthesis folder as `combine.py` and `answer.md`; nothing was committed.

Sources: [RAEX 24.04.2026](https://raexpert.ru/releases/2026/apr24a), [eastrussia: all-season road](https://www.eastrussia.ru/news/vsesezonnuyu-dorogu-ot-baimskogo-goka-postroyat-na-chukotke/), [eastrussia: ice roads](https://www.eastrussia.ru/news/ledovye-dorogi-dlya-gdk-baimskaya-postroyat-na-chukotke/), [Mining Weekly 2020](https://www.miningweekly.com/article/russia-infrastructure-plans-raise-risk-for-baimskaya-copper-project-kaz-2020-11-18), [Mining Technology](https://www.mining-technology.com/news/kaz-minerals-baimskaya-project/)