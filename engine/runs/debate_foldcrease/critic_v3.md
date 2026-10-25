The author's numbers reproduce, but the main claim, that the nominal design meets the 0.024 mrad target with 18% margin, does not survive. The budget leaves out three terms. Adding them puts the nominal design at about 0.047–0.058 mrad, which is 1.9–2.4× over the target. The target itself is also about 2–3× looser than the best human eye can manage.

## 1. Re-run and re-derived numbers

All six scripts (`lever3`, `ramp_grid`, `budget3`, `phig_limit`, `seat_limit`, `checks3`) re-run and match their stored outputs exactly (`critic3/rerun_out/`). My own checks are in `critic3/check4.py` and `check4.out`.

| Claim | My check | Holds? |
|---|---|---|
| Crease 0.0074 / 0.0128 / 0.0237 mrad and depth 0.19 / 0.33 / 0.60 µm at φ_g = 0 / 1e-3 / 3e-3 | The simple formula (ΣφD·max\|κ′\|/T) gives 0.0077 / 0.0134 / 0.0248 mrad and 0.19 / 0.33 / 0.62 µm. Tension length 0.77 mm, Rn 16.7 mm. | ✓ |
| Seat kink 0.0122, bow 0.0029, thermal bow 0.0002 (AlSiC) / 0.0049 (Ti) mrad | Same | ✓ |
| Limits: φ_g ≤ 2.8e-3, seat σ ≤ 0.135 µm, eccentricity e ≤ 0.125 mm | Same | ✓ |
| Hanging strips: tension length 57 mm, longer than the 30 mm tail | Correct. Bare UTG has D = 4.8e-5 N·m, and about 46 mm curls freely. My first doubt here was an arithmetic slip on my side. | ✓ |
| Servo gearing: 1 nm = 0.0073 Pa; Hertz contact peak 2.6 GPa; opening work 65 mJ; core tension 244 MPa | Same | ✓ |
| HTX 48→167 µm and 1.24°; Oppo flatness 0.2→0.05 mm, 82% shallower than its predecessor, TÜV 600k folds; PolyU abstract | All match the sources. HTX is secondhand only. Engadget says the N6 crease is "still visible". | ✓ |

## 2. Unfair or unsupported points

1. **Tension enters the glass off-centre (new and largest).** The 600 N reaches the sandwich through its bottom face, 38 µm below the glass mid-plane. That puts a bending moment of T·c into the glass at each clamp line.
   - I modelled it as a beam resting on its adhesive bond (grid-converged and linear in the offset). The permanent kink is 0.82–0.87 mrad for any bond from 3 to 100 µm thick. That is about 36× the target.
   - "Lamination under 600 N" cannot cancel it. While the adhesive cures, the load has to come in some other way, so the load path changes when the fixture is released.
   - Even if that permanent part is compensated, a 2.5% change in tension (ΔF) still moves the kink by 0.018–0.021 mrad.
   - Effect on the nominal case: **0.0197 → 0.040 mrad.**
2. **The servo's 0.05 Pa residual has no basis.** The capacitor measures the gap between the glass and the bridge, but the bridge is redeployed on every fold. Any error in the bridge's height relative to the wings becomes an equivalent pressure.
   - A 100 nm error is 0.73 Pa and adds 0.0064 mrad.
   - A 300 nm error is 2.2 Pa and brings the worst feature to 0.040 mrad, no better than the passive seal. 300 nm is what 20 K of temperature change does to a 2 mm AlSiC support.
   - The gravity sag the servo is cancelling is only 0.20 µm, so the bridge would have to repeat to about 7 nm.
3. **Gravity torque on the hinge is not in the budget.** When the phone is held by one half, the other half hangs off the hinge with a torque of 0.047 N·m.
   - Keeping the resulting kink at or below 0.012 mrad needs a joint stiffness of at least 2000 N·m/rad. Two 5×4 mm AlSiC tongues give about 1070.
   - The tongue only stops motion in one direction, and no preload holds it on its pad. Holding it would take about 0.08 mm of deliberate offset in the 600 N load path.
   - Adding items 1 to 3 together: **nominal 0.0197 → 0.047–0.058 mrad.**
4. **The target is not conservative.** 0.024 mrad is 10″ of reflected deviation. Under good viewing conditions people can detect vernier offsets of 3–5″, which corresponds to 0.007–0.012 mrad. Against that, even the author's own nominal 0.0197 fails by 1.6–2.7×.
5. **The 26× and 12× gains are against a baseline the author built.** The "v2 hardware" tolerances are the author's assumptions, not a v2 specification. The meaningful comparison is with the target, not with the earlier version.
6. **The touch analysis ignores the sealed gas.** A 0.05 N press would push out about 9% of the gas volume. So "lands on the skin at 0.054 N after 5–8 µm of pre-travel" is not physical.
   - This **undersells** how solid a press feels: it is stiffer than claimed.
   - It also leaves out that the rest of the fold zone bulges while the finger presses.

**Where the answer undersells itself:** the press stiffness (point 6), and the strip test, which works as written (57 mm is correct). Its sourcing and its comparison with Apple, Samsung and Oppo are fair.

## 3. Where a larger honest gain is most likely

- **Remove the off-centre load:** introduce the tension at the glass mid-plane, or calibrate a laminating reference with the inverse kink built in. Then hold tension variation to 0.5% or less.
- **Make the servo measure shape, not mean gap:** compare the gap at the centre with the gap near the clamps. Bridge height then drops out.
- **Stiffen the hinge joint:** at least 1e4 N·m/rad, with a defined preload moment.
- **Use R = 7 mm.**

With these I get about 0.029 mrad at 2000 N·m/rad and about 0.020 mrad at 1e4 N·m/rad. That is near the 10″ target, but not a 5″ one.

**Cheapest decisive experiment:** the author's tensioned-strip rig, with real bonded wings, measuring the clamp-line kink by deflectometry at T = 0, 2000 and 4000 N/m. This tests the 0.87 mrad term directly. Run it alongside the edge-on glass-set strips.

One housekeeping note: one of my check runs left a bytecode cache in `round3/`. I deleted it, and the author's files are unchanged.

Sources:
- [PolyU – plastic deformation and recovery in UTG](https://research.polyu.edu.hk/en/publications/plastic-deformation-and-recovery-in-ultrathin-aluminosilicate-gla/)
- [Vernier acuity 2–5″ (Wolfe, Sensation & Perception essay)](https://learninglink.oup.com/public/files/cdn/wolfe4e/essay03.01.html)
- [Mukamel KITP lecture](https://online.itp.ucsb.edu/online/neuro10/mukamel/pdf/Mukamel_Neuroscience_KITP.pdf)
- [Mobile World Live – Oppo Find N6](https://www.mobileworldlive.com/oppo/oppo-irons-out-foldable-crease-with-find-n6/)
- [Engadget – Find N6](https://engadget.com/mobile/smartphones/oppos-find-n6-might-be-the-foldable-of-your-dreams-131036055.html)
- [iThinkDiff – HTX Duo test](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)

HONEST GAIN: worst visible feature ≈ 0.047–0.058 mrad at nominal tolerances (≈10× below the author's own v2-hardware 0.51 mrad, not 26×), which is still 1.9–2.4× over the 0.024 mrad target, and only if the 0.87 mrad static bond-moment kink is fully compensated; invisibility is not shown.