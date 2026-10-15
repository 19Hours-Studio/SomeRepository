=== IDEAS ===
IDEA 1
NAME: Carbonyl nickel rides gas pipelines
MECHANISM: Anchor kept: nickel travels as Ni(CO)4 vapour in the Power of Siberia line's own gas flow (9.8 MPa, 38 bcm/yr) and is split back out at the Amur gas plant where the line ends. Repaired design: 0.027 mol% carries 25 kt Ni/yr, which is Kun-Manie scale. That dose is at a saturation ratio of 0.25 at -10 °C. Compressor discharge is capped at 45 °C, so only 0.035% CO is needed to keep the carbonyl stable (the original 0.15% was sized for 80 °C). At the plant, a cold-oil absorber (20-60 kg/s of oil, 10-16 stages) catches 99.999% and leaves 2.7 ppb in sales gas, instead of heating the whole 879 kg/s stream (423 MW gross). The concentrated carbonyl is then decomposed at 200 °C. Propane hydrate does not apply here; the binding cost is CO make-up of 2.53 t CO per t Ni (about $514/t Ni).
VALUE: The physics works, but the pipeline leg costs about $960/t Ni more than running the same carbonyl refinery at the BAM/PoS junction and shipping pellets by rail, which saves only $27/t Ni of freight (about 0.03x). The whole chain at $6.6-8.4k/t Ni is no cheaper than selling concentrate at 70-75% payability ($5.4-6.1k/t Ni lost), so it FAILS on cost.

IDEA 2
NAME: Freeze-Engine Vitriol Winning
MECHANISM: Anchor kept: freezing the stored copper leach liquor runs a Rankine engine that rejects heat to Arctic air, and the same freezing crystallises CuSO4·5H2O. Repairs:
(1) The direct-contact refrigerant changes from propane to n-butane. Propane boiling at -6 to -8 °C (3.5-3.9 bar) sits inside the propane-hydrate field.
(2) Fan power is now counted: 8.7 kJ per kg of ice against 15.2 gross at -40 °C. The fans are replaced by a natural-draft dry tower.
(3) Integrated over a real Yakutsk November-March winter, the engine nets 7.6 kJ per kg of ice. That covers 50% of electrowinning power at 2.5 g/L, not 80-104%.
(4) Freezing costs $1.5-2.5 per m³ of feed, so dilute liquor loses. The process is moved to 10-15 g/L liquor from leach-solution recycle on siliceous low-Mg oxide ore (Mg ≤ 2 g/L, Fe ≤ 1 g/L, since impurities concentrate 24x). There it needs 77-117 kg of ice per kg Cu, and the engine supplies 8-12% of electrowinning power.
VALUE: $1,222-1,379/t Cu against $1,590/t Cu for diesel-powered solvent extraction plus electrowinning (1.15-1.3x cheaper), but it loses to grid-powered SX-EW ($1,086/t). NICHE.

IDEA 3
NAME: Self-Charging Frost Separator Cascade
MECHANISM: Anchor kept: grains charged on the chute lining build the separating field themselves, through bins cross-wired to the opposite plates, with no power supply. The stated 30 kV/m gives only 4-9 cm of drift (not 30-60) and is space-charge-limited to 0.15 t/h per metre, which would need 7 km of plates. Repaired design:
- A 0.3 m gap self-excites to 90 kV (300 kV/m, 8% of breakdown at -40 °C). That gives 41 cm of drift over a 1.5 m fall and 1.47 t/h per metre, or about 700 m of plates in total for 1 Mt/yr.
- Insulating grains cannot hand over charge the way water drops do in a Kelvin dropper. Instead, discharges inside the charged grain pile pass about 98% of it to the bin. Leakage must stay above 2.2e10 Ω per metre.
- Intake air must be heated to 20-40 °C, not 0 °C, to dry ore with 1-2% moisture: 137 MJ/t against 43-54 MJ/t of mill heat.
VALUE: $3,994/t Li2O delivered against $4,588 for dense-media separation plus haul (the best baseline, 1.15x) and $6,292 for Arctic flotation (1.6x). NICHE.

