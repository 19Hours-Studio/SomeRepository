=== REVIEW ===
IDEA 1: Develop by value per tonne
DEFECT | FATAL | Vostok Oil is filed under "rail or pipeline access", but its pipeline ends at an NSR terminal, so all of its oil leaves by ice-class tanker. It sits on the same constraint the idea says it avoids, and Idea 3 itself limits it to about 1.2–1.54 Mt/y per hull. | The Vankor–Payakha–Bukhta Sever line (770–790 km) runs to an Arctic export terminal; the first cargo was loaded onto the 69 kt tanker Valentin Pikul in Sept 2026 (gCaptain; Neftegaz.ru)
DEFECT | MAJOR | The ranking assumes rail freight is cheaper than the NSR. Elga coking coal travels about 1,500 km of rail to the Pacific ports. Tariffs of that length are about $40/t or more, which is above the idea's own $30/t NSR figure. So the ordering rule does not favour rail on freight cost per tonne. It is really about who carries the capacity risk, and that is not argued. | $30/t has no source; long-haul RZD coal tariffs are about 3,000–4,000 RUB/t (my estimate, not sourced in the text)
DEFECT | MAJOR | The $30/t freight figure has no source, and for ice-class LNG it is too low. At a typical $1–1.5/MMBtu Arc7 cost (my estimate, not sourced), freight is about 10–15% of LNG value, not 7%. | python: $30 reproduces 33/18/7/1.3/0.3% only if prices are $91, $167, $429, $2,308 and $10,000 per t
DEFECT | MAJOR | The "re-ordering" is the status quo, so it changes no decision. Udokan, Baimskaya, Elga and Vostok Oil are already producing or under construction, Tomtor and Syradasay are already waiting, and Arctic LNG 2 is already limited by ships. | Udokan began producing cathode in Sept 2026 after a fire delay (Moscow Times, 2 Sept 2026); Vostok Oil was commissioned in 2026
DEFECT | MINOR | Red Dog argues against the rule. It ships about 1.24 Mwmt a year of low-value bulk concentrate in a 100-day ice-limited season by stockpiling, which is exactly the model the idea tells Syradasay to defer. The 950 kt storage figure is one of three published figures (850 kt, 950 kwmt, 1.2 Mt). | Teck; U Waterloo; AIDEA 2021/2023 fact sheets
SURVIVES | NSR 37.02 Mt in 2025 (−2.3%, Gekon/Kommersant); Arctic LNG 2 at about 1.05–1.3 Mt in 2025 (14–17 cargoes); the freight shares are correct arithmetic given the implied prices.
RATIO | 1.01 | Almost every project it names is already sequenced this way, and moving Vostok Oil into the right bucket removes most of what remains.
KNOWN | yes | Russia's current project sequencing, plus the NSR cargo plan revisions (Rosatom/Minvostokrazvitiya).
NEW FACT | Vostok Oil's first Bukhta Sever cargo went onto the 69 kt Arc6 Valentin Pikul; a roughly 120 kt Aframax, Akademik Gubkin, waited for the second cargo | gCaptain Sept 2026; Baird Maritime

IDEA 2: Pre-staged flood-crest barges
DEFECT | MAJOR | It never counts the cost of holding the cargo 7–8 months longer. Diesel worth about 70,000 RUB/t, held 8 months at a key rate of about 17%, costs about 7,900 RUB/t. That is as large as or larger than the claimed saving of 1,600–8,200 RUB/t. | python: 70,000 × 0.17 × 8/12
DEFECT | MAJOR | The 2.5 m wintering depth leaves almost no water under the ice. End-of-April ice on the lower Yana, Indigirka and Kolyma averages 1.42–1.67 m, which leaves 0.8–1.1 m below it before the winter stage drop. A loaded barge drawing 1–2 m is frozen in or grounded, and its hull takes ice load. | AARI forecasts: Yana (Yubileynaya) 152 cm mean, Indigirka (Chokurdakh) 167 cm, Kolyma (Chersky) 142 cm
DEFECT | MAJOR | The barges sit at river mouths through breakup and ice drift. Ice jams and jam floods are the main breakup hazard on these rivers, and fuel barges frozen into a water body for 8 months bring a spill risk and permitting exposure that are not mentioned. | Lena basin experience; 2004 high water flooded fuel and dry-cargo terminals and cost about 2 weeks (RG/Kommersant)
DEFECT | MINOR | The 35–62% loss for a 5–10 day delay comes from an unstated model. A linear 12-day recession gives 42–83%. | python
SURVIVES | 4,700–11,300 / 3,100 = 1.52–3.65 is correct arithmetic.
RATIO | 1.05 | After inventory carrying cost the saving on the leg is about 0–1.4×, and that leg is a small share of delivered cost.
KNOWN | partly | Yakutia already winters fleet in backwaters (zatons) and leaves cargo on barges after failed navigations; early-delivery and spring-flood runs are part of the northern supply operation (Lena Basin Administration). Not verified in detail.

