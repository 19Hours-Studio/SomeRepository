=== REVIEW ===
IDEA 1: Kupol winter-road toll hub

DEFECT | FATAL | The first target is wrong. Kekura is not a greenfield site waiting on a mill or on Bilibino power: Highland Gold started its own 0.8 Mt/y mill there in March 2023 (about 85% design recovery), and a branch of the 235 km Bilibino–Peschanka line now powers it, replacing its diesel. So the $322/oz saving is mostly spent already, and the $1,018/oz stand-alone baseline does not exist. | [biznes-gazeta 29.03.2023](https://biznes-gazeta.ru/?id=location.view&obj=905697ad890a3743bf6bd5e1bb4996b8), [zolteh](https://zolteh.ru/news/fabrika_na_mestorozhdenii_kekura_na_chukotke_gotova_k_zapusku/), [prochukotku](https://prochukotku.ru/news/promyshlennost/mestorozhdenie_kekura_na_chukotke_poluchilo_elektroenergiyu_ot_lep/)

DEFECT | MAJOR | The sorter step destroys value. Rejecting 7% of the gold costs about $50 per ROM tonne (0.07 × 0.241 oz/t × 0.85 recovery × $3.5k/oz). It saves only about $12/t of haul (0.35 × 160 km × $0.22) plus about $7/t of milling. At the stated 7.5 g/t, a single 7% loss is about $260/oz of revenue foregone, which is more than the $155/oz advantage claimed. | python recompute

DEFECT | MAJOR | The cap does not "match the Tibbitt–Contwoyto record". It is 14% more loads and 1.5× the tonnage. The 2007 record was 10,922 loads, 330 kt and about 4,783 t/day in 69 days. The idea needs 12,500 loads, 0.5 Mt and 6,667 t/day in 75 days. It also assumes 40 t loads against about 30–37 t on the TCWR (2018: 304,685 t in 8,300 loads, 36.7 t/load). And it runs overland through mountains, not mostly on lake ice. | [JVTC poster](https://jvtcwinterroad.ca/wp-content/uploads/2021/01/2021-Winter-Road-Poster.pdf), [NNSL](https://nnsl.com/nwtnewsnorth/winter-road-haul-amounts-to-257176-tonnes-7260726)

DEFECT | MAJOR | The 75-day window is assumed, not measured for a Kekura–Kupol route. The reference road averages 67 days. A warm winter in 2026 shut it early. At 67 days and 37 t loads, the corridor carries about 0.4 Mt, roughly 20% below the cap. | [Skillings](https://skillings.net/arctic-logistics-crisis-record-warmth-shuts-diamond-mine-ice-roads), [Wikipedia TCWR](https://en.wikipedia.org/wiki/Tibbitt_to_Contwoyto_Winter_Road)

DEFECT | MINOR | The $177/oz haul figure ignores the sorter. It only reproduces for unsorted ore at about 82% recovery (35.2 $/t ÷ (0.241 × 0.825)). With the 65%/93% sort it is $113–120/oz. The 300 km "advantage $20–45/oz" also fails: a linear haul cost gives about −$20/oz. | python: 177×300/160 = $332/oz against $322/oz saved

DEFECT | MINOR | The tailings dam is not avoided, only moved to Kupol. 0.5 Mt/y over 10 years needs about 3.5 Mm³ more permafrost dam capacity at Kupol. Kupol's own mine life was put at 2025 (Kinross 40-F), so the "marginal 1.7 MW" holds only while Kupol's own ore carries the fixed costs. | [Kinross 40-F FY2021](https://www.sec.gov/Archives/edgar/data/701818/000110465922041156/kgc-20211231xex99d1.htm)

DEFECT | MINOR | Equipment and fleet are not costed. 167 loads/day on a 15.8 h round trip needs about 130 domestic 40 t tractor-trailers, idle about 290 days a year. The mine-only satellite still needs its own diesel for mining, crushing, the sorter and the camp. The 160 km distance and Kekura's 7.5 g/t "second stage" are unsourced. | python

SURVIVES | 1.7 MW and 3.4 kt/y diesel: about 0.228 kg/kWh, about 30 kWh/t at 0.5 Mt. Arithmetic: 167 loads/day, 40 t/load, 0.863/1.018 = 0.85. Thawing frozen ore adds only about 0.7 MW thermal on average.

RATIO | ≈0.85 | Against the best current practice, Kekura's own grid-fed mill whose capex is already spent (about $700–800/oz). The idea comes to about $890/oz: $863 plus the sorter loss. For a truly mill-less satellite under the tonnage cap it is at best about 0.95.

KNOWN | partly | Kupol has milled Dvoinoye ore trucked about 100 km since 2013. Highland Gold has owned both Kupol and Kekura since 2022. | [Kinross 40-F](https://www.sec.gov/Archives/edgar/data/701818/000110465922041156/kgc-20211231xex99d1.htm), [Interfax](https://www.interfax.ru/business/833256)

NEW FACT | Bilibino's replacement power centre is a 25 MW diesel plant (56.75 Gcal/h of heat) burning about 30,000 m³ of diesel a year. The nuclear plant was stopped in 2025. | [eprussia](https://www.eprussia.ru/news/base/2025/7077732.htm)

NEW FACT | Kekura lies about 120 km south of Bilibino. JORC reserves were 2.009 Moz at end-2017. | [zolteh](https://zolteh.ru/news/fabrika_na_mestorozhdenii_kekura_na_chukotke_gotova_k_zapusku/)

IDEA 2: Diesel-sized first line, nuclear expansion

DEFECT | MAJOR | The diesel figure breaks the energy balance. 117 kt/y at 80 MW (700.8 GWh) implies 0.167 kg/kWh, which no diesel genset achieves; leased units run 0.20–0.25. Correcting it gives either 140–175 kt/y (+20–50% fuel, tankage, tanker calls and road loads) or only 53–67 MW average, which is about 11–14 Mt/y at the stated 46.7 kWh/t. | python

DEFECT | MAJOR | The road load count does not reproduce. 268 kt of concentrate at 25% Cu plus 117 kt of diesel over 7,000 loads means 55 t per load. Concentrate can't ride in fuel tankers unless a swap system (ISO tank plus concentrate box) is designed and costed. Separate loads come to about 10,600 a year, or 11,500 at 22% Cu. Consumables add about 50 kt (about 1,250 loads). On a winter road only, that is 118–140 loads/day, near the TCWR record rate. | python

DEFECT | MAJOR | Recovery is assumed. The text gets 87.6% Cu recovery (67/76.5 kt) from a coarser grind than design, on a SAG mill built for a 35 Mt/y line running at 15 Mt/y. Each 4 points of lost recovery removes about 3 kt Cu and about $30m/y of margin. The 0.51% head is not sourced. | [KAZ BFS 2021](https://www.kazminerals.com/completion-of-baimskaya-bankable-feasibility-study/): 70 Mt/y in two lines

DEFECT | MAJOR | The bridge window may be short, and the full plan's power is underestimated. The full plan needed 356 MW (44.6 kWh/t), against 440 MW installed on the floating units. Floating-unit dates slipped from 2026 to 2028–29, with some sources at 2028–31. Line 1 is planned for end-2028. So the years of margin per slip could be 0–2, while gensets, about 174k m³ of tankage and its Arctic tank-farm capex (unpriced; my rough guess $150–250m) are paid up front. | [paluba](https://paluba.media/news/79251), [neftegaz](https://neftegaz.ru/news/spg-szhizhennyy-prirodnyy-gaz/625765-elektrichestvo-na-baimskiy-gok-na-chukotke-budet-postavlyat-plavuchaya-spg-stantsiya/), [Bosfor](https://ao-bosfor.ru/baimskaja/)

DEFECT | MINOR | The margin rests mostly on gold and on prices the text doesn't state. Solving back gives Cu about $9.7k and Au about $4.0k. The gold credit is $5.8k/t Cu, about 75% of the $7.8k/t gross cost. TC/RC, payability, freight, sanctions discounts and MET are not shown. | python

DEFECT | MINOR | $0.30/kWh is at the low edge. Delivered diesel at about $1.3k/t × 0.22 kg/kWh gives $0.29/kWh for fuel alone. Adding lease and O&M makes about $0.33, which is +$21m/y or +$0.3k/t Cu. | python estimate

DEFECT | MINOR | Concentrate can leave Pevek only in the 4–5 month navigation season. That needs about 150–180 kt of concentrate storage at the port, which is not provided. | python

SURVIVES | 46.7 kWh/t is consistent with the full plan's 44.6 kWh/t. 6 calls × 19.5 kt is plausible for Pevek tankers. 20 loads/day on an all-season road is plausible if the road exists. The $1.2bn/y idle carry is 15% × $8bn.

RATIO | ≈0.8 | Against the nuclear full plan at $2.0k/t Cu: corrected bridge cost is about $2.4–2.6k/t Cu (power +10–30%, recovery −4 points). It is still far better than idle.

KNOWN | partly | Baimskaya's 2021 EIA covered a "diesel power plant and 35 kV switchgear" at the 330 kV Baimsky GOK substation. Earlier plans used 15–20 MW of diesel for construction loads, and a floating LNG plant was considered in 2020. | [RPN](https://rpn.gov.ru/regions/49/public/221120210805126-5767615.html), [neftegaz](https://neftegaz.ru/news/spg-szhizhennyy-prirodnyy-gaz/625765-elektrichestvo-na-baimskiy-gok-na-chukotke-budet-postavlyat-plavuchaya-spg-stantsiya/)

NEW FACT | The 2021 BFS put capex at $8.5bn, start-up by end-2027, and two lines brought on 12–18 months apart. | [KAZ Minerals](https://www.kazminerals.com/completion-of-baimskaya-bankable-feasibility-study/)

NEW FACT | The Bilibino–Peschanka line (235 km) is finished and links Baimskaya's site to the Bilibino diesel node. | [prochukotku](https://prochukotku.ru/news/promyshlennost/mestorozhdenie_kekura_na_chukotke_poluchilo_elektroenergiyu_ot_lep/)