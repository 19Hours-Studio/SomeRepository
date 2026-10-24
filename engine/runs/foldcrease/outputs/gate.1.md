=== GATE ===
IDEA 1: Gel-slip decoupled glass stack
KILLER | Locked-in interlayer slip at the edges of the gel band. The layers are still bonded outside the band, so the full 157 µm slip (π × 50 µm, exact arithmetic) has to be carried by the OCA just beyond each band edge: about 630% shear spread over a ~12 mm shear-lag length. The gel does not stop the adhesive from creeping; it moves the creep to the band edges. For ≤20 µm depth over a 4.7 mm band, residual slip must stay ≤1.7 µm, i.e. ≤1.1% of the slip | required ≤1.1 % residual slip | available ≥10 % (foldable-OCA creep-recovery target of ≥90%, Samsung US 11334117; ≤15% residual at 600 s, US 12473469) | MARGIN 0.11
CHAIN | Bonded UTG/CPI/OCA stack plus laser-drilled plate (Apple/Samsung reported) or Oppo N6 liquid-printed under-layer | now ~50 µm residual unevenness (Oppo, 0.05 mm height variance) | with idea ~50 µm, split into two creases at the band edges with the same OCA set; a fluid layer also gives up the elastic UTG's restoring coupling | RATIO 1.0
VERDICT | DEAD | Bending kinematics put the slip back into adhesive at the band edges, so the crease moves instead of disappearing, and the residual-slip budget fails by about 10x.
NEW FACT | Foldable OCAs show 40–50% stress relaxation at 60 °C, with G′ of 4.5–6.5×10⁴ Pa at 60 °C | https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11334117

