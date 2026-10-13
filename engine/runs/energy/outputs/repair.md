=== IDEAS ===
IDEA 1
NAME: Oligomer sugar-glass granule store
MECHANISM: The charged electrolyte is vitrified into sugar-glass granules (Tg about 50°C) that sit in ambient silos with their mobility frozen, and they are melted only to discharge. In the repaired design the posolyte and negolyte are separate granule streams, because in one shared melt they would annihilate with a half-life of about 1e-7 s. The redox centres are bulky oligomeric quinones (r about 2.5 nm). They reach the electrode by electron hopping (D_app about 2.5e-12 m²/s), while charge through the separator is carried by a small, fast proton or Li+ carrier. This cuts the geometry-independent product of crossover and ohmic loss from 15.7 mV to 0.53 mV, so crossover falls from 31% to 1.1% at a 50 mV separator drop. The 15 µm half-channel cell at 170°C runs at about 15 A/m² with 16 mV ohmic loss and 1.5 bar per 2 cm, which is 0.30 m²/kWh at 300 h.
VALUE: Multi-week (300-1000 h) storage with zero self-discharge, kept as dry granules in silos, viable if oligomeric quinone actives cost under about $1-2/kg.

IDEA 2
NAME: Winter-locked tread-strip bale yard
MECHANISM: Strain-induced crystallisation locks stretched rubber so that baled bundles store elastic energy with no holding force, and warming releases it against a generator. In the repaired design the bands are cord-free tread strips peeled from scrap truck tyres, stretched to 4x (300%, below the 400-500% break strain). Fixity is achieved by storing the bales below the crystallite melting point in a cold-climate winter yard, cycled once per season. This gives about 4.35 Wh/kg input and about 2.4 Wh/kg recoverable, 418 kg of rubber per kWh, about $7/kWh of yard and a 900 kN winch per 1.5 kWh stroke. It is only a niche: medium bought at market price costs $143-810/kWh, and the US scrap-truck-tyre supply supports only about 0.5 GWh/yr.
VALUE: Cold-climate industrial sites with waste heat and tyre waste get a non-hazardous, leak-free seasonal mechanical store at small (MWh) scale, not a grid-wide solution.

IDEA 3
NAME: Crystallizing Twin-Ditch Flow Battery
MECHANISM: The charged organic molecule crystallises only after a delay, so it nucleates on seeds in each side's downstream basin, and the energy sits in powder heaps while the solution stays saturated at about 20 mM. In the repaired design the electrodes are flow-through carbon felts on both faces of the 2.5 mm porous divider, and the ditches serve only as feed channels. This lifts the mass-transfer limit from about 10 to about 300-480 A/m². At 50 A/m² the cell has 48 mV of ohmic loss and 0.31% crossover, and the converter costs about $1/W, or $4.9/kWh at 200 h and $2.0/kWh at 500 h. The decisive remaining limit is the powder: 7.5 kg/kWh (2 e⁻, about 200 g/mol, 1 V) must cost about $1.5/kg or less, and nucleation induction must exceed about 17 min of ditch residence.
VALUE: Months-long storage as dry powder heaps, with a converter costing a few dollars per kWh, once a cheap molecule with delayed-crystallising charged state is found.

IDEA 4
NAME: Vapour-swing salt-clay store
MECHANISM: Energy is stored as unmet hydration of static clay beds in vacuum-tight, earth-covered enclosures that only resist atmospheric pressure. One reversible vapour compressor/turbine is the whole converter. In the repaired design the plain smectite (4.5 Wh/kg, 220 kg/kWh) becomes a CaCl2-in-clay composite with a hydration step near RH 0.3-0.45, giving 9.2 Wh/kg, 109 kg/kWh and about $10/kWh. Because heat is 15-23x the work, a 3 K heat-coupling gap would cost 45% of round trip. The beds are therefore 6 cm thick and interleaved with pond-water bags (about 3.2 m² of film per kWh) to keep the gap at 0.5 K or less, which limits the loss to about 7%. Running at 35°C cuts the machine to 0.5 m³/s per kW at a single-stage pressure ratio of about 2.2. That is about $2-4k/kW, or $1.3-2.6/kWh at 1500 h, with round-trip efficiency of only about 50%.
VALUE: For durations of 1000 h and more, the capacity costs about as much as salted clay and plastic film, with one vapour machine sized only for power.

