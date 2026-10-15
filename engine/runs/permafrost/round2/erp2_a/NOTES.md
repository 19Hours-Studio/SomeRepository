# NOTES: repair pass on 4 ideas (calculations in calc/idea1.py, idea2.py, idea3.py, idea4.py, econ.py)

## Sources used
- Ni(CO)4 vapour pressure: NIST WebBook fit via Cheméo, ln P[kPa] = 14.5275 - 2837.86/(T - 28.762), valid 228-337 K (https://www.chemeo.com/cid/35-741-0/Nickel-tetracarbonyl.pdf). Thermochemistry from NIST-JANAF: dHf Ni(CO)4(g) = -602.9 kJ/mol, S = 410.6; CO = -110.53 / 197.66; Ni S = 29.87 (taken from memory of the tables).
- Power of Siberia: 9.8 MPa, 1,420 mm, 38 bcm/yr, permafrost route (gazprom.com/projects/power-of-siberia).
- Kun-Manie: 155 Mt at 1.02% Ni-eq; about 350-394 kt/yr of concentrate; 338 km access road to BAM (Ulak); base case sells concentrate FOB Vladivostok (miningweekly / engineeringnews 2018-2023).
- Ni concentrate payability: conventional 70-75% (RNC/Dumont); awaruite 85-95% (FPX); matte 80% in the TMC model.
- Closest prior art to idea 1: patents US 8,840,692 and US 9,669,374 (Ni carbonyl in a dedicated conduit, with a fail-safe burner). Nothing found on carrying it inside natural gas.
- CuSO4 eutectic freeze crystallisation: Van der Ham, Witkamp, de Graauw, van Rosmalen, Chem. Eng. Process. 37 (1998): 12 wt% CuSO4 stream, 1,037 kJ/kg vitriol.
- Freezing cost analogue: direct-contact freeze desalination of produced water, LCOW $0.31-0.69 per bbl of input brine (Oklahoma thesis, shareok.org), i.e. $2-4.3/m3.
- Propane hydrate: 3-phase (ice-hydrate-vapour) temperature at 0.1 MPa is about -14 C, so propane at its own vapour pressure (3.5-3.9 bar) at -6 to -8 C lies inside the hydrate field.
- Yakutsk normals: Jan -38.6, Feb -31 to -34, Dec -36.5 C (weather-site compilations; the Nov and Mar values of -27 and -20 C were taken from memory).
- Tribo minerals: feldspar/quartz in a free-fall chamber (Peretti, Zucca, Serci 2010); free-fall electrostatic separator tests on spodumene at -315+60 um (Montanuniversitaet Leoben thesis, 2018); STET belt separator (powered).
- Udachnaya brines: Cl-Ca, TDS 94-391 g/L, average Li 147 mg/L. Siberian platform brines: 170-631 g/L, Li up to 600 mg/L (Gornyi Zhurnal 2012).
- These cost inputs are engineering estimates with no source (flagged): truck $0.10/t-km, winter road $0.15-0.20, rail $0.03; CO from POX/coal $150-250/t; Ni smelter+refinery capex $30-45k per annual t; SX-EW capex $5k per annual t, SX opex $240/t; EW 2.1 kWh/kg; natural-draft tower plus ORC capital charge $0.30-0.45/kWh; DMS opex $8/t, flotation $22/t, sorting $3/t.

## Idea 1 - carbonyl nickel in the gas line
Anchor kept: Ni(CO)4 travels in the trunk line's own gas flow and is split back out at the plant where the line ends (Amur GPP, Svobodny).
Decisive numbers: dose 0.027 mol% carries 25 kt Ni/yr in 38 bcm/yr. Saturation ratio is 0.25 at -10 C and 9.8 MPa. CO needed for stability is 0.024% at 45 C (0.035% with a 1.5x margin), 0.07% at 60 C and 0.16% at 80 C. Stoichiometric CO is 1.91 t per t Ni, 2.53 t per t Ni including stabiliser. A cold-oil absorber at the GPP inlet needs 20-60 kg/s of oil and 10-16 stages to catch 99.999%. Heating the whole stream instead means 423 MW gross.
Baseline per t Ni delivered: concentrate sale (best current practice) loses $5.4-6.1k per t Ni. Matte + carbonyl + pipeline costs $6.6-8.4k. The same refinery shipping pellets by rail costs $5.7-7.5k. So the anchor adds about $960 per t Ni and saves only $27 per t Ni of freight.

| Limit or window | Value | Design point | Holds? |
|---|---|---|---|
| Dew point at 9.8 MPa | 0.027% gives sat. ratio 0.25 at -10 C | gas >= -10 C | Yes, but if line flow falls 40% the dose goes to 0.045% and it fails below -20 C, so injection must follow flow |
| Stability against CO | CO >= 0.024% at 45 C | discharge capped at 45 C, CO 0.035% | Only with the cap |
| Decomposer | eq. 2e-4 atm at 200 C | concentrated stream, CO recycled | Yes |
| Residual in sales gas | REL 1 ppb in air at a 1% gas leak | 2.7 ppb in gas | Yes |
| Rupture | IDLH reached after 135x dilution | 700-900 km toxic segment | Hazard |
| Geography | Kun-Manie is 340 km from BAM and from PoS | matte trucked to injection | Rail runs alongside PoS, so freight saved is small |

Hazards: rupture toxicity, a whole trunk line becoming a toxic-gas pipeline under Rostekhnadzor rules, and export-gas contract specs.
Deciding unknown: the CO price. Even free CO leaves about $450 per t Ni of extras, against $27 of freight saved. Cheapest experiment: a 1,000 h high-pressure loop (9.8 MPa, 45 C, 3 CO levels x 3 temperatures) measuring Ni deposited on pipe-steel coupons. It cannot rescue the cost case.
Verdict: FAILS on cost (physics works). The only niche is a nickel source on a roadless trunk-line stretch of at least 4,800 km of winter road, which does not exist on PoS.

## Idea 2 - freeze-engine vitriol
Anchor kept: freezing the liquor drives an ORC that rejects heat to Arctic air, and the same freezing crystallises CuSO4·5H2O.
Repairs: (a) n-butane replaces propane, because propane forms hydrate in this regime. (b) Fan power is counted (8.7 kJ/kg ice at -40 C) or a natural-draft tower is used. (c) The engine is integrated over a real season: Yakutsk Nov-Mar gives 7.6 kJ/kg ice net with natural draft, so 50% of EW power at 2.5 g/L, not 80-104%. (d) Freezing cost of $1.5-2.5/m3 of feed makes dilute PLS uneconomic, so PLS goes to 10-15 g/L and ore is restricted to siliceous, low-Mg oxide (Mg <= 2 g/L, Fe <= 1 g/L at 24x concentration).
Baseline per t Cu: SX-EW on diesel $1,590, on grid $1,086. Freeze route $1,222-1,379 at 10-15 g/L, which is 1.15-1.30x cheaper than diesel SX-EW and loses to grid SX-EW.

| Limit | Value | Holds? |
|---|---|---|
| Hydrate | propane, no; n-butane, yes | After repair |
| Season hours with net power > 0 | 2,860 (fans) / 3,560 (natural draft) | Yes |
| Impurity concentration | 96x at 2.5 g/L, 24x at 10 g/L | Only for low-Mg ore |
| Spring meltwater | 1.2-5 Mt/yr of dilute acidic water | Must be used as heap make-up water |

Hazards: n-butane inventory near acid liquor, acid entrained in the ice, and the pond in permafrost.
Deciding unknown: vitriol purity and Cu recovery in EFC on real PLS with Mg and Fe present (5 compositions x 3 replicates), then a 100 kW n-butane rig run through one winter to measure the season-average net kJ/kg ice.
Verdict: NICHE. The power half of the anchor only breaks even against diesel.

## Idea 3 - self-charging tribo cascade
Anchor kept: product charge collected in bins cross-wired to the opposite plates builds the field (Kelvin-dropper principle), with no power supply.
Repairs: the stated 30 kV/m gives only 4-9 cm of drift and 0.15 t/h per m (7 km of plates). Changed to a 0.3 m gap self-excited to 90 kV (300 kV/m; breakdown at -40 C is 3.6 MV/m), giving 41 cm of drift over a 1.5 m fall, 1.47 t/h per m and 700 m of plates in total. Insulating grains hand over their charge through pile (cone) discharges, leaving about 0.2 uC/kg against 10 delivered. Leakage must stay above 2.2e10 ohm per m. Air must be heated to 20-40 C, not 0 C, to dry 1-2% moisture (137 MJ/t against 43-54 MJ/t from the mill).
Baseline per t Li2O delivered 700 km: raw ore $9,250, DMS $4,588, ore sorting $5,312, flotation $6,292, tribo cascade $3,994. That is 1.15x cheaper than the best (DMS) and 1.6x cheaper than flotation.
Hazards: HV bins (the product sits at 90 kV), static discharges, silica dust in a dry plant.
Deciding unknown: net charge-delivery efficiency and the spodumene/gangue q/m at -40 C. Single-stage rig 1 m wide with a 0.3 m gap, 5 ores x 3 air conditions, 200 kg each.
Verdict: NICHE (works on paper, about 1.15x).

## Idea 4 - night-sky eutectic freeze
Anchor tested: radiative trays below the CaCl2-ice eutectic. The film cools net at -52 C only when air is at -45 C or colder: 288 h a year, 36 kg/m2. That means 13,000-35,000 m2 per t LCE/yr and at least $65-178k per t LCE, against $3.4-6.2k for DLE.
The above-eutectic variant (antarcticite from brines with >= 36-40% CaCl2) needs only plain air and reaches Li x1.3-1.9; radiative trays add almost nothing (x1.81 to x1.92).
Verdict: FAILS. Niche: freeze-concentrate Ca-free sorbent eluate with -40 C air in thin flooded layers (about 100 m2 per t LCE). The baseline it would replace, RO + MVR, costs $260-440 per t LCE on grid and $690-1,150 on diesel, so the niche helps only off-grid. Deciding number: Li rejection by flood ice (10 trays x 3 layer thicknesses).
