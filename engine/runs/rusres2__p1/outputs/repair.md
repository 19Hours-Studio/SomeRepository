Idea 1 works within a limited regime. Idea 2 fails as originally written, but works once the starter is redefined as the first line of the plant now being built, run on diesel until the floating units arrive. Everything is in `repair/`: `LOG.md` (10 rounds), `NOTES.md` (check tables) and three Python scripts.

=== IDEAS ===
IDEA 1
NAME: Kupol winter-road toll hub
MECHANISM: Anchor: third-party high-grade lodes are developed as mine-only satellites. Their ore goes by winter road to the Kupol mill, which runs on its own diesel plant, so it needs none of the 8 MW the Chaun–Bilibino node has spare. Repaired design: haul radius ≤200 km, head grade ≥4 g/t, and at most 0.5 Mt per winter season per corridor. That cap comes from 12,500 loads in a 75-day season, about 167 a day, which matches the Tibbitt–Contwoyto record. Each satellite runs a domestic RADOS X-ray sorter and ships only the sorted fraction (assumed 65% of mass, 93% of the gold). The first target is Kekura's second-stage ore (7.5 g/t, 160 km west of Kupol). Kekura's feasibility study assumed grid power from Bilibino, which has now closed. Ore is stockpiled frozen at Kupol and milled all year. Haul costs $0.22/t-km, or $177/oz at 7.5 g/t. Avoiding a satellite mill, tailings dam and power plant saves $322/oz. The extra milling adds only about 1.7 MW and 3.4 kt a year of diesel at Kupol.
VALUE: Full cost is $863/oz delivered against $1,018/oz for a stand-alone Kekura-type mill (0.85×), and first gold comes about 2 years after decision against about 4 for the stand-alone mill and 4–5 for Natalka. At 300 km the advantage almost disappears ($20–45/oz).

IDEA 2
NAME: Diesel-sized first line, nuclear expansion
MECHANISM: Anchor: a diesel-sized starter on leased domestic or unrestricted gensets comes first. The nuclear-sized expansion follows when the floating units deliver, and the gensets then move to other sites. Repaired design: the starter is no longer a separate 6 Mt/y plant. That version still fails: $8.3k/t Cu net against $2.0k/t for the full plan, and a $45m a year margin on $1.08bn of capex. Instead, line 1 of the Baimskaya plant now under construction (start planned for end-2028) runs at a throughput sized to 80 MW of leased gensets. It uses the SAG mill and one of two ball mills at a coarser grind, on the highest-grade benches. That gives 15 Mt/y of ore at about 0.51% Cu (the first-decade head implied by the feasibility study), 67 kt Cu and 98 koz Au a year. It burns 117 kt of diesel a year at $0.30/kWh, which takes 6 tanker calls into Pevek and needs 174k m³ of tankage. With fuel coming in and concentrate going out on the same trucks, that is about 7,000 loads a year: 20 a day on the all-season road, or 78 a day on a winter road alone. Net cash cost is $1.95k/t Cu after gold credit. Line 1 is also commissioned on diesel, so the ramp-up is done before the reactors arrive.
VALUE: Each year the floating units slip, the bridge earns about $0.52bn of cash margin ($0.29bn at Cu $8k / Au $2.8k) from a plant whose $8bn would otherwise cost about $1.2bn a year to carry idle. Waiting idle earns nothing in those years.

=== NOTES ===
**Idea 1: Kupol winter-road toll hub**
- **Anchor kept?** Yes (pooled, mine-only satellites milled at Kupol on its own diesel). The kill test was right that 300 km is too far, so the design now limits the haul radius instead of the grade.
- **Decisive numbers:**
  - Haul cost is $0.21–0.24/t-km, estimated bottom-up in `idea1_kupol.py`. No published Chukotka winter-road tariff was found.
  - Kekura: 7.49 g/t head, 800 kt/y plant, $229m capex in the 2018 feasibility study, which assumed regional grid power. A 2022 plan had its ore milled at Kupol, 160 km east.
  - Tibbitt–Contwoyto record: 10,922 loads in a season (2007).
  - Omolon hub: its Kubaka mill has been fed from satellites over winter roads only (Sopka is 150 km away).
- **Best-baseline comparison (per oz delivered):**
  - The alternatives are (a) a stand-alone small mill on its own diesel, which is what Kekura actually built in 2024, (b) an Omolon-style hub owned by one company, and (c) a seasonal heap leach, the cheapest option but only for oxide ore.
  - Hub: $863/oz against $1,018/oz for (a) at 7.5 g/t, and $1,175/oz against $1,407/oz at 5 g/t.
- **Consistency checks:** the season length (75 days), radius, power, stockpile and diesel load all pass. Kupol's spare mill capacity and its tailings-dam life are unverified.
- **Hazards:**
  - Shorter winter-road seasons (Tibbitt–Contwoyto loses about 7 days a decade) are handled by sizing for 75 days.
  - Frozen stockpiles need breaking before milling.
  - Satellite ore may interfere with Kupol's silver-rich circuit, so recovery is not guaranteed.
  - Sampling disputes between the mill and its toll clients.
  - A large truck fleet working through the polar night.