IDEA 4
NAME: Night-sky lithium freeze cascade
MECHANISM: Anchor tested: trays radiating through the 8-13 µm window push Ca-Li brine below the CaCl2-ice eutectic (-49.8 °C) so Ca locks up and LiCl stays liquid. My own band model agrees with the original:
- With no brine load the film settles 8.1 K below -40 °C air.
- A film at -52 °C cools only when the air is at -45 °C or colder. That is 288 hours a winter, freezing 36 kg per m².
- So the trays need 13,000-35,600 m² per t LCE per year (Udachnaya brine averages 147 mg/L Li).
Keeping the anchor above the eutectic does not help: crystallising CaCl2·6H2O from brines with 36-40% CaCl2 needs only plain -40 °C air (Li concentrates x1.3-1.9), and radiative trays add only x1.81 to x1.92. Only niche: freeze-concentrate Ca-free sorbent eluate in thin flooded layers with -40 °C air (about 100 m² per t LCE), which drops the anchor.
VALUE: As stated, at least $65-178k/t LCE against $3.4-6.2k for the whole sorption route, so it FAILS. The eluate niche beats RO plus mechanical evaporation ($690-1,150/t LCE on diesel) only off-grid; on grid power that route costs $260-440/t LCE.

=== NOTES ===
Files: notes are in `/home/user/SomeRepository/engine/runs/permafrost/round2/erp2_a/NOTES.md`, with sources and consistency tables. The per-round log is `/home/user/SomeRepository/engine/runs/permafrost/round2/erp2_a/LOG.md` (15 rounds). The calculation scripts are in `/home/user/SomeRepository/engine/runs/permafrost/round2/erp2_a/calc/` (idea1.py, idea2.py, idea3.py, idea4.py, econ.py). Many cost inputs are my own engineering estimates with no source, and NOTES.md flags them: road, rail and winter-road rates, CO at $150-250/t, smelter and SX-EW capital, dense-media and flotation operating costs.

**Idea 1 — anchor kept; physics works, cost fails.**
- Sources: Ni(CO)4 vapour pressure from the NIST/Cheméo fit. Thermodynamics for Ni + 4CO from NIST-JANAF (taken from memory): ΔH -160.8 kJ, ΔS -410 J/K. Power of Siberia figures (9.8 MPa, 38 bcm/yr) from Gazprom. Kun-Manie: 340 km road to the BAM railway, concentrate sold FOB Vladivostok. Concentrate payability 70-75% (RNC Minerals).
- Consistency check:
  - Dew point holds at gas temperatures of -10 °C or warmer. If line flow drops 40%, the dose must drop with it.
  - Stability holds only with compressor discharge at 45 °C or below.
  - Residual Ni(CO)4 in sales gas stays under the exposure limit even during a 1% gas leak.
  - The toxic stretch is 700-900 km, and a rupture reaches the danger limit only after 135x dilution.
- Hazards: toxic rupture plume; the whole trunk line would be regulated as a toxic-gas pipeline; export-gas contract specs.
- Deciding unknown: the price of CO. Even free CO leaves about $450/t Ni of extra cost against $27 of freight saved. Cheapest experiment: a 1,000-hour high-pressure loop (3 CO levels × 3 temperatures) measuring Ni deposited on pipe steel. It cannot rescue the cost case.
- Closest existing work: US patents 8,840,692 and 9,669,374 (Ni carbonyl in a dedicated pipe with a fail-safe burner). I found nothing on carrying it inside natural gas.
- Break-even would need about 4,800 km of winter road between source and plant, which does not exist on this line. Verdict: FAILS.

**Idea 2 — anchor kept, but the power half is weak.**
- Sources: Van der Ham et al. 1998 (Delft) on CuSO4 eutectic freeze crystallisation, 12 wt% stream, 1,037 kJ/kg. Propane hydrate's three-phase point is -14 °C at 0.1 MPa. Freezing cost analogue: direct-contact freeze desalination at $0.31-0.69 per barrel of brine. Yakutsk monthly normals.
- Consistency check:
  - Propane hydrate fails; n-butane fixes it.
  - Net power hours: 2,860 with fans, 3,560 with natural draft.
  - Impurities concentrate 96x at 2.5 g/L, so only low-Mg ore works.
  - 1.2-5 Mt/yr of acidic spring meltwater must go back to the heap.
