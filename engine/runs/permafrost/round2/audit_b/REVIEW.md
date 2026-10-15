=== REVIEW ===
IDEA 1: Self-feeding ore-ice buttress dam
DEFECT | MAJOR | Gravity flow at 2.2-3.2 m³ of water per m³ cannot carry the thawed gravel from the face to the sluice, so loaders or dozers are still needed and much of the $2.65/m³ saving goes. | Meyer-Peter-Müller / Wong-Parker bedload capacity at slope 0.05-0.08 with d50 10-20 mm needs 14-145 m³ of water per m³ of gravel (47 L/s carries 28-280 m³/day against 1,270-1,850 m³/day thawed); a 20-30% slurry deposits at sluice slopes (c2_toe.py)
DEFECT | MAJOR | The baseline is the washing stage only, so per recovered gram the gain is far below "several times". | (4.65+M)/(2.0+M) = 1.38-1.08x for an assumed winter-mining/hoisting cost M of $5-30/m³
DEFECT | MAJOR | "A sluice needs about 3 m³/m³" is the bottom of the measured range, so bypass water must be routed around the face, and that routing is not designed. | USBM stationary plants use 650-2,000 gal/yd³ = 3.2-9.9 m³/m³ (911metallurgist.com/blog/gravity-gold-process-water-requirements); a modern Yukon trommel uses 1,600 igpm for 130-140 loose yd³/h ≈ 4.1-4.4 (ygsftp.gov.yk.ca placer atlas)
DEFECT | MINOR | 50-55 MJ/m³ needs a pile at -5 °C or warmer; a pile hoisted into -30 to -40 °C air stays at -10 to -20 °C inside, so thaw energy and water per m³ rise 10-40% and season output falls by the same factor. | E = 0.15×306 MJ + ~1.6 MJ/m³K×ΔT = 60-78 MJ/m³ (c1_dam.py)
DEFECT | MINOR | The sliding safety factor of about 5 is lost at season end, when only the 3 m skin is left. | 3 m skin × 3.5-4 m high, μ 0.5-0.7, 3 m head: SF 2.4-3.8, or 1.9-3.1 with base uplift
DEFECT | MINOR | A 0.4 m lift freezes in 10-19 h only at about -40 °C with freezing from both sides; the forebay breach estimate is extrapolated. | One-sided Stefan at -20 to -30 °C gives 49-95 h; Froehlich (1995) is fitted for heads of 3.4 m or more and far larger volumes, while 34 m³/s implies 8,300 m³ at 3 m
SURVIVES | Face heat-transfer margin (70 m/day needs h ≈ 5,800-8,100 W/m²K, so even 10x less is still far above 0.8 m/day), peat thaw (0.38-0.45 m in 90 days at 5-7 °C), the 2.3x washing-stage ratio and $2.95 vs $6.8/g (at 85% recovery) all reproduce.

IDEA 2: Solar-pond self-dosing ore pile
DEFECT | FATAL | The toe channel cannot carry what it thaws: gravel builds up at the face, insulates it, and feed falls to the transport rate, so a machine at the face is still needed and the 1.03-1.13x gain becomes 1x or worse. | Needed 1,500-3,200 m³/day (101 MJ/m³, 47-100 L/s at 9 °C, 123,000 m³ in 38-81 days) vs 28-610 m³/day capacity for d50 10-20 mm at slope 0.05-0.08 = 2-19% (c2_toe.py)
DEFECT | MAJOR | Clasts above the movable size stay where they fall along the 40-100 m face toe instead of reaching the downstream grizzly, and the movable size is smaller than stated. | Steep-slope critical Shields θc = 0.15 S^0.25 = 0.071-0.080 (Lamb et al. 2008) moves only 21-52 mm, not 42-78 mm
DEFECT | MAJOR | The heat e-folding length of 10-31 m does not reproduce: water 5-15 cm deep touches the frozen face only over its wetted depth, so much of the heat passes the face unused and feed is less than flow × heat. | Dittus-Boelter gives h = 1,800-2,400 W/m²K and L_e = 63-400 m; reaching 29-57 m needs a fully frozen perimeter plus 3x roughness enhancement
DEFECT | MAJOR | The pond cannot add 4-6 K to the upper flows: 100 L/s on 0.7 ha needs more net heat than all the sunshine that falls on it, while the 2.26x output assumes +5 K all season. | 239-358 W/m² net needed vs July mean global radiation of 228 W/m² at Oymyakon (611.7 MJ/m²/month, dnaop.com/html/66253_7.html); May and September are much lower
DEFECT | MINOR | Loader time of 2-3 h/day is not tied to any measured size grading. | At 1,500-3,200 m³/day with an assumed 30-50% oversize, a 150 m³/h loader needs 3-11 h/day
SURVIVES | 123,000/54,500 = 2.26 ≈ (4+5)/4; 30-57 Pa and 42-78 mm reproduce with θc 0.045; water ratio 2.4-12.1 matches ΔT of 10-2 K at 101 MJ/m³.

