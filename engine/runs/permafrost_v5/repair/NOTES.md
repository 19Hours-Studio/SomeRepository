# NOTES — repair of 4 ideas (calcs in calc/*.py)
Sources used:
- S1 Zyryanka coal 2019: 174.6 kt, 2020: 160.4 kt (plan 250 kt); winter road 48 km to Zyryanka inter-navigation stockpile; barges along the Kolyma — nedradv.ru / uk42.ru / sakha.gov.ru; 2024 revenue 710 M rub (list-org)
- S2 Kolyma fuel to Zyryanka/Srednekolymsk/Nizhnekolymsk etc. >13 kt = 3/4 of plan (2025); 2025 Northern Delivery plan 3.4 Mt incl. 2 Mt coal — portnews.ru/378849, marine.org.ru
- S3 Large Yakutopttorg dry-cargo ships can't enter the Kolyma since 2019; shallow "Freyer" carries >50 t of food per season — vostok.today/46234
- S4 Fresh exposed placer surface thaws ~4 in/day in summer (Yukon/Alaska) — "Solar Thawing Increases Profit from Sub Arctic Placer Gravels", onemine.org
- S5 Coal matrix k 0.22–0.55 W/mK (FACT 9, Herrin & Deming 1996)
- S6 Kolyma at Srednekolymsk (641 km): mean 2,220 m3/s, max 25,100 m3/s in June; high water mid-May to Sept — bigenc.ru
- S7 Polynya turbulent loss 250 W/m2 (calm) to 575 W/m2 (20 m/s) — Annals of Glaciology (Cambridge)
- S8 Arctic micro-pits: 20–50 kt/yr, max 100 kt, local supply — arctica-ac.ru "small deposits" paper; Arctida: delivery raises coal price 4–5x
- S9 Alaska DGGS village-coal exploration since 1981 (Chicago Creek, Unalakleet, Cape Beaufort...) — dggs.alaska.gov pdf1986_066
- FACT 6 barge $3M/5 kt; FACT 7 winter bottom water 0.01–0.2 C; FACT 4/5 ice-drift losses.
UNSOURCED (assumptions, flagged): delivered imported coal 15–23k rub/t; equipment prices; tanker day cost 0.3–0.6 M rub; ice-road 0.15–0.3 M rub/km; bladder price; boilerhouse capex 30–50 M rub/MW; tributary hydrograph (tau = 12 d).

## Idea 1 — anchor: the river has already exposed the seam; take it by natural thaw, no drilling or blasting
Repair: scrape a 0.1 m thawed skin every 1–3 days off the face (the Stefan thaw clock restarts each time) instead of waiting for the one-shot seasonal thaw. Thaw 3–7 cm/d -> 2.7–5.6 m/season vs 0.9–1.35 m. Best regime: a ≥6 m seam, 20 kt/yr from ~850 m of face, serving several villages.
Consistency:
| limit | value | design | ok? |
| thaw window | ~85 d Jun–Aug | 3.5 m retreat needs 4.1 cm/d | ok in 10/16 parameter cases; fails at 35% moisture with 0.2 m skins |
| surface energy | ≤110 W/m2 | 0.1 m skins need 53–120 W/m2 | capped in 2 cases |
| overburden | strip ≤1 m3/m3 | site selection; overhang risk if seam mid-bluff | must retreat the whole face |
| turbidity | fishery norm +0.25 mg/L SS | work above high water only, berm + sump | design-dependent, unverified |
| stockpile | wet thawed lignite freezes into lumps, self-heats | spread and drain in Aug; compact | handling cost not in calc |
Cost: 3.2k rub/t lignite = 1,390 rub/useful Gcal vs 3,850–5,900 imported hard coal -> 2.8–4.3x. At 6 kt/yr only 1.3–2.0x. Vs a conventional micro-pit on the same deposit: ~1.0–1.5x (saves explosives and winter ripping).
Deciding unknown: thaw rate of frozen lignite under repeated scraping. Experiment: one summer, a 10 m x 3 m test panel at a known exposure (e.g. a Zyryanka-basin outcrop), thermistor strings, scrape at 1/2/4-day intervals, ~30 cycles per interval -> rate ±15%. Plus a desk count of seams ≥3 m within 30–60 km of villages on 1:200k geological maps.
Closest work: placer layer-by-layer natural thaw stripping (standard); Alaska village-coal (S9), Meade River/Atqasuk; Yakutian micro-pit concept (S8). New: river-bluff face with no overburden, mined by natural thaw only, sized for village boilers. Verdict: WORKS conditionally (niche siting).

