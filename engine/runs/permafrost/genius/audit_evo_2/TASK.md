# Task: adversarial review - find what would make these ideas fail or overstate their value

QUESTION: Russia holds vast natural resources (oil, gas, metals, diamonds, coal, rare earths) in Siberia, Yakutia and the Arctic, mostly under permafrost and far from roads, railways and ports. Propose a fundamentally new way to reach, extract, process or bring these resources to market that is extremely cheap (several times cheaper than current practice), has never been tried or seriously costed by anyone, can be deployed within a few years, and works with known physics. Not incremental improvements of existing mining, drilling, pipelines or winter-road logistics.

Below are 4 ideas, already repaired once against reality by a researcher. Your job is to be the toughest competent
outside reviewer: an engineer who will lose money if any of these claims is wrong. You do NOT fix or improve the
ideas; you find their defects, prove each one with a number, and rank them.

You have tools: WebSearch/WebFetch and Bash with python3 (check every claim in real code). Work only in
`/home/user/SomeRepository/engine/runs/permafrost/genius/audit_evo_2/`: read no other files in the repository, do not modify other files, do not commit.

For each idea, attack in this order:
1. Recompute every number the text states (arithmetic, units, mass/energy balances). Flag any that do not reproduce.
2. Consistency: list every tolerance, margin and window the design relies on, and check every rate in the design
   against it over the whole operating time (rate x duration vs window). Check that the site/route/season named
   really has the conditions assumed (temperatures, flows, ice, distances) - find measured data.
3. Baseline: is the comparison against the best current practice a competent operator would use, per unit of
   recovered/delivered product? Name the real competing alternatives it ignores and recompute the ratio.
4. Assumptions: which decisive numbers (efficiencies, friction, rates, loss fractions, costs) are assumed rather
   than sourced? How far can they move, and does the claim survive the plausible range?
5. Evidence and statistics: are the proposed tests able to show what is claimed (sample sizes, confidence bounds)?
6. Hazards and showstoppers not mentioned (safety, environment, regulation, logistics, scale-up).
Do not pad: a defect needs a mechanism and a number. If a claim survives your check, say so in one line.

Final answer (text only), exactly this format:
=== REVIEW ===
IDEA 1: <name>
DEFECT | <FATAL/MAJOR/MINOR> | <one sentence: what is wrong> | <the number or source that shows it>
(as many DEFECT lines as needed, most severe first)
SURVIVES | <claims that held up under your check, one line>
(same for the other ideas, in the same order as below)

THE 4 IDEAS:
IDEA 1
NAME: Pond-Heated Jet Undercut Caving
MECHANISM: Anchor: creek water thaws and removes the pay from under the frozen overburden, and the overburden then caves onto bedrock under its own weight, with no stripping and no roof support. A creek flowing through a gallery fails: at valley slopes of 0.5-1 % the Shields number is 0.026-0.043, below the 0.047 needed to move gravel, so the thawed gravel stays put and the gold settles on the gallery floor under the caving roof. Repaired design: low-pressure jets (monitors) using water from the solar-warmed recycle pond and the creek (a 3 ha pond absorbs about 5.4 MW in July-August) thaw the face. Heat delivered vs needed is 1.27 at 4 °C and 2.5 at 7 °C, at 7 m³ of water per m³ of gravel. A hydro-elevator lifts the slurry to a sluice at the portal. Panels about 25 m wide retreat with nobody underground, and the roof caves within hours to days (0.58 MPa bending stress against 0.2-0.5 MPa long-term tensile strength). Two monitors give about 216 k m³ of pay per 70-day season at about 650 rub/m³ (556-965 across the sensitivity range).
VALUE: For deep, thin frozen placers (overburden:pay ratio 6 or more) it costs about 620 rub/g against 1,100-2,650 rub/g for the cheaper of open-cut and drill-blast underground mining, 1.8-3.4× cheaper.

