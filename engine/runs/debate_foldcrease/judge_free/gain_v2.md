The answer shows no real gain over current practice yet. All its gains are model predictions resting on assumed inputs, and the model has never been checked against a real crease. Its headline "4× deeper, 20× lower slope" compares the design with the answer's own earlier model, not with a phone that exists.

**What I checked**
- I reran `design3.py` and `sag_combo.py`. The outputs match the shipped `.out` files exactly, so the arithmetic is reproducible.
- The physics is sound as a linear model. A symmetric stack (glass, adhesive, panel, adhesive, glass) puts the OLED on the neutral plane, and the glass carries 99.2% of the bending stiffness. Leftover curvature then scales with each layer's stiffness share times its assumed set fraction, divided by the tension.
- I checked the outside facts. HTX did measure the iPhone Duo at 48 µm new and 167 µm (1.24°) after 3,000 folds, left closed before the rescan. The Oppo Find N6 figures come from Oppo: 82% less crease than the N5, and a reported 22 µm of extra depth after 600k folds against 165 µm for the Fold 7. I found no official Oppo document confirming the 22 µm figure.

**Why the claimed gain doesn't hold**
1. **The model is uncalibrated.** Applied to a stack like today's (`round1/retrofit.out`), the same model family predicts a 4–9 µm crease with no tension. Real phones measure 48–167 µm. So the model under-predicts real creases by about 10–40×, and comparing it with a measurement ("700× shallower than the aged Duo") means nothing.
2. **It misses its own target.** At the design tension of 3000 N/m, crease plus face-up gravity sag gives 0.0246 mrad, above the answer's own 0.024 mrad limit. It passes only at 4000 N/m. The main criterion, no worse than 1.2× the non-fold area, is never computed.
3. **The deciding number is unknown.** The design passes only if the glass's delayed set is at most 6e-4. At 1e-3 it is already 0.029 mrad. The answer admits this.
4. **Tensioning the display is prior art.** LG (magnetic tensioning), Huawei (EP4567555 / US 2024/0069604) and Apple (EP 4738056 A1) all have tensioning patents. What is new is the glass on both sides of the panel and the 15 mm curvature ramps.
5. **The costs are understated:**
   - the folded spine is about 13–14 mm, against 8.9 mm for the Fold 7;
   - the 70 mm unsupported fold zone is about half the open screen's width;
   - a 1 N press dents that zone by about 120 µm, which matters for stylus feel and pen-drop survival;
   - the 20 µm glass carries about 450 N of constant edge load;
   - shear through the OLED's organic layers is not modelled.

**What's good:** the hypothesis is clear and testable, the trade-offs are mostly stated, and the cheap decisive experiment is well chosen. Wrapping glass and sandwich strips on 5.5 mm mandrels and measuring the leftover curvature would settle the glass-set question. That experiment, plus calibrating the model against a real Duo or Fold, has to come before any gain can be claimed.

My notes are in `review.md` in the current folder.

Sources:
- [iThinkDiff – HTX iPhone Duo 167 µm](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/)
- [Notebookcheck – Duo crease test](https://www.notebookcheck.net/iPhone-Duo-crease-put-to-the-test-revealing-some-interesting-quirks.1431319.0.html)
- [Mac Observer – Apple publishes no crease number](https://www.macobserver.com/news/iphone-duo-crease-measurement-not-published/)
- [Android Authority – Find N6](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272/)
- [Nasi Lemak Tech – Find N6 review (22 µm vs 165 µm)](https://nasilemaktech.com/oppo-find-n6-review/)
- [Forbes – Find N6](https://www.forbes.com/sites/prakharkhanna/2026/03/11/the-oppo-find-n6-gets-closer-than-ever-to-a-crease-free-foldable-phone/)
- [EP4567555 (Huawei-style tensioning)](https://data.epo.org/publication-server/rest/v1.2/patents/EP4567555NWA2/document.html)
- [US 2024/0069604](https://patents.justia.com/patent/20240069604)
- [EP 4738056 A1 (Apple tension assembly)](https://www.goveda.com/patent/EP-4738056-A1)

HONEST GAIN: none