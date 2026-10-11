**Answer 1: Walk-forward self-backtesting**
- **Why it's hard:** Open-ended domains have no oracle. The hidden assumption is that the correctness signal has to be available *now*, about questions whose answers nobody knows yet.
- **Move (b):** This is the backtesting problem that quantitative finance has already solved. Nobody knows the future, but walk-forward evaluation on history gives a strict signal. Here a model frozen at time T predicts what the archive later settled after T, and the archive does the grading. What does not map: the corpus "leaks" (text from after T can contaminate the training data), and the world is non-stationary, so the cutoff must be enforced strictly.
- **One sentence:** Train copies on history up to a cutoff, score them against what came after, and transfer the reasoning habits that win.
- **Inevitability:** "Of course: history is an answer key with a timestamp."
- **Honesty:** The closest work is LLM forecasting with retrieval cutoffs (Halawi et al., 2024). Here backtesting is the general correctness signal for improving reasoning, not a forecasting benchmark.

**Answer 2: Metamorphic-relation oracle**
- **Why it's hard:** The hidden assumption is that you need to know the right answer to detect a wrong one.
- **Move (b):** Software engineering solved this "test oracle problem" with metamorphic relations. You never learn the true output, but you do know provable relations between outputs on transformed inputs. Examples: changing units must rescale the answer, permuting irrelevant details must leave it unchanged, and a counterfactual edit must move it in a known direction. What does not map: a systematic error that stays the same under every transformation goes undetected.
- **One sentence:** A library of transformations with provable output relations, where the violation rate is the loss.
- **Honesty:** The closest work is consistency checks on superhuman models (Fluri et al., 2023). That work only evaluates; here the violations drive training, and the relation library grows.

**Answer 3: Teachability on raw data**
- **Why it's hard:** The hidden assumption is that the correctness of a claim must be judged at the level of the claim itself.
- **Move (a):** Drop that assumption and judge a claim by whether a small, fresh student given it predicts held-out *unlabeled* observations better. Unlabeled observations exist in every domain, and the data does the grading instead of the model.
- **One sentence:** Claims are rewarded by the predictive gain they give a naive student on real data.
- **Honesty:** The closest work is teacher-to-student explanation evaluation (Pruthi et al., 2022). That work evaluates explanations against labels; here the gain on raw data is the self-improvement signal.

=== IDEAS ===
IDEA 1
NAME: Walk-Forward Self-Backtesting
MECHANISM: The system keeps snapshot copies of itself, each trained only on data before a strict cutoff date, and asks them questions that the archive settled after that date. The archive grades their answers with no model judgment involved. The system stores which reasoning strategies and update rules improved these later-verified answers and transfers only those to the present model. Contamination audits drop any snapshot whose training data leaked material from after its cutoff.
VALUE: It turns the passage of time into an oracle for open-ended domains, so improvement is graded by the world rather than by the model itself.

IDEA 2
NAME: Metamorphic-Relation Correctness Oracle
MECHANISM: The system keeps a growing library of input transformations, each paired with a relation its outputs must provably satisfy: unit changes rescale answers, irrelevant permutations leave them unchanged, and counterfactual edits move them in a known direction. Each answer is re-asked under these transformations, and violations of the relations are the training loss. New relations are kept only if they are derivable a priori, for example from symmetry, dimensional analysis or the structure of the edit.
VALUE: It detects and corrects errors without ever knowing the true answer, as metamorphic testing does for programs that have no test oracle.

IDEA 3
NAME: Teachability-Graded Claims
MECHANISM: Each claim or explanation the system produces is given to a small, freshly initialized student model. The claim is scored by how much it improves the student's prediction of held-out raw observations from the domain, compared with a student that did not receive it. The system stores these gains per claim and trains itself toward claims with high gains, while claims with no gain are demoted.
VALUE: It grounds correctness in abundant unlabeled data, which exists everywhere, instead of in the system's own fallible judgment.