IDEA 3: Trimmed snow-buoyed under-ice ore pods
DEFECT | FATAL | The idea's own shell melt uses up the +3 to +9 kg trim in 0.7-2.1 days of a 41-68 day trip, so pods sink to the bed after 7-36 km. | 39.3 m² × 0.06 m × 83 kg/m³ = 196 kg per 45 days = 4.3 kg/day
DEFECT | FATAL | A flat 8-10 cm ice box cannot hold the 10-20 kPa head across 2.2 m spans; the load passes to the snow, which creeps and loses buoyancy. | Bending 1.8-2.8 MPa vs ice flexural strength 0.5-1 MPa; snow at 250 kg/m³ under 13-20 kPa creeps 47-72% per day (Vionnet 2012 viscosity, c3_pods.py)
DEFECT | MAJOR | The trim cannot be measured to the window. | Crane scales are ±0.1-0.5% of full scale (OIML R60 class III), i.e. ±10-50 kg on 10 t, against a 6 kg window; a 10 t PCE scale reads in 5 kg steps
DEFECT | MAJOR | The transit figures break the idea's own route rule and shell budget. | 700 km in 41-68 days = 0.12-0.20 m/s (the rule requires at least 0.2 m/s); 68 days melts 9.1 cm against an 8-10 cm shell
DEFECT | MAJOR | The named routes below dams start in warm tailwater and frazil-jam zones. | The Yenisei stays open 200-300 km below the Krasnoyarsk dam (en.wikipedia.org/wiki/Krasnoyarsk_Dam); Angara tailwater has polynyas tens of km long and "powerful frazil jams" (BSE); at +0.5-2 °C a 10 cm shell melts in 0.2-1.4 days
DEFECT | MAJOR | Catching pods across a 0.5-2 km wide river is not designed, and lost pods mean ore dumped in a river, which Water Code art. 56 bans. | 5% loss = $3-15/t of cargo value ($60-300/t), about equal to or above the whole $7.3/t handling cost; showing ≤5% loss at 95% confidence needs ≥60 pods with no loss
SURVIVES | Drag of ~154-170 N at 0.16 m/s (Cd ≈ 2 on 6 m²) is above the 15-44 N of friction; $0.118/t·km by winter road and 120 pods/day × 120 days = 144 kt reproduce.

IDEA 4: Sun-face windrow freeze-dry placer
DEFECT | MAJOR | The 2.6x irradiance is the noon beam ratio on 21 March only; the daily total gain is much smaller in the April window that carries most of the claimed sublimation. | Hourly integration at 71.6°N for a 37° south face, diffuse fraction 0.3-0.7: 1.5-2.5x on 15 March, 1.3-1.9x on 31 March, 1.1-1.5x on 20 April (c4_deflation.py)
DEFECT | MAJOR | Snow is not dealt with: 37° faces hold snow (avalanches release on 30-45° slopes) and the ridge troughs, where sand and gold should settle, are drift traps. | A few mm w.e. of snow equals the whole 5.2 kg/m² season budget; idea 6 gives about 10 mm w.e. of spring snowfall at Pevek
DEFECT | MAJOR | It costs more than current practice by its own count, so it fails the brief. | $4.4-12.1 vs $1.7-6.0/m³
DEFECT | MINOR | The area is understated. | At the design 0.06 pore ice, 5.2/(0.06×917) = 0.095 m of retreat → 1.05 km² and 249 km of ridges, not 0.9 km² and 213 km; the stated 0.02-0.09 m implies 1.1-5.0 km²
DEFECT | MINOR | The deflated fines are a large fugitive-dust source that needs an air-emission permit. | 100,000 m³ × 1.8 t/m³ × an assumed 10-30% fines = 18-54 kt/yr
SURVIVES | Retreat of 0.019-0.095 m at 0.30-0.06 pore ice and 4.2 m of face per metre of ridge (2.5 m ridges) reproduce; 5.2 kg/m² is 30-49% of the unpenalised rate sum (10.7-17.4), which fits the stated lag penalty.

