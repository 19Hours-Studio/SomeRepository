=== IDEAS ===
IDEA 1
NAME: Reservoir-Talik Tributary Dredging
MECHANISM: Anchor: placers drowned under a Far-North hydro reservoir get thawed by the water above them, so they can be mined from open water with no stripping-by-thaw, pond building or ice sawing. Reality check: after 40 years a 1-D enthalpy model gives a talik of only 5.8/8.5/10.8/12.5 m for mean bottom water at 1/2/3/4 °C, so the "whole floor thawed" claim is false for deep main-valley sections. The repaired design targets drowned tributary mouths with total sections of 8 m or less and an overburden:pay ratio of 2 or less, on the 130 km² band 1.5-25 m below the minimum operating level (UMO, 432 m). It uses an electric 600 m³/h submerged-pump cutter dredge fed from the Kolyma HPP grid, starts at ice-off when the reservoir is at its lowest, and discharges tailings below the surface into the mined-out cut. That discharge keeps fines escape under the 0.5-1.3 % that the fishery limit allows; at 5 % escape the plume would add 1.0-2.6 mg/L. Modelled cost is 526-683 rub/m³ of section (1.2 Mm³ per 120-day season).
VALUE: It adds a resource that is now sterilised, at roughly the same cost as open-cut placer gold (0.7-1.0× of 1,050-2,000 rub/g at the same section), not several times cheaper.

IDEA 2
NAME: Pond-Heated Jet Undercut Caving
MECHANISM: Anchor: creek water thaws and removes the pay from under the frozen overburden, and the overburden then caves onto bedrock under its own weight, with no stripping and no roof support. A creek flowing through a gallery fails: at valley slopes of 0.5-1 % the Shields number is 0.026-0.043, below the 0.047 needed to move gravel, so the thawed gravel stays put and the gold settles on the gallery floor under the caving roof. Repaired design: low-pressure jets (monitors) using water from the solar-warmed recycle pond and the creek (a 3 ha pond absorbs about 5.4 MW in July-August) thaw the face. Heat delivered vs needed is 1.27 at 4 °C and 2.5 at 7 °C, at 7 m³ of water per m³ of gravel. A hydro-elevator lifts the slurry to a sluice at the portal. Panels about 25 m wide retreat with nobody underground, and the roof caves within hours to days (0.58 MPa bending stress against 0.2-0.5 MPa long-term tensile strength). Two monitors give about 216 k m³ of pay per 70-day season at about 650 rub/m³ (556-965 across the sensitivity range).
VALUE: For deep, thin frozen placers (overburden:pay ratio 6 or more) it costs about 620 rub/g against 1,100-2,650 rub/g for the cheaper of open-cut and drill-blast underground mining, 1.8-3.4× cheaper.

IDEA 3
NAME: Bluff-Anchored Barge Coal Augers
MECHANISM: Anchor: a floating highwall auger drills a frozen river-bluff coal seam at summer water level and loads straight into the hold, so no rock is moved. A cycle model of a 1.8 m × 100 m hole (331 t) gives 33-53 t/h, so a 20 kt season is 60 holes, 26 days and 145 m of bluff; the original 40 t/h claim holds. Repairs: the 300 kN thrust goes into two adfreeze anchors in the frozen bluff (283-424 kN each) instead of spuds (about 100 kN usable each). Webs are 0.6 m where cover is up to 30 m and 0.9 m deeper (unfrozen safety factor 3.1/1.5/0.9 at 15/30/50 m with 0.6 m webs). A ±3 m adjustable frame gives a 60-120 day water-level window against the 26 days needed. Hole mouths are plugged afterwards against oxidation. One barge must serve at least about 60 kt/yr on one river system; one village alone costs about 6,500 rub/t.
VALUE: About 3,200 rub/t delivered to the village shore against 5,300-10,300 rub/t for long-haul river coal and 3,700-7,400 rub/t for a micro-pit plus winter road (1.2-3.2× cheaper).

