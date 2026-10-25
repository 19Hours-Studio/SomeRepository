The answer shows no measured gain over the best phones shipping now. What it offers is a well-built model that predicts a near-zero crease, if two quantities nobody has measured turn out to be favourable.

**What I checked**
- **Scripts:** I reran all six round-3 scripts. Their output matches the stored `.out` files exactly.
- **Hand checks:** my own estimates agree with the code. The crease slope comes to about φ·D·κ′/T ≈ 0.007 mrad, the hinge-seat kink to about 0.012 mrad, and gravity sag to about 0.015 mrad. The core physics is sound and consistent: pulling the glass sandwich tight divides any set it has taken by the tension.

**Why the headline "26×" isn't a gain over current practice**
- **It compares the design with itself.** The 0.51 → 0.020 mrad drop is measured against the answer's own earlier version, which was never built either, using tolerances the answer chose for it. No shipping phone is in that comparison.
- **The real benchmark is measured.**
  - iPhone Duo (HTX Studio test): 48 µm deep with a slope under 0.1° when new; 167 µm and 1.24° (21.6 mrad) after 3,000 folds.
  - Oppo Find N6: Oppo claims 82% less crease depth than the N5. It cites about 0.05 mm (50 µm) of height variation under the screen. I found no independent µm measurement.
- **The answer's figures are model output only.** It predicts a crease 0.19–0.6 µm deep with a slope of 0.02–0.12 mrad.
- **Two unmeasured numbers carry the whole result:**
  - **Glass set:** the glass must take a permanent set of no more than 2.3e-3. Against that, a 2024 PolyU study reports plastic creasing in ion-exchanged ultra-thin glass, and the HTX test shows creases growing with cycles. So lasting 2,000 cycles is unproven.
  - **Hinge seat:** the open hinge must re-seat to within 0.135 µm every time, in a phone exposed to dust and drops. Only laboratory couplings have shown 0.1–0.25 µm.
- **Its own pessimistic case fails.** Even inside the model, that case misses its invisibility target by 5×.
- **The costs are large:**
  - a folded spine of about 14–15 mm, against about 8.9 mm for the Fold 7;
  - 600 N of compression in the frame;
  - 244 MPa of sustained tension in the glass core, which needs ion-exchanged edges and leaves a fracture risk;
  - 10–17 g of extra mass;
  - a piezo servo and a seal.

**The cheapest test of the central claim** is the one the answer proposes itself: wrap ultra-thin glass strips and sandwich strips on 5.5 mm mandrels (heat, long holds, 2,000 cycles), hang them vertically and measure the set. If the set exceeds 2.3e-3, the idea is dead.

I wrote these findings to `gain_check.md` in the current folder.

Sources:
- [HTX test via iThinkDiff](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [TechEBlog on HTX](https://www.techeblog.com/htx-studio-iphone-duo-inner-display-crease-test/)
- [Notebookcheck](https://www.notebookcheck.net/iPhone-Duo-crease-put-to-the-test-revealing-some-interesting-quirks.1431319.0.html)
- [GSMArena on the Find N6](https://fo.gsmarena.com/oppo_details_find_n6s_impressive_creasefree_display-news-71887.php)
- [TYN Magazine on the Find N6](https://tynmagazine.com/oppo-irons-out-foldable-crease-with-find-n6/)
- [Tom's Guide on the Find N6](https://www.tomsguide.com/phones/android-phones/i-have-been-testing-oppo-find-n6-crease-free-foldable-phone)
- [Android Authority on the Find N6](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272)

HONEST GAIN: none