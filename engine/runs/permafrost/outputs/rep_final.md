All four ideas keep their anchor after repair, and all four end up NICHE. Each works physically, but none reaches the claimed "several times cheaper" against the best current practice except in narrow site conditions; versions 2 and 4 fail as originally proposed. Many cost inputs are my own assumptions rather than sourced figures (flagged and varied over ranges in `calc.py`): WebFetch could not resolve most Russian domains, so sourced numbers come from search-result text only.

=== IDEAS ===
IDEA 1
NAME: Talik Dredging Under Lakes
MECHANISM: Anchor: a floating dredge mines placer gravel that a lake has already thawed (a natural talik), with no stripping or pre-thawing, and keeps working under the winter ice. Repaired: target only lakes at least 2-2.5 m deep (maximum ice is 1.2-1.9 m at 5,000-6,500 °C·day of frost) and at least 100 m across. There the steady talik is 15-22 m deep (36-67 m under 200 m lakes), so water plus silt plus pay of 18 m or less fits a 250-L-class dredge. The dredge must make its own diesel-electric power: about 1 MW of generator waste heat keeps a working pond of up to 1,500 m² open, which needs 0.69-0.81 MW at -35 to -45 °C. The sheet ice ahead of the bow (300-850 m³/day, which would take 2-3 MW to melt) is sawn into 2×2 m blocks, about 500 m of cut per day, and sunk or stacked. Running about 300 days a year instead of 165 gives about 210 rub/m³, or about 710 rub per gram recovered.
VALUE: About 1.6× cheaper per gram recovered than thawing and dredging (1.5-1.85× across the range) and 2× cheaper than draining the lake and digging, but only 1.16× cheaper than summer-only dredging of the same talik, so most of the gain comes from the talik, not the winter work.

IDEA 2
NAME: Jacked Frozen-Block Stripping
MECHANISM: Anchor: frozen overburden is cut free and pushed sideways with jacks, as intact blocks, into the previously mined cell, and only the paystreak beneath is thawed with summer creek water. Repaired: blocks of 40×40×10 m (30,400 t), with the cuts around them kept flooded by creek water; this gives buoyancy and stops the cut from refreezing in about 1.2 days. The push is 92 MN (19 hydraulic cylinders of 5 MN), the stress on the pushed face is 0.23 MPa, and the jacks brace against the next block's still-frozen base with a safety factor of 3.5. The next block's paystreak is thawed only after the push, through needles on a 3 m grid using about 10 m³ of water per m³. Diesel use is 0.12-0.15 l/m³, against 0.30 for natural layer-thaw dozing and 0.65 for ripping and dozing. Output is limited by hot-water drilling: about 7,600 m of holes per block, so at 1 m/min one drill rig and crew move about 190,000 m³ a season at about 62 rub/m³.
VALUE: About 760 rub/g against about 990 rub/g for the cheapest current practice (natural layer-thaw dozing), so about 1.3× cheaper per gram (2-5× less diesel, not the claimed 10×), and the vegetation mat ends up back in place; at a drilling rate of 0.5 m/min it only breaks even.

IDEA 3
NAME: Floating Bluff Coal Miner
MECHANISM: Anchor: a self-propelled barge with an autonomous excavator mines frozen coal at a river-bluff outcrop and re-stacks the removed rock as an open dry-stone revetment, which lets winter cold in and keeps the cut bank frozen. Repaired: re-stacking all the rock in place only balances when overburden is at most 2.5 times the seam thickness. So only a facing layer at least 1 m thick is placed as dry stone (0.23-0.46 m³ per tonne of coal, matching the 0.8-1.5 m used in crushed-rock slope protection), and the surplus rock goes as riprap for the villages' own eroding banks. Sites need at most 1 m³ of rock per m³ of coal and must lie within about 50-150 km of the villages; bluffs on the outside of river bends give deep water at the face. One barge working 60 mining days cuts 42-56 thousand tonnes a season for 5-8 villages (about 7 t per person per year), provided autonomous stone placement reaches at least 15 m³/h; at 5 m³/h output is capped at 8-16 thousand tonnes.
VALUE: Delivered at 2,100-2,500 rub/t (117-141 rub/GJ even for weathered coal at 18 MJ/kg) against 6,962 rub/t (332 rub/GJ) for today's barge supply to the Kolyma coal depots, about 2.4-2.8× cheaper per GJ delivered; it is only 1.2-1.4× cheaper than a small land pit plus winter road, and about 10× cheaper only against the multi-leg Arctic chains at up to 25,000 rub/t.

