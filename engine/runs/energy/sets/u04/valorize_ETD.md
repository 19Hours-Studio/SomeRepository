=== CHECKED D01 ===
ANCHOR: Protons stored on cheap carbon piles
VERDICT: FIX
ESTIMATE: 1 wt% H is 10 mol e⁻/kg. Hydrogen goes onto carbon about 0.3 V below the H2 potential and only comes off about 0.3–0.4 V above it, so a cell against air delivers about 0.5 V while charging takes about 1.9 V (round trip about 25%). That gives 10 × 96,485 C × 0.5 V ≈ 0.13 kWh/kg, roughly 1/250 of hydrogen's 33 kWh/kg, so this is not hydrogen-level density. The ratio that really controls cost is uptake per dollar of carbon, not loading per kg. Uptake scales with surface area (about 0.5 wt% per 1,000 m²/g), and price climbs steeply with surface area: raw char at ~300 m²/g costs about $0.2/kg, while 2,000 m²/g carbon costs $3–10/kg. Capacity therefore costs $10–40/kWh, about 1,000x more than "bulk coal" ($0.01/kWh thermal), but a mid-grade char can reach the ~$15/kWh goal.
NAME: Charged-char proton pile
MECHANISM: Steam-activated coal char (about 1,000 m²/g, about $1/kg) is the negative electrode in an acidic water-splitting cell. Charging loads about 0.5 wt% H onto its surface, and the loaded slurry is pumped into sealed bins flooded with electrolyte. During lulls the slurry is oxidized against air at about 0.5 V. The store holds 5 mol e⁻/kg × 96,485 C × 0.5 V ≈ 0.067 kWh/kg, which works out to about $15/kWh of capacity at about 25% round-trip efficiency. The go/no-go test is open-circuit retention, which must stay above about 95% per week in the sealed bins.
VALUE: Utilities get multi-week reserve capacity at about $15/kWh from a coal-industry commodity, where low capital matters more than round-trip efficiency.

=== CHECKED D02 ===
ANCHOR: Acetone/isopropanol two-electron liquid loop
VERDICT: PASS
ESTIMATE: Isopropanol has 13.1 mol/L and 2 e⁻ per molecule, so at 1.1 V it holds 26.2 × 96,485 × 1.1 ≈ 2.8 MJ/L = 0.77 kWh/L in theory. At a realistic 0.5 V discharge that falls to about 0.35 kWh/L, so the liquid ($1/kg, about $2.2/kWh) plus steel tanks ($100/m³, about $0.3/kWh) cost about $2.5/kWh. The platinum-group stack dominates: about 50 mW/cm² with about 2 mg/cm² PtRu is about 40 g/kW, or about $1,500/kW. Spread over a 100–170 h discharge that adds $9–15/kWh, so stack cost per kWh scales as 1/duration. Round trip is about 0.5 V / 1.8 V ≈ 28%, and the total of about $12–18/kWh is roughly 10x below today's battery storage.
NAME: Isopropanol-acetone liquid electricity store
MECHANISM: In surplus hours a proton-exchange cell at about 1.8 V reduces acetone to isopropanol, taking its protons from water, so no hydrogen gas is made. During lulls a sister cell oxidizes the isopropanol back to acetone against air at about 0.5 V and about 50 mW/cm². Both liquids sit in ordinary steel tanks at about 0.35 kWh/L delivered, for about $2.5/kWh of stored energy. The PGM stack (about $1,500/kW) dominates cost, so the system is sized for discharges of 100 hours or more, where it adds only about $10–15/kWh. Round-trip efficiency is about 28%.
VALUE: Grid operators get week-scale storage at about $15/kWh using existing tank and pipeline infrastructure, with no hydrogen caverns or compressors.