IDEA 5: Spring Sun-Wind Deflation Placer
DEFECT | FATAL | The 57-day season runs past melt onset: dark gravel melts from about 28 April (idea 6's hourly model for Pevek; Pevek May mean -2.2 °C, mean daily maximum +1.0 °C), so the 3.6x claim falls apart. | 57 d × 0.4-0.7 = 23-40 mm w.e. vs 7.8 mm w.e. modelled, 2.9-5.1x overstated; 0.5 km² becomes 0.9-1.8 km²
DEFECT | MAJOR | Raking once a day does not avoid the lag penalty: the dry lag builds within hours and halves the rate for each mm. | Integrating rate × 2^(-lag/1 mm), with 80% of freed material left as lag, gives 1.7-2.4 mm/day freed, not 2.5-5 (48-60%)
DEFECT | MAJOR | "No gold moves at 7 m/s" depends on roughness and particle shape, conflicts with idea 6 (flakes move at u* 0.23-0.32), and the wind between rakings is not controlled. | At 7-8 m/s, u* = 0.24-0.42 for z0 0.1-5 mm vs a gold-sphere threshold of 0.38 (Shao-Lu); Pevek's yuzhak reaches 40-60 m/s with about 20% of events above 20 m/s (bigenc.ru), giving u* 0.7-2.1
DEFECT | MAJOR | Clearing snow from the cut is neither planned nor costed. | Spring snowfall of about 10 mm w.e. equals the whole budget (idea 6)
DEFECT | MINOR | Old washed tailings have lost the sand matrix that deflation removes, and their gold is the fine fraction that blows away. | Idea 6 itself rates tailings at about 1x
SURVIVES | 0.4-0.7 mm w.e. → 2.9-5.1 mm/day at 0.15 pore ice; 0.21 m → 0.48 km²; midwinter 0.014-0.041 → 0.05-0.15 mm at about 0.3 pore ice.

IDEA 6: Albedo-steered freeze-dry deflation placer
DEFECT | MAJOR | If flakes start moving at the same u* as sand, a lip that traps the gold traps the sand too, so only silt and very fine sand leave and the volume reduction is small. | Suspension needs u*/w_s > 1: only quartz finer than about 60-100 µm (w_s 0.2-0.6 m/s) leaves at u* 0.3
DEFECT | MAJOR | "Gold never goes into suspension" is wrong for fine gold and flakes in storms. | Drag-corrected settling: gold 10-20 µm 0.06-0.24 m/s, a 100×10 µm flake about 0.5-0.7 m/s (Stokes 6.6 m/s overstates 100 µm gold by 2.3x); yuzhak at 20-40 m/s gives u* 0.7-2.1 m/s
DEFECT | MAJOR | Even as stated, 1.3-1.6x (1x on tailings) fails the brief, and the $3.7-4.5/m³ is not itemised (daily raking of 0.94-1.76 km², blading, fences, summer wash). | The two $/g figures imply different recoveries (0.77 vs 0.83)
DEFECT | MINOR | The top of the area range is understated. | 100,000/0.057 m = 1.76 km², not 1.4
DEFECT | MINOR | 0.6-1.4 m fences store little drift at a windy site, and dust emission is as in idea 4. | Tabler storage ≈ 8.5 H^2.2 = 2.8-18 t/m; 18-54 kt/yr of fines
SURVIVES | 13 × 0.6 = 7.8 mm w.e. → 57-106 mm at 8-15% pore ice; melt onset in late April fits Pevek's climate; $/g reproduces at about 0.8 recovery.

IDEA 7: Freeze-and-float boulder pond
DEFECT | FATAL | Ice that reaches the boulders in March keeps freezing gravel onto its base for the rest of winter, which outweighs its buoyancy, so the floe stays grounded. | Stefan through 1.7 m ice with 0-0.3 m snow over 775 °C·d: 31-73 cm = 326-827 kg/m² vs 141 kg/m² buoyancy; 3.2 m ice: 239-491 vs 266 (c5_ice.py)
DEFECT | MAJOR | The baseline is inflated: boulders are normally dozed aside or grappled, not drilled and blasted. | Dozer or grapple costs $2.7-3.0/m³ (idea 12), so at most 2.7-3x even at $1; idea 12 prices the same ice lift at $5.1-5.7/m³
DEFECT | MAJOR | Lifted stones hang below the floe, so the draft equals the original depth; dragging them to the dump bay needs a spring rise and route depth that are not shown. | Stones protrude 0.3-1 m below a floe with 1.5-1.65 m ice draft
SURVIVES | 0.080-0.166 m³/m² of stone for 1.6-3.3 m ice (83 ÷ 1,650) reproduces; dropping wave-pumped sorting is correct.

IDEA 8: Short-haul trimmed under-ice ore pods
DEFECT | FATAL | The buoyancy budget forces very light snow, and light snow collapses under the water head far faster than the 90 kg window allows; denser snow does not give enough lift. | 8 t coal at 1.25-1.45 t/m³ is 1,600-2,480 kg heavy; minus shell lift of 235-511 kg, the snow must be ≤112-381 kg/m³ (impossible for 1.35-1.45 t/m³ coal with a 7 cm shell); at 250-300 kg/m³ and 13-20 kPa, creep costs 218-1,270 kg/day (Vionnet 2012; c6_pod8.py)
DEFECT | MAJOR | The "rigid ice shell" is not rigid at 0 °C. | 7-13 cm walls over 1.0-1.2 m spans at 15 kPa carry 0.44-2.2 MPa and creep 1.8-222% per day (Glen, A = 2.4e-24)
DEFECT | MAJOR | The test route is beyond the usable range unless the water is at the best case. | 330 km at 0.18 m/s = 21 days → losses of 79/233/390 kg at +0.01/0.03/0.05 K vs a 90 kg window
DEFECT | MAJOR | The decisive superheat of +0.01-0.05 K is assumed; field probes cannot resolve it, and in early winter the water is at or below 0 °C with frazil that sticks to pods. | River-ice thermistor profiler accurate to about 0.1 K (IEEE Access 2020); 0.01 K needs a special CRREL instrument (1985)
DEFECT | MAJOR | No measured winter riffle depth supports the 1.75-2.1 m needed. | 327 m³/s at 0.18-0.33 m/s over 400-1,000 m width = 1.0-4.5 m mean under-ice depth, and riffles are shallower; the natural April minimum is 23.5 m³/s (bigenc.ru, Kolyma), raised by 130-268 m³/s after regulation (Majhi 2007)
DEFECT | MAJOR | The coal arrives as a frozen coal-and-ice block that must be thawed and crushed before burning, which is not costed. | Flooded voids = 1/0.85 - 1/1.35 = 0.44 m³ of water per t of coal, plus the shell
DEFECT | MINOR | The flexible-bag figure (390 kg) belongs to another pod, and the nearest dam is closer than stated. | This pod's ≤1.2 m³ of air gives 43-75 kg per 0.7 m; the Ust-Srednekan HPP is 217 km below the Kolyma HPP, so the route is about 1,170 km below a dam
SURVIVES | Cold reserve (+11/+70 kg), 1.75-2.1 m depth, the 76 km minimum range, $0.118/t·km, and the honest 0.6-3.7x against barges (Zyryanka-Srednekolymsk navigation runs to 10 October, neftegaz.ru) reproduce.

IDEA 9: Ice-lift oversize boulder clean-up
DEFECT | MAJOR | "The floor never freezes" ignores the boulder as a thermal bridge: rock conducts better than ice, so the freezing isotherm dips beside each gripped boulder and freezes its base to the floor. | 1-D series bound with k_rock 2.5-3.5 W/mK puts the isotherm at 1.79-2.26 m vs a 2.12 m floor, leaving 0.33 to -0.14 m of gap against a design 0.30-0.47; spreading in 2-D reduces this but does not remove it
DEFECT | MAJOR | The cost comparison is against the wrong practice: oversize on a mined-out floor is pushed or grappled, not blasted. | Against $2.7-3.0/m³ the gain is 1.1-1.5x, and the idea itself puts it at 0.04-2.5% of cost per gram
DEFECT | MINOR | The 99% gap uses only the frost-index spread (σ 0.08 m) and ignores winter level change in an undammed pit pond. | Each 0.1 m of level loss removes a third of the 0.30 m gap; showing P ≈ 1.00 grip at 95% confidence needs ≥59 boulders without a failure
DEFECT | MINOR | The stated net lift does not follow from the stated ice. | 1.8 m × 83 = 149 kg/m², not 101-126
SURVIVES | Gap 2.12 - 0.917×1.8 = 0.47 m (0.30 m at 99%), 23-29 m² of floe for a 1.5 m boulder (2,916 kg submerged), and the ~2 m size cap reproduce.

IDEA 10: Cold-sealed rolling snow-log pods
DEFECT | FATAL | The velocity needed to pass keels is the velocity at which rivers stop forming or keeping ice cover, so suitable ice-covered reaches essentially do not exist. | Under-cover deposition limit 0.61 m/s (Kivisild, Fr 0.08), 0.69 m/s (MacLachlan), 0.8 m/s (IAHR 1986), as cited in mdpi.com/2073-4441/15/24/4242, vs 0.62-0.95 m/s required
DEFECT | FATAL | A shell sealed at -35 °C and put into 0 °C water cracks from thermal shock, venting the +14.9 kPa and flooding the snow. | Eα ΔT/(1-ν) ≈ 24 MPa vs ice tensile strength of 2-3 MPa; King & Fletcher find a median cracking temperature of -16 °C for water-shocked ice spheres
DEFECT | MINOR | The +14.9 kPa does not balance the outside pressure on the lower half of a 1.6 m log. | Hydrostatic +13-21 kPa at the axis and +21-29 kPa at the bottom; creep at 550 kg/m³ is only 0.02-0.03% per day if the seal holds
SURVIVES | +14.9 kPa, 0.58/1.40 m³/t of snow before shell credit (0.74/1.6 stated), creep of 0.1-1.1% per 45 days, and tailwater melt in 0.2-1.4 days reproduce; the idea's own "moot" verdict stands.

IDEA 11: Self-feeding ore-ice buttress dam
DEFECT | FATAL | A winter-hoisted stockpile is loose broken rock with open voids, so it cannot hold the forebay, and 101 MJ/m³ (ice-cemented) is the wrong thaw energy for it. | Bulk ice 0.15 gives 50-55 MJ/m³ (idea 1); cold content at -2 to -7 °C refreezes only 4-11% of 0.20-0.25 voids
DEFECT | MAJOR | The repaired version of the same mechanism contradicts the 5x gain. | Idea 1: $4.65 → $2.0 (2.3x) vs idea 11: $6.7 → $1.3 (5.2x)
DEFECT | MAJOR | Gravity transport at this water rate is well below the feed. | 47 L/s at slope 0.05-0.08, d50 10-20 mm carries 28-280 m³/day vs 632 m³/day needed (60,000 m³ in 95 days), i.e. 4-44%
DEFECT | MAJOR | Per recovered gram, washing is a small share of underground placer cost. | (6.7+M)/(1.3+M) = 1.86-1.17x for an assumed M of $5-30/m³
DEFECT | MINOR | The water figures are inconsistent and below plant data. | 4.3-7.6 m³ of 8 °C water implies outflow at 2.4-4.8 °C, but a 20-100x heat-transfer margin means about 0 °C and 3.0 m³/m³; "2.2 m³/m³" is below the measured 3.2-9.9
DEFECT | MINOR | The "small forebay" still releases a large flood onto the sluice crew. | 128 m³/s is about 2,700x the 47 L/s baseflow (Froehlich: about 87,000 m³ at 5 m head)
SURVIVES | 47 L/s × 95 days at 6.4 m³/m³ = 60,000 m³, 0.8 m/day × 94 days = 75 m of buttress, and peat thaw of 0.45-0.51 m reproduce.

IDEA 12: Drawdown-timed ice boulder lift
DEFECT | MAJOR | A 1.7-3.2 m ice sheet is far too stiff to settle onto a boulder field; it rests on the tallest few boulders and bridges the rest. | Characteristic length 18-35 m; bending it 0.3 m locally needs a 7-29 MN point force, while boulders are 1.6-2.2 m apart at 10-20% cover
DEFECT | MAJOR | 4.4 cm of freeze-on needs about 0.3 m of snow on the ice; on snow-free or flood-built ice the lift is 2-3x lower. | Stefan over 91 °C·d gives 8.5-9.9 cm → 0.018-0.031 m³/m² (not 0.058), and a 0.8 m boulder needs 9-29 m² of floe
DEFECT | MAJOR | The chosen niche conflicts with the method: a dredge pond is deeper than the ice, so it would have to be drawn down by metres under ice in winter. | An assumed 3-5 m pond vs 1.7 m ice → 1.3-3.3 m of drawdown
DEFECT | MAJOR | By its own figures it costs about twice the baseline, so it fails the brief. | $5.1-5.7 vs $2.7-3.0/m³ (0.47-0.59x)
SURVIVES | 775 °C·d → 31-73 cm of freeze-on (39 cm with about 0.25 m snow), 402 vs 141 kg/m², 0.058/0.133 m³/m² after 4.4 cm, and 442 kg submerged for a 0.8 m boulder reproduce.

All check scripts are in /home/user/SomeRepository/engine/runs/permafrost/round2/audit_b/: c1_dam.py, c2_toe.py, c3_pods.py, c4_deflation.py, c5_ice.py and c6_pod8.py.

Sources:
- [911metallurgist: gravity gold process water requirements](https://www.911metallurgist.com/blog/gravity-gold-process-water-requirements/)
- [Yukon placer atlas](https://ygsftp.gov.yk.ca/ygsftp/publications/placer_atlas/)
- [dnaop.com climate table 17](https://dnaop.com/html/66253_7.html)
- [Krasnoyarsk Dam (Wikipedia)](https://en.wikipedia.org/wiki/Krasnoyarsk_Dam)
- [BSE Angara article (booksite.ru)](https://booksite.ru/FullText/1/001/008/056/290.htm)
- [Crane scale accuracy classes](https://b2bwiki.baidu.com/en/encyclopedic/crane-scale)
- [PCE crane scales](https://pce-instruments.com/english/index.php/cat/c142_Load_Scales.html)
- [MDPI Water 15(24):4242 on hanging dams](https://www.mdpi.com/2073-4441/15/24/4242/xml)
- [King & Fletcher, thermal shock of ice](https://openresearch-repository.anu.edu.au/items/f34a8e52-6384-41d7-8e5e-8c30fc74848c)
- [Pevek yuzhak (BRE)](https://bigenc.ru/c/pevekskii-iuzhak-41abb8)
- [Pevek (Wikipedia)](https://wikipedia.com/wiki/Pevek)
- [Kolyma (BRE)](https://bigenc.ru/c/kolyma-85f4e3)
- Majhi 2007, Kolyma streamflow changes (cybrary.friendsofmerrymeetingbay.org)
- [neftegaz.ru: Ust-Srednekan HPP](https://neftegaz.ru/news/view/107935/)
- [neftegaz.ru: northern delivery and navigation dates](https://neftegaz.ru/news/transport-and-storage/936822-osnovnye-postavki-v-yakutiyu-v-ramkakh-severnogo-zavoza-zavershatsya-k-kontsu-sentyabrya/)
- [IEEE Access 2020 river-ice thermistor profiler](https://doaj.org/article/89232ae6f8614453bc8998ddc1625eef)
- [CRREL 1985 0.01 °C instrument (SPRI catalogue)](https://www.spri.cam.ac.uk/library/catalogue/records/75774/)