IDEA 2
NAME: Frozen-In Barge Auger Drift Mining
MECHANISM: Anchor kept: horizontal augers from a barge at the bank bore the frozen paystreak and leave the frozen overburden in place as roof. The ground holds for a while: under 10-20 m of cover the pillars between holes carry 0.9-1.8 MPa against 5-8 MPa short-term strength. This holds only if tailings are pumped back and freeze in each hole within weeks. Two design fixes are needed. Round holes centred in the gravel miss the gold on bedrock, so the hole centre is set 0.3-0.5 m above bedrock; that sweeps 65-74% of the bedrock surface but dilutes the feed with 0.4-0.6 m of bedrock, and only 0.61 of the seam is extracted. A 130-day open-water season gives only 70-100k m³ at $68-96/m³, so the barge is frozen into a notch in the bank and run for 280 days with a heated plant (215k m³ at $45-55/m³). The target becomes deep river-cut placers (30-40 m cover) with at least 1.8 m of pay, gold spread through the gravel and clasts under 0.4 m, which are now drift-mined or left in the ground.
VALUE: Even repaired it costs about $36/g at 3 g/m³, against $23/g for frozen open pit and an estimated $29/g for drift mining. It is not cheaper, so it is only a niche for deep placers that open pits cannot reach.

IDEA 3
NAME: Sealed Derelict-Hull Coal Bunker
MECHANISM: Anchor: a surplus river hull, floated in once, becomes a permanent multi-year sealed coal bunker beside the heat network and is topped up straight from barges. An 8 kt hull holds 7.4-8 kt (2.1-4 winters of a 2-3.5 kt burn), 0.52 m light draught and 3.3 m loaded. If it is frozen in afloat, the winter burn makes it want to rise 1.05 m; the ice cracks along the hull (1.3 MPa against 0.5-0.8 MPa ice flexural strength), which is harmless. A 76 kW moat kept open with waste heat (3.3 % of the 2.3 MW boiler) removes thermal ice pressure. Alternatively the dock is dewatered and the hull rests on a gravel pad at 33 kPa. The flue-gas blanket is dropped: a sealed hold holds only 1.4 t O₂ (at most 1.9 K bulk heating), and breathing adds about 80 kg O₂/day (about 12 kW), so sealed hatches, a small N₂ membrane and CO monitoring are enough. A derelict hull, an existing backwater and a short conveyor to the existing boiler house bring the annualised cost to about 2,800 rub/t at 3 kt/yr.
VALUE: Parity to 1.8× in general; 1.4-2.5× cheaper only for failure-prone shallow-river villages (20-30 %/yr chance of a failed delivery), with removable handling costs being 12-29 % of 8,080 rub/t, not half.

IDEA 4
NAME: Under-Ice Brine-Thawed Tin Dredging
MECHANISM: Anchor kept: seawater keeps the shelf tin placer unfrozen, so a dredge can dig it with no thawing, stripping or roads. The summer-only version has already been tried twice. Sevmorolovo worked Vankina Bay in the late 1970s and stopped because waves upset its onboard gravity plant; the BIMA dredge at Nome (1986-90) lost money. Repaired design: the same dredge also works December to June in a covered slot under the stationary landfast ice of the SE Laptev Sea, where there are no waves or storms. That raises effective days from about 58 to about 214 a year. Holding the slot open takes 0.65 MW against 2.25 MW of diesel waste heat. Ice ahead (0.17 m³ per m³ of ground) is sawn and lifted out, because melting it would need 4.3 MW. Work is limited to water deeper than about 4 m and at least 0.3-1 km offshore, where ice-bonded permafrost lies below the 17 m dig depth (Buor-Khaya borehole: 28 m down at 800 m offshore).
VALUE: For a 600 m³/h dredge, cost falls from about $126k/t Sn in the open-water-only mode to $37k/t at 0.5 kg/m³ and $23k/t at 0.8 kg/m³, 3-5× cheaper than the known seasonal mode. It beats PT Timah's offshore cost ($14-22k/t) only if the shelf grade is at least 0.85 kg/m³.

