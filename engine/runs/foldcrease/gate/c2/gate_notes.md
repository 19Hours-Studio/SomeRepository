# Gate c2 notes (calc: gate_calc.py)

Model: a plate whose stress-free shape is the set w0, under in-plane tension T: w_k = w0_k·Dk²/(Dk²+T).
Checked against the analytic single-sinusoid case: 0.229207 numerical vs 0.229205 analytic.
D(UTG 30 µm) = 1.66e-4 N·m. Decoupled stack sum without the plate = 4.0e-4 N·m.
Visibility target (my assumption, not sourced): depth ≤ 1 µm and max slope ≤ 0.5 mrad.

- Tension needed for a 20 µm / 3 mm FWHM set: 4.1e3 N/m (UTG only) to 1.0e4 N/m (whole stack).
- Tension needed for a 50 µm / 3 mm set: 1.07e4 to 2.6e4 N/m.
- Tension needed for a sharp 50 µm / 1 mm set: 3e5 N/m or more.
- Feeding tension into the UTG through OCA (G = 90 kPa, 25 µm thick): shear lag 24 mm, τ = T/24 mm. At 600 N/m τ = 25 kPa; at 4,000 N/m τ = 168 kPa.
- OCA reference stress: a 10.5 kPa test gives 16–18 % creep in 10 min at 60 °C / 93 % RH (USPTO "Foldable display device", 11334117 / 12174665).
- Largest tension the OCA can carry at that stress: about 254 N/m. That reduces a 50 µm set to 15–23 µm, a 2–3x cut that leaves the crease visible.
- Idea 4 at 600 N/m: a 20 µm set falls to 3.4–6.1 µm with a 2.3–3.9 mrad slope. Needs 4,000 N/m or more.
- Idea 3: adjacent layers about 50 µm apart slip by π·50 µm = 157 µm at the edges of the strip. Over 25 µm of OCA or seal that is a shear strain of 6.3. Foldable OCA is quoted at more than 200–300 % (3M whitepaper; flexible-OCA patent 11492515 family).