IDEA 4
NAME: Sealed Derelict-Hull Coal Bunker
MECHANISM: Anchor: a surplus river hull, floated in once, becomes a permanent multi-year sealed coal bunker beside the heat network and is topped up straight from barges. An 8 kt hull holds 7.4-8 kt (2.1-4 winters of a 2-3.5 kt burn), 0.52 m light draught and 3.3 m loaded. If it is frozen in afloat, the winter burn makes it want to rise 1.05 m; the ice cracks along the hull (1.3 MPa against 0.5-0.8 MPa ice flexural strength), which is harmless. A 76 kW moat kept open with waste heat (3.3 % of the 2.3 MW boiler) removes thermal ice pressure. Alternatively the dock is dewatered and the hull rests on a gravel pad at 33 kPa. The flue-gas blanket is dropped: a sealed hold holds only 1.4 t O₂ (at most 1.9 K bulk heating), and breathing adds about 80 kg O₂/day (about 12 kW), so sealed hatches, a small N₂ membrane and CO monitoring are enough. A derelict hull, an existing backwater and a short conveyor to the existing boiler house bring the annualised cost to about 2,800 rub/t at 3 kt/yr.
VALUE: Parity to 1.8× in general; 1.4-2.5× cheaper only for failure-prone shallow-river villages (20-30 %/yr chance of a failed delivery), with removable handling costs being 12-29 % of 8,080 rub/t, not half.

=== NOTES ===
How this was done: Python scripts and LOG.md are in /home/user/SomeRepository/engine/runs/permafrost/genius/repair_evo_a/ (idea1.py to idea4.py; LOG.md has one line per round, 18 rounds). WebFetch failed on every domain (DNS errors), so all sourced numbers come from WebSearch result summaries. Cost inputs that are not sourced are bottom-up estimates: diesel 95 rub/L, labour 300 k rub/month, frozen-ground stripping 200-350 rub/m³, washing 350 rub/m³, drill-blast underground 2,500-4,000 rub/m³. They are cross-checked against the World Gold Council's Russian AISC of $1,018/oz for 2022, which the open-cut model reproduces. I could not verify the input figures of 8,080 rub/t and 1.77 t of rock per tonne of coal.

IDEA 1. Anchor kept: yes.
- Decisive numbers: UMO 432 m; area 292 km² at UMO and 443 km² at full level (voda.gov.ru register, ru.wikipedia Kolyma HPP); river ice 0.8-1.3 m and about 200-day ice cover (Great Russian Encyclopedia); a talik forms where water is deeper than the maximum ice (Burn 2002 / Arp 2016); Damen DOP submerged pumps reach 50-100 m, DOP250 = 1,250 m³/h of mixture.
- Baseline per gram recovered (pay 0.8 g/m³):

| Overburden:pay ratio | Open-cut | Land bucket-line dredge (with pre-thaw) | Reservoir dredge |
|---|---|---|---|
| 1 | 1,051-1,338 rub/g | 1,176 rub/g | 1,290-1,860 rub/g |
| 4 | 2,200-3,350 rub/g | 2,940 rub/g | 2,730-3,950 rub/g |

- Why it is not cheaper: the overburden still has to be dredged, and the season is short for the capital involved.
- Consistency table: floor sits 1.5 m or more below the ice, OK. Talik vs section depth: OK only if bottom water is 2 °C or warmer and the section is 8 m or less. Water depth 3-46 m vs pump reach, OK. Season volume vs the 130 km² area, about 1000× margin. Winter drawdown of 19.5 m, so the dredge must be parked over floor at 427 m or lower, or hauled out. Turbidity fails at 5 % escape and needs 0.5-1.3 % or less.
- Hazards: plume in a fishery and hydropower reservoir; drowned timber snagging the cutter; mooring through a 15-19 m seasonal level change; poor bedrock cleanup (recovery assumed 0.70); permits under the Water Code.
- Deciding unknown: whether unmined pay grade exists in reach, including reserves written off at flooding (archive check), and the in-situ talik depth. Cheapest experiment: winter drilling from the ice on 2 tributary mouths, about 60 holes (placer grade CV 1-1.5 gives ±25 % on the mean) plus 4 thermistor strings.
- Closest existing work: offshore tin bucket-line dredging off Bangka/Belitung in 50 m of water, deep cutter-suction dredges, reservoir desilting. No reservoir-floor placer mining in Russian permafrost reservoirs was found.
- Verdict: NICHE.