=== CHECKED D03 ===
ANCHOR: Single peroxide liquid, membraneless cell
VERDICT: FIX
ESTIMATE: A membraneless cell gets only 1 e⁻ per H2O2 (theory 1.07 V, about 0.5 V in practice) at just 1–5 mW/cm², while charging spends 2 e⁻ at about 1.3 V, so round trip is about 0.5/2.6 ≈ 19%. 3 wt% peroxide (0.88 mol/L) stores 0.88 × 96,485 × 0.5 ≈ 42 kJ/L ≈ 12 kWh/m³, about $8/kWh in $100/m³ tanks. At 2 mW/cm², 1 kW needs 50 m² of electrode; at about $100/m² that is $5,000/kW, or about $30/kWh over 168 h, so the total of about $40/kWh is about 3x over the ~$15/kWh goal. Electrode cost scales as 1/(power density × duration) and liquid cost as 1/concentration. Power per footprint grows with internal electrode area because the cell is kinetics-limited.
NAME: Ten-percent peroxide flow-through cell
MECHANISM: Carbon cathodes reduce air to peroxide, which is concentrated to about 10 wt% (2.9 mol/L, about 40 kWh/m³ at 0.5 V) and held stabilized in HDPE tanks, for about $3/kWh including the liquid. During lulls the peroxide flows through one separator-free cell built from thick carbon felts. A selective iron-cyanide cathode and a nickel anode use the felts' internal area to reach about 5 mW/cm² of footprint. At about $50/m² that is about $1,000/kW, about $6/kWh over a week-long discharge, for a total near $9/kWh at about 20% round-trip efficiency.
VALUE: Regions with plenty of cheap surplus power get week-long reserves at under $10/kWh from one benign liquid made of water and air, trading efficiency for very low capital.

=== CHECKED D04 ===
ANCHOR: Electricity-bred thorium fuel as the store
VERDICT: FAIL
ESTIMATE: A 1 GeV proton costs about 6.7 GeV of grid power at 15% wall-plug efficiency and frees about 25 neutrons, so each source neutron costs about 270 MeV. At equilibrium a thorium blanket nets about 1 bred U-233 per source neutron: about 200 MeV of heat, or about 70 MeV of electricity. The bred fuel therefore returns only about 0.25 kWh per kWh stored. The apparent energy gain comes from the blanket's own fissions (at k = 0.95, about 1.5 GeV of heat per source neutron), and those happen during the surplus, when no one needs the power. Separately, reactors that run only in lulls (about $6,000/kW, about 7% capacity factor, 8% capital charge) cost about $0.8/kWh delivered whatever the fuel, against fuel that is already almost free (mined uranium is under $0.01/kWh).
NAME: Surplus-power thorium fuel breeder
MECHANISM: Curtailed renewable power drives an accelerator whose spallation neutrons breed U-233 in a subcritical thorium blanket. Each ~270 MeV of grid electricity yields about one net U-233 atom, worth about 70 MeV of electricity later, so the energy return is only about 25%. The blanket's own fission heat means the plant is effectively a reactor itself. The bred fuel goes to reactors that already run near baseload, because a reactor kept idle for lulls costs about $0.8/kWh. This is a power-to-fuel sink, not a cheap way to cover lulls.
VALUE: Thorium-rich countries without enrichment get a way to turn curtailed electricity into reactor fuel, but it does not lower the cost of covering calm, dark spells.

=== CHECKED D05 ===
ANCHOR: Battery ships shuttling between decorrelated lulls
VERDICT: PASS
ESTIMATE: Multi-day lulls are synoptic and correlated over about 1,500–2,000 km. At 15 knots (about 670 km/day) a ship covers that in about 3 days, well inside the 7-day forecast horizon, and this transit-to-forecast ratio (about 0.4) is what controls feasibility. A 120,000 dwt hull filled with LFP containers at about 120 Wh/kg carries about 14 GWh, which puts a $100M hull at about $7/kWh. Per 2,000 km leg it burns about 10–15% of its cargo, and it needs a port connection of about 200 MW to empty in 3 days. Serving three decorrelated regions raises lull discharges from about 5–8 to about 15–25 per year, a gain of about 3x, which matches the claim.
NAME: Lull-chasing battery fleet
MECHANISM: Bulk carriers holding about 14 GWh of cheap LFP containers charge at whichever coastal grid has surplus. A forecast-driven router then sends them about 2,000 km (about 3 days) to the region where the next lull is predicted. They discharge through port substations of about 200 MW, losing about 10–15% of the cargo energy to propulsion per leg. Because lulls in regions about 2,000 km apart rarely coincide, each kWh serves about 3x more lull events per year than a stationary unit.
VALUE: Coastal grids share one storage fleet, which cuts the capital cost per delivered lull kWh by about 3x for regions whose lulls rarely line up.