IDEA 3: Size Sever to hulls
DEFECT | MAJOR | It is benchmarked against Rosneft's 30 Mt/y plan, not against current practice. Vankor oil already goes south today, so the "$29/t on every Vankor tonne kept south" saves nothing against what happens now. | the idea's own text: "stays on the existing Vankor–Purpe line"
DEFECT | MAJOR | It assumes only the 69 kt Arc hulls can lift oil. In summer and autumn, 120 kt Aframaxes also lift at Sever, so the 1.54 Mt/y per hull ceiling and the "19 hulls" figure understate seasonal capacity. | Akademik Gubkin (~120 kt) waiting at Sever, Sept 2026 (gCaptain)
DEFECT | MINOR | The $80–190 per tonne of deferred capacity uses inconsistent denominators. $5.8bn over 25 Mt/y × 3 y is $77/t; $190 only comes out if $5.8bn is divided by the low case's 30 Mt. | python: 2.4/30 = 80; 5.8/75 = 77; 5.8/30 = 193
DEFECT | MINOR | The $57 vs $86/t comparison ignores Kozmino and ESPO capacity, Transneft's quota allocation and eastbound NSR summer voyages to China. The 25 Mt/y Vankor–Purpe rating is not sourced (my search did not confirm it). | none found
SURVIVES | 365/15.5 × 69 kt = 1.62 Mt/y (1.54 implies about 95% availability), and the 20-day cycle gives 1.26 Mt/y; 30/1.54 = 19.5 hulls; the 69 kt deadweight is confirmed.
RATIO | 1.00 | Against current practice nothing changes. Only the PV avoided against Rosneft's plan remains, and that depends on unsourced capex.
KNOWN | partly | Rosneft is already ramping Sever in stages to tanker deliveries from Zvezda.

IDEA 4: Shared nuclear grids replace site diesel
DEFECT | MAJOR | For Baimskaya this is already the plan. Four floating units with RITM-200S reactors, the first due in 2028, are dedicated to the mine, so the 1,900 $/t Cu saving is not new against current practice. The reactor type is wrong: it is RITM-200S, 2 × about 58 MWe per FPU-106 unit, not RITM-200M. | WNN; 3dnews Jul 2026 (first RITM-200S shipped to the yard)
DEFECT | MAJOR | The grid has no spare capacity before the new units arrive. Akademik Lomonosov (70 MW) is replacing Bilibino NPP for Pevek and Bilibino, and the two single-circuit 110 kV Pevek–Bilibino lines (987 km), first due in 2020 and then in 2023, are still under construction. The proposed 3–5 year test therefore cannot start until those lines exist. | Government Decree No. 231 (2019); Interfax; Neftegaz (second line still being built)
DEFECT | MAJOR | 9.6 RUB/kWh is a regulated or contract tariff, not full cost. Line capex of 150–250 km per mine and the Far East tariff subsidy are left out. | unsourced
DEFECT | MINOR | The copper saving is compared against "diesel-only Kupol", which is a gold mine. | the idea's own text
SURVIVES | (26 − 9.6) × 9.6 MWh = 157k RUB = $1,850/t Cu at 85 RUB/$ ($1,660 at 95); 0.22 kg/kWh is a plausible plant-level figure; the Diavik and Raglan figures are plausible.
RATIO | 1.05 | The Baimskaya part adds nothing beyond the existing plan. A modest gain remains for Kyuchus and grid-adjacent gold mines once the lines and units exist.
KNOWN | yes | The Chaun–Bilibino hub plan, Baimskaya's floating units, the Yakutia RITM-200N plant for Kyuchus, and the Bilibino–Peschanka 110 kV line (EastRussia).

