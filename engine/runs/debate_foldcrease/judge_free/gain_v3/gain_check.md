# Gain check for answer.md (round 3)

- All six round-3 scripts were rerun. Their output is byte-identical to the stored `.out` files.
- Hand estimates agree with the code:
  - crease slope ≈ φ·D·κ′/T ≈ 0.007 mrad;
  - seat kink ≈ 0.012 mrad;
  - gravity slope q·a/T ≈ 0.015 mrad.
- The answer's headline gain (26× nominal, 12× pessimistic) compares the model with **its own unbuilt v2 design**, using v2 tolerances it chose itself. It is not measured against any shipping phone.
- Best current practice, measured:
  - iPhone Duo (HTX): 48 µm and < 0.1° new; 167 µm and 1.24° (21.6 mrad) after 3000 folds.
  - Oppo Find N6: Oppo claims 82% less crease depth than the N5. Its under-screen height variation is about 0.05 mm.
- The answer predicts 0.19–0.6 µm and 0.02–0.12 mrad. That is a model result, conditional on two unmeasured numbers:
  - glass set φ_g ≤ 2.3e-3. PolyU 2024 reports plastic creasing in UTG, and HTX shows creases growing with cycles.
  - hinge-seat repeatability σ ≤ 0.135 µm in a phone exposed to dust and drops. Only lab couplings at 0.1–0.25 µm have been shown.
- Even inside the model, the pessimistic case is 5× over its own invisibility target.
- Costs: a 14–15 mm folded spine (Fold 7 is about 8.9 mm), 600 N of frame load, 244 MPa sustained core tension, +10–17 g, a servo and a seal.
- Conclusion: there is no demonstrated gain over current practice, only a testable hypothesis. The φ_g mandrel/strip test is the cheapest decisive test.
