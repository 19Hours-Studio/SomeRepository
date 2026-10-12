**Answer 1: Thick slabs sized to the discharge time**
1. LAW: Transport-length law, used in the long-t, high-κ regime. Thickness grows as √t, so at E/P ≈ 250 h with KOH at 12 S/m the slab can be about 3 cm thick.
2. MECHANISM: Alkaline iron anode slabs and MnO₂ cathode slabs, each about 3 cm thick, are filled with coke and face each other across one separator sheet.
3. COUNT: L = √(2·12·0.05·9e5 / 1e9) ≈ 3 cm, which means about 50× less foil and separator per kWh. The materials are about 1 kg Fe + 3 kg MnO₂ per kWh at about 1 V, roughly $8/kWh.
4. HONESTY: The nearest work is Edison Ni-Fe and Zn-MnO₂ cells. This design has no nickel, no zinc and no air, and its electrode thickness is set by t rather than by habit.

**Answer 2: Polymer flow cell separated by sand**
1. LAW: Crossover-ohmic invariant, used in the high salt-to-active mobility regime. Actives have D ≈ 1e-13, in 4 M NaCl at about 20 S/m.
2. MECHANISM: Lignin-derived quinone macromolecules flow on both sides of a centimetre-wide gap packed with sand instead of a membrane.
3. COUNT: nFDc/(σV) = 96485·1e-13·1000/20 ≈ 5e-7. So 0.5% ohmic loss comes with only 1e-4 crossover.
4. HONESTY: The nearest work is Janoschka's polymer flow battery from 2015, which uses a dialysis membrane. This design removes the membrane entirely and relies on the invariant.

**Answer 3: Iron-chromium flow with a spent-electrolyte buffer**
1. LAW: Homogeneous co-mixing law, used in the spatial-separation regime. A spent-electrolyte buffer s = 1.5 mm wide is much thicker than √(Dt) for a contact time of about 2 minutes.
2. MECHANISM: The charged Fe³⁺ stream and the charged Cr²⁺ stream run side by side down a plastic channel, separated by a sheath of discharged FeCl₂/CrCl₃. The streams are split again at the outlet.
3. COUNT: exp(−2.25e-6 / (4·1e-9·120)) ≈ 1% leak. The ohmic drop across the sheath is about 10 mV at 200 A/m², against a 1.18 V cell. The chemicals cost about $10/kWh.
4. HONESTY: The nearest work is microfluidic co-laminar cells (Kjeang; Braff 2013). Those run for seconds with µm-wide interfaces. This design uses mm-wide buffers of the cell's own discharged state, and any mixing in them does no harm.

=== IDEAS ===
IDEA 1
NAME: Centimetre Iron-Manganese Slabs
MECHANISM: Alkaline iron anode slabs and MnO₂ cathode slabs, each about 3 cm thick and filled with coke, sit in 12 S/m KOH across a single separator. The slab thickness is chosen from the 250-hour discharge time, since the ion-conduction length grows with the square root of time. The result stores about 1 V per electron pair, using roughly 1 kg Fe and 3 kg MnO₂ per kWh.
VALUE: About 50× less collector and separator per kWh, with materials near $8/kWh, makes ten-day storage cheap.

IDEA 2
NAME: Sand-Gapped Polymer Flow Cell
MECHANISM: Lignin-derived quinone macromolecules (D ≈ 1e-13) in 4 M NaCl flow on both sides of a centimetre-wide bed of packed sand, with no membrane. Crossover fraction times ohmic fraction is fixed at about 5e-7, so 0.5% resistive loss comes with only 0.01% crossover. Capacity scales with tank volume.
VALUE: It removes the costliest flow-battery part, the ion-exchange membrane, while keeping crossover negligible.

IDEA 3
NAME: Spent-Sheath Iron-Chromium Flow
MECHANISM: The charged Fe³⁺ stream and the charged Cr²⁺ stream run side by side down a cheap plastic channel. A 1.5 mm sheath of their own discharged mixed electrolyte separates them, and they stay in contact for about two minutes. Diffusive leak through the sheath falls as exp(−s²/4Dt), to about 1%, while ions conduct across it with only about 10 mV of loss.
VALUE: An iron-chromium flow battery with no membrane and chemicals near $10/kWh.