IDEA 5: Shaft-bottom XRT sorting, hoist-bound mines
DEFECT | MAJOR | Hoisting the same tonnage while rejecting waste means mining 1.11–1.40× more ore underground. Stoping, development, ventilation and cooling at about 2 km depth must all grow by that much, but only the sorter cost is counted. | python: mined = 1/(1 − 0.65r) = 1.108 and 1.401
DEFECT | MAJOR | The rejects are coarse lumps, roughly 10–100 mm, produced at the shaft bottom. Norilsk's hardening backfill is made at surface plants and sent down boreholes, so using the rejects needs an underground crushing and backfill plant plus haulage up to stopes above. None of this is costed. | 0.40 t of rejects per t hoisted at 44% rejection (python)
DEFECT | MAJOR | Applying it to "massive ore" contradicts the ore: massive sulfide has little internal waste, so 15–44% rejection is only possible on dilution. The 150 t/h domestic XRT unit has no source. I found only a Urals prototype and a Bourevestnik application note, with no throughput given. | RG 2025; bourevestnik.ru application note
DEFECT | MINOR | "Hoist is the limit" at Skalisty and the Talnakh deep levels is asserted, not shown. | none
SURVIVES | ×1.094 and ×1.364 metal hoisted and the NPV of ×1.083–1.307 (with shorter life) reproduce exactly; rejects ≤0.41 t/t reproduces.
RATIO | 1.05 | The metal gain is real, but extra mining and backfill-plant capex take away most of the 1.2–1.8× claim.
KNOWN | partly | Underground pre-concentration has been studied (Selebi and other XRT tests); not deployed at Norilsk.

IDEA 6: Ore sorting plus dry-stack tailings
DEFECT | FATAL | The cited test results contradict the claimed recovery. Rejecting 70% of the mass while gold grade rises only 1.5–1.6× means only 45–48% of the gold is kept, a 52–55% loss. At the assumed 50% rejection the same upgrade gives a 20–25% loss, not 1–5 percentage points. | python: 0.3 × 1.5 to 1.6; 0.5 × 1.5 to 1.6
DEFECT | MAJOR | The cost claim breaks once that loss is counted. Halving comminution, at about 35% of cost, cuts cost to about 0.83×, but recovering only 0.75–0.80× the gold raises cost per oz by 3–10%. | python on the idea's own data
DEFECT | MAJOR | The benchmark is wrong: Fort Knox irrigates its heap all year through buried drip lines. It does not "leach in season". | Kinross 6-K 2015/2018
DEFECT | MINOR | "Frozen fine ore" is not among the causes the Eagle review board named: poor drainage, over-steepened slope, rising water table, poor ore quality, and a lift at 975 m. Greens Creek is not on permafrost. No domestic maker of large filter presses is named, and filtered tailings at Natalka scale (>20 kt/d) is unproven. | IRB report 2 Jul 2025 (Northern Miner, CBC)
SURVIVES | Eagle slide volume of 5.95 Mm³ (11.3 Mt dry) is confirmed; dry stacking at Raglan and Pogo holds.
RATIO | 0.97 | At the grade upgrade it cites, extra metal loss outweighs the processing savings; only rejects at tailings grade, as at Dukat, would make it positive.
KNOWN | yes | Bourevestnik and RADOS sorters in Russian trials; dry stacks at Raglan, Pogo and Greens Creek.

