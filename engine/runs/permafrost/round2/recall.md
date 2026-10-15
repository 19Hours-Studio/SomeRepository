# Red-team recall on the 10 pre-registered known defects (scored strictly: the defect's mechanism must be named)

| K | defect | critic | found? | where |
|---|---|---|---|---|
| K1 | shell melt drift vs +3..+9 kg trim | B | YES (FATAL) | idea 4: 4.35 kg/day, neutral after 0.7-2.1 days |
| K2 | warm polynya below dams | B | YES (FATAL) | idea 4: Yenisei 200-300 km ice-free, Vilyuy +5-6 C, frazil hanging dams |
| K3 | baseline = summer barge, not winter road | B | YES (MAJOR) | idea 4: "fair comparison is the barge leg alone, $12-37/t" |
| K4 | 20 pods cannot bound losses | B | YES (MINOR) | idea 4: ~456 pods per route-year for 5% +-2% |
| K5 | snow must stay dry, else payload collapses | B | NO (partial) | idea 4 notes the snow/void bookkeeping only reproduces with flooded voids, but not the soaking risk |
| K6 | stage selectivity 0.85/0.45 assumed | A | YES (MAJOR) | idea 3: 80/50 -> 4.6% Li2O, 75/55 -> 2.9% |
| K7 | competitor dry sorting / best baseline | A | YES (MINOR) | idea 3: TOMRA XRT >1,000 t/h at Pilgangoora |
| K8 | ice in permafrost ore (humidity wording) | A | YES (MAJOR) | idea 3: 1-3% ice needs 28-85 MJ/t, 0.8-2.4x mill heat |
| K9 | space charge of the falling stream | A | YES (MAJOR) | idea 3: 0.2-1.0 t/h per metre of plates |
| K10 | carbonyl-by-pipeline prior art (McAlister) | A | NO | not mentioned (novelty of carbonyl not attacked) |

Recall 8/10 (prediction >= 6/10: met; K1 found: met).
New defects not in the known list (examples): carbonyl toxic inventory ~1,000 t in Power of Siberia and vent releases;
CO open-loop cost $550-1,100/t Ni; propane hydrate in the freeze engine; Udokan has grid power; drift impossible at 45 kV;
deflation window inside the snow season; no wind separates 25-500 um quartz from gold; ore-ice dam debris coat and
seepage; boulder floe grounding; frazil accretion; coal over-buoyant.

# ERP2 (new repair rules, NO critic) - which known defects it found and fixed by itself

| K | found by ERP2? | how |
|---|---|---|
| K1 | YES | b/idea 4: shell melt -196 kg vs +-3-9 kg window; plus NEW snow creep and Cartesian-diver depth instability (521 kg/m) |
| K2 | YES | b/idea 4: tailwater +0.5..+2 C melts the shell in 0.3-1.1 days |
| K3 | YES | b/idea 4: summer barge + stockpile $27-33/t as the baseline |
| K4 | partial | b/idea 4: sizes a 20-log test for +-10% arrival fraction, does not bound industrial loss |
| K5 | partial | b/idea 4: snow pre-compacted to 550 kg/m3 and sealed at -35 C (self-pressurised); soaking not discussed |
| K6 | partial | a/idea 3: names spodumene-vs-gangue charge at -40 C as the deciding unknown |
| K7 | YES | a/idea 3: dense-media separation + haul is the best baseline -> 1.15x |
| K8 | YES | a/idea 3: 0 C air dries only 0.33%; intake must be 20-40 C (137 MJ/t) |
| K9 | YES | a/idea 3: space charge caps 0.15 t/h/m at 30 kV/m; repaired to 1.47 t/h/m at 300 kV/m |
| K10 | YES | a/idea 1: cites US 8,840,692 / 9,669,374 |
Self-catch 7 full + 3 partial of 10. It also found on its own what critic A found (propane hydrate, fan power, grid-power
baseline) and NEW strawman baselines (boulders: excavator $3/m3 vs claimed $6/m3 drill-blast).
