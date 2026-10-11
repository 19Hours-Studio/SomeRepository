SCORES
ID | O | C | V | G | R | BASIN | X | closest
A01 | 4 | 6 | 6 | 5 | N | NEW | Y | forecasting tournaments, ForecastBench-style training
A02 | 6 | 5 | 5 | 4 | N | NEW | Y | SIMEX / zero-noise extrapolation
A03 | 5 | 5 | 5 | 4 | N | COMPMAP | Y | capture-recapture, Dawid-Skene latent class
A04 | 3 | 6 | 5 | 4 | Y | NEW | Y | Platanios unlabeled accuracy estimation, Dawid-Skene
A05 | 3 | 5 | 6 | 4 | N | NEW | Y | forecasting tournaments, proper scoring rules
A06 | 5 | 6 | 5 | 4 | N | COMPMAP | Y | Mills error seeding, Lincoln-Petersen
A07 | 3 | 5 | 4 | 3 | Y | NEW | Y | co-training, PATE disjoint teachers
A08 | 3 | 7 | 5 | 4 | Y | NEW | Y | metamorphic testing, consistency regularization
A09 | 4 | 6 | 6 | 5 | N | NEW | Y | temporal backtesting, time-cutoff evaluation
A10 | 7 | 4 | 4 | 4 | N | NEW | Y | turbo decoding, EXIT charts
A11 | 6 | 6 | 5 | 5 | N | NEW | Y | geodetic adjustment, Baarda data snooping
A12 | 6 | 4 | 5 | 4 | N | NEW | Y | Desroziers data-assimilation diagnostics
A13 | 5 | 6 | 6 | 5 | N | NEW | Y | prequential MDL, V-information
A14 | 5 | 6 | 5 | 4 | N | NEW | Y | least-squares adjustment, gross-error detection
A15 | 2 | 6 | 5 | 3 | Y | NEW | Y | metamorphic testing

TOP3:
- A11: The redundancy number is the key idea. It separates beliefs that other observations can check from beliefs nothing can check, so the system knows where it is blind instead of trusting everything it holds.
- A01: Grading against frozen resolvers on future data is the cleanest oracle in this set that the model cannot game, and it can be built today.
- A02: Fitting a line to planted perturbations and extrapolating to zero is a new transfer of error-mitigation ideas. It turns known differences into bias-corrected absolute answers.

NOTE: All 15 answers go after the oracle crux, and they fall into three groups: the world's future as the grader (A01, A05, A09), statistics on agreement between independent views (A03, A04, A06, A07, A11, A12, A14) and invariances known by construction (A02, A08, A15). Several are near-duplicates (A01/A05, A11/A14, A08/A15), and all of them are verification layers rather than new architectures, which limits their value for the original question.