IDEA 7: Design for warming ground, with monitoring
DEFECT | MAJOR | The proposed 3-year pad test cannot show the effect. Warming of 0.039 °C/yr gives about 0.12 °C over 3 years, and foundation failures are rare events, so settlement differences between pads will be inside measurement noise. Detecting the claimed 20–50% life loss needs decades or hundreds of foundations. | python: 0.039 × 3
DEFECT | MAJOR | The main value figure, 20–50% of design life lost, is the author's own assumption. The only study I found implies about 5–6 years earlier degradation per +1 °C, which is roughly 20% of a 30-year life, the bottom of the range. | BMSTU Eng. Journal 306
DEFECT | MINOR | "Size to end-of-life ground temperature" is already moving into code: SP 25.13330.2020 Change No. 3 (in force 14 June 2026) adds forecasting under a changing climate. Udokan is described in sources as a permafrost deposit, which contradicts "matters less". "Thermosyphons do nothing in summer" is how they are designed to work, not a risk. | normacs.info/ФЦС; Udokan sources
SURVIVES | GTN-P +0.39 ± 0.15 °C/decade; 1.4 bn/165 = 8.48 M RUB per object; damages of about 146 bn RUB; Streletskiy 16.7 + 67.7 bn USD.
RATIO | 1.01 | It is mostly existing code and Nornickel practice, with a small cost of a few tenths of a percent of capex.
KNOWN | yes | Nornickel's post-2020 foundation monitoring, the state permafrost monitoring system, and SP 25.13330 Change No. 3.

IDEA 8: Diesel-sized first line, nuclear expansion
DEFECT | FATAL | The energy balance does not close. 117 kt of diesel gives 532 GWh (60.7 MW average, 35.5 kWh/t). At Idea 9's 46.7 kWh/t, 15 Mt/y needs about 700 GWh, which is 80 MW average, i.e. 100% load on 80 MW of leased gensets with no reserve, and about 155 kt of diesel. | python
DEFECT | MAJOR | Bulk fuel tankers cannot back-haul concentrate. With separate fleets it takes about 3,900 fuel loads at 30 t plus about 7,240 concentrate loads at 40 t, about 11,100 loads (about 30 a day), not 7,000. | python
DEFECT | MAJOR | Coarse grind with copper recovery staying at 87.6% (67 of 76.5 kt contained) is inconsistent. Idea 9 for the same plant implies 77%. At 77%, output is about 59 kt Cu and the margin drops by roughly $0.06–0.08bn a year. | python: 48 / (12.2 × 0.51%)
DEFECT | MAJOR | The baseline is set up to lose. "$8bn idle costing $1.2bn a year" charges the whole project's capital to the delay, including line 2, the port and the road, which are not all complete either. It also ignores grid power from Chaun–Bilibino via the Bilibino–Peschanka line. Tankage of about $170m and genset lease costs are not netted out of the $0.52bn. | the idea's own text; EastRussia (Bilibino–Peschanka line)
SURVIVES | $0.30/kWh ↔ $1,364/t delivered diesel; 174k m³ ≈ 15 months of use; 20 a day and 78 a day reproduce given 7,000 loads.
RATIO | 1.02 | A small life-of-mine gain if the units slip, after fixing throughput and costs.
KNOWN | partly | Diesel bridging before grid or nuclear power is common practice (Kupol, Raglan); not announced for Baimskaya.

IDEA 9: Gated diesel bridge plus pooled spares
DEFECT | MAJOR | The diesel figure contradicts the stated load. 65 MW average at 0.225 kg/kWh is 128 kt/y, not 146; 146 kt implies 74 MW, close to the 80 MW ceiling. Fuel cost and tankage are therefore overstated, or the throughput is. | python
DEFECT | MAJOR | The "35% chance of no gain" looks too high. The first RITM-200S was only shipped to the shipyard in July 2026, so mooring trials of two units by Q4 2027 are unlikely, and the gate is close to decided already. The expected value then depends almost entirely on how long the slip lasts, which is not sourced. | 3dnews 27 Jul 2026; WNN (target slid from 2027 to 2028)
DEFECT | MAJOR | "6.3 t Ni-eq lost per machine-hour" assumes every hour a machine is down is lost output. Underground fleets carry standby units, so the loss only counts where the fleet is the bottleneck, and +8 to +29 kt is unsupported. | none sourced
DEFECT | MINOR | A −0.85% group cost change does not follow from +15 kt at $5.4k. It needs a base of about 857 kt Ni-eq and gives −0.80%. The Bering-route diesel still has to pass Long Strait and the Ayon ice massif, which need icebreaker escort. | python
SURVIVES | RITM-200S is the correct reactor; concentrate at 21.6% Cu wet and 5–6 × 40 kt ships are consistent; $0.31/kWh ↔ about $1,380/t diesel; break-even at a 0.44-year slip is consistent with about $173m fixed cost over a margin of about $0.39bn a year.
RATIO | 1.02 | Copper gains about 2–4.5% of life-of-mine cost if the units slip; the Ni-eq gain is under 1%.
KNOWN | partly | Nornickel is localising spares and has the BelAZ joint venture; diesel bridging is common at Arctic mines.

