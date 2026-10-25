The script ran all four ideas. Three come out DEAD and one WOUNDED; none is ALIVE. The calculations are in `/home/user/SomeRepository/engine/runs/rusres/gate/c1/gate_c1.py`; nothing was committed. Two inputs are my own estimates, not sourced: Arc7 ice and open-water speeds of 9 and 17 kn, and the ~$540/t/y split for field, port and utilities.

=== GATE ===
IDEA 1: Plant-chilled foundations
SCREEN | 6 heat budget (summer flux to remove): 0.38; 4 frozen-ground strength (adfreeze at −0.5 vs −3 °C): 0.30 — this is the loss the loop would prevent, so not a killer of the idea itself; 9 baseline (piles plus thermosyphons already hold at Yamal LNG): ratio ceiling 1.01
KILLER | summer heat flux the loop must remove | required ≈13 W/m² (thawing a ~1 m active layer, 35% ice, from −3 °C, takes 113 MJ/m³ over ~100 thaw days; kit `thaw_energy_per_m3`, F85, F86) | available 5 W/m² (the idea's own sizing) | MARGIN 0.38
CHAIN | Yamal LNG T1–3 with passive thermosyphons and piles (F205, F271) | now ≈$7.5/mmBtu delivered | with idea ≈$7.4–7.5/mmBtu: foundation risk is under 1% of delivered cost, and the loop adds its own capex and a 6.5 MWe load at the corrected flux | RATIO 1.01
VERDICT | DEAD | The loop is undersized by about 2.6x, and fixing that would still leave no cost gain, because foundations are not a meaningful share of LNG delivered cost.
NEW FACT | none

IDEA 2: Murmansk winter shuttle loop
SCREEN | 1 season and ship-time (Arc7 tonnage vs output): 0.36 (T1) and 0.18–0.36 (T1+T2); 9 baseline (Murmansk-area transshipment already exists as an FSU route): ratio ceiling 1.06–1.08; 8 storage: Saam FSU holds 361,600 m³, which is enough
KILLER | Arc7 ships needed to clear Arctic LNG 2 Train 1 (6.6 Mt/y) | required 2.8 ships (shuttle round trip ≈11.7 d against ≈18.6 d via Zeebrugge, so about 1.58x per ship; 172,600 m³ cargo gives ≈2.37 Mt per ship-year) | available 1 Arc7 for Arctic LNG 2 (Alexey Kosygin; Christophe de Margerie is a Yamal LNG ship) (F139, F140) | MARGIN 0.36
CHAIN | Yamal LNG with Arc7 to Zeebrugge or Murmansk transshipment (F138, F140) | now ≈$7.5/mmBtu | with idea ≈$6.9–7.1/mmBtu, even granting the claimed 25–35% cut on the 22% outbound-logistics share | RATIO 1.07
VERDICT | DEAD | The per-ship gain of about 1.6x is real, but this route is already in use and only trims a 22% cost share; for Arctic LNG 2 the binding limit is the number of Arc7 hulls and sanctions, not voyage length.
NEW FACT | Saam FSU (361,600 m³, about 400 m long) arrived in Ura Bay on 26–27 June 2023 and was still idle in February 2024. Its owner, Arctic Transshipment (a Novatek subsidiary), was added to the US sanctions list in September 2023. Koryak FSU went to Kamchatka. | [LNG Prime](https://lngprime.com/?p=84927); [Barents Observer](https://thebarentsobserver.com/en/arctic-lng/2024/02/six-months-after-arrival-ura-guba-novateks-brand-new-400-long-storage-tanker-left)

IDEA 3: Rock-socketed piles with slip sleeves
SCREEN | 4 frozen-ground strength (warm adfreeze loss the sleeve avoids): 0.30 lost on the current design, so this is the idea's justification rather than a failure; geometry (depth to rock in Norilsk vs the 30 m limit): 1.5; 9 baseline (the national pile code already prescribes rock-bearing piles): ratio ceiling 1.008
KILLER | depth to competent rock | required ≤30 m (idea) | available: rock within ≤20 m is the code trigger, and 1940s–50s Norilsk excavations reached rock at up to 20 m ([SP 25.13330.2020 via normacs](https://www.normacs.info/answers/6285)) | MARGIN 1.5. The idea fails on cost, not physics.
CHAIN | SP 25.13330.2020 end-bearing piles on rock, as the Ambarnaya tank was designed (F258) | now ≈$8bn/yr Nornickel full cost | with idea ≈$7.94bn/yr: the Ambarnaya award of 146bn RUB (F262), spread over 30 years, is ≈0.8% per year, and that tank's failure was a construction defect, not the design | RATIO 1.01
VERDICT | DEAD | The idea restates current Russian code practice, and foundation failures are under 1% of chain cost, so there is nothing left to win.
NEW FACT | SP 25.13330.2020 says foundations bearing on rock (end-bearing piles and others) should be considered where rock lies within 20 m of the surface. | [normacs.info](https://www.normacs.info/answers/6285)

IDEA 4: Numbers-up Arctic Cascade trains
SCREEN | 1 season and shipping (winter Arc7 capacity for new output): 0.42 (only the Jul–Nov conventional-carrier window is open; the Yamal fleet of 15 is fully used and Arctic LNG 2 has 1–2 ships); schedule (2.5 years claimed vs Train 4 actual): 0.56; 9 baseline capital: ratio 1.21; 13 pilot (3 trains measure capex but cannot prove reliability): not decisive
KILLER | share of the year the added output can be shipped | required 12 months | available ≈5 months: no spare Arc7 hulls (F139, F141), and the NSR window for non-Arc7 ships is Jul–Nov (F308) | MARGIN 0.42
CHAIN | Yamal LNG T1–3 at ≈$1,640/t/y total project cost (F43, F174) | now ≈$7.5/mmBtu | with idea ≈$6.2/mmBtu: trains at $500/t/y plus ≈$540/t/y field, port and utilities still needed, cutting capital about 37%. The claimed 60% cut is not supported, because the $450–500/t/y figure (F174, SOFT) was marginal cost on shared infrastructure | RATIO 1.21
VERDICT | WOUNDED | The domestic technology works and capital does fall by about 1.2x, but Train 4 took about 4.5 years, not 2–3, and new trains have no winter ships to deliver through.
NEW FACT | Yamal LNG Train 4 (0.95 Mtpa) was due by end-2019 and was delayed to 2021, reportedly because its process piping was not designed for such low gas temperatures (Kommersant). Novatek said Ob LNG would not use Arctic Cascade as planned. | [Barents Observer](https://thebarentsobserver.com/en/arctic-lng/2021/06/new-yamal-lng-plant-made-russia-and-comes-more-year-after-schedule); [Natural Gas World](https://www.naturalgasworld.com/novatek-confirms-yamal-lng-t4-delay-76721)

Sources:
- [Barents Observer — Train 4 more than a year late](https://thebarentsobserver.com/en/arctic-lng/2021/06/new-yamal-lng-plant-made-russia-and-comes-more-year-after-schedule)
- [Natural Gas World — T4 delay](https://www.naturalgasworld.com/novatek-confirms-yamal-lng-t4-delay-76721)
- [LNG Prime — Saam FSU arrival](https://lngprime.com/?p=84927)
- [Barents Observer — Saam idle, sanctions](https://thebarentsobserver.com/en/arctic-lng/2024/02/six-months-after-arrival-ura-guba-novateks-brand-new-400-long-storage-tanker-left)
- [normacs — SP 25.13330.2020 rock-bearing rule](https://www.normacs.info/answers/6285)