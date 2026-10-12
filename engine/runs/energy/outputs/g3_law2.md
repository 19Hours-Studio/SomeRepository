**A. Poured-slab multi-day electrodes**
1. LAW: Transport-length law. Thick electrodes work when κ is high and t is long. With L = √(2κΔV·t/q_vol), KOH at κ = 12 S/m, ΔV = 0.05 V, t = 100 h and q_vol = 1.8e9 C/m³ give L ≈ 1.5 cm.
2. MECHANISM: Three cast layers are poured like concrete into flat trays: an iron-oxide paste with coke filler and 1% Bi₂S₃, a KOH gel, and a MnO₂-ore paste with coke filler.
3. COUNT: 0.015 m × 1.8e9 J/m³ ≈ 7.5 kWh/m². At about $1/m² for foil and tray, hardware is about $0.1/kWh. Iron plus Mn ore at about 4 kg/kWh costs about $1.5/kWh, so the medium stays under $10/kWh.
4. HONESTY: The closest existing work is mm-thick Zn–MnO₂ and iron–nickel plates. What is new here is that the layers are poured in place and sized to 100 h, which cuts hardware per kWh about 50x.

**B. Three-lamina falling-film cell**
1. LAW: Co-mixing law, buffer opening. A spent lamina of thickness s cuts the leak by exp(−s²/4Dt). With s = 1.5 mm, D = 1e-9 m²/s and t = 100 s, the exponent is −5.6, so the leak is about 0.4%.
2. MECHANISM: Three layers fall together down a gap between two plates, with no membrane: charged ferric catholyte on one wall, spent FeCl₂ in the middle, and an iron-plating wall on the other side. A splitter at the bottom separates the three streams again.
3. COUNT: The gap is about 4 mm at 20 S/m, which gives R ≈ 2e-4 Ω·m², or about 20 mV at 100 A/m². FeCl₂ costs about $0.3/kg, so the medium is about $5/kWh.
4. HONESTY: The closest existing work is microfluidic laminar H₂–Br₂ cells. Those operate at the µm scale and need forced flow. This design works at mm scale under gravity, uses all-iron chemistry, and makes the buffer layer out of spent electrolyte.

**C. Sand-divided dilute salt-flooded flow cell**
1. LAW: Crossover-ohmic invariant, dilute-in-salt regime. nF·D·c/(σV) = 96485 × 6e-10 × 200 / (25 × 1.0) ≈ 4.6e-4.
2. MECHANISM: Fe and Cr chlorides at 0.2 M each sit in 4 M NaCl/HCl, mixed the same way on both sides, and flow on either side of a 5 mm packed-sand divider.
3. COUNT: The product 4.6e-4 means about 2% ohmic loss alongside about 2.3% crossover. Each kWh needs 185 L of brine, which costs about $2 for salt, $6 for chromium and $3 for a lined pond, about $12/kWh in total.
4. HONESTY: The closest existing work is Fe–Cr redox flow cells (NASA, EnerVault). Those use 1 M actives and membranes. The supporting salt here does what the membrane did.

=== IDEAS ===
IDEA 1
NAME: Poured-slab multi-day electrodes
MECHANISM: Iron-oxide paste and manganese-ore paste, each made conductive with coke, are cast in centimetre-thick layers with a KOH gel between them, in cheap trays. A 100-hour discharge lets ions cross 1.5 cm of electrode, so foil, separator and housing per kWh drop about 50x. Bi₂S₃ added to the iron layer suppresses hydrogen evolution during weeks of holding.
VALUE: Batteries stamped out like concrete paving, at under $10/kWh, sized for week-long lulls.

IDEA 2
NAME: Three-lamina falling-film cell
MECHANISM: Charged ferric chloride, spent ferrous chloride and an iron-plating wall share one membraneless gap that the liquids fall through. The 1.5 mm spent middle layer gives charged species too little time to diffuse across it. A splitter at the bottom separates the streams back into their tanks.
VALUE: Membrane-free flow storage that uses only iron salt as the medium.

IDEA 3
NAME: Sand-divided dilute-brine flow cell
MECHANISM: Dilute iron and chromium chlorides (0.2 M) ride in concentrated sodium chloride brine, which carries most of the current. Because the salt is much more mobile than the actives, a plain sand layer keeps crossover and resistance both near 2%. The same mixed electrolyte is stored in lined ponds on both sides.
VALUE: Flow storage at about $12/kWh using only commodity salt, iron, chromium and sand.