Most of the figures above I reproduced in Python. Several checks did not come back clean:
- I could not open the gCaptain article directly (the proxy blocked it), so the Vostok Oil details come from search summaries. One source dates the commissioning to Sept 2025, not 2026.
- I could not confirm the 25 Mt/y Vankor–Purpe rating, the Udokan permafrost thickness, or any throughput for a domestic XRT sorter.
- The rail tariff, Arc7 freight and inventory interest figures are my own estimates, as marked.

Sources:
- [Red Dog storage – U Waterloo](https://uwaterloo.ca/wat-on-earth/node/296); [Teck supply chain](https://www.teck.com/news/stories/2014/managing-the-supply-chain-above-the-arctic-circle); [AIDEA DMTS fact sheet](https://www.aidea.org/Portals/0/ProjectFactSheets/DMTS%20Project%20Fact%20Sheet%202023.pdf)
- [Eagle IRB – Northern Miner](https://northernminer.com/news/board-cites-poor-drainage-for-eagle-gold-leach-failure/1003880103); [CBC](https://www.cbc.ca/1.7575769); [PwC IRB report](https://www.pwc.com/ca/en/services/insolvency-assignments/victoriagold/independent-review-board-report.html)
- [WNN RITM-200S](https://world-nuclear-news.org/articles/nuclear-fuel-development-completed-for-ritm-200s-f); [3dnews RITM-200S shipped](https://3dnews.ru/1142454)
- [gCaptain Vostok Oil](https://gcaptain.com/russia-launches-massive-vostok-oil-project-marking-new-arctic-shipping-era/); [Baird Maritime](https://www.bairdmaritime.com/shipping/tankers/russian-built-arctic-oil-tanker-sanctioned-by-us-delivered-to-new-owner); [Neftegaz](https://neftegaz.ru/news/view/138508/)
- [High North News NSR 2025](https://en.highnorthnews.com/business/northern-sea-route-2025-season-concludes-with-stable-transit-traffic-amid-challenging-ice-conditions/1096859); [Gas Processing News Arctic LNG 2](https://gasprocessingnews.com/news/2025/11/update-russias-arctic-lng-2-ships-14th-cargo-in-2025-despite-western-sanctions)
- [Kinross 6-K 2015](https://www.sec.gov/Archives/edgar/data/0000701818/000157104915002523/t81903_ex99-2.htm); [Kinross 6-K 2018](https://www.sec.gov/Archives/edgar/data/0000701818/000114420418033836/tv496119_ex99-2.htm)
- [AARI ice forecast 2012](https://old.aari.ru/resources/f0021/2012_spring.pdf); [AARI 2014](https://old.aari.ru/resources/f0021/2014_spring.pdf); [RG 2004 Yakutia](https://rg.ru/2004/10/20/saha.html)
- [normacs SP 25.13330 changes](https://www.normacs.info/news/78881); [BMSTU Eng. Journal](https://engjournal.bmstu.ru/articles/306/306.pdf)
- [Decree 231 Pevek–Bilibino](https://rulaws.ru/goverment/Postanovlenie-Pravitelstva-RF-ot-02.03.2019-N-231/); [Interfax](https://www.interfax.ru/business/675037); [EastRussia Baimskaya line](https://www.eastrussia.ru/news/stroitelstvo-vl-dlya-baimskogo-goka-zavershaetsya-na-chukotke-/)
- [Moscow Times Udokan cathode](https://ru.themoscowtimes.com/2026/09/02/udokan-nachal-proizvodstvo-katodnoy-medi-posle-zaderzhki-iz-za-pozhara-a205107); [RG XRT prototype](https://rg.ru/2025/03/26/reg-urfo/rentgen-vidit-pustuiu-porodu.html); [Bourevestnik XRT note](https://bourevestnik.ru/upload/iblock/174/melat4es6e7eukiyo1b38imrekjjmx9r/Application-note_Rentgenoabsorbtsionnaya-olovo_medsoderzhashchey-rudy-Pravourmiyskogo-mestorozhdeniya_rev.1-_szhatyy_.pdf)