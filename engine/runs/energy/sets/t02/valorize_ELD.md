=== CHECKED D01 ===
ANCHOR: Membraneless mineral bed between quinone brines
VERDICT: FIX
ESTIMATE: Any pressure difference Δp across the bed drives Darcy flow u = kΔp/(μL), and the useful current is j = fσ_eff·V/L. So the ratio of convective leak to useful current, cFkΔp/(μ·f·σ_eff·V), depends on neither the bed width L nor D. Assumed numbers: 0.1-mm sand, k ≈ 1e-11 m², μ = 1.3e-3 Pa·s, c = 500 mol/m³ of electrons, σ_eff ≈ 4 S/m, V = 0.7 V, f = 0.5%. That gives a leak of about 26x the useful current per pascal, so a realistic 10-100 Pa imbalance means a leak 250-2600x the useful current (and by Stokes-Einstein, D = 1e-13 m²/s implies ~2 µm particles; real lignin macromolecules have D ≈ 1e-10). Grain size controls the leak because k ∝ d², while bed width only sets power, which is about 1 W/m² at 1 cm. Fix: 1-µm silica (k ≈ 1e-15) at f = 2% gives 6.5e-4 per Pa, about 0.7% at 10 Pa; diffusion adds DcF/(fσV) ≈ 1.7% at D = 1e-10; and a 0.2-mm layer carries about 280 A/m².
NAME: Silica-flour membraneless quinone cell
MECHANISM: Lignin-derived quinone electrolytes in 4 M NaCl flow on both sides of a 0.2-mm layer of 1-µm silica flour on a coarse-sand backing, with no membrane. Leak through a porous bed is set by grain size, not thickness. At a permeability of about 1e-15 m², a 10 Pa imbalance between the sides leaks under 1% of the current, and mirrored low-pressure-drop flow-by channels keep the imbalance that small; diffusion adds about 1.7%. The thin layer carries about 280 A/m² at 2% resistive loss (about 170 W/m²), and capacity scales with tank volume.
VALUE: Grid operators get flow storage with no ion-exchange membrane: cents of ground quartz per m² replace the costliest stack part, and crossover stays at a few percent.

=== CHECKED D02 ===
ANCHOR: Layered membraneless all-iron liquid gap
VERDICT: FIX
ESTIMATE: Free fall down a vertical 3-mm gap reaches u = ρgw²/(12μ) = 1000×9.8×(3e-3)²/(12×1.5e-3) ≈ 5 m/s. That gives Re ≈ 1e4, so turbulence mixes the 1.5-mm buffer within milliseconds, and keeping free fall laminar (Re < ~100) would need a gap under about 0.65 mm. The flow speed is set by the slope that drives it, not by layer thickness. Tilting to sinθ ≈ 0.004 gives u ≈ 2 cm/s, Re ≈ 40, and 50 s over 1 m. Fe³⁺ then diffuses only √(6e-10×50) ≈ 0.17 mm, much less than 1.5 mm (leak about erfc(4.4) ≈ 1e-9), and the mass-transfer limit 2Fc√(D/πt) is about 380 A/m² at 1 M.
NAME: Tilted layered iron-salt channel
MECHANISM: Charged ferric chloride, a 1.5-mm layer of spent ferrous chloride and an iron-plating wall share one membraneless 3-mm channel tilted only about 0.25°. The liquids creep at about 2 cm/s (Reynolds number about 40) instead of falling turbulently. The layers are stacked by density: the salted, densest ferric layer sits on a carbon floor and the plating wall forms the ceiling, where hydrogen vents. Fe³⁺ spreads only about 0.17 mm in each 50-s pass, a splitter at the outlet returns each layer to its tank, and at about 150 A/m² the cell gives about 150 W/m².
VALUE: Utilities that need multi-day backup get membrane-free flow storage whose only active medium is iron salt.

=== CHECKED D03 ===
ANCHOR: Thick slabs sized by √(discharge time)
VERDICT: PASS
ESTIMATE: With uniform reaction, the ohmic drop across a slab is ΔV ≈ jL/(2σ) with j = q_v·L/t, so ΔV = q_v·L²/(2σt) and L = √(2σΔVt/q_v). MnO₂ at 40 vol% (5 g/cm³, 308 mAh/g) gives q_v ≈ 0.62 Ah/cm³ = 2.2e9 C/m³. With σ = 12 S/m, t = 9e5 s and 50 mV allowed per slab, L ≈ 2.2 cm, against 3 cm claimed (0.09 V at 74 A/m², within 2x). Iron holds about 2.3 Ah/cm³, so a 1.5-cm iron slab (about 0.05 V) is enough. The total drop is about 0.14 V on a cell of about 1 V, at about 18 kWh per m² of separator.
NAME: Thick-slab iron-manganese cell
MECHANISM: An alkaline iron anode slab (about 1.5 cm) and a coke-filled MnO₂ cathode slab (about 3 cm) sit in KOH (12 S/m effective in the pores) across one separator. Ohmic drop grows as L²/t, so a 250-hour discharge lets the cathode be 3 cm thick with only about 0.09 V of drop at about 74 A/m². Each m² of separator and collector then stores about 18 kWh, using roughly 1 kg Fe and 3 kg MnO₂ per kWh at about 1 V.
VALUE: Grids riding through calm, dark spells get ten-day storage with about 50x less collector and separator per kWh and materials near $8-15/kWh.

