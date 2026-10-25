All four ideas come out **DEAD**. Ideas 3 and 2 fail on physics or capacity as well as on cost. Ideas 1 and 4 fail mainly because they touch too small a share of the full cost: even if they worked perfectly they could not reach a 1.5x cost ratio. The calculations are in `gate_calc.py`, with output in `gate_calc.out`, both in `gate_fill/`. Nothing was committed.

Some inputs are my own estimates rather than sourced figures, and they are marked "est." below. The most important ones are:
- Idea 1: processing cost of $15/t of ore, sorter cost of $1.5/t, and a PGM basket price of about $1,300/oz.
- Idea 2: a cost share of about 2% for foundation repair and upkeep.
- Idea 4: a cost share for underground haulage.
- Idea 3: a small extra unit-opex penalty for the smaller plant (about 1.6x on the ~$3,600/t opex). Without that penalty the ratio is 0.46 instead of 0.40, so still DEAD.

Changing any of these within a reasonable range does not change a verdict.

=== GATE ===
IDEA 1: Underground X-ray ore pre-concentration
SCREEN | Recovery losses (class 10): 0.37; Missing best-practice baseline (class 9, ceiling ratio): 1.017 against 1.5 needed; Market/fixed cost (class 8, concentrator capacity value): about 0, because Talnakh concentrator is already being expanded from 10 to 18 Mtpa; Pilot provability (class 13): 59 zero-failure trials to show <5% loss, feasible
KILLER | waste-rejection fraction needed to break even at a 2% metal loss, on Norilsk-1 disseminated ore worth about $235/t (F2, est. prices) | required 41% mass rejected (est. $15/t processing, $1.5/t sorting) | available 15.2% mass rejected at about 98% Cu+Ni recovery (NexMetals Selebi bulk XRT test, July 2025, company claim, unaudited) | MARGIN 0.37
CHAIN | Norilsk Division full cost (ledger B), whole run-of-mine ore to the concentrator | now $8.0bn/yr | with idea ≥$7.87bn/yr, an upper bound even if 15% of the 11% processing share were removed on all ore; disseminated ore is only 2.7% of reserves (F1, F2) | RATIO 1.02
VERDICT | DEAD | The measured XRT rejection on Ni sulphide is about a third of what pays for the lost metal, and the concentrator it would free up is already being expanded, so the chain gain cannot exceed about 2%.
NEW FACT | Talnakh concentrator is to rise from 10 to 18 Mtpa by 2030–31 (third start-up complex under construction) | https://www.techinsider.ru/technologies/1648381-apdeit-promyshlennosti-kak-iskusstvennyi-intellekt-ustroilsya-na-rabotu-na-gorno-obogatitelnuyu-fabriku/
NEW FACT | Selebi Cu-Ni-Co bulk XRT: 15.2% of mass rejected, head grade up more than 15%, about 98% recovery claimed (company release, unaudited) | https://www.newsfilecorp.com/release/260258

IDEA 2: Re-levelling thaw-tolerant foundations
SCREEN | Frozen-ground strength / thaw settlement (classes 4 and 12, life settlement against stroke): 0.25–0.5; Season window (class 1, seasonal movement against stroke): 1.67; Missing best-practice baseline (class 9): adjustable jack and space-frame foundations are already standard guidance in Alaska and Nunavut, ceiling ratio 1.02
KILLER | settlement against jack stroke over the structure's life, with the ground allowed to thaw in ice-rich Yamal/Norilsk ground (tabular ice 10–20 m, F97; kit thaw strain 0.2–0.4) | required 600 mm (3 m extra thaw × 0.2; 1.2 m at strain 0.4) | available 300 mm stroke (idea) | MARGIN 0.5
CHAIN | Norilsk/Yamal full cost with today's adjustable foundations, thermosyphons and piles (ledger B; Hjort: road upkeep loss about $0.23bn/yr across all of Russia, F270) | now $8.0bn/yr | with idea ≥$7.84bn/yr, even if the est. 2% foundation share were removed entirely | RATIO 1.02
VERDICT | DEAD | The stroke covers seasonal movement (180 mm, F101) but not thaw settlement once ice-rich ground is allowed to thaw; it does not apply to heavy plant; it already exists as northern practice; and foundations are too small a cost share to move the chain.
NEW FACT | The Nunavut permafrost guide lists pad-and-wedge, space-frame and screw-jack foundations as existing adjustable options needing yearly adjustment; Alaska calls adjustable foundations a "standard recommendation" | https://climatechangenunavut.ca/sites/default/files/permafrost_nunavut_eng_reduced_size_0.pdf ; https://www.commerce.alaska.gov/web/Portals/4/pub/NFIP/Foundations%20for%20Building%20on%20Permafrost%202022%20Version.pdf

