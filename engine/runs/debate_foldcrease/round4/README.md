Round 4 files (self-contained: sandwich.py, design2.py, design3.py, lever3.py copied unchanged from round3)
- float4.py / float4.out : floating tensioned display (no bond under the active area; two-face edge clamps under the
  side bezels; 30 um grooved, slow-vented air gap over the backing).
  A crease on the clamp-to-clamp span (R 5.5/6/7 mm, ramps, T 4000/5000, phi_g 0-3e-3, nominal and pessimistic polymer set)
  B how each v3 clamp-line term (bond moment, seat kink, bow, thermal bow, hinge gravity torque, servo reference) maps:
    shape effect 0, only consumes gap
  C edge-clamp tail into the active area (critic's FD bond model, two-face jaws with shear asymmetry 5-20%, slope vs chord)
  D gap budget by holding case, slow-vent cushion residual, touch landing force, squeeze film, lift-off time, drum mode,
    stylus stress
  E folded-state retention by electroadhesion: edge shear V = D kappa', lift-off length 2V/p
  F vernier thresholds (3/5/10 arcsec) and the comparison table
  G Poisson-free clamp requirement, frame load, cam work, glass stress
  H like-for-like ratios vs v3 as re-budgeted by the critic, tolerable phi_g per geometry
Assumed (not measured): every phi, wing flatness 2 um, seam step 3 um, open-body EI 5-10 N m^2, hinge k_theta 300-1000
N m/rad, clamp shear asymmetry 5-20%, electroadhesive hold 2-20 kPa.
