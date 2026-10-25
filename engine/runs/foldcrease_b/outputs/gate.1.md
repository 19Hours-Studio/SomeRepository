=== GATE ===
IDEA 1: Tensioned membrane open state
KILLER | Peak shear the OCA must hold for as long as the phone stays open, at 60 °C, to carry the tension that pulls the crease down to ≤1 µm | required ≈63 kPa. My model treats the stack as separate layers held together by a soft adhesive (UTG 30 µm, two PET films of 50 µm, panel 30 µm, bending stiffness D = 2.8e-4 N·m). It is checked against a known case: with no tension it returns the input crease unchanged. The starting crease is the HTX-measured 167 µm (Gaussian width σ = 4.7 mm, from HTX's 167 µm depth and 1.24° slope). Flattening that to 1 µm needs T ≈ 3.0 kN/m, or 0.11 % strain. The tension passes into the panel through the OCA over a shear-lag length of about 48 mm, giving the 63 kPa peak. | available ≈10.5 kPa. That is the stress a foldable-OCA patent tests at 60 °C/93 % RH, where the adhesive already creeps 10–30 % in 10 minutes, with a modulus of 0.02–0.045 MPa (USPTO 11348487 family). At 63 kPa the shear strain is about 200 % and keeps creeping, so the tension relaxes or the bond slips. | MARGIN 0.17
CHAIN | iPhone Duo-class stack (best measured shipping result) | now 167 µm after 3000 folds (HTX) | with idea about 6 µm, if the tension relaxes to the ~500 N/m the OCA can hold; this is a model only and needs a prototype | RATIO ~28 (model)
VERDICT | DEAD | As written (≤1 µm), the bond has to hold about 6x the shear at which foldable OCAs already creep. The same model says ~120 N/m (0.004 % strain, 2.5 kPa peak shear) would reach the 20 µm target with about 4x margin, so the cheapest test is to tension a coupon of the stack after folding. Note that if the layers bond tightly (cold, about −20 °C) the stiffness rises about 40x and the margin goes away.
NEW FACT | The HTX lab measured the iPhone Duo crease at about 48 µm peak-to-valley new and about 167 µm after 3,000 folds, with a 1.24° slope. An older phone in the same test showed 350 µm, and one unnamed rival did better than the Duo. Hands-on reports still see a crease under some lighting. | ithinkdiff (HTX test), Notebookcheck

IDEA 2: Gel-slip decoupled glass stack
KILLER | Bending strain in the solid polymer layers that still bend at the phone's small radius (cover PET or CPI, back film); the gel does not change this | required ≤0.5 %, the creep-safe limit at 60 °C. This value is assumed (Idea 3 uses the same figure), not sourced. | available 1.67 % for a 50 µm film bent at R = 1.5 mm about its own midplane (ε = t/2R = 50/3000). Films set badly on their own: crosslinked polyurethane protective films kept a 50–70° residual angle after 24 h folded at 5 mm radius, 60 °C/93 % RH (USPTO 9780318). | MARGIN 0.30
CHAIN | Fold7/Duo stack, which already has no polarizer (Samsung Eco² colour-filter-on-encapsulation since the Fold3) | now 167 µm | with idea about 142 µm. Only the OCA term (15 %) is removed, and the thinner-polarizer gain is already shipped. | RATIO 1.18
VERDICT | WOUNDED | Even if the gel stores no shear set, the polymer films still bend at about 3x their creep-safe strain, and the polarizer saving is already in Samsung's design, so the gain is at most ~1.2x.
NEW FACT | Samsung's Eco² OLED (Galaxy Z Fold3, 2021) already removes the polarizer by putting a colour filter on the encapsulation, saving about 50–100 µm of thickness. | thelec.net; oled-info.com

IDEA 3: Sub-creep strain budget fold
KILLER | Fraction of the 180° bend that does not recover after 8 h folded at 60 °C. The depth of a free crease is about πR·θ/8, which I checked on an exact circle. | required ≤0.32 % unrecovered (≥99.7 % recovery) for ≤20 µm at R = 5 mm. The idea's own limit of 0.05 % residual strain at 0.5 % strain means 10 % unrecovered, an 18° residual angle and about 620 µm free sag. | available about 4–5 % unrecovered for the best foldable OCA (95–96 % recovery at 60 °C/93 % RH, USPTO 11348487 family). Polyurethane films at R = 5 mm kept 28–39 % (USPTO 9780318). Also, 60 µm bonded at R = 5 mm gives 0.6 % strain, not ≤0.5 %. | MARGIN 0.08
CHAIN | iPhone Duo-class stack | now 167 µm after 3000 folds | with idea about 250 µm free-state estimate at 4 % unrecovered and R = 5 mm, because a larger radius spreads the same set fraction over a longer arc. A supported panel would come out lower, which needs a prototype. | RATIO ~0.7–1
VERDICT | DEAD | A larger radius lowers strain, but the same unrecovered fraction spread over a 15.7 mm arc makes a deeper crease. It would need about 99.7 % recovery, and the measured OCA and film recoveries are 10–100x short. The 5 mm radius also pushes the folded phone past 12 mm, versus 8.9 mm for the Fold7.
NEW FACT | A standard static-fold test (5 mm radius, 24 h at 60 °C/93 % RH, then 24 h hanging) left crosslinked PU films at 50–70° and thermoplastic PU at 180°, meaning it did not unfold at all. | USPTO 9780318 / 10090480

IDEA 4: Large-radius tensioning teardrop hinge
KILLER | Peak shear the OCA must hold for as long as the phone stays open, at 60 °C, to carry the specified 0.1 % panel tension (T = 0.001 × EA = 2.74 kN/m, shear-lag length about 48 mm) | required ≈57 kPa | available ≈10.5 kPa, the same creep test level as Idea 1 (USPTO 11348487 family). Separately, the claim that every layer stays below 0.3 % at R = 3 mm fails: 30 µm UTG is at 0.5 % and 50 µm PET at 0.83 %. A layer would have to be ≤18 µm. | MARGIN 0.18
CHAIN | iPhone Duo-class stack | now 167 µm | with idea about 1 µm if the full tension holds, or about 6 µm after the tension relaxes to what the OCA can hold. Model only. | RATIO ~28 (model)
VERDICT | DEAD | The specified 0.1 % tension loads the edge bonds about 5x above the level where certified OCAs already creep. The model says about 25x less tension would be enough, but that is a re-spec, not the idea as written.
NEW FACT | Oppo's own figure for the Find N6 is about 0.05 mm (50 µm) surface variation. It is a manufacturer claim, not an independent measurement. | tomsguide.com

All four ideas share a problem: the crease is not a simple elastic dent, it is a set that grows with folds and time, as HTX's 48 → 167 µm over 3,000 folds shows. Everything above that I marked "model" is a beam calculation I wrote, not measured data. The single cheapest experiment is a coupon of the stack folded 2000 times, with 24 h held folded at 60 °C/90 % RH after every 500 folds. Then measure the depth with a profilometer, flat with no tension and again with about 120 N/m and 3 kN/m of in-plane tension.

Files are in /home/user/SomeRepository/engine/runs/foldcrease_b/gate/c1/:
- gate_calc.py
- coupled.py

Sources:
- [ithinkdiff – HTX 3,000-fold test](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [Notebookcheck – iPhone Duo crease](https://www.notebookcheck.net/iPhone-Duo-does-have-a-visible-crease-despite-Apple-s-clever-nano-texture-surface.1395055.0.html)
- [USPTO 11348487 (OCA modulus/creep at 60 °C)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/11348487)
- [USPTO 9780318 (static fold recovery test)](https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/9780318)
- [3M foldable OCA whitepaper](https://multimedia.3m.com/mws/media/1793258O/optically-clear-adhesives-for-foldable-oled-displays-whitepaper.pdf)
- [TheElec – Eco² COE](https://thelec.net/news/articleView.html?idxno=3239)
- [oled-info – Eco² OLED](https://www.oled-info.com/samsung-display-announces-polarizer-free-eco2oled-tech)
- [Tom's Guide – Oppo Find N6 0.05 mm](https://www.tomsguide.com/phones/android-phones/i-have-been-testing-oppo-find-n6-crease-free-foldable-phone)