IDEA 2. Anchor kept: yes (the caving is unchanged; how the heat and water are delivered changed).
- Decisive numbers: thaw energy 69 MJ/m³ (20 % ice, -4 °C); Dittus-Boelter gives h = 330-860 W/m²K; Meyer-Peter Müller transport fails at slopes of 1 % or less; caving span 11-28 m at long-term and 31-49 m at instantaneous tensile strength.
- Baseline: 620 rub/g (1.5 g/m³, recovery 0.70) against open-cut at 1,100-4,400 rub/g and drill-blast underground at 2,080-3,330 rub/g, so 1.8-3.4× cheaper for overburden:pay ratios of 4-12.
- Consistency table: water at 5-7 °C or warmer only in July-August (about 70 days, estimate). Heat ratio is 1.27 or more and below 1 under 4 °C. Face advance is about 4 m/h, so large roof areas fall at once and nobody can be underground. Subsidence of 1-1.5 m means the creek must be diverted around the panel. Pump load 0.8 MW.
- Hazards: air blast or slurry surge from sudden falls; water inrush through subsidence cracks; ice-rich silt flowing in and diluting the feed; losing face equipment (winched sleds); a cold roof hanging up and failing later.
- Deciding unknown: the in-situ caving span and the heat-use efficiency. Experiment: one 25 m × 150 m test panel at an operating artel, measuring water temperatures in and out and slurry density, with 6-8 cave events recorded by extensometers and drone survey (gives the span to ±20 %).
- Closest existing work: the NIOSH borehole miner (jet thawing plus hydraulic lift in permafrost gravel); Ryveem, Chukotka (Gornyi Zhurnal 2019, jetting in an unflooded chamber plus borehole lift); drill-blast underground placer mining with caving. The novel part is full-width caving retreat heated by the pond and creek.
- Verdict: WORKS, for deep thin placers in July-August.

IDEA 3. Anchor kept: yes.
- Decisive numbers: a 30-inch scroll auger runs at about 10 ft/min, about 118 t/h (US patent 6,293,628), so cutting does not limit output and adding and pulling flights does. Typical auger depth is 55-67 m; a 1.83 m BryDet single-flight reaches about 244 m. Auger recovery is 35-50 % (NIOSH); panel recovery here is 48 %.
- Baseline per tonne delivered: 3,200 rub/t against long-haul river coal at 5,300-10,300 rub/t (mine price + 1,000-2,000 km of freight + handling) and micro-pit plus winter road at 3,700-7,400 rub/t. Mining-only cost is about 2,090 rub/t, so it does not beat an existing riverside open pit.
- Consistency table: seam of 2.0-2.2 m or more within ±3 m of summer water level; deep water at the toe of a cut bank; webs safe up to 30 m cover; anchors take the thrust; window 60-120 days against 26 needed.
- Hazards: bluff blocks falling onto the barge (work only stable bedrock bluffs, not ice-rich ones); later fires in open auger holes (plug them); ice in frozen coal cargo.
- Deciding unknown: whether such outcrops exist near villages with no mine nearby, and the penetration rate in frozen coal. Experiment: a boat survey of cut banks, then a 2-week trial of a rented auger on a spud pontoon, about 10 holes 60-100 m long (mean rate to ±15 %).
- Closest existing work: land-bench highwall augering. No barge-mounted variant was found.
- Verdict: WORKS, conditional on the site.

IDEA 4. Anchor kept: yes (the flue-gas blanket was replaced).
- Decisive numbers: IMSBC / P&I club guidance treats coal as an oxygen-depleting cargo, requires CO monitoring and warns against ventilation. Open stockpiles of oxidation-prone coal are limited to about 6 months (enterprise rules citing RD 34.44.101-86); the sealed hold is what lets storage go multi-year. Six Yakutian districts were short of coal in December 2025, though because of debts, not logistics. Low water cut deliveries on the upper Lena (PortNews).
- Baseline per tonne burned: benefit 1,300-5,100 rub/t (removed transshipment, stockpile and trucking 950-2,350; freight 350-875; insurance against a failed delivery 625-1,875 at p = 5-15 %) against an annualised cost of 2,800 rub/t. The cheapest alternatives are a bigger shore stockpile (limited by self-heating rules) and a closed warehouse (about 6,700-11,000 rub/t at 3 kt/yr).
- Consistency table: capacity OK; dock depth 3.8 m or more; ice behaviour OK with the moat; O₂-limited self-heating OK; reclaiming frozen coal needs coal moisture of 8-10 % or less, or a ripper on the excavator.
- Hazards: CO in the hold; hull corrosion; thaw slumping around the basin (put it on thaw-stable gravel); permitting a vessel as a fuel store.
- Deciding unknown: the real chance of a failed delivery for each village, and how coal behaves in a sealed hold over 12-18 months. Experiment: one barge with 1-2 kt of coal, sealed, with about 25 O₂/CO/temperature probes through one summer and one winter, plus a frozen-coal reclaim test.
- Closest existing work: floating power plants (Akademik Lomonosov, powerships), river fleet overwintering frozen in backwaters, closed coal stores. No hull used as a multi-year bunker was found.
- Verdict: NICHE.