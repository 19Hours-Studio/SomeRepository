I repaired both ideas without losing their anchors, but both end up niche. The kill tests are right that neither moves company-wide cost per tonne by 10% or more. The repair finds the setting where each anchor pays: for idea 1 that is infrastructure life and tail risk at the coldest sites; for idea 2 it is deep mines where the hoisting shaft is the bottleneck.

=== IDEAS ===

**IDEA 1**
NAME: Cold-margin triaged thermosyphon retrofit
MECHANISM: Anchor: borehole temperatures plus InSAR rank existing foundations by remaining pile capacity, and retrofit thermosyphons only on the worst ones, only where the winter is cold enough. The cutoff is now a computed number: the cooling margin M, which is winter heat a unit can pull out of the ground divided by the yearly heat flowing in per pile. In 2050 climate (+2.5 K in winter), M is 1.53 at Norilsk, 2.10 at Udachny/Mirny and 1.57 at Pevek, which pass the M ≥ 1.5 cutoff. It is 1.05 at Salekhard, 0.88 at Nadym, 0.90 at Fairbanks and 0.41 at Beiluhe on the Qinghai–Tibet line, which fail. That ranking matches where cooling was actually seen to fade on the Trans-Alaska pipeline (TAPS) and the Qinghai–Tibet line (F320–321). Triage step 0 is the cheapest fix: reopen crawlspace vents and repair utility leaks. Only structures that keep warming after that get vertical units drilled with low-headroom rigs from the ventilated crawlspace, or inclined units from the outside edge for buildings under about 20 m wide. That is about 50 of the 165 monitored Norilsk/Talnakh structures and about 8,500 units. Each unit finishes cooling the ground to the target in about one winter.
VALUE: It keeps structures on thawing ground in service past 2050 for about $64M, against $198M for retrofitting all 165 structures and $196–392M for new piles to bedrock. That is about 3× cheaper than either. It adds only about $3–19 per t Ni-eq (0.04–0.20% of full cost) and avoids an expected $26–86M/yr of thaw-related losses.

**IDEA 2**
NAME: Shaft-bottom XRT sorting, hoist-bound mines
MECHANISM: Anchor: domestic X-ray transmission (XRT) sorters at the shaft bottom reject waste lumps before hoisting, and the rejects go straight into stope backfill. The repair moves it from "freeing concentrator capacity" to deep mines where the 2.1 km shafts set the limit, such as Skalisty and the Talnakh/Oktyabrskoye deep levels. There every tonne of waste rejected below ground is replaced by ore in the fixed skip capacity. With the fines (about 35% of ore) bypassing the sorter, metal hoisted per year rises ×1.095 at Selebi-type results (15% rejected, 2% metal lost) and ×1.36 at stringer-type results (44%, 4%). After counting the metal lost for good in the backfill, metal NPV is still ×1.085–1.31 over a 30-year reserve at 14%. Two or three 150 t/h units cover 2 Mt/yr hoisted. Rejects of at most 0.41 t per t of ore fit in the backfill needed (0.44–0.67 t per t), so no tailings go to the surface. The design is restricted to cuprous/stringer and massive ores at contacts. Disseminated Norilsk-1 and Maslovskoye ore is left out (16% metal loss at 23% rejection on disseminated test ore), as are mines where hoisting is not the limit.
VALUE: Each extra tonne of Ni-eq from a hoist-bound deep mine costs $5.0–8.3k by sorting against $6.7–12.6k from a new deep shaft, 1.2–1.8× cheaper. It comes in about 2–3 years instead of about 10 years of shaft sinking.

=== NOTES ===

**Idea 1: anchor kept** (triage plus a freezing-index cutoff).
- **Decisive numbers** (calc/idea1.py, idea1b.py):
  - M is computed from monthly air normals (Norilsk freezing index about 4,360 °C·day) with R = 0.12 K/W per unit and 42 W of heat load per pile.
  - Norilsk full cost is $8.1bn/yr (cash cost $5.1bn, F62, plus capex $3bn, F61) over 0.89 Mt Ni-eq, i.e. $9,124/t (revenue F241).
  - An Ambarnaya-scale award is 146 bn RUB (F262).
  - Unit price is the largest guess: hardware is listed from 10k RUB, and I assumed 0.3–1.0M RUB installed with drilling.