IDEA 5
NAME: Earthen bipolar clay pile
MECHANISM: The pile is built from excavated Fe-smectite (layer Fe(III)/Fe(II)) and crushed MnO2 ore laid as earth layers, separated by a compacted bentonite liner and stacked in series through graphite-foil sheets. The original 10 vol% char is below the percolation threshold, so the repaired design uses 25 vol% char (about 4.4 S/m). Ordinary bentonite (about 0.4 mmol e⁻/g) gives only 0.25 kWh/m² and about $24/kWh of foil, so the pile needs Fe-rich smectite with about 1.5 mmol e⁻/g accessible (nontronite NAu-2 has 4.1 mmol Fe/g, only part of it active). With 4 cm layers, 2 M brine and 4-week discharge, it holds 1.25 kWh/m² with 59 mV total loss of about 600 mV. Mediator shuttling through the 5 mm liner costs 0.1-0.7% per 2 weeks, and the total is about $16/kWh.
VALUE: Landowners on Fe-rich clay deposits get a weeks-long store built with earthmoving equipment, where the earth electrode is the converter and the only fabricated part is graphite foil at about $5/kWh.

IDEA 6
NAME: Floating PV-strung gravity-cell trays
MECHANISM: Gravity and a dense charged phase replace the separator. Bromine bound to a polyquaternary complexer condenses on a 6 cm coke bed (0.84 M Br2 in the pores holds 1.9 kWh/m²), and zinc plates onto a floating carbon mat above it. A plain open water gap convects when the surface cools at night (Ra about 9.5e5), which would self-discharge about 43% per 10 days. Filling the gap with a nonwoven mat (Darcy-Ra 0.1, below 39.5) returns the cell to diffusion, at 1.4% per 10 days. The pond is split into isolated lined trays, each charged by its own sub-string of 4 c-Si cells at about 1.95 V. That needs no charging inverter and gives self-balancing cells at 86% of maximum PV power, with a dark leakage of 2 mA, under 0.1% per 10 days. Total cost is about $34/kWh, PV excluded.
VALUE: Floating-solar operators get 10-day storage under their arrays with cell-level DC charging and no charging inverter, at roughly $30-35/kWh.

=== NOTES ===
Overview: all estimates are computed in `/home/user/SomeRepository/engine/runs/energy/repair/calc.py`, with one line per round in `LOG.md` in the same folder. Ideas 1, 3, 4 and 5 can work around their anchors, but each depends on one stated condition that is not yet demonstrated. Idea 2 survives only as a niche. In idea 6 the core cell is already published, so its novelty is in the solar coupling.

IDEA 1:
- Anchor kept? Yes (vitrified charged electrolyte in silos, melted only to discharge).
- Decisive numbers:
  - Viscosity 0.63 Pa·s at 170°C, from the WLF equation (Williams-Landel-Ferry 1955).
  - Smoluchowski annihilation half-life of 1e-7 s, which forces two separate granule streams.
  - New result: crossover × ohmic loss is independent of geometry, equal to (RT/F)·c_aD_a/Σc_iD_i: 31% crossover with ordinary radicals vs 1.1% with oligomers plus a decoupled carrier.
  - Melt heat is 1.6 kWh_th/kWh_e, or 0.16 after 90% recovery.
  - Actives must cost $0.5-1.9/kg (at 1.0-1.4 V) to stay at or below $10/kWh. This is the binding limit.
- Unverified: the decoupled fast carrier (10x Stokes-Einstein) and the electron-hopping rate are assumptions.
- Closest existing work: the PNNL freeze-thaw molten-salt battery (also freezes to stop self-discharge, but not as decoupled granules); thermal reserve batteries; solid-booster and redox-targeting flow batteries (PMC8067695). No vitrified-granule electrolyte store was found.

