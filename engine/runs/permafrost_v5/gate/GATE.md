=== GATE ===
IDEA 1: Downstream coal on empty barges
SCREEN | 11 draught at late-season depth: 0.41-0.66; 9 baseline (barge leg share 0.35, ceiling 1.53): 1.21; 8 market: n/a (Zyryanka already ships 160-250 kt/yr downstream)
KILLER | payload at late-season depth | required 2,214 t (full load, 80x15 m barge, 2.5 m) | available 918-1,458 t at 1.5-2.0 m water (kit river.yana_indigirka_low_water_depth; naval.payload_at_draught) | MARGIN 0.41
CHAIN | dedicated coal barges from Zyryanka down the Kolyma, then to the boiler | now 23,000 RUB/t at boiler (barge leg 8,000) | with idea ~19,000 RUB/t (barge leg halved at marginal cost, generous) | RATIO 1.21
VERDICT | WOUNDED | Zyryanka coal already goes down the Kolyma on coal barges, most upbound fuel comes in tankers that can't carry coal, and a coal-loaded return hull hits the same shoals, so the barge leg (35% of cost) shrinks only slightly.
NEW FACT | Zyryanka coal is already distributed down the whole Kolyma each summer on dedicated coal barges (баржи-углевозы) | https://www.kolymastory.ru/glavnaya/morskie-vorota-kolymy/rechnye-gruzoperevozki/
NEW FACT | Kolyma-basin tankers are 38-54 years old; fuel moves up by tanker | https://www.korabel.ru/news/comments/dlya_severnogo_zavoza_zadeystvovali_3_6_tys_km_rek_lenskogo_basseyna.html
NEW FACT | Zyryanka-Srednekolymsk is being dredged (about 23k m3 since July); navigation closes 10 Oct | https://www.korabel.ru/news/comments/opredeleny_sroki_zakrytiya_navigacii_v_lenskom_basseyne.html

IDEA 2: Frozen-in bunker-boiler barge
SCREEN | 3 depth under loaded hull: needs 3.63 m (unverified for a backwater by the village); 11 uplift on ice as 3 kt is burnt: 0.20-0.38; 8 hull-year cost vs removed cost: 0.09; 9 baseline: 0.39
KILLER | removed handling cost vs added hull-year + deck boiler | required 13,935 RUB/t (new 3 kt barge 185 M RUB at 14%/25 yr + 3% O&M = 10,850; boiler + 200 m main 3,085) | available 1,209 RUB/t removed at a riverside settlement (unloading + 3% stockpile loss, est.) | MARGIN 0.09
CHAIN | summer barge to the riverside shore depot, loader to the existing boilerhouse | now ~8,200 RUB/t (Kolyma depot 6,962 + handling) | with idea ~20,900 RUB/t | RATIO 0.39
VERDICT | DEAD | A village a barge can winter beside has no winter-road last mile anyway, so the idea saves only about 1,200 RUB/t of handling and ties up a whole hull for the year at about 10,900 RUB/t.
NEW FACT | Two motor ships (Sofron Danilov, Kapitan Burkovsky) sank at their winter berth during Lena ice drift, Zhigansky district | https://www.eastrussia.ru/news/na-reke-lena-iz-za-ledokhoda-zatonulo-dva-teplokhoda-/
NEW FACT | 28 May 2026: 10 vessels (5 Lena waterways administration, 5 LORP) broke loose and drifted on the Indigirka at Belaya Gora | https://www.fontanka.ru/2026/05/30/76451529/
NEW FACT | Ukrrechflot estimate ~$3 M per 5,000 t river barge (2020) | https://gmk.center/news/ukrrechflot-hochet-postroit-5-nesamohodnyh-barzh-v-2021-godu/

IDEA 3: Frozen-in barge boilerhouse
SCREEN | 6 bubbler heat budget: 0.010; 11 uplift as cargo is burnt: 0.20-0.38; 8 hull-year vs removed: 0.17; 9 baseline: 0.58
KILLER | heat to keep a 1 m moat open round the hull | required 100 kW (525 W/m2 at -40 C, 3 m/s x 190 m2; thermal.open_water_heat_loss) for 200 d | available 16.6 GJ = 1.9 d in a 3 m berth pool at 0.2 C (winter bottom water 0.01-0.2 C, DTIC ADA148739; ice season 200 d, BRE) | MARGIN 0.010
CHAIN | summer barge on high water to the shore stockpile at the same settlement | now ~8,200 RUB/t | with idea ~14,100 RUB/t (scrap hull 12 M RUB over 5 yr + 5 M RUB/yr survey/repair + boiler/main, est.) | RATIO 0.58
VERDICT | DEAD | A bubbler works only on stored heat, and 0-0.2 C river water holds about 2 days of it against 200 days of ice, while the saving the idea claims (11-15k RUB/t) is really about 1.2k at a settlement the barge can already reach.
NEW FACT | Winter bottom water in candidate bubbler sites measured 0.01-0.2 C, not 4 C | https://apps.dtic.mil/sti/pdfs/ADA148739.pdf

