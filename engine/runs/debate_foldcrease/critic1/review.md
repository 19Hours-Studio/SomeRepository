# Critic 1 review of round-1 answer (neutral-plane glass sandwich + tension spring)

Files: check.py/.out (independent checks, imports author's sandwich.py unchanged), panel30.py/.out.

## 1. Re-derived numbers
| Claim | Status |
|---|---|
| sandwich.out (strains, D-shares 49.77/0.30/0.08 %, 490/306 MPa, teardrop 50.9 deg / 38.8 mm, shear-lag 61 um, 0.97 MPa, spring <=211/762 N/mm) | re-run, identical |
| glass_flaw.out | re-run, identical |
| retrofit.out (3.9-8.5 um untensioned, 0.5-1.1 um @1000 N/m, panel axial 0.46-0.93 %, 1.21 % stiff OCA) | re-run, identical; stored file only lacks the final G=1e6 T=1000 row (0 um, 1.21 %) |
| table.py sandwich rows 0.10-0.42 um / 0.04-0.16 mrad @1000 N/m; 1.09 um / 0.43 mrad pessimistic | reproduced numerically and by closed form w = (sum phi_i D_i)(1/R+1/Rn)/T, theta = eff*dk*sqrt(D/T)/2 (within 5-10 %) |
| table.py round-0 rows | re-run stopped at its time limit (slow lstsq); same function's stored output critic0/oca_coupled2.out gives 0.67-20.9 um @1000 N/m |
| 66 um equivalent glass, 1.33 mm tension length, 2.3 g glass | hold |
| 150-1600x vs HTX 167 um | holds (153-1670x) |
| "4-40x below new Duo slope 1.75 mrad" | arithmetic holds; 1.75 mrad has no source (HTX reports only 1.24 deg aged) |

## 2. Unfair / unsupported points
1. Panel 22 um incl. CPI+TFT+TFE+CF+touch: optimistic. At 30 um (R raised to 5.58 mm to keep 490 MPa): 0.21-0.89 um / 0.07-0.30 mrad (x2.1 depth, x1.8 slope); at 40 um: 1.77 um / 0.51 mrad for phi 0.2/0.1, which fails the answer's own <=1 um / <=0.2 mrad targets.
2. Slope target inconsistent with its own vernier argument: 0.2 mrad -> 83 arcsec reflected deviation; vernier 5-10 arcsec needs <=0.024 mrad. Realistic rows (0.04-0.16 mrad = 17-66 arcsec) are not "invisible" by the answer's logic.
3. Glass anelasticity set to 0: phi_g 1e-3 -> 0.97 um / 0.38 mrad at T=1000 (phi 0.2/0.1), 29 um untensioned. Sign-off needs the bare-UTG control (already in the strip test).
4. Flaw check ignores central tension: 20 um sheets with CS 450-800 have CT 217-400 MPa, so bottom-glass interior/edge tension is 476-818 MPa over the whole sheet vs 582-680 MPa on half of a 30 um UTG at R 1.5. "No worse than current glass" is not shown; edges are the concern.
5. Backstop 10-20 um below glass at rest: best shipping hinge flatness is 50 um (Oppo N6). Any rest contact pushes a bump; glass lands on the backstop at 0.01-0.07 N anyway, so a 50-100 um gap costs nothing.
6. Pessimistic case (1.09 um / 0.43 mrad) and every untensioned case (0.29-1.22 mrad) fail the answer's own backstops; the text doesn't say so. Spring failure = visible crease.

## 3. Undersold
- Step-curvature teardrop is pessimistic for slope: 5/10 mm curvature ramps -> 0.074/0.042 mrad (vs 0.164), depth almost unchanged.
- Like-for-like comparison with old design is 7-50x (low/low 6.7x, high/high 50x), not 7-19x.
- HTX's 48->167 um happened in only 3000 folds: the 2000-cycle regime is where shipping set appears, which supports the time-held-not-cycles argument.
- Tension while open also drives polymer recovery.
- Tensioned residual is independent of glass D: w ~ sum(phi_i D_i polymer)*dk/T.

## 4. Largest honest gain
The crease scales as panel D x (1/R+1/Rn) / T. Levers: thinnest panel at the neutral plane (t^3), clothoid hinge (about 4x on slope), larger Rn, T up to ~2000 N/m (48 MPa glass, 300 N hinge load). Visibility metric: use deflectometric slope <=0.024-0.07 mrad.