- **Baselines:**
  - Monitoring and repair-on-failure, which is current practice (F263).
  - Blanket retrofit: $198M.
  - New piles to bedrock: $196–392M.
  - Crawlspace and leak repair is the cheapest, so it is built in as step 0.
- **Consistency checks:**
  - M passes at Norilsk across R 0.08–0.12, but fails at R 0.2 (0.68–1.20).
  - Cool-down takes about 1 winter.
  - The +2.5 K winter warming is consistent with about 0.07 K/yr (F104) over 25 years.
  - Inclined units only reach about 20 m in from the edge, hence the crawlspace route.
- **Hazards:**
  - Non-condensable gas fade (seen on TAPS; it can be refilled).
  - Sideways temperature gradients and moisture movement (F322).
  - Failures that are not caused by thaw: the 2021 gallery collapse (F264) and the corroded Ambarnaya tank (F258) would not have been prevented.
- **Deciding unknown and test:** R and the real heat load in saline Norilsk loam. Instrument 20 units with heat-flux and evaporator temperature strings for 3 winters. That gives ±15% on the mean margin at CV 0.3, since n ≈ 15 is needed.
- **Closest existing work:** Nornickel's monitoring of 165 objects and the Qinghai–Tibet pile thermosyphons. This idea adds the quantitative M cutoff, step-0 triage and crawlspace installation.
- **Verdict: NICHE.** Worth doing on infrastructure life and tail risk, but it does not change cost per tonne.

**Idea 2: anchor kept** (shaft-bottom XRT, rejects to backfill).
- **Decisive numbers** (calc/idea2.py, idea2b.py, idea2c.py):
  - Test results: Selebi 15.2% rejected at 98% recovery (F350, unaudited); NickelSearch Carlingup stringer ore 44% at 96% and 63% at 94%; Carlingup disseminated ore 23% at 84%.
  - Grades from F1, F2 and F7. Ore mining cost of $60/t and new shaft capex of $400–600 per t/yr of capacity are my assumptions.
- **Kill test reproduced:** if the concentrator is not the limit, break-even metal loss is only 0.08–0.42%, so it fails.
- **Baselines:**
  - A new deep shaft (Skalisty's shafts took years to sink to 2.1 km).
  - Selective mining and dilution control, the cheapest option. Do it first; sorting only pays on dilution that cannot be avoided.
  - Surface sorting, which saves no hoisting.
- **Mine-level average cost per t Ni-eq** improves only 1.003–1.06×, so the value is extra capacity and time, not unit cost.
- **Consistency checks:**
  - Backfill balance has a thin margin on massive ore.
  - Sorter count: 2–3 units.
  - Stoping and ventilation must supply +10–41% more ore. If they cannot, the idea fails.
- **Hazards:** dust and X-ray shielding underground; whether domestic XRT units hold up (Egoteh and RADOS are named from memory, not checked); whether deep mines are limited by stope or ventilation rather than the hoist.
- **Deciding unknown and test:**
  - How grade varies from lump to lump in Norilsk deep run-of-mine ore at 25–100 mm.
  - Test: scan about 1,000 lumps per ore type × 3 ore types on a domestic XRT, then assay them in about 10 bins.
  - Also check from the mine plan that the hoist really is the limit.
- **Closest existing work:** Selebi/Kutcho. This idea adds the hoist-bound deep-mine setting, closing the backfill balance and skipping surface tailings on permafrost.
- **Verdict: NICHE**, and it WORKS if a hoist-limited mine is confirmed.

My working files are in `/home/user/SomeRepository/engine/runs/rusres/repair/c2/`: `LOG.md` (one line per round) and the scripts in `calc/`.

Sources:
- [NexMetals Selebi XRT release](https://www.newsfilecorp.com/release/260258)
- [NickelSearch Carlingup ore sorting](https://stockhead.com.au/?p=250791)
- [Nornickel AR2017 mining projects (Skalisty shafts)](https://www.ar2017.nornickel.ru/pdf/ar/ru/business-group_key-projects_mining-projects.pdf)
- [Thermostabiliser price listing](https://productcenter.ru/products/115295/tiermostabilizator-grunta)
- [Thermosyphon foundations in warm permafrost](https://geocryology.com/wp-content/uploads/2014/03/thermosyphon-foundations-in-warm-permafrost.pdf)
- [Nornickel AR2020 Norilsk operations](https://ar2020.nornickel.ru/pdf/ar/ru/business-overview_operational-performance_norilsk.pdf)