IDEA 4: Frozen-in barge as bunker-boilerhouse
SCREEN | 11 payload at 0.8 m draught vs the village's year of coal: 0.13-0.17; 3 pool depth: needs 2.23 m (kit) / 2.8 m (idea), not checked; 11 uplift: 0.20-0.38; 9 baseline: 0.53
KILLER | coal one 0.8 m hull can hold | required 3,000 t/yr (1,000 people x 3 t, kit base.arctic_yakutia_utility_coal) | available 378-520 t (80x15 to 100x16.5 m hull, naval.payload_at_draught) | MARGIN 0.13
CHAIN | barge to depot, transshipment, 300 km winter road | now 23,000 RUB/t | with idea ~43,700 RUB/t (winter road and transshipment removed, but about 8 shallow hulls frozen in for a year) | RATIO 0.53
VERDICT | DEAD | A 0.8 m draught holds about 1/8 of a village's year of coal per hull, and "full load" at 0.8 m carries the same tonnes per square metre of hull as today's deep barges at 50%, so the per-trip cost does not halve.

IDEA 5: Long-season tracked sled trains
SCREEN | 2/1 ice season for a 40 t tractor (needs 1.07 m, same as a loaded truck): 139 d vs 150 claimed, 0.93; 9 cost per t-km vs 5 RUB target: 0.012 (0.12 even if 10x cheaper than Antarctica); 11/tow load per tractor measured 73 t vs 200 t: 0.36
KILLER | cost per t-km | required <= 5 RUB/t-km | available ~402 RUB/t-km (South Pole Traverse delivered $3.60/lb over 1,660 km, DTIC ADA602402) | MARGIN 0.012
CHAIN | truck winter road | now 20 RUB/t-km | with idea >= 40 RUB/t-km (SPoT divided by 10 for flat Arctic terrain, generous) | RATIO 0.5
VERDICT | DEAD | The heaviest unit, not ground pressure, sets the ice season (same as trucks), a tractor tows about 73 t of measured payload, not 200 t, and the only modern costed tractor train runs about 400 RUB/t-km.
NEW FACT | SPoT: 8 tractors, ~768,000 lb/yr payload, one 24,000-gal four-bladder set per tractor, ~1 lb of support load per lb delivered | https://apps.dtic.mil/sti/pdfs/ADA602402.pdf ; https://www.equipmentworld.com/applications-and-innovations-get-ready-for-winter/

IDEA 6: River-thawed bluff lignite scraping
SCREEN | 5/6 summer thaw depth of the face: 0.61-0.90; 7 turbidity at a small river (2% of fines into the water, est.): 0.30-1.8; 1 scraping window: 4.5; 8 face length needed: 838 m/yr (geology within 30 km not verified)
KILLER | summer thaw depth of a lignite face | required 1.5 m | available 0.92-1.35 m (Stefan, TDD 1,800 C*d kit climate.thawing_index_N_Yakutia, k 0.33-0.55 W/mK Herrin & Deming 1996, 40% ice by volume, n 1.0-1.3) | MARGIN 0.61
CHAIN | coal barged in and carried by winter road to the boiler | now 23,000 RUB/t | with idea ~10,400 RUB per hard-coal-equivalent t (2.5 FIFO worker-years, 45 M RUB of plant, 30 km winter road, 5 M RUB other, est.) | RATIO 2.2
VERDICT | WOUNDED | The economics hold at 2.2x, but the face thaws only 0.9-1.35 m, so about 1.1-1.6 km of seam face per village per year is needed, and whether that much exists within 30 km of a village plus the river turbidity limits are unproven.
NEW FACT | Coal matrix thermal conductivity 0.22-0.55 W/mK (mean 0.33), 55 coals incl. 6 lignites | doi:10.1029/96JB01884 (Herrin & Deming 1996)

IDEA 7: Flood-crest barge launch
SCREEN | 1 crest window vs transit: ~10 (flood mid-May to Sep, BRE; ~4 d transit); 3 loaded hull in backwater: needs 2.90 m at winter low water (not verified); 11/2 winter loading of a frozen-in hull (ice must let it sink 1.85 m): 0.23-0.36; 9 trips improved: 1 of ~5
KILLER | ice-edge line load when 2,214 t is loaded into a frozen-in hull | required 114 kN/m | available 26-41 kN/m (1.05-1.5 m ice, flexural 1 MPa; ice.edge_line_load_capacity) | MARGIN 0.23
CHAIN | coal barges from Zyryanka through the season (~5 trips at <50% on shoal water) | now 23,000 RUB/t at boiler / ~7,000 at riverside depot | with idea barge cost per t -17% (one full trip of five), 21,700 / ~6,400 RUB/t | RATIO 1.06
VERDICT | DEAD | Only the first trip of the season is full, which cuts the barge leg by about 17% (not 50%), and loading a frozen-in hull in winter breaks the ice it is frozen into.
NEW FACT | Kolyma navigation opens 23 May (Oroek-Zyryanka) | https://www.korabel.ru/news/comments/opredeleny_sroki_zakrytiya_navigacii_v_lenskom_basseyne.html

IDEA 8: Frozen-in barge boilerhouse
SCREEN | 9 share of cost after the barge haul: 0.23; 8 hull-year vs removed cost: 0.09; 11 uplift as cargo is burnt: 0.20-0.38; 3 depth under loaded hull: needs 3.63 m
KILLER | share of delivered cost after the barge haul | required 0.65 | available 0.15 at a riverside settlement (1,209 of 8,171 RUB/t; Kolyma depot 6,962 RUB/t, kit price.kolyma_depot_coal) | MARGIN 0.23
CHAIN | summer barge to the riverside depot, loader to the boilerhouse | now ~8,200 RUB/t | with idea ~20,900 RUB/t (hull-year + deck boiler) | RATIO 0.39
VERDICT | DEAD | Where a barge can freeze in beside the village there is no winter road, so only about 15% of cost comes after the barge, short of the 65% needed (ceiling 1.17x even if it were free), and the idle hull costs more than it saves.