- Hazards: butane next to acid liquor; acid entrained in the ice; a large liquor pond on permafrost.
- Deciding unknown: vitriol purity and Cu recovery from real liquor containing Mg and Fe (5 compositions × 3 replicates), then a 100 kW rig through one winter.
- Closest existing work: Delft eutectic freeze crystallisation of CuSO4; butane direct-contact freeze desalination. Coupling it to an air-cooled engine appears new. Verdict: NICHE.

**Idea 3 — anchor kept.**
- Sources: drift, space-charge and Gauss-limit charge calculations (202 µC/kg maximum at 300 µm). Literature charge levels from Peretti et al. 2010 (feldspar/quartz, free fall). A 2018 Leoben thesis ran powered free-fall electrostatic separation on -315+60 µm spodumene; that is the closest existing work. No self-excited, Kelvin-type mineral separator found.
- Consistency check: 300 kV/m is 8% of breakdown at -40 °C. Space charge sets 1.47 t/h per metre. Leakage must exceed 2.2e10 Ω per metre. Drying with 0 °C air removes only 0.33% moisture, so hotter air is needed.
- Hazards: product bins sit at 90 kV; static discharges; silica dust.
- Deciding unknown: how much charge the grains actually hand to the bins, and spodumene versus gangue charge at -40 °C. Experiment: one-stage rig, 1 m wide, 0.3 m gap, 5 ores × 3 air conditions, about 200 kg per run.
- Verdict: NICHE (about 1.15x).

**Idea 4 — anchor cannot be kept.**
- Sources: 8-13 µm band carries 21-23% of blackbody output (own Planck integral). Udachnaya brines: TDS 94-391 g/L, Li 147 mg/L. Siberian platform brines up to 631 g/L, Li up to 600 mg/L.
- Consistency check: only 288 hours a winter give net cooling, the tray area is unworkable, and the above-eutectic route makes the radiative trays redundant.
- Hazards: brine spills on permafrost.
- Deciding unknown: none can rescue the anchor. For the eluate niche, the number to measure is how much Li the flooded ice rejects (10 trays × 3 layer thicknesses).
- Closest existing work: radiative sky cooling and eutectic freeze crystallisation are each known; I found nothing on combining them for lithium brines.
- Verdict: FAILS. The niche (eluate freezing) works only off-grid.

Search sources: [Cheméo Ni(CO)4](https://www.chemeo.com/cid/35-741-0/Nickel-tetracarbonyl.pdf), [Gazprom Power of Siberia](https://www.gazprom.com/projects/power-of-siberia), [Kun-Manie update](https://www.miningweekly.com/article/kun-manie-nickelcopper-sulphide-project-russia-update-2023-03-10), [RNC payability](https://canadianminingjournal.com/news/nickel-cobalt-new-roasting-method-ups-nickel-payability-by-25-for-rnc), [US 8,840,692](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/8840692), [Delft EFC CuSO4](https://www.literature.wolkersdorfer.info/literature/Eutectic%20freeze%20crystallization%20Application%20to%20process%20streams%20and%20waste%20water%20purification.pdf), [freeze desalination LCOW](https://shareok.org/items/57618c37-fe0e-44c1-8adb-d24a8819f5a4), [Udokan](https://www.kitco.com/news/off-the-wire/2026-09-02/russias-udokan-launches-copper-cathode-production-after-fire-related), [Peretti tribo feldspar/quartz](https://iris.cnr.it/handle/20.500.14243/54284), [Leoben spodumene dry processing](https://pureadmin.unileoben.ac.at/portal/en/publications/analysis-of-a-spodumene-ore-in-regard-of-its-processability-by-dry-processing(a0a6f31a-7e73-4c3d-bb0b-fca82deb2b4f).html), [Udachnaya brines](https://pure.nsu.ru/portal/en/publications/geochemistry-of-brines-and-oil-occurrences-in-the-udachnaya-kimberlite-pipe-siberian-platform(72b6db52-c266-4222-939c-996cfa66d49b)/export.html), [Siberian Li brines](https://rudmet.com/journal/694/article/9081/), [Yakutsk climate](https://weather2travel.com/russia-far-east/yakutsk/climate/?Units=1).