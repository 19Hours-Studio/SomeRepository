SCORES
ID | O | C | V | F | R | BASIN | closest
S01 | 6 | 6 | 3 | 2 | N | NEW | shape-memory natural rubber (strain crystallisation)
S02 | 4 | 5 | 6 | 3 | N | METALAIR | Ni-Fe iron electrodes, Bi2S3 additive
S03 | 5 | 6 | 6 | 4 | N | NEW | membraneless stratified redox, solar pond
S04 | 6 | 7 | 6 | 4 | N | NEW | redox-mediated solid boosters, Fe-clay redox
S05 | 3 | 6 | 3 | 6 | Y | NEW | all-iron flow battery, pickle-liquor electrolyte
S06 | 2 | 6 | 4 | 4 | Y | NEW | thick-electrode Li-ion (24M semisolid)
S07 | 6 | 6 | 3 | 2 | N | NEW | shape-memory natural rubber
S08 | 5 | 7 | 5 | 3 | N | METALAIR | Ni-Fe iron-oxide electrode, tailings
S09 | 5 | 5 | 3 | 2 | N | NEW | MOST norbornadiene, electrochemical back-conversion
S10 | 6 | 7 | 5 | 4 | N | NEW | sorption thermochemical storage, vapour turbine
S11 | 4 | 6 | 6 | 4 | N | NEW | membraneless static Zn-Br battery
S12 | 5 | 7 | 7 | 4 | N | NEW | biphasic membrane-free redox flow battery
S13 | 6 | 6 | 5 | 3 | N | NEW | sorption storage, adsorption heat pumps
S14 | 6 | 6 | 6 | 3 | N | NEW | redox-mediated solid boosters, clay
S15 | 2 | 7 | 4 | 5 | Y | NEW | Janoschka 2015 polymer RFB, cellulose membrane
S16 | 5 | 7 | 5 | 2 | N | METALAIR | alkaline Fe-MnO2 cells, steel slag
S17 | 6 | 6 | 6 | 4 | N | NEW | precipitation/slurry RFB, solid boosters
S18 | 5 | 6 | 5 | 1 | N | OREFLOW | redox-targeting solid boosters, lignin
S19 | 5 | 3 | 4 | 2 | N | NEW | quinone-functionalised biochar electrodes
S20 | 4 | 8 | 6 | 5 | N | NEW | membraneless static Zn-Br battery
S21 | 5 | 7 | 2 | 3 | N | NEW | shape-memory natural rubber
S22 | 3 | 5 | 4 | 6 | Y | NEW | LDES power/energy decoupled sizing studies
S23 | 5 | 6 | 5 | 2 | N | METALAIR | alkaline Fe-MnO2 cells, steel slag
S24 | 6 | 6 | 6 | 3 | N | NEW | precipitation/slurry redox flow battery
S25 | 5 | 7 | 6 | 4 | N | NEW | membraneless diffusion-barrier static redox cell
S26 | 6 | 6 | 5 | 3 | N | NEW | sorption storage, adsorption heat pumps
S27 | 7 | 6 | 6 | 3 | N | NEW | Sandia freeze-thaw molten-salt battery
S28 | 5 | 7 | 7 | 5 | N | NEW | gravity-stratified membraneless redox battery
S29 | 6 | 6 | 6 | 3 | N | NEW | precipitation/slurry redox flow battery
S30 | 5 | 6 | 6 | 4 | N | NEW | membraneless stratified redox, solar pond
S31 | 5 | 6 | 3 | 3 | N | FLEXLOAD | H2O2 electrosynthesis and H2O2 fuel cells
S32 | 7 | 6 | 6 | 2 | N | NEW | Sandia freeze-thaw molten-salt battery
S33 | 7 | 7 | 6 | 4 | N | NEW | Sandia freeze-thaw battery, size-exclusion RFB
S34 | 5 | 6 | 2 | 4 | N | NEW | all-iron hybrid flow battery
S35 | 5 | 6 | 2 | 2 | N | METALAIR | iron-air (Form Energy)

Key checks behind the F scores:
- S18 fails on flow rate. Flushing 0.1 M mediator at about 3 m/day carries about 0.7 A/m² of cross-section. A 100 h discharge of a 2.5 m bed needs about 300 A/m², so it is short by more than 100x.
- S32 is over its diffusion limit. At 0.5 Pa·s, Stokes-Einstein gives D of about 1e-12 m²/s, which caps current at about 8 A/m² against the 30 A/m² claimed. It also puts both polarities in one melt, where they would annihilate.
- S33 gets the same limit right (5 A/m²). Its open questions are radical and quinone stability in sugar at 170 °C, and about 1 m²/kWh of 30 µm-gap cell.
- S10, S13 and S26 move about 1 m³/s of vapour per kW, which is huge per-kW machinery. Adsorption heat is 10-20x the stored work, so a 3 K heat-transfer gap costs 20-45% of round trip. S13 and S26 ignore this; S10 fixes it. Air leaking into an earth-covered vacuum enclosure is not addressed.
- S01 and S07 assume tyre rubber holds its stretch at room temperature. Heavily crosslinked, carbon-filled tread rubber does not; that effect is only seen in lightly crosslinked lab natural rubber.
- S16 and S23 are let down by the slag. Its Mn is Mn(II) locked in silicate, so it is mostly inaccessible. 6 M KOH also attacks the slag and puts groundwater under the road at risk.
- S06 cannot reach $20/kWh. Electrolyte in the pores does not shrink with thicker electrodes, and LFP plus graphite materials already cost about $40/kWh or more.
- S25 has a buoyancy problem. Darcy-Rayleigh in 0.4 m sand layers is about 1e3, far above the onset, so convection is likely unless the density stratification is stable.
- S04 checks out: about 1.4 kWh/m² at 4 cm, about 50 mV ohmic loss and about 0.3% mediator leak per 2 weeks. What is unproven is reversible Fe-clay capacity and MnO2 recharge in neutral brine.
- S28 checks out: about 4% leak across the spent layer and about 0.5% idle loss per day.

TOP3:
- S33: storing charged electrolyte as vitrified granules gives near-zero self-discharge at silo-like cost. Its numbers are self-consistent and a bench test is cheap.
- S28: the simplest membraneless design. A single-liquid stratified pond whose leak and ohmic numbers check out; it only needs one redox pair with a big enough density contrast.
- S04: an earth-pile Fe-clay/MnO2 bipolar cell whose capacity, ohmic and leak numbers all hold up. Its make-or-break unknowns (clay Fe reversibility, MnO2 recharge) can be tested quickly.

NOTE: The set is mostly near-duplicate clusters of an original plus "repaired" versions: S01/S07/S21, S03/S30, S04/S14, S10/S13/S26, S16/S23, S17/S24/S29, S27/S32/S33 and S11/S20. Almost all of it converges on membraneless, stack-free electrochemistry housed in earthworks. That makes containment cheap, but every design still hinges on cheap, stable redox actives that nobody has shown exist.