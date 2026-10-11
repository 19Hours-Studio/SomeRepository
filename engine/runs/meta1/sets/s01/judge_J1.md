SCORES
ID | O | C | V | R | BASIN | closest
A01 | 6 | 7 | 6 | N | NEW | mutation testing, gold-standard judge items
A02 | 5 | 7 | 7 | N | PROBANCH | failure-mode walkthroughs, unsolved-problem lists
A03 | 7 | 6 | 6 | N | NEW | MDL / conditional compression novelty
A04 | 5 | 6 | 4 | N | NEW | futures wheel, scenario planning
A05 | 4 | 7 | 5 | N | LEDGER | novelty search, feature-based clustering
A06 | 5 | 6 | 4 | N | NEW | morphological analysis, solutions-seeking-problems
A07 | 5 | 6 | 5 | N | NEW | mutation testing, honeypot evaluation items
A08 | 5 | 8 | 4 | N | NEW | Chao1 species-richness estimators
A09 | 5 | 5 | 5 | N | NEW | retrosynthesis, backward-chaining planning
A10 | 5 | 7 | 7 | N | PROBANCH | gap analysis of build plans
A11 | 4 | 7 | 5 | N | NEW | problem reformulation, step-back prompting
A12 | 4 | 7 | 6 | N | QDMAP | Zwicky morphological box, MAP-Elites
A13 | 4 | 7 | 5 | N | NEW | problem reformulation operators, SCAMPER
A14 | 5 | 7 | 6 | N | NEW | ablation-guided mutation, saliency
A15 | 5 | 6 | 6 | N | NEW | Amazon working-backwards PR/FAQ

TOP3:
A01 - It measures the judges' shared blind spots with planted defects of known types, and it is the only answer that turns the same-model-family judge weakness into a calibrated number.
A03 - The hint-rebuild differential is an originality signal that does not depend on judges, it can be tested, and it rewards ideas that are both crisp and unexpected.
A10 - It ties originality to the vague steps inside already-valuable plain plans and checks the fix by expanding the plan again, which directly targets the value and concreteness losses.

NOTE: The set falls into a few repeated clusters: judge mutation testing (A01/A07), question reframing (A11/A13), anchoring on failures or gaps in plain answers (A02/A10/A14) and backward derivation from a target (A09/A15). Few answers fit the listed families exactly, but most are known methods (mutation testing, reformulation, morphological analysis, working backwards) applied to a new setting rather than new mechanisms.