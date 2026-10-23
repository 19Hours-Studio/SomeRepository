# Task: repair original ideas against reality WITHOUT losing what makes them original

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas an idea engine produced for this question, with the results of the checks run on them so far
(judges' scores, kill tests or reviews, where present). Your job is NOT to invent new ideas and NOT to replace them with safer
known solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it
original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/permafrost_v5/repair/`: read no other files in the repository, do not
modify other files, do not commit.

For each idea, loop until it works or you can prove it cannot:
1. Name its ANCHOR (the distinctive idea) in a few words. This must survive.
2. Find the binding quantity (what decides whether it works at the needed scale - a rate, an energy balance, a
   recovery, a throughput, a safety limit) and compute it in Python with real numbers from the literature (cite the
   source in your notes).
3. BASELINE: compare against the BEST current practice a competent operator would actually use for the same job
   (list at least two real alternatives, including the cheapest one), and compute cost per unit of RECOVERED or
   DELIVERED product (per kg of metal recovered, per tonne delivered), not per tonne of raw material moved, with
   sourced numbers. Never compare against a strawman nobody would do.
4. CONSISTENCY PASS: list every tolerance, window and limit your design relies on (buoyancy margins, temperature
   limits, strengths, breakdown fields, stage efficiencies, site conditions where you placed it) and check every
   rate you computed against every one of them over the whole operating time (rate x duration vs window). Check
   that the site or route you chose really has the conditions you assumed. Write the check table in your notes.
5. If it fails, change the DESIGN AROUND the anchor (materials, geometry, operating regime, scale, season, which
   resource/cargo/deposit type it is used for) and recompute. Look for the regime where the anchor is strongest.
   Repeat - several rounds per idea is normal.
6. Name the hazards honestly and design them down where possible; say which unknown number decides the idea and the
   cheapest experiment that would measure it (with the sample size it needs).
7. Check novelty: if the repaired design turns out to be a known system, keep the anchor and find the version that is
   not known.
8. Only if no anchor-preserving design can work, say so and give the best honest niche.

Facts that earlier checks in this run found (data; verify before relying on them):
FACT 1: Zyryanka coal is already distributed down the whole Kolyma each summer on dedicated coal barges (баржи-углевозы) | NEW from gate, check before relying on it | https://www.kolymastory.ru/glavnaya/morskie-vorota-kolymy/rechnye-gruzoperevozki/
FACT 2: Kolyma-basin tankers are 38-54 years old; fuel moves upstream by tanker | NEW from gate, check before relying on it | https://www.korabel.ru/news/comments/dlya_severnogo_zavoza_zadeystvovali_3_6_tys_km_rek_lenskogo_basseyna.html
FACT 3: Zyryanka-Srednekolymsk is being dredged (about 23k m³ since July); navigation closes 10 Oct | NEW from gate, check before relying on it | https://www.korabel.ru/news/comments/opredeleny_sroki_zakrytiya_navigacii_v_lenskom_basseyne.html
FACT 4: Two motor ships (Sofron Danilov, Kapitan Burkovsky) sank at their winter berth during Lena ice drift, Zhigansky district | NEW from gate, check before relying on it | https://www.eastrussia.ru/news/na-reke-lena-iz-za-ledokhoda-zatonulo-dva-teplokhoda-/
FACT 5: 28 May 2026: 10 vessels (5 Lena waterways administration, 5 LORP) broke loose and drifted on the Indigirka at Belaya Gora | NEW from gate, check before relying on it | https://www.fontanka.ru/2026/05/30/76451529/
FACT 6: Ukrrechflot estimate ~$3 M per 5,000 t river barge (2020) | NEW from gate, check before relying on it | https://gmk.center/news/ukrrechflot-hochet-postroit-5-nesamohodnyh-barzh-v-2021-godu/
FACT 7: Winter bottom water at candidate bubbler sites was measured at 0.01-0.2 °C, not 4 °C | NEW from gate, check before relying on it | https://apps.dtic.mil/sti/pdfs/ADA148739.pdf
FACT 8: SPoT: 8 tractors, ~768,000 lb/yr payload, one 24,000-gal four-bladder set per tractor, ~1 lb of support load per lb delivered | NEW from gate, check before relying on it | https://apps.dtic.mil/sti/pdfs/ADA602402.pdf ; https://www.equipmentworld.com/applications-and-innovations-get-ready-for-winter/
FACT 9: Coal matrix thermal conductivity 0.22-0.55 W/mK (mean 0.33), 55 coals including 6 lignites | NEW from gate, check before relying on it | doi:10.1029/96JB01884 (Herrin & Deming 1996)
FACT 10: Kolyma navigation opens 23 May (Oroek-Zyryanka) | NEW from gate, check before relying on it | https://www.korabel.ru/news/comments/opredeleny_sroki_zakrytiya_navigacii_v_lenskom_basseyne.html
Notes from the user (data; the user may be wrong):
(none)
Keep `LOG.md` in your folder: one line per round (idea, change, decisive number, result). Spend about 45-60 minutes at most.

Final answer (text only): first the 4 repaired ideas in exactly this format, then a short NOTES section (per idea:
anchor kept?, decisive numbers with sources, best-baseline comparison per unit of recovered/delivered product,
consistency table summary, hazards, deciding unknown and experiment, closest existing work, verdict WORKS / NICHE / FAILS).
=== IDEAS ===
IDEA 1
NAME: (max 5 words)
MECHANISM: (2-5 sentences: the anchor first, then the repaired design, with the decisive computed numbers)
VALUE: (1 sentence, with the cost ratio vs the best current practice)
(same for the other ideas, in the same order as below)

THE 4 IDEAS:
IDEA 1
NAME: River-thawed bluff lignite scraping
MECHANISM: Many Yakutian rivers cut lignite or coal seams in their bluffs. A sun-facing bluff thaws about 1.5 m deep each summer (est.), so a small excavator can scrape the thawed face without drilling or blasting. The scraped coal goes to a stockpile and moves to the village by a winter road of 30 km or less. A 3 m seam gives about 6 t per metre of face, so about 1 km of face per year covers a village of 1,000 people burning about 6,000 t of coal-equivalent. The closest earlier attempts were Corwin Bluff and Qullissat, which stopped on rare ship calls, falling profit and poor coal. Here the buyer is the village boiler, priced against the 23,000 rub baseline, and no ship is involved. The deciding quantity is summer thaw depth multiplied by the length of seam face within 30 km of the village.
VALUE: Estimated 4,800 rub per coal-equivalent tonne (3,500 kcal lignite, about 4.8x cheaper), which turns stranded small river-bluff deposits into a settlement fuel base.
KILL TEST: killer summer thaw depth of a lignite face | margin 0.61 | whole-chain ratio 2.2 | WOUNDED: The economics hold at 2.2x, but the face thaws only 0.9-1.35 m, so a village needs about 1.1-1.6 km of seam face a year, and it is not proven that this much exists within 30 km or that the river turbidity limits can be met.

IDEA 2
NAME: Downstream coal on empty barges
MECHANISM: On the Kolyma, the summer Northern Delivery convoys bring fuel and goods upstream from Chersky and come back down empty. They pass riverside pits like Zyryanka on the way, so they could carry coal down on that return leg. The cost is only marginal: a short loading stop plus a little extra draft. Return-cargo pricing is common in shipping, but no Kolyma coal-on-the-return contract was found. Such cargo normally fails when directions do not match, and here they do. The deciding quantity is how much load the empty barges can take at late-season water depths, given that shoaling already limits loaded barges to under 50%.
VALUE: Cuts the barge cost per tonne several-fold using vessels that already make the trip, with no new capital.
KILL TEST: killer payload at late-season depth | margin 0.41 | whole-chain ratio 1.21 | WOUNDED: Zyryanka coal already goes down the Kolyma on coal barges, most upbound fuel comes in tankers that can't carry coal, and a coal-loaded return hull hits the same shoals, so the barge leg (35% of cost) shrinks only slightly.

IDEA 3
NAME: Flood-crest barge launch
MECHANISM: Coal goes from the pit in winter and is loaded onto barges wintering in a sheltered backwater near it. The barges wait out the ice drift and leave on the spring flood crest. That way they travel fully loaded, not under 50% as on summer shoal water. The closest attempt is the "early delivery" voyages, which hit drifting ice and lost the crest. Here the barges shelter during the drift, and the timing is computed from gauge forecasts. Deciding quantity: the days between the reach clearing of ice and water falling below loaded draft, compared with the transit time.
VALUE: The cost per tonne of the main barge haul roughly halves.
KILL TEST: killer ice-edge line load when 2,214 t is loaded into a frozen-in hull | margin 0.23 | whole-chain ratio 1.06 | DEAD: Only the first trip of the season goes full, which cuts the barge leg by about 17% rather than 50%, and loading a frozen-in hull in winter breaks the ice it is frozen into.

IDEA 4
NAME: Frozen-in barge boilerhouse
MECHANISM: A barge from the ageing Lena/Kolyma fleet, near scrap value, gets a containerised boiler and a 2–3 kt coal hold. It arrives at the settlement on high water and is frozen in at a berth, with an air-bubbler kept running to stop ice pressure. All winter it burns its own cargo and sends heat to shore through an insulated pipe. This deletes three steps: transshipment, the shore stockpile and the winter-road last mile. The closest attempt is the Akademik Lomonosov floating plant, which was stopped by 70 MW of scale and a 4x capital overrun. This uses a written-off hull and a boiler of about 1–5 MW. Deciding quantity: annualised hull plus boiler cost per hold-tonne against the last-mile and handling share it removes (about 11,000–15,000 rub/t, est.). That share needs sourcing.
VALUE: A settlement could be fuelled with no winter road and no shore coal yard.
KILL TEST: killer heat to keep a 1 m moat open round the hull | margin 0.01 | whole-chain ratio 0.58 | DEAD: A bubbler works only on stored heat, and 0-0.2 °C river water holds about 2 days of it against 200 days of ice, while the saving the idea claims (11-15k RUB/t) is really about 1.2k at a settlement the barge can already reach.