IDEA 4
NAME: Wintering Miner-Barge Boilerhouses
MECHANISM: Anchor: the coal barge is itself the village boilerhouse; its hold is the winter coal bunker, it freezes into a backwater beside the heat network, and it leaves after the spring ice breaks up to refill. Repaired: unpowered 2,000 t barges (100×22 m, drawing 1.26 m instead of 3.5-3.9 m for 5,000-8,000 t hulls, which the shoaling Yana and Indigirka cannot float). Each carries a containerized automatic coal boiler (1.3 MW average, 3.2 MW peak, enough for about 300-700 people). One tug serves several barges, the hold is loaded directly by the floating bluff miner or a riverside mine, and the haul is at most 300-800 km. The barge is away from the village for 92 summer days; its own round trip takes only 12-22 days, which leaves about 75 days of paid freight work that covers the cost of a used hull.
VALUE: 3,000-5,000 rub/t at 300-800 km against about 8,080 rub/t for current river supply plus transshipment, trucking and stockpile losses, so 1.6-2.7× cheaper; at the original 1,500 km with new 8,000 t hulls it is 0.66-0.88× (more expensive), and it only fits sub-Arctic river villages that need no summer heating.

NOTES
Idea 1 (Talik Dredging Under Lakes)
- **Anchor kept:** yes.
- **Decisive numbers:**
  - Talik depth from the standard steady-state formula for a circular lake (Lachenbruch 1957), cross-checked against measured lake taliks: 91 m by electromagnetic survey (Creighton et al. 2018) and about 25 m under a Yakutian lake (SPbU).
  - Lake ice from Stefan's ice-growth law.
  - Open-water heat loss of 460-540 W/m², consistent with Maykut's 400-700 W/m² for winter leads.
  - Dredge season of 160-180 days (Nafikov, Siberian Federal University).
  - Cross-check on dredging cost: a Yukon floating plant at US$0.90 per loose cubic yard, about 125 rub per bank m³ (Yukon Geological Survey).
- **Baselines (per gram recovered):** thaw and dredge 1,143 rub/g; drain the lake and dig 1,401; summer-only talik dredging 824; repaired idea 709.
- **Consistency:** ice margin at least 0.1 m; talik reaches bedrock under lakes at least 100 m across and more than about 50 years old; heat margin of 1.2-1.4× in winter only with on-board generators (a grid-fed dredge pays an extra 41-49 rub/m³ and should work only the shoulder seasons).
- **Hazards:** working on thin ice around the pond; brash ice build-up; frozen tailings piles; fine-gold loss; permits for working in water.
- **Deciding unknown:** how much pay, at what grade, lies under lakes at least 2 m deep. Experiment: in March, drill through the ice using it as a platform, with electromagnetic soundings plus 12-16 holes per lake on a 40 m grid at 3-5 lakes (about 50 holes), and a 2-week trial of sawing and sinking the ice.
- **Closest existing work:** through-ice winter dredging at Nome; the Nome shelf dredge since 1986 (SIBRAN); the 2023 Siberian Federal University proposal for a hangar over the dredge pit; Soviet dredge-crew winter ice work in the official job handbook.
- **Verdict:** NICHE.

Idea 2 (Jacked Frozen-Block Stripping)
- **Anchor kept:** yes.
- **Decisive numbers:**
  - Long-term frozen-ground bond strength about 0.2 MPa (Russian code SP 25.13330).
  - Thawing water about 10 m³ per m³ of ground (Zabaikalsky State University method).
  - Dozer fuel 55-75 l/h (Caterpillar handbook).
- **Rounds:** as proposed (20 m blocks) it fails: push 48 MN, bracing safety factor only 1.7, kerf diesel 0.21 l/m³, cost 381 rub/m³ against 110. Flooded cuts and 40 m blocks bring it to 62 rub/m³ and 760 against 988 rub/g, about 1.3×.
- **Consistency:** face stress 0.11-0.23 MPa against about 1 MPa strength; about 80 days of usable creek water against a 13-31 day cycle per row; cuts refreeze in about 1.2 days unless flushed.
- **Hazards:** crushing at the jacked face in ice-rich silt; boulders stopping the hot-water drill; uncontrolled thawing of the bracing block; blocks tipping into the cell; workers between 10 m frozen walls.
- **Deciding unknown:** the field sliding friction of a block on thawed gravel, and the hot-water drilling rate in gravelly frozen ground. Experiment: 3-5 test blocks of 6×6×H m at a working placer, pushed by two 5 MN cylinders bracing on rock anchors (n=3 per needle spacing gives friction to about ±20%).
- **Closest existing work:** the Soviet method of cutting frozen ground into small blocks with slot-cutting machines; jacked-box tunnelling and pipe jacking; hydro-needle thawing. Nothing found that pushes intact frozen overburden sideways.
- **Verdict:** NICHE.

