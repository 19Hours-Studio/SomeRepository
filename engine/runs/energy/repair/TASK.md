# Task: repair original ideas against reality WITHOUT losing what makes them original

QUESTION: How could storing electricity for days to weeks become ten times cheaper than today, so that wind and solar can run a whole grid through long calm, dark spells? Propose fundamentally new mechanisms or system designs - not incremental improvements of existing battery chemistries.

Below are 6 of the most ORIGINAL ideas an idea engine produced for this question. Blind judges rated them highly
original but doubtful in feasibility. Your job is NOT to invent new ideas and NOT to replace them with safer known
solutions. Your job is to make each one work while keeping its anchor - the one distinctive idea that makes it original.

You have tools: WebSearch/WebFetch (check what exists, find real material data and costs) and Bash with python3
(do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/energy/repair/`; do not modify
other files, do not commit.

For each idea, loop until it works or you can prove it cannot:
1. Name its ANCHOR (the distinctive idea) in a few words. This must survive.
2. Find the binding quantity (what decides whether it works at the needed scale) and compute it in Python with real
   numbers from the literature (cite the source in your notes).
3. If it fails, change the DESIGN AROUND the anchor (materials, geometry, operating regime, scale, what it is used
   for) and recompute. Look for the regime where the anchor is strongest. Repeat - several rounds per idea is normal.
4. Check novelty: if the repaired design turns out to be a known system, keep the anchor and find the version that is
   not known.
5. Only if no anchor-preserving design can work, say so and give the best honest niche.
Keep `repair/LOG.md`: one line per round (idea, change, decisive number, result). Spend about 45-60 minutes at most.

Final answer (text only): first the 6 repaired ideas in exactly this format, then a short NOTES section (per idea:
anchor kept?, decisive numbers with sources, closest existing work).
=== IDEAS ===
IDEA 1
NAME: (max 5 words)
MECHANISM: (2-4 sentences: the anchor first, then the repaired design, with the decisive computed number)
VALUE: (1 sentence)
(same for ideas 2-6, in the same order as below)

THE 6 IDEAS:
IDEA 1 (mean originality 7.4/10, mean feasibility 3.0/10)
NAME: Sugar-glass radical granule store
MECHANISM: Charged posolyte and negolyte radicals are dissolved in a water-free sugar eutectic with Tg about 50°C and quenched into glass granules, which sit in ambient silos with their mobility frozen (about 40 Wh/kg, 25 kg per kWh, so the sugar must cost under about $0.4/kg to keep the medium near $10/kWh). For discharge, granules pass through a counterflow exchanger that recovers at least 90% of the heat. They are melted to about 170°C (about 0.5 Pa·s, about 0.01 S/m) for a residence of only minutes, and the melt flows once through a plain carbon cell with a 30 µm gap at 3 mA/cm², losing about 0.1 V to resistance. That needs about 20 m² of cell per kW, which for a 100-hour store is only about 0.2 m² per kWh. The stack's loss heat (about 15% of output) covers the exchanger's leftover heat demand (about 13%), and the melt is re-quenched as spent glass.
VALUE: Grid operators get weeks of charge stored like grain in silos, with no drying or redissolving, discharged through a cheap, large-area, slow carbon cell sized for days-long output.

IDEA 2 (mean originality 7.4/10, mean feasibility 2.8/10)
NAME: Locked-rubber bale yard
MECHANISM: Bands cut from natural-rubber-rich scrap truck tyres, screened for strain fixity at room temperature, are pulled in bundles of about 100 by a shared motor-generator winch to about 5x their length while warm. They are spray-cooled in the grip for about 30 s (a 3 mm band cools in about L²/α ≈ 20 s), so strain-induced crystallites lock the stretch. The now force-free bundles are baled densely (about 600 kg/m³) in shaded, covered yards at about $10/m³, about $5/kWh at about 3 Wh/kg. To discharge, a bundle is gripped again and warmed with about 45°C waste heat at a rate set by the grid frequency signal; the crystallites melt and the bundle contracts against the generator, drawing part of its work from that heat. Each stroke of about 1.5 kWh on a 30 s cycle gives about 180 kW per winch head, and about 0.3 t of rubber is handled per kWh.
VALUE: Industrial sites with waste heat get leak-free, non-hazardous multi-week storage whose medium comes with a disposal fee and whose housing is a covered bale yard instead of steel racks.

IDEA 3 (mean originality 7.2/10, mean feasibility 3.2/10)
NAME: Crystallizing Twin-Ditch Flow Battery
MECHANISM: Two parallel carbon-lined ditches, separated by a porous divider about 2.5 mm thick, each carry one dissolved organic molecule. Its charged form is a strained isomer that crystallises only after a delay, so it nucleates on seed crystals in that side's own downstream settling basin rather than on the electrode. Each side stays saturated at about 20 mM, which keeps the voltage flat and holds crossover to about 1.5% of a 10 A/m² current at 0.05 V ohmic loss. A potential-gated catalyst on each floor speeds snap-back only at discharge potential, and discharge redissolves slurry fed back upstream. The two powders sit on separate covered heaps for months. The converter is two lined ditches at about $30/m², or about $3/W at 10 W/m² (about $15/kWh over a 200 h discharge).
VALUE: Grid operators get months-long storage whose energy sits in heaps of cheap dry powder, provided molecules with about 20 mM charged-state solubility and delayed crystallisation can be found.

IDEA 4 (mean originality 6.8/10, mean feasibility 3.2/10)
NAME: Vapour-swing clay hydration store
MECHANISM: Thin swelling-clay beds sit fixed in earth-covered, vacuum-tight enclosures that only have to resist atmospheric pressure (0.1 MPa instead of about 260 MPa). Energy is stored as unmet hydration energy at about 7 Wh/kg, about 150 kg of clay per kWh, roughly $7/kWh at $50/t. To charge, one shared vapour compressor draws water vapour off one bed at a time at about 0.5 kPa (RH about 0.15) and condenses it into a pond. To discharge, pond water evaporates and expands through a low-pressure vapour turbine into the dry clay, valved from bed to bed. The adsorption heat (about 10x the work) must flow back to the pond across 3 K or less, so beds and pond are interleaved through thin walls. The machine handles about 1 m³/s of vapour per kW, so it is costly per kW and pays only at multi-week durations.
VALUE: Grid operators get multi-week storage whose capacity costs about as much as clay earthworks and a vacuum liner, with one vapour machine, sized only for power, as the converter.

IDEA 5 (mean originality 6.2/10, mean feasibility 4.5/10)
NAME: Earthen bipolar clay pile
MECHANISM: Excavated iron-rich smectite (layer iron switching between Fe(III) and Fe(II), about 1 mmol e⁻/g) and crushed manganese-oxide ore are laid as 3 cm layers, each mixed with about 10 vol% cheap char so every platelet is within about 2 mm of carbon. A dissolved mediator in salty pore water ferries electrons over that last distance. The layers are stacked as a bipolar earth pile: Fe-clay, a 5 mm compacted bentonite liner, MnO2 ore, then a graphite-foil sheet into the next cell. Each cell stores about 0.7 kWh per m² of sheet with about 0.07 V of ohmic loss at two-week discharge. The only fabricated parts are the about $5/m² sheets (about $7/kWh) and an inverter; everything else is earth at tens of dollars per tonne.
VALUE: Utilities and landowners get a weeks-long store built with earthmoving and layering equipment from local clay and ore, where the electrode itself is the converter, so no stack capex sits idle.

IDEA 6 (mean originality 6.2/10, mean feasibility 3.2/10)
NAME: Floating Solar Gravity-Cell Pond
MECHANISM: The pond's positive electrode is a 6 cm bed of 3-5 mm coke grains on a carbon-felt floor. A charged redox molecule binds a polyelectrolyte and condenses as a dense phase on the coke, always within about 3 mm of carbon. A cheap metal plates onto a floating carbon mat a few centimetres above, and gravity plus the phase boundary replace the separator. PV modules on part of the mat feed DC straight into series-wired cell strings. The mat is about five times the panel area because a 6 cm bed holds about 1.9 kWh/m² at under 0.1 V ohmic loss over a 10-day discharge (about 7 A/m²). Coke adds about $4/kWh, and at about 8 kg of molecule per kWh the molecule must cost $2/kg or less to keep the total near $20/kWh.
VALUE: Floating-solar operators gain 10-day storage in the pond under and around their arrays, with no charging inverter and a cell structure costing a few dollars per kWh.
