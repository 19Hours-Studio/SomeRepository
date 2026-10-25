# Review of answer.md (tensioned neutral-plane glass sandwich, 15 mm curvature ramps)

Reproduction: design3.py and sag_combo.py rerun byte-identical to the shipped .out files.

What the numbers are: every crease value (0.24 um / 0.016 mrad) is the output of a linear
tensioned-beam model with assumed set fractions (phi_panel/adh = 20%/10%, phi_glass = 0). None is measured.
The headline "4x depth, 20x slope" compares the model with its own round-1 model, not with a shipping phone.

Issues
1. No calibration. The same model family applied to a shipping-like UTG/OCA stack (round1/retrofit.out)
   predicts 4-9 um untensioned. Real devices measure 48 um new and 167 um after 3,000 folds (HTX, iPhone Duo).
   The model has never been tied to a real crease, so model-vs-measurement ratios (the "700x") have no support.
2. It misses its own pass line. Crease plus face-up sag at the design T = 3000 N/m gives 0.0246 mrad,
   which is above the answer's own 0.024 mrad backstop (sag_combo.out). It passes only at T = 4000. The
   primary criterion (<= 1.2x the non-fold zone) is never computed.
3. The central unknown is open. The design passes only if glass delayed elasticity is phi_g <= 6e-4.
   At phi_g = 1e-3 it is already 0.029 mrad. The answer says this itself.
4. Tension is prior art: LG magnetic tensioning, Huawei EP4567555 / US 2024/0069604, Apple EP 4738056 A1.
   The new parts are the double-UTG sandwich and the long ramps.
5. Costs are understated:
   - folded spine of about 13-14 mm, against 8.9 mm for the Fold 7;
   - a 70 mm unsupported span, about half the width of the open screen;
   - a 1 N press dents the screen by about 120 um, so stylus use and pen drops are a problem;
   - 450 N of sustained edge load on 20 um glass;
   - shear transfer through the OLED organic layers is not modelled.
6. Best current practice for comparison: Oppo claims (not officially documented) that the Find N6 crease
   deepens by 22 um after 600k folds, against 165 um for the Fold 7. HTX measured the Duo at 48 -> 167 um.

Verdict: a coherent, testable hypothesis with a good cheap experiment (the mandrel strip test).
It shows no gain over current practice yet.
