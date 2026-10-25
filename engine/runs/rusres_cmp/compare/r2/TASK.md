# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia wants to develop and extract minerals and energy in its permafrost regions at the lowest full cost, in the shortest time from investment decision to first production, and with the highest effectiveness. Effectiveness means resource recovery, working time across the year, and how long infrastructure lasts on thawing ground. All three are measured per unit of product delivered to the buyer. The scope covers:
- Hard-rock and placer metals: Norilsk and Taimyr nickel, copper and platinum-group metals; gold in Yakutia, Magadan and Chukotka; Udokan and Baimskaya copper; Tomtor rare earths.
- Diamonds in Yakutia, plus the Arkhangelsk deposits (see CORRECTED).
- Coal in Taimyr, Elga and the rest of Yakutia.
- Oil and gas in Yamal, Gydan and Taimyr.
The whole chain counts: choosing and exploring deposits, building and powering sites, mining or drilling, processing, staffing, and delivering the product. The conditions are:
- Permafrost that is thawing under a warming climate.
- Extreme cold, with short building and shipping seasons.
- Long distances with no roads or railways.
- Ice seasons on the Northern Sea Route (NSR) and the rivers.
- A shortage of workers.
- Expensive energy at remote sites.
- Restricted access to imported mining, drilling and LNG equipment and software since 2022.
What changes to any stage, or to the order in which deposits are developed, would beat the best current practice in Russia and in comparable cold regions (northern Canada, Alaska, Greenland, northern Scandinavia)?
A good answer: 
- Each proposal states its effect, with an estimate and its basis, on three measures: (a) full cost per unit delivered (annualised capital plus operating plus logistics); (b) years from investment decision to first production; (c) effectiveness (recovery, days worked per year, infrastructure life on thawing ground).
- Each proposal is compared with a named benchmark, either Russian (e.g. Yamal LNG, Norilsk, Vankor/Vostok Oil, Kupol/Pavlovskoye, Nord/Elga) or foreign (e.g. Canadian Arctic mines such as Raglan and Diavik, Red Dog in Alaska, Kiruna/Aitik, Greenland).
- It names which deposits or stages it applies to and which it does not.
- It states what physical law or measured data it relies on.
- It lists the equipment or technology by its domestic maker or unrestricted supplier.
- It includes the main risks and how to test the idea within 3–7 years.
Constraints: 
- It must obey known physics.
- It must be deployable within 3–7 years.
- It may use only equipment and technology Russian operators can get from domestic makers or from suppliers not restricted for them.
- It must not depend on ways around sanctions.