IDEA 2: Sub-creep strain budget fold
KILLER | Peak strain in the bend zone compared with the strain at which polyimide shows no residual strain. A 60 µm bonded stack at R = 5 mm gives t/2R = 0.60%, not the claimed 0.3–0.5%. CPI wrapped on mandrels keeps no residual strain only at R ≳ 5 mm, which is ≈0.5% if the test film was ~50 µm (film thickness not confirmed; test probably at room temperature, not 60 °C) | required ≤0.50 % | available 0.60 % design strain, measured threshold ≈0.5 % (Kumoh CPI study, koreascience JAKO202102455512209) | MARGIN 0.83
CHAIN | Fold 7 / Apple-reported / Oppo N6 small-radius fold with a support plate | now ~50 µm unevenness at 8.9 mm folded thickness (Samsung) | with idea ≥20 µm (speculative: the idea's own 0.05% residual-strain spec allows a 514 µm free-film sag, so it needs ≤0.32%-of-strain residual plus plate flattening), and the spine is ≥11.7 mm (2R + panel + walls), not 10 mm | RATIO 2.5 (upper bound on depth gain; thickness gets worse by 0.76x)
VERDICT | WOUNDED | It is close to the measured no-set radius for CPI, but the stated stack is 20% over that strain, any adhesive in it never stops creeping, and the hinge geometry cannot reach the claimed 10 mm.
NEW FACT | The Kumoh study found that CPI keeps no residual bending strain at a critical radius of about 5 mm, and that residual strain falls roughly with log(time) | https://koreascience.or.kr/article/JAKO202102455512209.pdf
NEW FACT | The Fold 7 inner UTG is 45 µm; the Fold 8 Wide is reported at 60 µm | https://m.gsmarena.com/samsung_galaxy_z_fold8_wide_may_use_thicker_ultrathin_glass_than_fold8_ultra-amp-73278.php

IDEA 3: Unbonded sliding bend-zone laminate
KILLER | Fluid volume needed to keep the gap uniform when folded. The layers are bonded outside the 15 mm zone, so the glass and the OLED (d ≈ 30 µm) differ in arc length by π·d = 94 µm, which is 1.5% membrane strain. If that mismatch is not taken up as strain, the inner layer buckles by ~0.49 mm and needs ~1.96 mm² of fluid per mm of width. The sealed 5 µm × 15 mm film holds 0.075 mm²/mm. The ±0.5 µm gap target also fails within 0.35 s under a 1 N stylus (squeeze film with 1 Pa·s fluid) | required 1.96 mm²/mm | available 0.075 mm²/mm (exact arithmetic from the idea's own dimensions; gate_calc.py) | MARGIN 0.04
CHAIN | Bonded stack with laser-drilled plate (Apple/Samsung reported) or Oppo N6 | now ~50 µm unevenness | with idea: cavitation or buckle under the glass when folded, and the slip goes back into adhesive at the zone boundary (the same mechanism as idea 1) | RATIO 1.0 (at best)
VERDICT | DEAD | Layers of equal length bonded at both ends cannot stay concentric through a 180° fold, so the ±0.5 µm gap criterion fails by more than 25x.
NEW FACT | In a perceptual study (25 participants, 17 prototypes), crease depth below 60 µm was graded "good". The mean perceived height was 143 µm (bright room, display off) and 185.5 µm (outdoors) | https://www.researchgate.net/publication/372284025

IDEA 4: Large-radius tensioning teardrop hinge
KILLER | Panel tension left after OCA stress relaxation, compared with the tension needed to flatten the crease 5x (50 µm → ≤10 µm). The beam-column model was checked by finite differences, which match the analytic result and give w/w₀ = 1 at T = 0. The stack bending stiffness is D = 6.6×10⁻⁴ N·m (45 µm UTG). At 0.1% strain the tension is 3,550 N/m. Assuming a 50% loss from the measured 40–50% OCA relaxation at 60 °C, ~1,775 N/m remains. A sharp crease profile (L = 4 mm) needs 1,625 N/m; at L = πR = 9.4 mm it needs only 294 N/m (margin 6). Risk: the OCA must carry a sustained ~89 kPa peak shear, above its G′ of 45–65 kPa | required 1,625 N/m | available ~1,775 N/m (Samsung OCA patent relaxation; ZDNet/GSMArena 45 µm UTG; elastic theory, needs a prototype) | MARGIN 1.09
CHAIN | Oppo N6 (titanium hinge plus liquid-printed fill) or Apple/Samsung laser-drilled plate | now ~50 µm unevenness (Oppo 0.05 mm variance; no profilometry published) | with idea ~9 µm (L = 4 mm) to ~2 µm (L = 9.4 mm) while open under tension, at +1.5 mm folded thickness and a ~536 N continuous preload along the 151 mm fold line | RATIO 5.4
VERDICT | ALIVE | This is the only idea whose mechanism gets stronger rather than weaker with residual creep, but the margin is thin and theoretical: the phone must be flat only while under tension, the crease must not be sharper than ~4 mm, and the OCA must not keep relaxing beyond 50%. The cheapest test is a 45 µm UTG/CPI/OCA strip folded 8 h at R = 3 mm and 60 °C, then profiled flat at 0 and at 0.1% tension, re-measured after a 24 h held-open dwell.
NEW FACT | The Oppo N6 "Auto-Smoothing Flex Glass" is 50% thicker than conventional UTG. TÜV testing showed up to 82% less long-term crease depth than the N5 (a relative figure only, no µm value) | https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/
NEW FACT | Reports say the Apple crease will be about ¼ the depth of the Fold 7's, achieved with a laser-drilled metal plate (mechanical), not a coating | https://appleinsider.com/articles/26/02/25/iphone-fold-hinge-crease-will-be-about-14-the-depth-of-the-galaxy-fold-7

Notes:
- **Baseline:** No public profilometry exists for any of these phones. The "now ~50 µm" baseline is Oppo's hinge height-variance figure, not a measured crease depth.
- **Target:** The ≤20 µm "invisible" target is my own assumption, set below the perception study's 60 µm grade and 143 µm mean threshold.
- **Cycle counts:** None of the ideas has been tested at 2,000 or 200,000 cycles. For ideas 1 and 3 the failure is geometric and shows up on the first fold. For idea 4, the open question is whether the OCA keeps its tension, which a dwell test can measure before any cycle test.
- **Cost:** No idea moves cost in a way the ledger can show. I judged the CHAIN ratio on crease depth, since that is the gain the question asks for.

Files are in `/home/user/SomeRepository/engine/runs/foldcrease/gate/c1/`: `gate_calc.py`, `gate_calc.out` and `gate_notes.md`. Nothing was committed.

Sources:
- [SNU crease visibility study](https://www.researchgate.net/publication/372284025_Effects_of_crease_features_on_crease_visibility_and_goodness_of_smartphone_foldable_display)
- [Kumoh CPI residual strain](https://koreascience.or.kr/article/JAKO202102455512209.pdf)
- [Samsung OCA patent US 11334117](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11334117)
- [Foldable adhesive patent US 12473469](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12473469)
- [GSMArena: Fold 8 Wide UTG](https://m.gsmarena.com/samsung_galaxy_z_fold8_wide_may_use_thicker_ultrathin_glass_than_fold8_ultra-amp-73278.php)
- [Oppo N6 newsroom](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/)
- [Samsung: Fold 7 8.9 mm](https://news.samsung.com/uk/from-17-1-mm-to-8-9-mm-the-galaxy-z-folds-journey-to-becoming-48-thinner)
- [AppleInsider: iPhone Fold crease](https://appleinsider.com/articles/26/02/25/iphone-fold-hinge-crease-will-be-about-14-the-depth-of-the-galaxy-fold-7)