- **Deciding unknown and cheapest experiment:**
  - The unknown is Kupol's spare mill and tailings capacity for 2026–30, together with recovery on blended feed.
  - Experiment: CIL tests at Kupol's grind on about 10 composites per satellite.
  - Then one bulk campaign of 3–5 × 100 t through the mill.
  - Also XRT sorting on about 5 t of each ore type.
- **Closest existing work:** the Omolon/Kubaka hub, Dvoinoye ore at Kupol, and Highland's 2022 Kekura-to-Kupol plan. This version adds open third-party toll access, a published rule for which lodes qualify (radius × grade × tonnage per season), sorting at the satellite, and use of Kupol's diesel to get round the Bilibino closure.
- **Verdict:** **WORKS** inside that regime.

**Idea 2: Diesel-sized first line, nuclear expansion**
- **Anchor kept?** Yes (diesel-sized first phase, nuclear-sized expansion, gensets move on afterwards). What changed is the form of the starter: line 1 of the plant being built, not a separate plant.
- **Decisive numbers:**
  - Implied first-decade head is 0.49% Cu and 0.33 g/t Au, from 300 kt Cu and 490 koz Au a year at 70 Mt/y.
  - Chukotka received 152 kt of petroleum products in 2025.
  - Nagleynyn terminal capacity is 1.842 Mt/y.
  - Start-up has slipped to end-2028, with full capacity in 2029–30.
- **Best-baseline comparison (per t Cu):**
  - The alternatives are (a) wait for the floating units (the current plan), (b) take the grid's spare (about 8 MW, trivial), and (c) the original separate starter.
  - The bridge's net cash cost of $1.95k/t Cu against nothing produced under (a) is the relevant comparison. The separate starter costs $8.3k/t.
- **Consistency checks:**
  - The added diesel is 77% on top of 2025 deliveries to Chukotka.
  - The tank farm has to sit on bedrock or ventilated pads with thermosyphons (the Ambarnaya lesson).
  - The SAG mill's ability to run at reduced load needs vendor confirmation.
- **Hazards:**
  - A diesel spill on permafrost.
  - Fuel supply depends on Pevek's navigation window.
  - Domestic 2 MW gensets may not be available in volume by 2028.
- **Deciding unknown and cheapest experiment:**
  - The unknown is the actual slip of the floating units and the lead time for leased gensets, plus line-1 performance at about 45% power.
  - The cheapest test is a mill-vendor simulation of SAG + one ball mill on 20–30 drill-core composites (grindability and flotation at the coarser grind).
- **Closest existing work:** remote diesel mines (Red Dog, DeGrussa). No source found for diesel-bridging a nuclear-powered mine.
- **Verdict:** **WORKS** as a bridge against slippage of the floating units. It is **NICHE** in that it does nothing if they arrive on time, beyond about a year of earlier ramp-up. The original separate 6 Mt/y starter **FAILS**.

Things I assumed that you should check before relying on these numbers:
- Prices: gold at $4,000/oz, copper at $10,000/t.
- Diesel delivered at $1,100/t.
- The sorting yields used in Idea 1.

Sources:
- [Highland Gold updates Kekura resource as DFS is completed (Engineering News)](https://engineeringnews.co.za/print-version/highland-gold-updates-kekura-resource-as-dfs-is-completed-2018-02-06)
- [Kekura gold project, Russia (Mining Weekly)](https://www.miningweekly.com/article/kekura-gold-project-russia-2018-03-02)
- [Ареал (компания), Wikipedia](https://ru.wikipedia.org/wiki/%D0%90%D1%80%D0%B5%D0%B0%D0%BB_(%D0%BA%D0%BE%D0%BC%D0%BF%D0%B0%D0%BD%D0%B8%D1%8F))
- [Недра Чукотки (vnedra.ru, 2022)](https://www.vnedra.ru/2022/05/23/diversifikacziya-chukotki-nabiraet-oboroty/)
- [Omolon Hub (Polymetal)](https://www.polymetal.ru/assets/where-we-operate/omolon-hub/)
- [Omolon Mining Hub, Russia (Mining Weekly)](https://www.miningweekly.com/article/omolon-mining-hub-russia-2020-07-10)
- [Omolon Hub (miningdataonline)](https://miningdataonline.com/property/1821/Omolon-Hub.aspx)
- [Diamond mine ice road expected to have record year (CBC)](https://amp.cbc.ca/news/canada/north/diamond-mine-ice-road-expected-to-have-record-year-1.2937270)
- [Winter road haul amounts to 257,176 tonnes (NNSL)](https://nnsl.com/nwtnewsnorth/winter-road-haul-amounts-to-257176-tonnes-7260726)
- [ГДК «Баимская»: запуск запланирован на конец 2028 (Прайм)](https://gold.1prime.ru/20260902/chukotka-1789610.html)
- [Запуск Баимского ГОКа перенесли на 2029 год (НедраДВ)](https://nedradv.ru/nedradv/ru/page_news?obj=f3d805e5ee17ab6def48bd6ab2ec725a)
- [Северный завоз на Чукотку, более 150 тыс. т нефтепродуктов (Нефтегаз.РУ)](https://neftegaz.ru/news/transport-and-storage/923893-na-chukotku-v-ramkakh-severnogo-zavoza-dostavyat-bolee-150-tys-t-nefteproduktov/)