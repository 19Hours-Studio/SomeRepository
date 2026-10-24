# Gate c1 — foldcrease screening notes

Calculations: `gate_calc.py` (output in `gate_calc.out`). Checks: the slip formula reproduces idea 1's 157 µm for d = 50 µm, and the finite-difference beam gives w/w0 = 1.000 at T = 0 and matches the analytic 1/(1+T/Tcr).

Assumed "invisible" target: residual depth ≤ 20 µm. This is an assumption. It sits below the 60 µm "good" grade and the 143 µm mean perception threshold (display off, bright room) from the SNU perceptual study.

Sources used:
- SNU crease perception study: https://www.researchgate.net/publication/372284025
- Kumoh CPI mandrel study (no residual strain at R ≳ 5 mm, residual decays with log t): https://koreascience.or.kr/article/JAKO202102455512209.pdf
- Samsung OCA patents (G' 4.5–6.5e4 Pa at 60 °C; stress relaxation 40–50 % at 60 °C; creep recovery target ≥ 90 %): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11334117
- Foldable PSA patent (residual ≤ 15 % at 600 s): https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/12473469
- Fold 7 UTG 45 µm, Fold 8 Wide 60 µm (ZDNet Korea via GSMArena): https://m.gsmarena.com/samsung_galaxy_z_fold8_wide_may_use_thicker_ultrathin_glass_than_fold8_ultra-amp-73278.php
- Oppo N6 (0.2 → 0.05 mm height variance, glass 50 % thicker, 82 % crease-depth cut per TÜV): https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/
- Fold 7 folded thickness 8.9 mm: https://news.samsung.com/uk/from-17-1-mm-to-8-9-mm-the-galaxy-z-folds-journey-to-becoming-48-thinner
- Apple ~1/4 crease depth: https://appleinsider.com/articles/26/02/25/iphone-fold-hinge-crease-will-be-about-14-the-depth-of-the-galaxy-fold-7

Key kinematic point for ideas 1 and 3: take two layers of equal flat length, bonded beyond a band, and bend them 180° about their own midplanes. Their arc lengths then differ by πd. The mismatch has to go somewhere: into adhesive slip at the band edges (idea 1), or into a buckle, a gap change or membrane strain (idea 3).
