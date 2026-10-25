All four ideas are dead at this gate. Nornickel already plans Idea 1. In each of the other three, the cost share being attacked is too small to reach a ratio of 1.1. Kit self-checks matched the catalog (`breakeven_loss_fraction(74.6, 2500)` gave 0.029 and `ceiling_ratio(0.05)` gave 1.05). The numbers are in `gate/screen.py`; `gate/gate_result.md` is a short summary. Nothing was committed.

Two inputs are my own assumptions, not sourced:
- **Processing cost:** $8–15/t is a typical range for sulphide flotation. I found no figure for the Norilsk concentrator.
- **Metal prices:** all 6PGM are valued at the palladium price ($1,096/oz on 17 Oct 2026, Kitco). Copper uses the kit's $8,500/t.

At those prices Norilsk-1 ore is worth about $231/t in the ground and Maslovskoye about $340/t.

=== GATE ===
IDEA 1: Freed Norilsk concentrator, disseminated feed
SCREEN | 8 market/capacity: concentrator room for Norilsk-1 plus Maslovskoye 0.50 (room for Maslovskoye alone, after the planned Norilsk-1 feed, 0.07–0.28); 9 baseline: Nornickel's own plan is already this idea, ratio about 1.0; ceiling if all concentrator capital (about half of the 37%) is removed 1.23; 10 recovery: no ore-type recovery found for the Norilsk concentrator (silicate-bound Ni floats poorly), not scored
KILLER | Concentrator capacity for the refill the idea needs | required 15.3 Mtpa (Norilsk-1 at 7.0 Mtpa to 2048 under Nornickel's 2024 plan + Maslovskoye 206.8 Mt ÷ about 25 yr = 8.3 Mtpa) | available 7.6 Mtpa (actual throughput, Nornickel annual report 2020; 9.3 Mtpa nominal, annual report 2018) | MARGIN 0.50
CHAIN | Nornickel's current plan: the Talnakh upgrade frees the Norilsk concentrator for South Cluster (Norilsk-1) feed (2019 press), and the South Cluster mine is deepened to 730 m for 7 Mtpa to 2048 (annual report 2024) | now: index 1.00 of full cost per t Ni-eq | with idea: about 1.00, because the Norilsk-1 part is already the plan and Maslovskoye has only 0.6 Mtpa of room | RATIO 1.0
VERDICT | DEAD | The capacity "freed" by Talnakh is already booked for Norilsk-1 at 7 Mtpa, so there is no new saving and only about 0.6 Mtpa is left for Maslovskoye's roughly 8 Mtpa.
NEW FACT | The Norilsk concentrator already processes all Norilsk-1 disseminated ore plus Talnakh cuprous and rich-disseminated ore. Nornickel's 2021 plan was a new disseminated-ore concentrator of up to 18 Mtpa (9 + 9) to replace it, with the second section for Talnakh, South Cluster and Maslovskoye ore. The South Cluster target was 9 Mtpa by 2027 and RUB 45bn+ of investment, with more than 140 Mt of reserves. | [Nornickel AR2021 strategic projects](https://ar2021.nornickel.ru/en/strategic-report/main-strategic-projects.html); [AR2020 Norilsk (RU)](https://ar2020.nornickel.ru/pdf/ar/ru/business-overview_operational-performance_norilsk.pdf); [NS Energy](https://www.nsenergybusiness.com/?p=213272)
NEW FACT | A 2019 press report says the Talnakh upgrade frees Norilsk concentrator capacity for South Cluster feed. In 2024 Nornickel launched development of Norilsk-1 reserves to 730 m for 7 Mtpa until 2048. Interfax (June 2023) reported the South Cluster timing slipping after equipment-supply problems; full capacity had been planned for 2024–25. | [Mining.com 2019](https://www.mining.com/web/russias-nornickel-spend-1-4b-two-expansion-projects/); [Nornickel AR2024 strategy](https://ar2024.nornickel.ru/en/strategic-report/strategy.html); [Interfax](https://www.interfax.com/newsroom/top-stories/91084/)
NEW FACT | Maslovskoye's commercial production was due by 1 Jun 2025 under the licence and has not started. Nornickel postponed it after dropping the joint project with Russian Platinum in 2021. Reserves are 215 Mt (C1+C2) and the life is about 25 years (2012 figure). | [Financial One](https://fomag.ru/news/-nornikel-dopustili-k-razrabotke-maslovskogo-mestorozhdeniya/); [Novaya Gazeta Europe 2025](https://novayagazeta.eu/articles/2025/07/04/vechnaia-merzlota-rastaiala-aga-aga)

IDEA 2: Pair Talnakh expansion with backfill
SCREEN | 10 recovery: metal loss XRT can afford vs claimed loss 0.35–0.65; 9 baseline: ratio 1.03–1.05 for a feed-grade gain of 1.094–1.156× at 98% recovery, applied to processing plus concentrator capital (40.5% of cost); 8 capacity: same Norilsk concentrator room as Idea 1, 0.50; 13 pilot proof: only an unaudited release from another ore (Selebi), not scored
KILLER | Metal loss XRT can afford on Norilsk-1 disseminated ore | required ≤0.7–1.3% Ni-eq lost (15.2% of mass rejected × $8–15/t processing saved, against $231/t ore × 75% recovered) | available: the best claim is 2% loss (98% recovery, Selebi, unaudited, F350) | MARGIN 0.35
CHAIN | Talnakh 3rd complex plus South Cluster feed to the Norilsk concentrator without sorting | now: index 1.00 | with idea: 0.95–0.97, and booking capex per t of contained Ni for the pair changes no cost | RATIO 1.05
VERDICT | DEAD | Pairing the two steps is only a booking change, and a 1.09–1.16× grade gain on 40% of the cost gives at most 1.05×, while the loss XRT can afford is below the best claim.
NEW FACT | Part of the nickel in Norilsk ores is held inside silicate minerals and floats very poorly. This caps recovery from disseminated ore whatever the feed grade. | [Rudmet, Tsvetnye Metally](https://rudmet.ru/journal/609/article/7393)

IDEA 3: Availability as capacity
SCREEN | 9 baseline: ratio 1.02 for +2 points and 1.04 for +5 points (80% of cost fixed); 8 scale: availability gain needed to stand in for the +8 Mtpa stage 0.06; 13 pilot proof: measuring a 2–5 point gain needs many months per arm, not scored
KILLER | Availability gain needed for a 1.5× cost cut | required +66 points (+71% output with 80% of cost fixed, from a 93% start) | available about 5 points of headroom (93→98%; assumed best-practice ceiling, no Nornickel figure found) | MARGIN 0.075
CHAIN | Keep the Western fleet on its current spares, with the BelAZ/Nornickel underground-equipment JV being set up (F184–186) | now: index 1.00 | with idea: 0.96–0.98 | RATIO 1.04
VERDICT | DEAD | Each availability point adds about 1% of output, so the few points available give at most 1.04× and cannot stand in for a capacity stage.
NEW FACT | none

IDEA 4: Defect-to-repair deadline register
SCREEN | 9 baseline: ceiling ratio 1.03–1.04 even if all foundation losses (2%) plus one Ambarnaya-scale claim ($1.74bn) every 10–20 years were removed, against about $8.1bn a year of cash opex plus capex; 13 pilot proof: events seen vs events needed to show the collapse rate halved 0.035; 4 frozen-ground strength: not decisive, since the register changes no design
KILLER | Serious failures to show the register halves the collapse rate (Poisson, 80% power, 2:1 split) | required about 49 events in the baseline period | available about 1.7 events per 5 years (2 events, Ambarnaya 2020 and the concentrator collapse in 2021, F256, F264; 95% CI 0.24–7.2) | MARGIN 0.035
CHAIN | Post-spill monitoring (F263, F326) plus the SP 25.13330 Amendment 3 design rule | now: index 1.00 | with idea: ≥0.96 | RATIO 1.04
VERDICT | DEAD | Cutting the median repair time from 30 to 6 months is right on safety and compliance grounds, but the losses it targets are about 3–4% of full cost, so the ratio stays under 1.1 and the benefit cannot be shown statistically.
NEW FACT | none

Sources:
- [Nornickel AR2021 strategic projects](https://ar2021.nornickel.ru/en/strategic-report/main-strategic-projects.html)
- [Nornickel AR2024 strategy](https://ar2024.nornickel.ru/en/strategic-report/strategy.html)
- [Nornickel AR2020 Norilsk (RU)](https://ar2020.nornickel.ru/pdf/ar/ru/business-overview_operational-performance_norilsk.pdf)
- [Nornickel AR2018 processing projects](https://ar2018.nornickel.ru/en/strategic-report/key-investment-projects/processing-projects.html)
- [Mining.com 2019](https://www.mining.com/web/russias-nornickel-spend-1-4b-two-expansion-projects/)
- [Interfax June 2023](https://www.interfax.com/newsroom/top-stories/91084/)
- [NS Energy](https://www.nsenergybusiness.com/?p=213272)
- [Financial One on Maslovskoye](https://fomag.ru/news/-nornikel-dopustili-k-razrabotke-maslovskogo-mestorozhdeniya/)
- [Novaya Gazeta Europe 2025](https://novayagazeta.eu/articles/2025/07/04/vechnaia-merzlota-rastaiala-aga-aga)
- [Rudmet on beneficiation of Norilsk ores](https://rudmet.ru/journal/609/article/7393)
- [Kitco palladium (Europe)](https://www.kitco.com/palladium-price-today-europe/)