# Russian permafrost resources: 4 proposals (baseline run, 2026-10-25)

Arithmetic: `calc.py` in this directory. Every number labelled "assumption" is an estimate, not a sourced figure.

## IDEA 1 — Shared nuclear-anchored grids instead of a diesel plant at each site
- **Mechanism:** Build 110/220 kV lines that tie clusters of deposits to one large power source (Akademik Lomonosov FNPP at Pevek, the Baimskaya FNPPs at Cape Nagloynyn, the RITM-200N plant at Ust-Kuyga). Then develop first the deposits that fall within about 150–250 km of those lines. Sites off the grid use wind or solar with diesel and LFP storage instead of diesel alone.
- **Physics:** A large genset uses about 0.22 kg of diesel per kWh. Every litre has to be shipped in during the summer navigation season or hauled over a winter road. A nuclear unit refuels about once every 5–10 years.
- **Numbers:**
  - Fuel alone costs about 20 RUB/kWh; all-in, diesel is about 26 RUB/kWh (assumption: 90k RUB/t delivered). That compares with about 9.6 RUB/kWh for the FNPP (6 RUB/kWh in 2020 prices per Atomflot, indexed by about 60%, which is an assumption).
  - At about 9.6 MWh per tonne of copper (Baimskaya: about 300 MW for about 250 kt Cu a year), that is about 1,900 USD/t Cu, roughly 20% of the copper price.
  - Hybrids save 10% (measured at Diavik and Raglan) to 30% (Yakutia AGEK plan) of diesel, which is about 2–6 RUB/kWh.
- **Lead time:** FNPP and SMR power arrives 2027–2031, so time to first production is set by power: plus 0–2 years for Baimskaya-type projects. A hybrid takes 1–2 years.
- **Effectiveness:** Working days rise because the fuel-delivery risk goes away (in 2015 Chukotka received only 46.2 kt of the 103 kt of fuel planned).
- **Benchmarks:** Diavik 9.2 MW wind (4–5 Ml/yr, 10% of diesel); Raglan 2 × E-82 turbines with storage (4.4 Ml/yr); Kupol (all diesel).
- **Applies to:** Chukotka (Baimskaya, Kupol/Dvoinoye, Mayskoye), Yakutia Yana–Indigirka gold (Kyuchus), the Magadan off-grid fringe.
- **Does not apply to:** Norilsk (already has its own gas and hydro), Yamal and Gydan (associated gas on site), Udokan and Elga (BAM grid).
- **Makers:**
  - Rosatom/OKBM Afrikantov (RITM-200M/N), Baltic Shipyard.
  - Novawind (wind turbines), Hevel/Unigreen (PV), Liotech (LFP batteries).
  - Kolomna/Ural Diesel/Zvezda (gensets), Rosseti-type 220 kV lines built by domestic contractors.
- **Risks:** FNPP schedule slips (Yakutia SMR moved from 2028 to 2030–31); take-or-pay exposure if the mine is late; the line crosses ice-rich ground.
- **Test (3–5 years):** Before committing to a full grid, connect one gold mine in the Pevek–Bilibino area by line and meter its delivered cost in RUB/kWh against diesel. Use the Bilibino NPP retirement load as the anchor.

## IDEA 2 — Design for warming ground, with automated monitoring
- **Mechanism:** Assume the permafrost will warm over the asset's life: 0.39 ± 0.15 °C per decade in the continuous zone in 2007–16 (GTN-P, Biskaborn 2019). Design pile capacity for the ground temperature expected at the end of design life, not at construction (SP 25.13330 procedure). Add passive two-phase thermosyphons wherever the ground is warmer than about −2 °C. Mandate automated monitoring of ground temperature and settlement, with alarm thresholds, on fuel tanks, tailings dams and pipelines.
- **Faults matter as much as thaw:** Rostekhnadzor (Nov 2020) attributed the Norilsk TPP-3 spill to construction and operating faults, with half the piles overloaded, not to thaw. Monitoring must therefore cover loads and maintenance, not only temperature.
- **Numbers:**
  - Nornickel stage 1 covered 165 objects for 1.4 bn RUB, about 8.5 M RUB per object. The 2020 spill was about 21 kt of diesel, with a 146–148 bn RUB damage claim.
  - Russia-wide (Streletskiy 2019): 248.6 bn USD of assets sit on permafrost; mitigation by 2050 costs 16.7 bn USD (structures) plus 67.7 bn USD (infrastructure).
  - Effect estimate: foundation life stays at the 30–50-year design life instead of being shortened by roughly 20–50% where ground near 0 °C is left unmanaged (assumption). The cost is about 0.3–1% of asset capex.
