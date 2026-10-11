SCORES
ID | O | C | V | R | BASIN | closest
A01 | 5 | 7 | 6 | N | NEW | mutation testing; honeypot judge calibration
A02 | 6 | 7 | 7 | N | NEW | failure-mode walkthrough; TRIZ contradiction finding
A03 | 7 | 7 | 6 | N | NEW | MDL / conditional compression novelty
A04 | 5 | 6 | 4 | N | NEW | futures wheel scenario planning
A05 | 4 | 7 | 5 | N | LEDGER | patent claim-element novelty analysis
A06 | 5 | 6 | 4 | N | NEW | random-stimulus ideation; technology-push inventory
A07 | 4 | 6 | 6 | N | NEW | mutation testing of evaluators
A08 | 5 | 8 | 5 | N | NEW | Chao1 species-richness coverage estimation
A09 | 4 | 4 | 5 | Y | NEW | retrosynthesis / backward goal regression
A10 | 5 | 7 | 7 | N | NEW | gap analysis via plan elaboration
A11 | 4 | 6 | 5 | N | NEW | problem reformulation; step-back prompting
A12 | 3 | 7 | 5 | Y | QDMAP | Zwicky morphological box; descriptor-conditioned MAP-Elites
A13 | 4 | 6 | 4 | Y | NEW | Polya/TRIZ problem reformulation operators
A14 | 5 | 7 | 6 | N | NEW | ablation attribution; constrained mutation
A15 | 4 | 6 | 5 | Y | NEW | Amazon working-backwards; backcasting

TOP3:
- A02: It goes straight at the value deficit. Generation starts from the exact step where plain answers fail, and the same walker replays the instance to confirm the fix. That gives a check you can actually run instead of an unnamed external verifier.
- A03: It is the one originality signal here that comes from rebuilding the idea, not from what a judge knows. "Rebuildable with a hint, not without it" also rewards concreteness, which these pipelines usually trade away.
- A01: It is the only proposal that measures the judges' shared blind spots and corrects for them. It does this per defect type, with planted defects as ground truth. Swapping in a different judge model does neither.

NOTE: Only A05 and A12 fit the listed families. The rest avoid them but land on recognizable known methods: mutation testing, problem reformulation, backcasting, morphological analysis. Three near-duplicate pairs (A01/A07, A11/A13, A02/A10) show new attractor families forming at this layer, which is the weakness the question already describes.