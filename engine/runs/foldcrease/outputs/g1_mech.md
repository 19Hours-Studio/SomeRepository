# Crease-free foldable: three architectures

**Shared targets (my proposal, not standards).** Measured after 2,000 cycles and an 8 h hold folded at 60 °C/90 %RH, then 1 h after opening.
- **Depth:** residual crease depth ≤5 µm by confocal profilometry.
- **Slope:** peak slope ≤0.03° (0.5 mrad). The line in reflections is set by slope, not depth.
- **Reflection:** no line visible in a striped-lightbox reflection at 0–70° viewing angle, judged by 20 observers (pass if fewer than 5% detect it).
- **Touch:** blind finger-swipe detection no better than chance.

**What is established vs speculative.** The bending strain ε = t/2R and the absence of creep in glass at room temperature are established. The 5 µm and 0.03° thresholds, all creep limits and all costs are speculation.

**Cheapest test of the central claim.** Bond laminate strips over mandrels, hold them 8 h at 60 °C, and profile them. This costs about $5k and needs no phone.

**Comparison with shipped and reported designs.** Samsung, Apple (perforated plate) and Oppo (liquid-printed fill) all smooth the support under bonded, creeping polymers. That is why they report relative reductions of 20–82%. Each idea below instead removes the source of the permanent strain.

**Budget.** Each idea adds roughly $15–40 per module. Against the ledger, that is about 1–2% of retail. Yield is the real cost risk.

=== IDEAS ===

IDEA 1
NAME: Sub-creep strain budget fold
MECHANISM: The hinge holds the bend zone at a radius of at least 5 mm. This is done with a deep teardrop cavity, with the panel sliding into each half on rails, so the closed phone stays about 10 mm thick. The panel stack in the bend zone is thinned to about 60 µm of polymer, so peak strain stays at or below 0.3–0.5%, under the yield and creep onset of polyimide and adhesive at 60 °C. The closest earlier attempt is the teardrop hinge, which stopped near R = 1.5–2 mm and therefore stayed in the creep regime. Translating the panel into the halves lifts the thickness cap that stopped it. The deciding quantity is the residual strain after an 8 h hold at 60 °C in the worst layer, which must be at or below 0.05%.
VALUE: Any crease that remains is elastic and recovers fully, giving a fold whose flatness can be certified rather than merely improved.

IDEA 2
NAME: Unbonded sliding bend-zone laminate
MECHANISM: Across the 15 mm bend zone, the glass, OLED-on-polyimide and support plate are left unbonded. They are separated by a sealed index-matched silicone fluid film (n ≈ 1.47, about 5 µm thick) and bonded only outside the zone. Each layer then bends about its own neutral axis, so strain is t_i/2R: about 0.75% for 30 µm glass and 0.5% for 20 µm polyimide at R = 2 mm. No adhesive shear creep can lock in a dent. The closest earlier attempt is low-modulus, high-recovery adhesive, which still couples the layers and creeps under heat and humidity. This design removes the adhesive from the bend zone entirely. The deciding quantity is fluid retention and edge-seal integrity over 2,000 cycles, measured as gap uniformity within ±0.5 µm.
VALUE: The polymer creep that sets every shipped crease is removed without adding thickness.

IDEA 3
NAME: Tensioned glass flattening hinge
MECHANISM: When the phone opens, cam-driven sliders in the hinge put the display under in-plane tension, about 20–40 N/m. The hinge also overbends about 2° past flat before settling. A force sensor stores the residual-curvature history and adjusts the overbend over the device's life. Tension reduces out-of-plane waviness in proportion to the residual bending moment divided by the tension. Because the glass is elastic, it returns the stack to flat as long as the polymer set stays small. The closest earlier attempt is Oppo's one-time laser mapping and liquid fill, which is static and cannot track creep that develops later. This design corrects on every cycle. The deciding quantity is the tension needed to reach 5 µm compared with the edge-flaw strength of the glass.
VALUE: The crease is held at zero throughout the device's life, so slow creep in the field never becomes visible.