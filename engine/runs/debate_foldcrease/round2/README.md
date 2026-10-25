Round 2 files (imports ../round1/sandwich.py for the stack function)
- design2.py/.out : panel 22/30/40 um, step teardrop R5 Rn8/12, T 0-3000 N/m, glass anelastic set phi_g; first ramp attempt (solver fails >5 mm ramps).
- design3.py/.out : geometry re-solved with free neck curvature so long curvature ramps still close the fold; baseline 30 um panel, R5.5;
                    ramps 0/5/10/15 mm (20/20 row is a spurious solver branch - ignore), T 0-3000, phi_g 0-3e-3.
- checks2.py/.out : edge stress incl. central tension, flaw thresholds, finger/backstop, gravity sag, spring sizing,
                    phi_g budget, reference display-glass waviness slopes. (Stroke column prints 0: true value T/EA*70 mm = 23/46/69 um.)
- sag_combo.py/.out: crease + face-up gravity sag superposed, worst-case sign.
