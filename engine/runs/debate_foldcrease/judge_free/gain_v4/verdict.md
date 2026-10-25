# Verdict on answer.md (v4 floating tensioned display)

**Supported gain over best current practice: none demonstrated.**

- Code (`round4/float4.py`) runs and reproduces every number in answer.md. Independent scaling estimate
  theta ~ (D/T)·kappa_r' gives 0.012 mrad vs code 0.0066 (smooth ramps), so the model is internally consistent.
- Every crease number is a model output driven by assumed set fractions (polymer 0.2/0.1, phi_g 0–3e-3).
  None is measured. Crease slope grows linearly with phi_g: 0.055 mrad at 1e-2, 0.15 at 3e-2, 0.49 at 1e-1 (check.out).
  PolyU (Extreme Mech. Lett. 71, 102219, 2024) confirms ion-exchanged UTG takes permanent plastic creases, and that
  longer holds and repeated loading reduce recovery. No number shows phi_g <= 1.1e-3 at R 5.5 mm.
- The only lever is membrane tension: about 320x vs T≈0 at the same set (check.out). With the tension off, the model gives
  134 µm, in the range of real creases. Tensioned / rolled crease-free OLEDs are prior art (US 10209746; Oppo X 2021
  rollable, "no visible crease" with a "slight rumple").
- The stated gains (7–9x) are against the author's own v3, not against shipping phones. The 80–3300x vs iPhone Duo compares
  a model with a measurement, as the answer admits.
- Under-weighted risks: a bare 20 µm UTG face (no protective film) with a 3 µm DOL under 244 MPa sustained core tension.
  A sand scratch deeper than 3 µm exceeds the ~2.4 µm critical flaw. While folded, the tensile-side UTG core sees about
  517 MPa (0.5 µm critical flaw). The design also needs 600 N frame load, 6–7 mm side bezels, a 100–200 V electroadhesion
  supply and a 30 µm air gap (dust, contact under grip). The pessimistic edge-hold gap is already negative.
- What it does contribute: a coherent, testable hypothesis and a cheap decisive test (mandrel strips measuring phi_g,
  a few hundred dollars).