Below are 9 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/rusres_cmp/compare/r2/`: read no other files in the repository, do not modify other files, do not commit.

For each idea, attack in this order:
1. Recompute every number the text states (arithmetic, units, mass, energy or memory balances). Flag any that do not reproduce.
2. Consistency: list every tolerance, margin and window the design relies on, and check every rate in the design
   against it over the whole operating time (rate x duration vs window). Check that the conditions assumed really
   hold where the idea is used (site, route, season, workload, hardware) - find measured data.
3. Baseline: is the comparison against the best current practice a competent operator would use, per unit of
   recovered or delivered product or service? Name the real competing alternatives it ignores and recompute the ratio.
4. Assumptions: which decisive numbers (efficiencies, friction, rates, loss fractions, costs) are assumed rather
   than sourced? How far can they move, and does the claim survive the plausible range?
5. Evidence and statistics: are the proposed tests able to show what is claimed (sample sizes, confidence bounds)?
6. Hazards and showstoppers not mentioned (safety, environment, regulation, logistics, scale-up).
Facts marked NEW were found by earlier checks in this run and are not yet verified: do not count them toward FIT,
and do not base a FATAL or MAJOR defect on a NEW fact alone unless you have verified it yourself (its source and,
for measurements, which object and which hole, face or item each number belongs to).
Do not pad: a defect needs a mechanism and a number. If a claim survives your check, say so in one line.

Final answer (text only), exactly this format:
=== REVIEW ===
IDEA 1: <name>
DEFECT | <FATAL/MAJOR/MINOR> | <one sentence: what is wrong> | <the number or source that shows it>
(as many DEFECT lines as needed, most severe first)
SURVIVES | <claims that held up under your check, one line>
RATIO | <whole-chain cost ratio against the best current practice after your corrections: current cost / cost with the idea, one number> | <one line basis>
KNOWN | <yes / partly / no: is this already done or seriously proposed?> | <the closest existing system, project or proposal, with source>
NEW FACT | <any hard fact you found that the material did not contain> | <source> (optional, any number)
(same for the other ideas, in the same order as below)

THE 9 IDEAS:
IDEA 1
NAME: Shared nuclear grids replace site diesel
MECHANISM: Instead of one diesel plant per mine, build 110/220 kV lines from a few large power sources: Akademik Lomonosov at Pevek, the Baimskaya floating units (RITM-200M) at Cape Nagloynyn, and the RITM-200N plant at Ust-Kuyga. Then develop first the deposits within about 150–250 km of those lines. Off-grid sites add wind (Novawind), solar (Hevel/Unigreen) and LFP batteries (Liotech) to domestic gensets (Kolomna, Ural Diesel, Zvezda). The physics is a large genset burning about 0.22 kg of diesel per kWh, all of it shipped in the short navigation season or by winter road; in 2015 Chukotka received only 46.2 kt of the 103 kt of fuel it planned. A reactor refuels once every several years, which removes that supply risk and the working days lost to it. This applies to Chukotka (Baimskaya, Kupol/Dvoinoye, Mayskoye) and Yana–Indigirka gold (Kyuchus), but not to Norilsk, Yamal/Gydan, Udokan or Elga, which already have gas, hydro or BAM grid power. Main risks are reactor schedule slips (the Yakutia plant moved from 2028 to 2030–31) and take-or-pay exposure if a mine is late. Test it in 3–5 years by connecting one Pevek–Bilibino gold mine by line and comparing its delivered RUB/kWh with diesel.
VALUE: At about 26 RUB/kWh for diesel against about 9.6 RUB/kWh for the floating plant, and about 9.6 MWh per tonne of copper, power cost falls by about 1,900 USD/t Cu (roughly 20% of the copper price) against diesel-only Kupol. Hybrids alone save 10–30% of diesel, about 2–6 RUB/kWh, against Diavik's 9.2 MW wind farm (about 10% of diesel) and Raglan's two turbines (4.4 million litres a year). Time to first production stays tied to reactor delivery in 2027–31, or 1–2 years for a hybrid.

IDEA 2
NAME: Shaft-bottom XRT sorting, hoist-bound mines
MECHANISM: Anchor: domestic X-ray transmission (XRT) sorters at the shaft bottom reject waste lumps before hoisting, and the rejects go straight into stope backfill. The repair moves it from "freeing concentrator capacity" to deep mines where the 2.1 km shafts set the limit, such as Skalisty and the Talnakh/Oktyabrskoye deep levels. There every tonne of waste rejected below ground is replaced by ore in the fixed skip capacity. With the fines (about 35% of ore) bypassing the sorter, metal hoisted per year rises ×1.095 at Selebi-type results (15% rejected, 2% metal lost) and ×1.36 at stringer-type results (44%, 4%). After counting the metal lost for good in the backfill, metal NPV is still ×1.085–1.31 over a 30-year reserve at 14%. Two or three 150 t/h units cover 2 Mt/yr hoisted. Rejects of at most 0.41 t per t of ore fit in the backfill needed (0.44–0.67 t per t), so no tailings go to the surface. The design is restricted to cuprous/stringer and massive ores at contacts. Disseminated Norilsk-1 and Maslovskoye ore is left out (16% metal loss at 23% rejection on disseminated test ore), as are mines where hoisting is not the limit.
VALUE: Each extra tonne of Ni-eq from a hoist-bound deep mine costs $5.0–8.3k by sorting against $6.7–12.6k from a new deep shaft, 1.2–1.8× cheaper. It comes in about 2–3 years instead of about 10 years of shaft sinking.

IDEA 3
NAME: Gated diesel bridge plus pooled spares
MECHANISM: (1) Norilsk, starting now: build one spares registry for the Western-built underground fleet. Spares are pooled across 6 mines and ranked by Ni-eq lost per machine-hour (6.3 t on rich ore, 1.2 t on Norilsk-1). Domestic reverse-engineering and casting start with the worst part families. The programme winds down as the BelAZ/MoAZ JV fleet (Sosnovoborsk, about 150 machines/yr) replaces those machines. The corrected effect is +8 to +29 kt Ni-eq/yr (central +15 kt) at about $5.4k per added tonne. (2) Baimskaya, decided at a gate in Q4 2027: if the first two RITM-200S floating units are not at mooring trials by then, they cannot power line 1 when it is ready in Q1 2029 (RAEX, Apr 2026). In that case Baimskaya leases about 80 MW of domestic gensets (Kolomna or UDMZ 1.5–2.5 MW units) and runs line 1 at about 65 MW average. That gives 12.2 Mt/y of ore (not 15), 48 kt Cu and 77 koz Au a year. It burns 146 kt/y of diesel at 0.225 kg/kWh, which costs about $0.31/kWh. Diesel comes from Far East refineries through the Bering Strait in 7–8 tanker calls into Pevek. That route keeps clear of the Kara Sea icebreakers Part 2 needs. The fuel is held in about 173k m³ of tankage (about $173m), built on cooled piles to bedrock with full secondary containment, which is the Ambarnaya lesson. Concentrate (222 kt wet a year, 5–6 ships of 40 kt) is stockpiled at Nagleynyn for the 3–4 month shipping season. The gensets leave when the floating units arrive. (3) Oil and gas: no change. Both Part 2 ideas only reproduce current practice: Vankor oil goes south on Vankor–Purpe, Payakha oil goes north as far as the hulls allow, and Yamal LNG uses Kildin ship-to-ship transfer plus summer cargoes east.
VALUE: Copper: expected value is +$185m (+$66m at $8k Cu / $2.8k Au), and the bridge breaks even if the floating units slip 0.44 years. Life-of-mine full cost is 0.98× the no-bridge case for a 1-year slip and 0.955× for a 2-year slip. First metal comes 1.05 years earlier on expectation, with a 35% chance of no gain. Nickel-equivalent: group full cost goes from about $10.05k to $9.97k/t Ni-eq (−0.85%, range −0.1% to −2.5%) within 6–18 months, and the gain fades over 3–5 years. LNG and oil: 1.00× current practice.

IDEA 4
NAME: Pre-staged flood-crest barges
MECHANISM: Anchor: a loaded barge waits out the ice drift in a sheltered backwater and leaves on the flood crest. Repair: load it in autumn while it is still afloat at a deep berth, so nothing is loaded through ice. It winters in a backwater at least 2.5 m deep, and it is used on a tributary that is navigable only on the spring flood, where there is just one trip a year anyway. With a modelled 12-day recession, a convoy arriving 5–10 days late loses 35–62% of its load. A barge pre-staged at the river mouth goes in full.
VALUE: About 3,100 rub/t against 4,700–11,300 rub/t on that leg today (1.5–3.6x). On the Kolyma main stem the gain is only about 14%.

IDEA 5
NAME: Ore sorting plus dry-stack tailings
MECHANISM: Domestic X-ray sorters (Bourevestnik, RADOS) reject barren rock before it is ground. In Russian tests up to 70% of the mass went to waste while the gold grade rose 1.5–1.6 times, and at Dukat (Magadan) the rejects matched tailings grade. As a result, each ounce or tonne of copper needs about 30–50% less grinding energy, water, reagents and tailings space, which pays most where power comes from diesel. The remaining tailings go into filtered dry stacks, as at Raglan, Pogo and Greens Creek, because a dry stack tolerates uneven thaw settlement better than a dam on ice-rich ground. Do not run year-round heap leaching on fine ore stacked frozen: the Eagle heap in Yukon slid in 2024 (5.95 million m³), and the review board blamed poor drainage and frozen fine ore. Mine and sort all winter and leach in season, as at Fort Knox. This applies to lode gold (Kupol, Pavlik, Natalka, Kyuchus) and coarse copper ore, not to placers, diamonds (already sorted at Alrosa) or oil and gas. The main risk is metal lost in the rejects; test with a 2-year pilot sorter at one Magadan or Chukotka mine.
VALUE: Full cost should fall about 5–15% per oz or per tonne of Cu at diesel-powered mines, assuming 50% of the mass is rejected, at a recovery cost of 1–5 percentage points. Tailings risk on thawing ground falls against dam-based Kupol and Norilsk.

IDEA 6
NAME: Diesel-sized first line, nuclear expansion
MECHANISM: Anchor: a diesel-sized starter on leased domestic or unrestricted gensets comes first. The nuclear-sized expansion follows when the floating units deliver, and the gensets then move to other sites. Repaired design: the starter is no longer a separate 6 Mt/y plant. That version still fails: $8.3k/t Cu net against $2.0k/t for the full plan, and a $45m a year margin on $1.08bn of capex. Instead, line 1 of the Baimskaya plant now under construction (start planned for end-2028) runs at a throughput sized to 80 MW of leased gensets. It uses the SAG mill and one of two ball mills at a coarser grind, on the highest-grade benches. That gives 15 Mt/y of ore at about 0.51% Cu (the first-decade head implied by the feasibility study), 67 kt Cu and 98 koz Au a year. It burns 117 kt of diesel a year at $0.30/kWh, which takes 6 tanker calls into Pevek and needs 174k m³ of tankage. With fuel coming in and concentrate going out on the same trucks, that is about 7,000 loads a year: 20 a day on the all-season road, or 78 a day on a winter road alone. Net cash cost is $1.95k/t Cu after gold credit. Line 1 is also commissioned on diesel, so the ramp-up is done before the reactors arrive.
VALUE: Each year the floating units slip, the bridge earns about $0.52bn of cash margin ($0.29bn at Cu $8k / Au $2.8k) from a plant whose $8bn would otherwise cost about $1.2bn a year to carry idle. Waiting idle earns nothing in those years.

IDEA 7
NAME: Design for warming ground, with monitoring
MECHANISM: Assume the permafrost keeps warming: GTN-P measured +0.39 ± 0.15 °C per decade in the continuous zone in 2007–16. Size piles for the ground temperature expected at the end of design life, not at construction, under SP 25.13330. Add passive two-phase thermosyphons (Fundamentproekt, NPO Fundamentstroyarkos) wherever ground is warmer than about −2 °C, and require automated temperature and settlement monitoring with alarms on fuel tanks, tailings dams and pipelines. Engineering faults matter as much as thaw: Rostekhnadzor found the 2020 Norilsk TPP-3 spill (about 21 kt of diesel, 146–148 bn RUB damages) came from construction and operating faults, with half the piles overloaded, and found no thaw under the tank. So monitoring has to check loads and maintenance as well as temperature. This applies to every site on ice-rich or warm permafrost: Norilsk, Yamal/Gydan, Vostok Oil, Yakutia and Chukotka. It matters less at Udokan and Elga, which sit in discontinuous permafrost, and not at all in Arkhangelsk. Risks are false alarms and thermosyphons that do nothing in summer if undersized. Test within 3 years by comparing settlement and maintenance cost on monitored and unmonitored Vostok Oil pads.
VALUE: Nornickel's first stage cost about 8.5 M RUB per object (1.4 bn RUB for 165 objects). Spending about 0.3–1% of asset capex should keep foundations at their 30–50-year design life instead of losing roughly 20–50% of it on unmanaged ground near 0 °C (my assumption). Against a Russia-wide mitigation bill of 16.7 + 67.7 bn USD by 2050 (Streletskiy 2019), it adds no time before first production. The benchmarks are Yamal LNG and Vankor, which use thermosyphons as standard, and the Alaska oil pipeline.

IDEA 8
NAME: Develop by value per tonne
MECHANISM: Order deposits by value per tonne and by access to rail or pipeline. At about 30 USD/t for Arctic freight, freight is about 33% of thermal coal value, 18% of coking coal, 7% of crude oil or LNG, 1.3% of copper concentrate and 0.3% of copper cathode. The NSR is not growing fast enough to carry everything: 37.0 Mt in 2025, down 2.3%. Arctic LNG 2 has 3–4 usable Arc7 carriers against 21 contracted and shipped only 1.3 Mt in 2025. So go first with high-value, low-tonnage products (Udokan cathode at 99.99%, Baimskaya), then deposits that rail or pipe can reach: Elga coal (35.1 Mt in 2025 on its own railway to the BAM) and Vostok Oil (first oil September 2026 through a 790 km pipeline, about 6 years from FID). Defer NSR bulk coal (Syradasay, whose ice-class fleet is not built), Tomtor (no development decision as of 2025) and more Arctic LNG 2 trains until ships and buyers exist. Arkhangelsk's Lomonosov diamond mine is not on permafrost, and mining there was paused in July 2026 on weak demand.
VALUE: This avoids capital stranded by missing ships or buyers per unit delivered. Time to first production then depends on rail or pipeline access, not on ice-class fleet supply. The benchmark is Red Dog in Alaska, which stores 950 kt of concentrate and ships it in a 100–122-day season.

IDEA 9
NAME: Size Sever to hulls
MECHANISM: The anchor is unchanged: each month Bukhta Sever receives only what the Russian-built Arc hulls can lift, about 1.54 Mt/y per 69 kt hull on the 15.5-day Murmansk cycle (1.2 Mt/y if winter stretches the cycle to 20 days). The allocation is reversed. Vankor-cluster oil (about 11.6–12.3 Mt in 2026–27) stays on the existing Vankor–Purpe line. That line is rated 25 Mt/y and has 12.7–13.4 Mt/y spare. The oil goes to the export outlet it already sells to, not to domestic refineries, which are already crude-long. South is the cheaper margin: about $57/t to an Asian buyer via Transneft and Kozmino, against about $86/t north via Sever, Murmansk and Suez. The north carries only Payakha oil, and Payakha drilling is scheduled to Zvezda Arc hull deliveries, so no well is drilled whose oil cannot be lifted. Because of that, no surplus ever has to go south and the Payakha–Vankor segment never needs reverse flow.
VALUE: Delivered cost per tonne falls by about $29/t on every Vankor tonne kept south, and holding back 15–25 Mt/y of Payakha capacity by 2–3 years saves $2.4–5.8bn in present value. That is about $80–190 per tonne of the capacity deferred, against the published plan of 30 Mt/y in H2 2027, which needs about 19 hulls that do not exist.

