# Critic round 3 – review of v3 (tensioned glass sandwich, kinematic seat, servo gas cushion)
Files: check4.py / check4.out (independent checks), rerun_out/*.rerun (author scripts re-run, identical to round3/*.out).

## Holds
- All six author scripts reproduce byte-for-byte.
- Crease: analytic eff·D·max|κ'|/T = 0.0077 / 0.0134 / 0.0248 mrad vs solver 0.0074 / 0.0128 / 0.0237 (φ_g 0/1e-3/3e-3); depth 0.19/0.33/0.62 µm. l = 0.77 mm, Rn 16.7 mm.
- Seat kink (δ/2+Δh/2a, 3σ = 0.3 µm, 30 mm lever) 0.0122 mrad; bow 0.0029; thermal bow AlSiC 0.0002 / Ti 0.0049; limits φ_g ≤ 2.8e-3, σ ≤ 0.135 µm, e ≤ 0.125 mm.
- Strip test: tension length 57 mm for bare 20 µm UTG hung lengthwise is right (D = 4.8e-5 N·m); signal survives.
- Sources: HTX 48→167 µm/1.24° (secondhand, iThinkDiff), Oppo 0.2→0.05 mm, 82% vs predecessor, 600k folds (TÜV), PolyU EML 71 102219 abstract – all match.

## Missing / unsupported (effect on worst feature, nominal)
1. Bond-eccentricity moment at clamp lines (new): tension enters through the bottom face, 38 µm off mid-plane -> M = T·c.
   FD beam-on-foundation model: static kink 0.82–0.87 mrad (≈36× target) for any bond 3–100 µm; change for ΔF = 2.5% = 0.018–0.021 mrad.
   Lamination "under 600 N" cannot absorb the static part unless the load path is identical during cure (it cannot be, adhesive uncured) -> needs a pre-shaped reference or mid-plane load path. Variable part: 0.0197 -> 0.040 mrad.
2. Servo reference: capacitor reads glass-to-bridge gap; the bridge is redeployed every fold. 1 nm = 0.0073 Pa. 100 nm -> 0.73 Pa -> +0.0064 mrad; 300 nm (≈20 K × 8 ppm/K × 2 mm) -> worst 0.040 mrad, same as passive. The 0.05 Pa residual (7 nm) is unsupported.
3. Gravity torque on the hinge: half held, other half cantilevered, 0.047 N·m. Kink ≤ 0.012 mrad needs k_θ ≥ 2000 N·m/rad; two 5×4 mm AlSiC tongues give ~1070. No preload moment is specified for the one-sided tongue stop (needs ≥0.047 N·m; e.g. e ≈ 0.08 mm of the 600 N).
   Sum 1–3: nominal 0.0197 -> 0.047–0.058 mrad (1.9–2.4× over target).
4. Threshold: 0.024 mrad = 10″ reflected; optimal vernier acuity is 3–5″ -> 0.007–0.012 mrad. Nominal fails ×1.6–2.7 even before items 1–3.
5. 26×/12× is against self-assigned v2 tolerances; not a measured or claimed v2 spec.
6. Touch: sealed 5 µm film – 0.05 N press displaces ~9% of gas volume, so the "lands on skin at 0.054 N / 5–8 µm pre-travel" analysis ignores the gas; press is stiffer (undersold) but makes the rest of the zone bulge while pressed.

## Larger honest gain
Mid-plane or edge-clamp load introduction + calibrated pre-shaped laminating reference; ΔF ≤ 0.5%; differential (shape) capacitive sensing so bridge height drops out; k_θ ≥ 1e4 N·m/rad joint; R = 7 mm. With these: 0.029 mrad (k_θ 2000) to ~0.020 (k_θ 1e4) – near the 10″ target, not the 5″ one.
Cheapest decisive test: tensioned-strip rig with bonded wings, measure clamp-line kink by deflectometry vs T (0, 2000, 4000 N/m) – checks the 0.87 mrad term directly – alongside the edge-on glass-set strips.
