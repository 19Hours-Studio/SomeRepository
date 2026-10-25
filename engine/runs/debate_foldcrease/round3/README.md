Round 3 files (self-contained: sandwich.py from round1, design2.py/design3.py from round2 copied unchanged)
- lever3.py      : unequal-ramp / bulb-radius / tension scan (material-set crease only).
- ramp_grid.py   : balanced-ramp grid (sane branches Rn>R only); picks 25/9 mm at R=5.5 (zone 71 mm, bulb 12.5 mm).
- budget3.py/.out: full open-state slope budget, same code for round-2 and round-3 hardware: crease + uniform pressure
                   (gravity, gas thermal/barometric; vented / passive sealed / servo modes) + clamp-line kinks
                   (seat repeatability, load-path eccentricity bow, through-thickness thermal bow, lamination residual).
                   Clamp feature = K + |span slope 3l inside clamp|; interior = max |crease+pressure| away from clamps.
- phig_limit.py/.out, seat_limit.py/.out: tolerable glass set, seat repeatability, load-path eccentricity.
- checks3.py/.out: glass stress/flaws at T=4000, spring, finger/backstop, particle embedding, servo stroke/leak,
                   Hertz at seat, strip-test signal (hang the strip vertically or edge-on: bare UTG self-sag 1 mm otherwise).
Assumed (not measured): every phi, seat sigma (0.1 um nominal from Schouten 1997 at 1.5 kN; 0.5 um pessimistic),
EI of a phone half (5-10 N m^2), heat flux 100-300 W/m^2 in hinge housing, servo residual 0.05-0.6 Pa,
round-2 hardware tolerances (2-5 um on a 4 mm detent lever, Al frame +-20% tension, e 1-2 mm, vented 1-10 Pa).