- **Lead time:** No change to years before first production for new builds.
- **Benchmarks:** Yamal LNG and Vankor (thermosyphons as standard); Alaska TAPS (thermosyphons on its vertical supports); Raglan and Pogo filtered (dry-stack) tailings.
- **Makers:** Fundamentproekt, NPO Fundamentstroyarkos (Tyumen); domestic fibre-optic and thermistor strings, for example from Skolkovo residents.
- **Risks:** False alarms; thermosyphons do not work in summer, so they need correct sizing.
- **Test (3 years):** A/B comparison of new pads at Vostok Oil, comparing settlement and maintenance cost.

## IDEA 3 — Ore sorting and dry-stack tailings at the mine
- **Mechanism:** Use domestic sensor sorters (Bourevestnik and RADOS X-ray sorters) to reject barren rock before grinding.
  - In tests, up to 70% of the ore mass went to waste while the gold grade rose 1.5–1.6 times. Dukat (Magadan) produced rejects at tailings grade.
  - Each tonne of product then needs about 30–50% less grinding energy, water, reagents and tailings volume. This matters most where power is from diesel.
- **Filtered dry-stack tailings:** Stack the remaining tailings dry instead of behind a dam on ice-rich ground. A dry stack tolerates uneven thaw settlement (SRK on Raglan, Pogo, Greens Creek).
- **Year-round heap leach:** Do not try it on clayey ore that is stacked frozen. The Eagle (Yukon) heap slid in 2024 (5.95 Mm³), and the review board blamed poor drainage and frozen, fine ore. Instead, mine and sort all winter, and leach in season (as at Fort Knox).
- **Effect:** Full cost about −5 to −15% per oz or per t Cu at diesel-powered gold and copper mines (assumption based on 50% mass rejection). Recovery falls by 1–5 percentage points (metal lost in the rejects), so the trade-off must be tested.
- **Applies to:** Lode gold (Kupol, Pavlik, Natalka, Kyuchus) and coarse copper ores.
- **Does not apply to:** Placers, diamonds (sorting is already standard practice at Alrosa), LNG.
- **Test:** A 2-year pilot sorter at one Magadan or Chukotka mine.

## IDEA 4 — Develop by value per tonne and access to rail or pipe
- **Mechanism:** At about 30 USD/t for Arctic freight (assumption), freight is about 33% of thermal coal value, about 18% of coking coal, about 7% of crude oil and LNG, about 1.3% of 25% Cu concentrate, and about 0.3% of copper cathode.
- **Logistics limits:** NSR cargo was 37.0 Mt in 2025, down 2.3%. Arctic LNG 2 has 3–4 usable Arc7 carriers against 21 contracted and shipped 1.3 Mt in 2025.
- **Order:**
  1. Ship high-value, low-tonnage products first: Udokan cathode (99.99%, Sept 2026), Baimskaya.
  2. Develop deposits with rail or pipeline access next: Elga coal (35.1 Mt in 2025) over its own railway to BAM; Vostok Oil (first oil Sept 2026 through a 790 km pipeline, about 6 years from FID).
  3. Defer NSR bulk coal (Syradasay: ice-class fleet not built), Tomtor (no decision as of 2025) and further Arctic LNG 2 trains until ships and buyers exist. Lomonosov diamonds (Arkhangelsk, not permafrost) were paused in July 2026 because the market is weak.
- **Benchmark:** Red Dog stores 950 kt of concentrate and ships it in a 100–122-day season.
- **Effect:** Avoids stranded capital per unit delivered; years before first production are set by corridor availability.
- **Risk:** Policy pressure to build anyway.
- **Test:** Rank deposits on a pre-FID screen of delivered cost per unit.