=== CHECKED D06 ===
ANCHOR: Steerable orbital solar beam to farm rectennas
VERDICT: FIX
ESTIMATE: From GEO (3.6×10⁷ m) at 5.8 GHz (λ = 5.2 cm), a 1-km transmitter casts a spot of 2.44λR/D ≈ 4.6 km. Each rectenna is therefore about 17 km², and spot size is fixed by R/D, not by power, so only GW-scale farms can host one. Cost is set by specific mass × launch price. At about 6–10 kg per delivered kW and about $10,000/kg to GEO today, launch alone costs $60,000–100,000/kW, or about $0.6–1/kWh at a 95% capacity factor. That is 10–20x above the $0.03–0.05/kWh the beam must compete with outside lulls. Areal mass, not array size, closes the gap: tiles at 150 g/m² delivering about 200 W/m² (30% PV, 50% chain) come to about 1 kg/kW.
NAME: Ultralight steerable orbital solar beam
MECHANISM: GEO arrays of integrated PV-microwave tiles at about 150 g/m² (about 1 kg per delivered kW) beam 5.8 GHz power through cloud to 17-km² rectennas built inside GW-scale solar farms. Rectennas cost about $10/m², or about $85/kW, so each satellite can be steered among several of them. With launch at or below $1,000/kg to GEO and about $1,000/kW of hardware, the system costs about $2,000–3,000/kW, or about $0.03–0.05/kWh running near-continuously. That keeps it competitive outside lulls and lets forecasts aim it at the region that is calm and dark.
VALUE: Large solar-farm regions get firm power on demand through multi-week calm, dark spells without storing it, provided launch to GEO reaches about $1,000/kg.

=== CHECKED D07 ===
ANCHOR: Salt-water acid/base bipolar-membrane store
VERDICT: FIX
ESTIMATE: Neutralization yields 0.059 V × 14 ≈ 0.83 V. At 1 M acid and base and a real discharge of about 0.6 V, the liquid stores 1,000 mol × 96,485 × 0.6 V per 2 m³ ≈ 8 kWh/m³. Covered HDPE-lined ponds at about $30/m³ then cost about $4/kWh, so the "well under $1/kWh" claim is off by 5–10x. Energy per m³ scales linearly with concentration while voltage grows only logarithmically, and acid/base leakage through the bipolar membrane caps concentration at about 1–2 M. Stacks run at about 20 mW/cm² with membrane triplets at $300–500/m², about $2,000/kW, which is about $12/kWh over a 168 h discharge.
NAME: Two-molar acid-base pond battery
MECHANISM: Bipolar-membrane stacks split brine into 2 M HCl and 2 M NaOH. These are held in large covered, HDPE-lined ponds at about 16 kWh/m³ (2,000 mol × 96,485 × 0.6 V per 2 m³), so storage costs about $2/kWh of capacity. During lulls the same stacks run in reverse at about 20 mW/cm² and about 50% round trip, adding about $12/kWh over a week-long discharge, and the stacks are drained when idle to stop leakage. The total is about $14/kWh, made from salt and water alone.
VALUE: Any coastal or inland grid gets week-scale storage at about $14/kWh from inexhaustible, non-toxic materials, with capacity that grows simply by digging ponds.

=== CHECKED D08 ===
ANCHOR: Tethered crosswind wings in upper-level winds
VERDICT: FIX
ESTIMATE: At 10 km the air density is about 0.41 kg/m³ and wind is about 25 m/s. A 500-m² wing (C_L 1, C_D 0.05) pulls about 0.4 MN, which needs about 2.2 cm of Dyneema at 1 GPa and weighs about 5.5 t over the ~15 km tether required to reach 10 km. That tether's drag area (C_D·d·L/4 ≈ 80 m²) is about 3x the wing's own (25 m²), so effective lift-to-drag falls from 20 to about 4.5 and power, which scales as (L/D)², drops about 20x to about 4.5 MW. In a 10-m/s blocked flow the wing's lift (about 90 kN) barely carries the tether plus wing (about 75 kN), so the design fails in exactly the weak-wind spells it targets. The controlling ratio is moving-tether length over √(wing area), not altitude.
NAME: Paired high-altitude dancing kites
MECHANISM: Two rigid wings fly crosswind loops on short bridles of about 1 km, joined at the top of one slowly moving 15-km main tether. The main tether reels out at about one-third of wind speed to drive a ground generator. The moving-tether drag area falls to about 4 m² per wing against the wing's 25 m², so lift-to-drag recovers to about 17, giving about 10x more power at the same wind. This lets each 500-m² wing stay aloft and still deliver megawatts in 10 m/s upper-level winds. Sites need permanent restricted airspace because 8–12 km is airline cruise altitude, so they belong offshore or in remote areas.
VALUE: Wind-heavy grids keep generating through many multi-day surface lulls, provided reanalysis data confirm upper-level winds stay at or above about 10 m/s during blocking. That cuts how much long-duration storage they must buy.