IDEA 3: Powered-first staged Baimskaya
SCREEN | Market/fixed cost (class 8, six-tenths scale penalty): ratio 0.40; Season window (class 1, Pevek NSR window 3–4 months, F148; 1.842 Mt/yr terminal, F147): about 0.1 Mt/yr of concentrate fits easily, margin >10; Spare power after Bilibino (no kit class, own calculation): 0.26 in winter, 1.33 in summer
KILLER | spare firm MW at Akademik Lomonosov in winter after Bilibino NPP shut down (Dec 2025) | required 30 MW (idea; 33 MW at the 36 kWh/t implied by Baimskaya's own plan for 3 working 106 MW units for 70 Mtpa) | available 7.8 MW = 44 MW in winter heat mode − 0.84 × 43 MW average node load (377 GWh in 2022, Chukotka power scheme 2023–27; Lomonosov carries 84% of the node in 2026, m-atom; 44/76 MW, Rosatom) | MARGIN 0.26
CHAIN | KAZ Minerals full 60–70 Mtpa plan (ledger D, about $6,500/t Cu before gold credit) | now $6,500/t Cu | with idea about $16,200/t Cu: 6.5 Mtpa costs $2.1bn by six-tenths scaling, for 24.6 kt Cu/yr at 0.43% and 88% recovery, capital charge 0.124 | RATIO 0.40
VERDICT | DEAD | After Bilibino closed there is about 8 MW of winter spare capacity against the 30 MW needed, the phase still needs the Bilibino–Peschanka line and the road, and the small plant costs 2.5 times more per tonne of copper.
NEW FACT | Chaun-Bilibino node consumption was 377 GWh in 2022 (+11.2%), forecast 715 GWh by 2027 (moderate case) | https://base.garant.ru/406977582/53f89421bbdaf741eb2d1ecc4ddb4c33/
NEW FACT | Akademik Lomonosov delivers about 76 MW to shore without heat supply and about 44 MW at maximum heat supply; it generated 250 GWh in 2024 (194 GWh in 2023) | https://goarctic.ru/work/pates-akademik-lomonosov-na-chukotke-za-5-let-vyrabotala-okolo-milliarda-kilovatt-chasov-elektroener/
NEW FACT | After Bilibino unit 4 stopped in late Dec 2025, its load moved to Lomonosov, which covered 84% of the node's demand in early 2026 | https://m-atom.ru/article/4421

IDEA 4: Crusher-conveyor underground ore haulage
SCREEN | Missing best-practice baseline (class 9, ceiling ratio): 1.06; Pilot provability (class 13): 59 zero-failure shifts to show <5% belt downtime, feasible in 3 years; Belt availability against maximum lump size: no measured Talnakh data, not computed, treated as about 1
KILLER | cost share that underground haulage must remove to reach 1.5x | required 33% of full cost | available about 5.6% (est.: 30% of the 6% energy share + 10% of the 27% labour share + 10% of the 11% spares share; ledger B) | MARGIN 0.17
CHAIN | Norilsk Division full cost with LHD/truck haulage to ore passes and shafts (ledger B) | now $8.0bn/yr | with idea $7.52–7.76bn/yr (the idea's own 3–6% claim, which matches the 5.6% ceiling) | RATIO 1.06
VERDICT | DEAD | Even taken at its own claim, the idea cuts full cost by at most 6%, so the ratio of 1.06 is below the 1.1 kill line; LHDs from stope to crusher are still needed.
NEW FACT | Kola's Oleniy Ruchey has a working crusher-conveyor complex that is extended as the underground mine develops, a domestic precedent | https://fertilizerdaily.ru/20200907-olenij-ruchej-oprobuet-novyj-kompleks

Sources:
- [Nunavut permafrost guide](https://climatechangenunavut.ca/sites/default/files/permafrost_nunavut_eng_reduced_size_0.pdf)
- [Alaska – Foundations for Building on Permafrost 2022](https://www.commerce.alaska.gov/web/Portals/4/pub/NFIP/Foundations%20for%20Building%20on%20Permafrost%202022%20Version.pdf)
- [NexMetals Selebi XRT release](https://www.newsfilecorp.com/release/260258)
- [MDPI Minerals sensor sorting study](https://www.mdpi.com/2075-163X/16/1/13)
- [Techinsider – Talnakh concentrator](https://www.techinsider.ru/technologies/1648381-apdeit-promyshlennosti-kak-iskusstvennyi-intellekt-ustroilsya-na-rabotu-na-gorno-obogatitelnuyu-fabriku/)
- [Chukotka power scheme 2023–27](https://base.garant.ru/406977582/53f89421bbdaf741eb2d1ecc4ddb4c33/)
- [m-atom – Lomonosov covers 84%](https://m-atom.ru/article/4421)
- [GoArctic – Lomonosov output](https://goarctic.ru/work/pates-akademik-lomonosov-na-chukotke-za-5-let-vyrabotala-okolo-milliarda-kilovatt-chasov-elektroener/)
- [Korabel – Lomonosov output](https://www.korabel.ru/news/comments/pates_akademik_lomonosov_za_pyat_let_vyrabotala_okolo_milliarda_kvt_ch_elektroenergii.html)
- [World Nuclear News – SMRs to power Arctic development](https://world-nuclear-news.org/Articles/SMRs-to-power-Arctic-development)
- [EastRussia – Bilibino–Peschanka line](https://www.eastrussia.ru/news/stroitelstvo-vl-dlya-baimskogo-goka-zavershaetsya-na-chukotke-/)
- [Fertilizerdaily – Oleniy Ruchey conveyor](https://fertilizerdaily.ru/20200907-olenij-ruchej-oprobuet-novyj-kompleks)