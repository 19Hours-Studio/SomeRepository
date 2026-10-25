# Check of answer.md (Continuum-8)
Re-ran model8.py (imports refine_continuum/round7 + round6). Results reproduce run8.txt exactly
(55.2 tok/s/W; ratios 1.13/1.25/1.51/1.71/2.51 vs Rubin trimmed 150 W, 128K).

Extra runs (lowtier.py, sram.py), ratios vs Rubin trimmed 150 W, 128K, tiers >=200/500/1000/1500/2000:
- Speed floors 20/50/100 tok/s/user: ratio stays 1.13 (both systems flat below 200). Bulk tier = tie.
- W-Tier SRAM 13.8 GB instead of 18.4 GB (~18 Mb/mm2, i.e. AMD V-Cache density scaled N7->N5, vs the
  24.5 Mb/mm2 implied by 18.4 GB on 8 x 750 mm2 N4 tiers): 1.06 / 1.17 / 1.42 / 1.67 / 2.51.
  The indexer-keys-in-SRAM lever (step 4) disappears; CSA goes back to 4 HBM stacks.
- Same + same node: 0.96 / 1.06 / 1.28 / 1.51 / 2.25
- Same + same node + eta 0.5: 0.84 / 0.92 / 1.12 / 1.33 / 1.93
Rubin+LPX baseline (6.5 tok/s/W at >=1000, about 5.6x worse than Rubin alone) assumes only 72 Rubins on the
attention side. That contradicts Nvidia's positioning of LPX for high interactivity, so the 8.5x "win" is not credible.
