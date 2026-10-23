# H1 throw simulation (MuJoCo 3.16), 2026-10-23

Scripts: `throw.py` (simulator), `summarise.py` (-> `results/summary.txt`), `bias_check.py` (-> `results/bias_check.txt`,
`results/wear_prediction.json`). Raw per-throw files `results/*.json` are not committed (large; rerun with
`python throw.py run <body> <surface> <protocol> <n>`). Other files in this folder were left unfinished by a stopped
agent and are not used.

## Set-up
- Body: the museum scan itself (Kleiner Feldberg FMb 2103; Hunt HCM 157). Contact uses the convex hull (on a flat
  surface only knob tips touch). Mass, centre of mass and inertia come from the scan's closed hollow shell (genus 11,
  real inner surface) at uniform density; which face lands up does not depend on the density value.
- Surfaces (ASSUMED contact parameters, not measured values): wood e = 0.48, board e = 0.62, cloth e = 0.00,
  earth e = 0.08 (restitution measured by `throw.py drop`); friction 0.3-0.8.
- Protocols: hand toss (10-30 cm above the surface, 0.3-1.5 m/s, spin 5-25 rad/s), cup (more spin), drop.
- Dice towers were not simulated: the known Roman towers (stair plates about 70 x 45 mm, Cobbett 2020) are too small
  for a 40-100 mm knobbed shell (tests/h1_practice/RESULT.md, step 4).

## Validation (same code and protocol)
| body | surface | n | faces up | chi2 p |
|---|---|---|---|---|
| fair cube | wood | 1200 | 186-211 per face (expected 200) | 0.87 |
| fair cube | cloth | 1200 | 185-213 | 0.80 |
| regular dodecahedron | wood | 1200 | 81-111 per face (expected 100) | 0.72 |
Time step halved (0.25 ms) on the Kleiner Feldberg piece: same favoured and disfavoured faces (pole share 0.105 vs 0.120).

## Results
| piece | surface / protocol | n | least / most frequent face up | chi2 p | pole pair up (fair 0.167) | top-face tilt at rest, median (p95) |
|---|---|---|---|---|---|---|
| Kleiner Feldberg | cloth toss | 2400 | 0.045 / 0.159 | < 0.001 | 0.117 | 1.6 deg (3.4) |
| Kleiner Feldberg | wood toss | 2400 | 0.047 / 0.145 | < 0.001 | 0.120 | 1.6 (3.4) |
| Kleiner Feldberg | earth toss | 2400 | 0.044 / 0.143 | < 0.001 | 0.110 | 1.6 (3.4) |
| Kleiner Feldberg | board toss | 1200 | 0.048 / 0.154 | < 0.001 | 0.113 | 1.4 (3.4) |
| Kleiner Feldberg | cloth, cup | 1200 | 0.031 / 0.147 | < 0.001 | 0.110 | 1.6 (3.4) |
| Hunt | cloth toss | 2400 | 0.060 / 0.121 | < 0.001 | 0.142 | 2.0 (4.2) |
| Hunt | wood toss | 2400 | 0.058 / 0.107 | < 0.001 | 0.148 | 1.9 (4.2) |
| Hunt | earth toss | 2400 | 0.061 / 0.122 | < 0.001 | 0.151 | 1.9 (4.2) |
| Hunt | cloth drop | 1200 | 0.063 / 0.111 | < 0.001 | 0.166 | 2.0 (4.2) |

1. **Both pieces are loaded dice.** The bias follows the centre of mass: on the Kleiner Feldberg piece it lies 1.9 mm
   off centre toward the face with the smallest hole (11.4 mm), and the chance of a face coming to rest DOWN rises with
   the centre-of-mass offset toward it (Spearman 0.82, p = 0.001; Hunt: offset 0.4 mm, Spearman 0.75, p = 0.005). Small
   holes leave more metal, so they act as weights. The faces are fixed by geometry, so the bias is the same on every
   surface and protocol.
2. **The unringed pole faces come up less than a fair share** (0.11-0.12 and 0.14-0.15 instead of 0.167): the two
   largest holes make the lightest faces.
3. **Behaviour:** it always comes to rest with one face clearly uppermost, but on 3-4 knobs, not 5: knob heights differ
   by +-0.5 mm (sd of tip distance from the centre), so the top face is tilted 1.6-2 deg (6-21% of throws more than 3 deg).
   On cloth it stops after a median of 1.5-1.7 s and travels 30 cm (p90 55-60 cm); on wood 48 cm (p90 1 m).
4. **Predicted wear map (H1):** every one of the 20 knobs is struck, but unevenly. The share of the summed contact impulse
   per knob is 2.8-8.5% (Kleiner Feldberg) and 2.8-6.5% (Hunt), against 5% if even. The ranking of the knobs is the same
   on cloth, wood and earth (Spearman 0.97), so each piece has a specific predicted order of knob wear
   (`results/wear_prediction.json`). The scans show no flattened tips (FACT 50), but they cannot see light polish.
5. **Reading variants:** the uppermost face is always unambiguous (tilt far below the 31.7 deg that separates faces);
   the bottom face is its opposite, so reading top or bottom gives the same information. On sight-through: with the
   piece at rest, the top and bottom holes are coaxial, so the smaller of the two bounds what is seen of the surface
   below; this adds no outcome that the top hole does not already give.

## What it means
- For H1: a thrown piece always gives a clear face, so a lot is physically possible on any surface.
- Against H1: the outcomes are strongly unequal (on Kleiner Feldberg one face comes up 3.5 times as often as another).
  A diviner would notice that within a few dozen throws. Hole sizes, the only face code, are also what loads the die.
  Together with FACT 46-49 (no size classes, at most 6-8 visually distinct faces) the "twelve readable outcomes" is not
  supported by the two measured pieces.
- Not decided here: whether the pieces were ever thrown. That needs the knob-tip microscopy, now with a
  piece-specific predicted order of wear to check against.
