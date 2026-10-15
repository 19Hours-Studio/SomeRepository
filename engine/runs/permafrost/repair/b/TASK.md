# Task: repair original ideas against reality WITHOUT losing what makes them original

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 of the most ORIGINAL ideas an idea engine produced for this question. Two blind judges rated them highly
original but doubtful in feasibility (F is an order-of-magnitude plausibility score out of 10). Your job is NOT to invent
new ideas and NOT to replace them with safer known solutions. Your job is to make each one work while keeping its
anchor - the one distinctive idea that makes it original.

You have tools: WebSearch/WebFetch (check what exists, find real material data, field data and costs) and Bash with
python3 (do every estimate in real code). Work only in `/home/user/SomeRepository/engine/runs/permafrost/repair/b/`; do not modify other files, do not commit.

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

IDEA 1 (mean originality 7.5/10, mean feasibility 4.0/10)
NAME: Winter Wind Deflation Placer
MECHANISM: All winter, frozen placer pay gravel is ripped and spread a few centimetres thick over a broad pad of flat, windy tundra next to the cut. The dry −30 °C wind sublimes the pore ice from the top of the layer, freeing up to about a millimetre a day, and because no liquid water ever forms, the freed silt and light quartz and feldspar sand blow off loose into a snow fence. Gold, cassiterite, wolframite and other heavy grains stay behind; a daily harrow exposes fresh frozen layer, and the residue is swept up and dry-screened to remove the gravel. Because the rate is fixed per square metre, the pad is sized by area (about a square kilometre handles a season's pay gravel), and the silt-free residue, a small fraction of the original volume, is stockpiled so that the short summer wash plant finishes the whole year's ore in a few weeks of clear water, with no mud reaching the river.
VALUE: Placer mines gain a second production season in midwinter and finish all their ore in a few clean-water summer weeks, with no water, reagent or silt discharge and almost no fuel for the winter concentration.

IDEA 2 (mean originality 8.0/10, mean feasibility 4.0/10)
NAME: Self-feeding ore-ice dam
MECHANISM: In early winter, the pay gravel stockpiled in autumn is laid across a creek in layers and sprayed with water, so the dam itself is frozen ore. A peat cover on its crest and upstream face keeps it frozen while spring snowmelt fills the basin behind it. All summer a fixed timber gate lets a steady flow of sun-warmed basin water run down the dam's bare downstream face. This water melts the ice cement at a rate set by the flow, so gravel drops into the water at roughly the right ratio for washing. The mix runs straight down a riffled chute, where cassiterite, wolframite or gold settle and the light gravel goes to a pit. The stored water and its head do both the feeding and the separation, with no loaders, pumps, fuel or reagents.
VALUE: A roadless placer can run a full washing season unattended from one autumn stockpile and one winter's snow, cutting out the summer fuel, pumps and loaders that make up most of its cost.

IDEA 3 (mean originality 7.5/10, mean feasibility 2.5/10)
NAME: Self-Sorting Wave-and-Ice Pond
MECHANISM: Over a stripped, ice-rich placer, a spillway holds a shallow pond of the ground's own meltwater. The pond absorbs the round-the-clock summer sun and thaws the gravel beneath it, wind waves lift silt and sand over the spillway, and their pressure pulses jig gold and heavy sand down through the stones onto the frozen floor. Each autumn the pond is set just shallower than the winter ice will grow, so the ice freezes onto the tops of the stones. In spring the spillway is closed, snowmelt lifts the bottom-fast ice, and the wind pushes the floes and their stones onto a dump shore, the way lake ice builds boulder ramparts. The spillway is lowered each year so the thin heavy layer rides down with the thaw front to bedrock, where only that layer is dug and washed.
VALUE: Even in the cobbly gravels typical of Siberian placers, sun, wind and winter ice remove the silt, sand and stones in place, so only a few percent of the deposit is ever dug and washed, with no pumps, washing-plant fuel or reagents.

IDEA 4 (mean originality 7.0/10, mean feasibility 4.0/10)
NAME: Snow-buoyed ice-shell ore pods
MECHANISM: Pods are made on the spot at a slot cut in the main-channel ice of a big north-flowing river. Crushed high-grade ore and enough dry snow to float it (roughly a cubic metre of snow per tonne of ore) are packed into a mould and sprayed with river water. The −40 °C air freezes this overnight into a sealed ice shell. The pods float up against the smooth underside of the ice and ride the current, out of reach of wind and waves, to a boom and recovery slot at a plant or year-round port downstream. There they are lifted out and cracked open, and the ice is thrown away. The 0 °C river cannot melt the pods, they cost nothing and they never go back upstream, so throughput is limited only by how fast the two slots work. Whole ore can therefore travel, and separation stays at an existing concentrator.
VALUE: A riverside deposit can send ore all winter to a downstream plant or port with no vessels, fuel, pod fleet or return haul, using only snow, river water and cold.