Idea 3 (Floating Bluff Coal Miner)
- **Anchor kept:** yes.
- **Decisive numbers:**
  - Kolyma depot tender: 100,778 t for 701.6 Mrub, about 6,962 rub/t delivered.
  - Delivered coal across Yakutia 3.5-25 thousand rub/t, 3-8× the shipping-point price (regional energy commission data, via E3S 2020).
  - Verkhoyansk district burns 77 thousand t/yr.
  - Crushed-rock slope protection needs at least 0.8-1.5 m to cool the ground.
  - ETH's HEAP autonomous excavator built a 6×65 m dry-stone wall, but its placement rate is not published.
- **Baseline (per GJ delivered):** 2.4-2.8× cheaper than current river supply, 1.2-1.4× than a small land pit with a winter road.
- **Consistency:** rock balance (overburden/seam at most 2.5); stone-placement rate caps output; 110-day navigation; at a rock-to-coal ratio of 2.5 it drops to 0.78× against a land pit, so the site rule is binding.
- **Hazards:** undercut face collapsing onto the barge; weathered, lower-energy coal that can self-heat; water-protection-zone rules; spring flood levels.
- **Deciding unknown:** energy content and ash of the coal in the first 5-20 m behind the outcrop face, plus the rock-to-coal ratio at each site. Experiment: boat-mounted coring, 4 cores at each of 10 outcrops (about 40 samples), and a 1-week autonomous stone-placement trial aiming for at least 15 m³/h.
- **Closest existing work:** Lena steamboats historically took coal from bank outcrops; the Kangalassy and Zyryanka riverside mines ship coal by barge; the HEAP wall; Batugina and Khoiutanov (2025) on local coal for Arctic Yakutia.
- **Verdict:** NICHE (works on sites that meet the rule).

Idea 4 (Wintering Miner-Barge Boilerhouses)
- **Anchor kept:** yes.
- **Decisive numbers:**
  - Draft calculated from hull dimensions.
  - Yana and Indigirka too shallow in 2025, so Verkhoyansk's coal moved to the winter road.
  - Barge cost: about $3M for a 5,000 t barge (Ukraine), and Russian shipbuilding costs 2.5-3× Chinese.
  - Same Kolyma depot price as Idea 3.
- **Rounds:**
  - As proposed it fails: 0.66-0.88×, and a new hull adds 11,250 rub/t.
  - 2,000 t hull with a used barge: 1.3-1.46× at 300 km.
  - Adding summer freight work: 1.6-2.7× at 300-800 km.
- **Consistency:** draft fits only for the 2,000 t hull; the 92-day absence window fails wherever summer heating is needed (high Arctic); bunker sized for about 300-700 people.
- **Hazards:** carbon monoxide and fire on board; ice pressure on the hull; ice-jam floods; the heat main across the moving bank and ice edge; ash, about 10-20% of the coal; a late barge leaving the village without heat, so a small land backup boiler is needed.
- **Deciding unknown:** the extra cost of a frozen-in hull plus heat-main connection against a land boilerhouse, net of summer freight income. Experiment: one winter with a used 1,000-2,000 t barge and a 2-3 MW containerized boiler at a Lena or Aldan village (n=1), measuring availability, heat-main losses and ice loads with strain gauges.
- **Closest existing work:** the Akademik Lomonosov floating nuclear plant at Pevek (70 MWe, 50 Gcal/h of heat); Soviet "Severnoye Siyaniye" floating diesel power plants; river fleets routinely winter in backwaters. Nothing found for a coal barge that is its own bunker and boilerhouse.
- **Verdict:** FAILS as proposed; NICHE once repaired.

Files are in /home/user/SomeRepository/engine/runs/permafrost/genius/repair_final/:
- calc.py
- LOG.md (one line per round)
- NOTES.md (source list and consistency tables)