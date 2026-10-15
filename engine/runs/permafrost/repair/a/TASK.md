# Task: repair original ideas against reality WITHOUT losing what makes them original

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 of the most ORIGINAL ideas an idea engine produced for this question. Two blind judges rated them highly
original but doubtful in feasibility (F is an order-of-magnitude plausibility score out of 10). Your job is NOT to invent
new ideas and NOT to replace them with safer known solutions. Your job is to make each one work while keeping its
anchor - the one distinctive idea that makes it original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/permafrost/repair/a/`; do not modify other files, do not commit.

For each idea, loop until it works or you can prove it cannot:
1. Name its ANCHOR (the distinctive idea) in a few words. This must survive.
2. Find the binding quantity (what decides whether it works at the needed scale - a rate, an energy balance, a
   recovery, a throughput, a safety limit) and compute it in Python with real numbers from the literature (cite the
   source in your notes).
3. Compute the cost per tonne of product (or per tonne of ore) against the CURRENT practice it replaces (e.g. winter-road
   trucking, a diesel-powered concentrator, evaporation ponds), with sourced numbers. The question demands several
   times cheaper.
4. If it fails, change the DESIGN AROUND the anchor (materials, geometry, operating regime, scale, season, which
   resource/deposit type it is used for) and recompute. Look for the regime where the anchor is strongest. Repeat -
   several rounds per idea is normal.
5. Name the hazards honestly (toxicity, environment, permafrost damage) and design them down where possible.
6. Check novelty: if the repaired design turns out to be a known system, keep the anchor and find the version that is
   not known.
7. Only if no anchor-preserving design can work, say so and give the best honest niche.
Keep `LOG.md` in your folder: one line per round (idea, change, decisive number, result). Spend about 45-60 minutes at most.

Final answer (text only): first the 4 repaired ideas in exactly this format, then a short NOTES section (per idea:
anchor kept?, decisive numbers with sources, cost vs current practice, hazards, closest existing work, verdict
WORKS / NICHE / FAILS).
=== IDEAS ===
IDEA 1
NAME: (max 5 words)
MECHANISM: (2-5 sentences: the anchor first, then the repaired design, with the decisive computed numbers)
VALUE: (1 sentence, with the cost ratio vs current practice)
(same for ideas 2-4, in the same order as below)

THE 4 IDEAS:

IDEA 1 (mean originality 8.0/10, mean feasibility 4.5/10)
NAME: Carbonyl nickel in gas pipelines
MECHANISM: This is set up beside a trunk line that ends at a gas processing or LNG plant. A small side stream of the line's own gas is partly burned to carbon monoxide and hydrogen. This gas first reduces roasted nickel ore to metal. Then, cooled to about 50 °C at a few bar, it carries the nickel off as nickel tetracarbonyl vapour, while iron, copper and rock stay behind. The vapour is metered into the line at about 0.1 mol%, which stays below its condensation pressure even in permafrost-chilled sections. A little extra carbon monoxide stops it breaking down in compressor stations, and the line runs under the same rules already used for lines carrying toxic sour gas. At the plant, heated beds in the inlet train, where mercury guard beds already sit, split the vapour into pure nickel pellets and carbon monoxide. The carbonyl never leaves the plant fence and no customer ever receives it.
VALUE: A line already carrying about 38 billion m³ of gas a year could also deliver about 100,000 t of refined nickel a year from a deposit along its route. It needs no new transport route and no reagents brought in, and nothing changes for gas customers.

IDEA 2 (mean originality 7.0/10, mean feasibility 5.0/10)
NAME: Freeze-Engine Vitriol Winning
MECHANISM: Copper-bearing liquor from a summer heap leach is stored in a pond, where it stays liquid at 0–4 °C under the winter ice. Through the winter nearly all of it is frozen in successive passes over coils, and the heat given off as it freezes boils propane, which drives a turbine and condenses in finned radiators open to −35 to −50 °C air, giving roughly 15–30 kJ of electricity per kilogram frozen. Each pass leaves a stronger drained brine, until copper sulfate reaches saturation and crystallises out as blue vitriol while the far more soluble ferric sulfate stays dissolved, so freezing both powers the plant and separates the copper from the iron. The crystals are redissolved in the spent electrolyte of a small, clean electrowinning cell run on the same power, and in spring the ferric, acidic brine and the ice meltwater, with any copper trapped in it, return to the heap as its oxidant and acid.
VALUE: A remote copper heap leach makes its own winter power, separates its copper from iron and wins clean cathode copper with no solvent extraction, no diesel and almost no acid shipped in.

IDEA 3 (mean originality 7.0/10, mean feasibility 5.0/10)
NAME: Self-Charging Frost Separator Cascade
MECHANISM: Dry crushed ore slides down a chute lined with a chosen material, so each mineral picks up its own sign of charge, and in −40 °C air, which holds almost no water vapour, that charge does not leak away. The grains fall between two plates into two metal-lined bins, each wired to the plate on the far side, so the charge carried into the bins keeps driving the plates up to a spark-gap cap of tens of kilovolts, as in a Kelvin water dropper. One unpowered pass gives only a modest upgrade, but each stage costs only a lining, two plates and a few metres of drop, so a dozen stages are stacked down a hillside or pit wall: each stage's concentrate bin feeds the next stage's chute, and a small conveyor lifts the reject of the lower stages back into the feed. The cascade reaches shipping grade with no power supply, water or reagent for the separation, and its only settings are the splitters, moved according to the grade measured in each bin.
VALUE: Remote deposits make shipping-grade concentrate on site all winter from dry ore, with no water, reagent or power for the separation, cutting the tonnage to be hauled by 5–20 times.

IDEA 4 (mean originality 6.5/10, mean feasibility 4.5/10)
NAME: Night-sky lithium freeze cascade
MECHANISM: Oil fields, gas fields and deep mines on the Siberian Platform already pump up strong calcium-chloride brine (often 0.2–0.5 g/L lithium) and must dispose of it. In winter this brine runs through a chain of shallow trays covered with polymer radiative-cooling film under an infrared-clear windshield. The film sheds heat through the 8–13 µm atmospheric window, so the trays sit about 10 K below air that is already at −40 to −50 °C. Each night every tray freezes past the calcium chloride–ice eutectic (about −50 °C). Ice and calcium chloride hexahydrate lock up together as a crust, while lithium chloride, which stays liquid down to about −75 °C, collects in a shrinking leftover liquid that drains by gravity into the next tray. After a few nights and steps, the liquid is tens of times smaller in volume and richer in lithium and bromide, and goes to an existing lithium plant. The spent crust melts in spring and goes back down the field's own disposal wells.
VALUE: Brine that Siberian oil, gas and mine operators now pay to reinject becomes a large-scale lithium concentrate, made with only the winter sky and the wells they already run.
