# Task: be maximally creative on one hard question, checking yourself against reality

QUESTION: How could storing electricity for days to weeks become ten times cheaper than today, so that wind and solar can run a whole grid through long calm, dark spells? Propose fundamentally new mechanisms or system designs - not incremental improvements of existing battery chemistries.

The hard part of this question (from an earlier analysis): The answers make the bulk medium nearly free (ore heaps, salt ponds, iron piles, quicklime, gas fields) but assume the power-conversion side (membrane and electrochemical stacks, reversible SOCs, iron combustors, CO2 turbines) is cheap and efficient, when at a handful of cycles a year that converter capex and 30-60% round-trip loss dominate the cost.

You are a researcher with tools: WebSearch (and WebFetch) to check what already exists, and Bash with python3 to
compute (do every order-of-magnitude estimate in real Python code, not in your head). Work only in
`/home/user/SomeRepository/engine/runs/energy/researcher/` (write notes and scripts there; do not modify other files,
do not commit).

Families that typical answers converge on (an idea that is a re-skin of these does not count):
- OREFLOW: Redox-mediator flow cell whose dissolved shuttle charges and discharges a huge heap of raw mineral ore, so energy capacity separates from the stack
- FLEXLOAD: Oversized energy-intensive industrial plants run hard during surplus and idle during lulls, with energy "stored" as product inventory
- SALINITY: Desalination splits water into fresh and brine ponds; pressure-retarded osmosis or reverse electrodialysis recovers the mixing energy
- CO2LOOP: Electrochemically reduce CO2 into a storable carbon fuel (methane or formate), then oxidize it back to power and recapture the CO2 in a closed loop
- IRONFUEL: Electrolytically or H2-reduced iron powder stored in piles, burned in air for steam power, with the rust re-reduced (metal-fuel cycle)
- CALOOP: Thermochemical calcium looping: power calcines limestone, then CaO and CO2 recombine to release high-temperature heat for a turbine
- THERMAL: Cheap sensible or latent heat storage (hot rock, sand, firebrick, molten salt, Carnot battery) with heat-to-power conversion
- CAES: Compressed or liquefied air or CO2 stored in caverns, aquifers, domes or tanks and expanded through turbines
- GEOMECH: Gravity or pumped-hydro variants (underground or seafloor pumped hydro, rock-fracture or geomechanical pressure storage, weights in shafts)
- H2GEO: Electrolytic hydrogen or ammonia stored in salt caverns or depleted fields and reconverted in turbines or fuel cells
- SUPERGRID: Continental or intercontinental HVDC grids that smooth weather across uncorrelated regions, plus overbuild and curtailment, so less storage is needed
- METALAIR: Ultra-cheap metal-air or rust-reversal batteries (iron-air, sulfur, zinc) built from abundant materials for multi-day duration

How to work - loop many times, this is the point of the task:
1. Invent a mechanism or system design that rests on ONE clear idea that gives the gain (everything else follows from
   it or is minimal wrapping). Aim for ideas that are genuinely new, not variants of the families above.
2. Check novelty against reality: 2-3 targeted web searches for the core mechanism. If it already exists, either drop
   it or find what about it would be new, and say so honestly.
3. Check truth against reality: write a short Python script that computes the ONE quantity that decides whether it
   works at the scale needed (e.g. power per area under the allowed loss, leak against useful rate, cost per kWh of
   the dominating part, energy per tonne). If it fails, repair the design along the scaling law you found and
   recompute, or drop it.
4. Keep a log in `researcher/LOG.md`: one line per idea attempt (idea, novelty verdict, decisive number, kept/dropped).
Aim for at least 15 idea attempts; spend about 60 minutes at most.

Final answer (text only), exactly this format, the 6 best ideas you kept (original AND checked):
=== IDEAS ===
IDEA 1
NAME: (max 5 words)
MECHANISM: (2-4 sentences: the one idea first, then the design as its consequence, with the decisive computed number)
VALUE: (1 sentence: what it makes possible and who gains)
(same for ideas 2-6)
After the IDEAS section, add a short NOTES section: for each idea the closest existing work you found and why yours
differs, and the 3 most informative things your checks taught you.