=== CHECKED D04 ===
ANCHOR: Brine-carried current over dilute Fe/Cr actives
VERDICT: FIX
ESTIMATE: Diffusion holds: crossover fraction × ohmic fraction = DcF/(σV) = 5e-10×200×96485/(22×1.18) ≈ 3.7e-4 ≈ 2%×2%, for any layer thickness. But a pressure difference drives Darcy flow, and the ratio of leak to useful current, cFkΔp/(μ·f·σ_eff·V), also does not depend on thickness. For 0.1-mm sand (k ≈ 1e-11 m², μ = 1.5e-3 Pa·s, σ_eff ≈ 4.4 S/m, f = 2%) the leak is about 1.2x the useful current per pascal, so a 10-100 Pa imbalance leaks 12-120x the useful current. Grain size controls this because k ∝ d²: 1-µm silica flour (k ≈ 1e-15) gives about 1.2e-4 per Pa, or about 0.4% at 30 Pa, and a 0.5-mm layer carries about 200 A/m².
NAME: Salt-carried iron-chromium silica cell
MECHANISM: Iron and chromium chlorides at 0.2 M are dissolved in about 4.5 M sodium chloride brine, and the brine carries the current. Between the sides, instead of a membrane, a 0.5-mm layer of 1-µm silica flour on a sand backing keeps both crossover and resistive loss near 2% at about 200 A/m². The silica's permeability of about 1e-15 m² means a 30 Pa pressure mismatch leaks only about 0.4%. The same mixed electrolyte, about 0.37 m³ per kWh, is stored in covered, lined ponds on both sides.
VALUE: Grids needing week-scale reserves get flow storage at about $12-20/kWh, made only from commodity salt, iron, chromium and ground quartz.

=== CHECKED D05 ===
ANCHOR: Self-sheathed co-flowing Fe/Cr streams
VERDICT: FIX
ESTIMATE: Diffusion is fine: s²/4Dt = (1.5e-3)²/(4×6e-10×120) ≈ 7.8, so the leak is about e^-7.8 ≈ 4e-4, and ohmic loss is about 100 A/m² × 1.5 mm / 30 S/m ≈ 5 mV. But side-by-side streams have vertical interfaces. A charged-to-discharged density difference of only 0.5% (g' ≈ 0.05 m/s²) makes them slump at about ½√(g'H) ≈ 1 cm/s in a 1-cm-deep channel, crossing the sheath in about 0.15 s instead of the 120 s needed, which is about 1000x too short. What controls the leak is how the interfaces sit relative to gravity, not sheath thickness. Stacked horizontally in stable density order, only diffusion is left, and the wall reaction limit 2Fc√(D/πt) ≈ 240 A/m² at 1 M sets about 100 A/m² as the working rate.
NAME: Stacked self-sheathed iron-chromium channel
MECHANISM: The charged Fe³⁺ stream flows along a carbon floor, a 1.5-mm sheath of discharged mixed electrolyte flows above it, and the charged Cr²⁺ stream runs along a carbon ceiling, where hydrogen vents. All three move through a flat plastic channel about 1.2 m long at about 1 cm/s, giving about 2 minutes of contact. Stacking them in density order, with the bottom stream salted at least 1% denser, stops buoyant overturning. That leaves only a diffusive leak of about e^-7.8 ≈ 0.04%, while ions cross the sheath with about 5 mV of loss at about 100 A/m².
VALUE: Multi-day grid storage from an iron-chromium flow battery with no membrane and chemicals near $10/kWh.

=== CHECKED D06 ===
ANCHOR: Cast tray layers of iron/manganese-ore paste
VERDICT: FIX
ESTIMATE: Discharge (Fe + 2MnO₂ + 2H₂O → Fe(OH)₂ + 2MnOOH) consumes one water molecule per electron: 1 kWh at about 1 V is 37 mol e⁻, or 0.67 kg of water. Assume a 1.5-cm ore cathode at about 0.5 Ah/cm³, giving 7.5 kWh/m² or 0.13 m² per kWh. With about 35% pores plus a 3-mm gel, the tray holds only about 1.4 L of 7 M KOH (about 1.2 kg of water). A full discharge then removes about 55% of the water and pushes KOH to about 14 M, near saturation, with conductivity roughly halved. The controlling ratio is water held per kWh against 0.67 kg, not electrode thickness; ohmic drop at 100 h is fine at about 75 A/m² × 1.5 cm / (2 × 10 S/m) ≈ 0.06 V. A gel reservoir about 1.2 cm thick raises the water to about 2.6 kg/kWh, so KOH only swings from 7 to 9.5 M, at an extra ~30 mV and under $1/kWh of KOH.
NAME: Paved iron-manganese ore trays
MECHANISM: Iron-oxide paste (with Bi₂S₃ against hydrogen evolution) and manganese-ore paste, both made conductive with coke, are cast about 1.5 cm thick in cheap trays. Between them is a KOH gel layer about 1.2 cm thick that also serves as a water reservoir. Discharging consumes 0.67 kg of water per kWh, and the gel holds about 2.6 kg/kWh, so the electrolyte only goes from 7 M to about 9.5 M. A 100-hour discharge at about 75 A/m² crosses each layer with about 0.06 V of drop, storing about 7.5 kWh per m² of tray.
VALUE: Utilities facing week-long calm, dark spells get batteries stamped out like concrete paving at roughly $10/kWh.