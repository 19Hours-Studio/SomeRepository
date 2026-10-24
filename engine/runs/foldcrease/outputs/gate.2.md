=== GATE ===
IDEA 1: Tensioned drumhead hinge
KILLER | Sustained shear stress the OCA must carry to feed the flattening tension into the UTG. I modelled the set as a plate under tension, w_k = w0_k·Dk²/(Dk²+T), and checked the code against the exact single-sinusoid case (0.229207 computed vs 0.229205 exact). Flattening a 20 µm, 3 mm-wide set to ≤1 µm depth and ≤0.5 mrad slope takes T ≈ 4,100 N/m with the UTG's stiffness alone (D = 1.66e-4 N·m) and about 10,000 N/m with the whole stack's (4.0e-4 N·m). The 0.5 mrad slope limit is my own assumption. Through a 25 µm OCA (G = 90 kPa, shear-lag length 24 mm) that means τ = T/24 mm | required ≥168 kPa held for as long as the phone is open | available ≈10.5 kPa, a stress at which foldable OCA already creeps 16–18% in 10 min at 60 °C / 93% RH, with 95–96% recovery (USPTO 11334117 / 12174665, "Foldable display device") | MARGIN 0.06
CHAIN | Oppo Find N6 (mapped hinge, ~50 µm unevenness, crease still visible in some light) | now ~50 µm | with idea: the OCA limits tension to ~254 N/m, which leaves ~15–23 µm and 10–14 mrad slope, still visible | RATIO 2.2–3.3
VERDICT | DEAD | The tension that flattens even a 20 µm set needs ~16x more sustained OCA shear than the adhesive tolerates without creeping, and the tension the adhesive can carry only cuts the crease 2–3x.
NEW FACT | IEC 62715-6-22 (2026) is now a standard method for measuring surface crease and waviness on foldable displays. A SID digest names stylus/optical profilometry and deflectometry as the accepted crease metrics | https://www.evs.ee/et/iec-62715-6-22-2026 ; https://sid.org/Portals/sid/Files/SID-Digest/docs/77-5.pdf

IDEA 2: Tensioned membrane open state
KILLER | OCA shear stress (and UTG membrane stress) needed to reach ≤1 µm depth. Starting from a 50 µm, 3 mm set (Oppo-class residual), it takes T ≈ 10,700 N/m (UTG stiffness) to 26,000 N/m (stack stiffness). That is τ ≈ 440 kPa in the OCA and about 360 MPa of sustained membrane tension in 30 µm UTG. A sharper 1 mm-wide set needs 3×10⁵ N/m or more | required ≥440 kPa | available ≈10.5 kPa (same patent creep test, which already gives 16–18% creep in 10 min) | MARGIN 0.02
CHAIN | Oppo Find N6 | now ~50 µm | with idea: ~15–23 µm at the tension the OCA can carry | RATIO 2.2–3.3
VERDICT | DEAD | Reaching ≤1 µm needs about 40x the adhesive's sustainable shear and puts sustained tension of hundreds of MPa in the glass. The tension that is feasible leaves a visible crease.
NEW FACT | Oppo's 0.2 → 0.05 mm figure is the hinge-surface height variation, not a measured crease depth. It is made in ~20 laser-scan and UV-cured liquid-print passes per unit. Engadget still saw the crease | https://www.voxelmatters.com/oppo-find-n6-uses-3d-liquid-printing-to-eliminate-foldable-display-crease/ ; https://engadget.com/mobile/smartphones/oppos-find-n6-might-be-the-foldable-of-your-dreams-131036055.html

IDEA 3: Liquid-coupled slip stack
KILLER | Shear strain at the boundary where the fluid strip meets the bonded region. If each layer bends about its own neutral plane, adjacent layers must slip past each other by θ·d. For a 180° fold with mid-planes ~50 µm apart, that is π·50 µm ≈ 157 µm. It has to be absorbed by the perimeter seal or the bonded OCA (~25 µm thick) where the strip ends. The idea's stated deciding quantity, gap uniformity within ±1 µm, comes after this | required γ ≈ 6.3 (630%), and 12–25 for the UTG-to-OLED span | available ~2–3 (200–300% shear strain is the range quoted for foldable OCA; 3M whitepaper and flexible-OCA patent 11492515) | MARGIN ~0.4 (0.3–0.5)
CHAIN | Oppo Find N6 | now ~50 µm | with idea: removes the OCA's creep share, but the PET/PI protective film, polarizer and PI still bend at R ≈ 2 mm and keep their own set (my estimate, not sourced) | RATIO ~1.3 (speculative)
VERDICT | WOUNDED | The slip does not disappear; it moves to the strip edges at about 2–3x what adhesives are quoted to take, and the polymer layers' own set remains.
NEW FACT | 3M specifies that foldable OCA must survive 100,000 or more dynamic folds at 1–5 mm radius, with bending raising adhesive shear strain by more than 300% | https://multimedia.3m.com/mws/media/1793258O/optically-clear-adhesives-for-foldable-oled-displays-whitepaper.pdf

IDEA 4: Drumhead tension hinge
KILLER | In-plane tension needed for an invisible residual. At the idea's own 600 N/m (its √(D/T) ≈ 0.5 mm and 0.03% glass strain both check out), a 20 µm, 3 mm set falls only to 3.4–6.1 µm with a 2.3–3.9 mrad slope. Reaching ≤1 µm / ≤0.5 mrad takes ≥4,100 N/m. Even 600 N/m puts ~25 kPa of shear on the OCA, about 2.4x the 10.5 kPa creep-test stress | required ≥4,100 N/m | available 600 N/m as specified, and an OCA-sustainable ~254 N/m | MARGIN 0.15 (0.06 if OCA-limited)
CHAIN | Oppo Find N6 | now ~50 µm | with idea: 8.6–15 µm at 600 N/m, visible | RATIO 3.3–5.9 on paper, but only if the OCA survives the 600 N/m it cannot sustain
VERDICT | DEAD | 600 N/m is 7x too little to flatten the set, and it already overloads the OCA in shear by about 2.4x.
NEW FACT | Apple's crease patent leaves room for the bent display (flaps retract when folded and extend when opened) rather than tensioning it. Patent US11644873 names the display being pulled during folding as a source of damage | https://www.imore.com/patent-suggests-apple-might-have-solved-folding-phone-creasing-problem ; https://patents.google.com/patent/US11644873

Notes on method:
- **CHAIN measure.** I used crease depth, not cost, because depth is the gain the question asks for. On cost alone, every idea adds parts and none saves money, so all would score RATIO <1.1.
- **Common killer for ideas 1, 2 and 4.** All three tension ideas hit the same limit. Tension flattens long, shallow features easily but barely moves sharp ones, and the force needed exceeds what the OCA can hold without creeping.
- **Unmeasured inputs.** Real crease profiles, the stack stiffness with the support plate included, and the visibility limit on slope still need profilometry or a prototype.
- **Cheapest test.** Laminate a creased panel offcut, clamp it, apply weights, and scan it with a profilometer.

Files are in /home/user/SomeRepository/engine/runs/foldcrease/gate/c2/:
- gate_calc.py
- gate_notes.md