IDEA 2:
- Anchor kept? Partly. It survives only in cold climates and seasonal use.
- Decisive numbers:
  - Medium cost dominates: at 3 Wh/kg, rubber at $1.7/kg gives $810/kWh, so only near-free scrap qualifies.
  - Tread M300 11-17 MPa and tensile strength 18-22 MPa (US5132357) give 4.35 Wh/kg input.
  - Resource ceiling of about 0.5 GWh/yr.
  - Heat needed to trigger is about 7x the work.
- Unverified: room-temperature fixity is shown only for lightly crosslinked NR (Katzenberg, Heuwers & Tiller, Adv. Mater. 2011, "superheated rubber"). It is not demonstrated for filled tyre vulcanizates, which is why the cold-climate lock is assumed.
- Closest existing work: shape-memory natural rubber; elastocaloric NR.

IDEA 3:
- Anchor kept? Yes.
- Decisive numbers:
  - Floor flow-by limiting current is about 9.6 A/m² at 20 mM.
  - Flow-through felts raise it to about 290-480 A/m².
  - At 50 A/m²: 0.31% crossover, 48 mV ohmic loss, $2-5/kWh converter at 200-500 h.
  - Powder 7.5-12.4 kg/kWh.
- Unverified: no real molecule with a delayed-crystallising charged state was identified; the felt mass-transfer coefficient (0.05 /s) is an order-of-magnitude assumption.
- Closest existing work: redox-targeting and solid-booster flow batteries; semi-solid flow; Zn-Br complexed phases. None found that self-crystallises the active molecule in a seeded basin.

IDEA 4:
- Anchor kept? Yes. The material changed from plain clay to a salt-in-clay composite.
- Decisive numbers:
  - Volumetric work is at most p_sat·RH·ln(1/RH), which gives 0.86-1.11 m³/s per kW at 25°C and 0.5 at 35°C (Magnus p_sat).
  - Heat-coupling ΔT is the hidden binding limit: a 3 K gap costs 45% of round trip, so ΔT must stay at 0.5 K or less.
  - The isotherm shape is from Keren & Shainberg 1975, with my own GAB fit.
- Unverified: the vapour machine cost of $3-6k per m³/s is my industrial-fan-class estimate, not a quote.
- Closest existing work: water-sorption thermal storage (silica gel 152 kWh/m³ thermal; salt-in-matrix composites) and R718 turbo-compressors (pressure ratio of about 2 per axial stage, TU Dresden/ILK). No work-in/work-out vapour-swing electricity store was found.

IDEA 5:
- Anchor kept? Yes.
- Decisive numbers:
  - The char fraction must exceed percolation (at 25 vol%, about 4.4 S/m).
  - Fe-accessible capacity sets the foil cost: 0.4 mmol/g gives $24/kWh, 1.5 mmol/g gives $4.8/kWh.
  - Gorski et al. 2012 (ES&T 46:9360) found Fe in nontronites partly redox-inactive.
  - Ionic loss estimated with Archie's law.
- Unverified: the cell voltage of about 0.6 V and the Fe-smectite capacity are assumptions; Fe-rich smectite is a scarce resource.
- Closest existing work: geochemical "clay redox battery" studies (EPFL, PNNL nontronite). No electrode or battery use was found.

IDEA 6:
- Anchor kept? Yes (gravity- and phase-separated pond cell with a floating metal mat and DC-coupled PV). The repaired chemistry is zinc-bromine.
- Decisive numbers: convective vs diffusive self-discharge, 43% vs 1.4% per 10 days; 86% of maximum PV power; about $34/kWh.
- Unverified: the free-Br2 level (10 mM) and the ZnBr2 price ($3/kg) are assumptions.
- Closest existing work: the core cell is close to the known membraneless Zn-Br battery of Biswas, Steingart et al. (Energy Environ. Sci. 2017, 10:114; above 90% coulombic efficiency, under $100/kWh projected). What appears new is the pond scale, the floating mat, the nonwoven that stops convection, and per-cell PV sub-strings.