## Idea 2 — anchor: one Kolyma flow rides the other flow's empty leg
Data: upbound dry cargo ~3 kt (S3) vs coal down 165 kt (S1) -> only 1.8% of coal fits; the original direction FAILS. Flipped: ~17 kt/yr of upbound fuel (S2) rides on the ~165 empty upbound coal-barge legs (17 legs needed) in pillow bladders, with the coal hold as secondary containment. 2.1k rub/t vs 2.7–12k rub/t for a dedicated old tanker leg -> 1.3–5.7x on the river leg, but that is <10% of the delivered diesel price.
Consistency: shoal-limited 1,000 t/leg ≥ 24 bladders x 42 t ok; season 23 May–10 Oct (FACT 3, 10) = 4 cycles ok; bladder abrasion from coal residue (needs liner); dangerous-goods carriage approval (Russian River Register) — UNKNOWN, deciding.
Experiment: a single-season trial with 5 bladders on 2 legs, counting leaks/abrasion and loading time; ask the operator for real tanker day costs.
Verdict: NICHE (fleet renewal of 38–54-year-old tankers avoided). Anchor kept as a principle, direction reversed.

## Idea 3 — anchor: a pre-loaded barge waits out the ice drift in shelter and rides the flood crest
Fixes: loading in autumn afloat at a deep berth (no loading through ice). A backwater ≥2.5 m deep at freeze-up. Moved to a tributary navigable only on the spring flood, where there is a single trip per year, so "only the first trip is full" is no longer a penalty. Model: a 5–10 d arrival delay costs 35–62% of the load (recession tau = 12 d, ASSUMED). Pre-loaded: 3.1k vs 4.7–11.3k rub/t -> 1.5–3.6x on that leg. Winter road baseline: 3.75–14k rub/t (150–400 km).
Hazards: ice drift (FACTS 4, 5): use a backwater off the main channel with a mooring designed for the ice-drift rise; a loaded hull sinking at its winter berth = coal in the river.
Deciding unknown: the tributary's daily level series around ice-out (Roshydromet gauge data, 10+ years) vs the convoy arrival date. Desk study, then one pre-staged barge for one season.
Closest work: unintended "wintering with cargo"; early-delivery voyages. Verdict: NICHE.

## Idea 4 — anchor: the coal barge is the boilerhouse and the coal yard, frozen in at the village
Fix: no bubbler. A covered 1 m moat heated by the boiler's own low-grade heat: 8 kW vs ~480 kW flue loss of a 3 MW boiler (0.3%). The open-moat case is 36 kW (S7 fluxes). Hull side losses of ~26 kW keep a melt film. Economics at a barge-reachable village: net saving 0.8–3.4k rub/t of 15–23k -> 1.04–1.3x. Best case is where the shore boilerhouse must be replaced anyway.
Hazards: hold self-heating and CO; ice drift and sinking at berth (FACT 4); flexible heat link to shore; classification as a hazardous facility on a vessel.
Deciding unknown: avoided boilerhouse capex vs the class and ops cost of a barge boilerhouse. Experiment: a quoted bill of materials plus a one-winter moat test (20 m covered heated trench in a backwater, power logged).
Closest work: Akademik Lomonosov; Thames barge heat; floating power barges. A coal-burning, self-stored, frozen-in barge boilerhouse: none found. Verdict: NICHE.
