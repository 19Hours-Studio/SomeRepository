# Critic review: glass-dominated elastic stack (vs_foldcrease_b/baseline)
Files: oca_coupled.py/.out (OCA-set coupled beam), oca_coupled2.py/.out (tension, cold, gel), checks.out.
Main finding: the author's model gives OCA set phi = 0 and treats the layers as fully decoupled.
With a 104 um glass-to-backplate offset the stack is ~10x stiffer when bonded than when decoupled
(lock fraction 0.9), so a small OCA set fixes a residual curvature in place.
Idea 1 residual depth: 0.3-1.7 um (author) -> 4-114 um (G=1e4-1e5 Pa, phi=2-10%, no tension)
                     -> 0.7-21 um with 1000 N/m tension (Idea 2). Meets the <=2 um target only if G~1e4 Pa and phi<=~6%.
Cold folding (G~1e6 Pa): extra axial stress on the Ti foil is ~680 MPa, so the total is ~1180 MPa, above beta-Ti yield. That gives a permanent plastic crease.
Tension cam: stroke 7.6-15 um, but Al-frame thermal mismatch over 35 K is ~71 um. A constant-force spring is needed.
Lever: a very-low-modulus (gel/liquid) optical coupling layer in the fold zone. G=100 Pa gives 1.3 um even at phi=0.5.
