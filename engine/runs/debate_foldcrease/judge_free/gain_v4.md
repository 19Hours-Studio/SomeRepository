**The answer does not show any gain over today's best practice.** It is a careful, consistent model of a hypothesis that nobody has tested.

The design keeps the display unbonded under the screen: a glass–OLED–glass layer, 76 µm thick, held under about 4000 N/m of tension from its two outer edges and floating over a 30 µm air gap.

**What holds up**
- I ran `round4/float4.py`. It reproduces every number in `answer.md`, and the code matches what the answer describes.
- My own rough estimate gives a crease slope of 0.012 mrad, against the code's 0.0066 mrad. They are the same order, which is expected because the code models smooth ramps where I assumed a cruder shape. So the model is consistent with itself.
- The physics behind it is sound: pulling a sheet tight flattens any leftover curvature over a short distance (about 0.77 mm here). In the model, tension cuts the crease about 320 times compared with no tension. With the tension off, the model predicts a crease about 134 µm deep, which is close to the 48–167 µm HTX measured on the iPhone Duo.
- It names a cheap test that would settle the main question: glass strips wrapped on mandrels, costing a few hundred dollars.

**Why the gain is "none"**
1. **Every crease number is a model output.** The results depend on assumed "set" fractions: how much of its folded curvature each layer keeps after unfolding (0.2 for the OLED panel and 0.1 for the adhesive). The design only passes if the glass keeps no more than about 0.1% (φ_g ≤ 1.1e-3), and nothing measured supports that. The crease grows linearly with that fraction: at 1% the slope is 0.055 mrad, 4.5 times over the answer's own visibility limit. The PolyU study the answer cites shows that ion-exchanged ultra-thin glass does form permanent creases, and that longer holds and repeated folding make recovery worse.
2. **The gains it quotes are not against shipping phones.** The 7–9× figure is against the author's own previous design (v3). The 80–3300× against the iPhone Duo compares a model with a measurement, which the answer admits.
3. **The idea is not new.** Tensioned displays already exist in patents (US 10209746), and the Oppo X 2021 rollable concept phone kept its screen crease-free by rolling it under tension. Reviewers still saw a "slight rumple" on it.
4. **Some durability risks are underplayed.**
   - The top glass is 20 µm thick, bare (no protective film), with a hardened surface layer only 3 µm deep.
   - While open, the glass core carries about 244 MPa all the time. A crack about 2.4 µm deep is then enough to break it, so a sand scratch that gets through the 3 µm hardened layer could shatter the panel.
   - While folded, the core of the outer glass sheet sees about 517 MPa, where a crack of about 0.5 µm is critical.
   - It needs 600 N of frame load, 6–7 mm side bezels, a 100–200 V supply to hold the glass while folded, and an air gap that dust can enter.
   - In its own pessimistic case for holding the phone by both edges, the air gap is already used up (−4.8 µm).
5. **The comparison phones also lack crease-depth data.** Oppo gives only relative figures (up to 82% less crease, hinge height variation cut from 0.2 to 0.05 mm, TÜV certification at 600k folds), and a reviewer called "zero crease" a slight exaggeration. The only real numbers are HTX's Duo results: 48 µm and under 0.1° new, 167 µm and 1.24° after 3000 folds.

Files are in the current folder:
- `check.py` and `check.out`: my independent checks.
- `verdict.md`: this verdict written out.

Sources: [HTX via iThinkDiff](https://www.ithinkdiff.com/iphone-duo-crease-test-3000-folds/), [PolyU UTG plasticity](https://research.polyu.edu.hk/en/publications/plastic-deformation-and-recovery-in-ultrathin-aluminosilicate-gla/), [Android Authority – Find N6](https://www.androidauthority.com/oppo-find-n6-zero-feel-crease-durability-3648272), [Oppo newsroom](https://www.oppo.com/en/newsroom/stories/oppo-find-n6-zero-feel-crease-foldable-innovation/), [Mobile World Live – N6](https://www.mobileworldlive.com/oppo/oppo-irons-out-foldable-crease-with-find-n6/), [Dezeen – Oppo X 2021](https://www.dezeen.com/?p=1590567), [Tom's Guide – rollables](https://www.tomsguide.com/uk/news/oppo-x-2021-rollable-phone-looks-like-the-future-but-the-future-is-a-long-ways-off)

HONEST GAIN: none