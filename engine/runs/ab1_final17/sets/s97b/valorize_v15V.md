=== VALORIZED V01 ===
ANCHOR: duplicate with complementary degeneration masks
NAME: World-Arbitrated Degenerate Twins
MECHANISM: When the gradient from new data conflicts with a module's frozen probe signature, the module splits into two twins. The twins get complementary sparse masks, so only the pair together reproduces the old signature, and the system judges between them only by which one better predicted the world's next observation. Because the pair holds the old signature by construction, neither twin can win by rewriting past behavior. They compete only on inputs where they disagree, and each disagreement is held as an open bet until the delayed outcome arrives (the next item in a stream, the result of an action, a later document). A twin's own sub-functions are pruned only after it loses bets it placed itself, so the correctness signal is always a prediction made before the outcome, never a judgment made afterward.
VALUE: The system keeps learning new skills after deployment, with old skills preserved in its structure and new ones checked against what the world later shows, not by grading itself.

=== VALORIZED V02 ===
ANCHOR: four-point violations become reticulation nodes
NAME: Cross-Metric Reticulation Detector
MECHANISM: Four-point-condition violations among concept quartets are computed separately in several distance metrics, each built from independent evidence (text co-occurrence, shared properties, form or etymology, perception). A concept becomes a two-parent reticulation node only when all of the metrics show the violation and each one gives the same admixture weight. A real hybrid is overdetermined: its mixing proportion is one number that every independent geometry must reproduce. An artifact of one embedding breaks tree-additivity in that metric only, and the weight it gives disagrees with the others. Accepted nodes inherit properties from both parents in that proportion, and the weights are re-solved as new evidence arrives, so a node whose weights drift apart across metrics is demoted.
VALUE: The system can represent concepts that blend lineages, such as loanwords, hybrid species and fusion genres, and can tell real hybrids from artifacts of its own embeddings without a labeled oracle.

=== VALORIZED V03 ===
ANCHOR: Wahlund heterozygote deficit splits units
NAME: Wahlund-Certified Unit Splitting
MECHANISM: Each unit's discretized activation states are treated as alleles over pairs of co-occurring contexts. A heterozygote deficit relative to the Hardy–Weinberg expectation triggers a split into child units. The split is kept only if it satisfies the Wahlund identity on new context pairs: each child must return to Hardy–Weinberg equilibrium (F_IS near 0), and the variance in allele frequency between the children (F_ST) must account numerically for the parent's deficit. This tests the unit against a calibrated null model with known false-positive rates rather than judging the model's own outputs, so a spurious split leaves a deficit inside a child or an unexplained gap, and is merged back.
VALUE: The model breaks apart conflated concepts while it runs, and every split is certified by a statistical identity checked on new data rather than by the model's own opinion of the result.

=== VALORIZED V04 ===
ANCHOR: double-entry ledger of conserved quantities
NAME: Double-Entry World Ledger
MECHANISM: Every state change is posted as a debit from one holder and a credit to another, across a learned set of conserved quantities. Any nonzero sum after a step is the error signal, and it needs no oracle because balance is an algebraic invariant, not a judgment. To stop the system from balancing its books by invention, a hidden holder created to absorb a persistent imbalance must be issued as a forecast of which future transfers it will settle. It is removed if those transfers never arrive or if a total stated in the input (a count, a balance, a census) contradicts it. A quantity is dropped from the conserved set when stated totals for it repeatedly fail to reconcile.
VALUE: The system can track world state exactly over very long sequences and infer unmentioned participants or leaks, and later input can disprove each such inference.

=== VALORIZED V05 ===
ANCHOR: loop misclosure adjustment with Baarda's w-test
NAME: Geodetic Reasoning Network Adjustment
MECHANISM: Each intermediate claim is a station derived along several routes. A least-squares adjustment with Baarda's w-test finds the faulty step in any loop that fails to close. Routes produced by the same model can share an error and still close perfectly, so the adjustment carries a covariance between routes, estimated from shared premises, sub-steps and tools. From that it computes, for every claim, its minimal detectable bias: the largest error that could still hide in that claim given those correlations. A claim whose minimal detectable bias is too large is not answered until the planner adds a new route to a control station, meaning a value fixed outside the model (a measurement, an executed computation, a cited source), just as a survey is anchored to fixed benchmarks.
VALUE: Long reasoning chains find their own faulty step and state, for each conclusion, how large an error could still be undetected, instead of mistaking self-agreement for verification.

=== VALORIZED V06 ===
ANCHOR: transfers as bar-framework equilibrium stresses
NAME: Rigidity Ledger with Floppy Modes
MECHANISM: Holders are points and transfers are bars between them. A quantity counts as conserved exactly when its observed transfers lie in the framework's equilibrium-stress space, which linear algebra checks without the model's judgment. A persistent imbalance is treated as a load. A hidden holder is placed where the floppy modes can carry that load, and Maxwell counting then fixes how many new bars it must have and to which holders, which predicts transfers not yet observed. The holder is kept only if later transfers fall on those predicted bars and the dimension of the stress space changes as counted. Where the predicted stresses conflict, the holder splits in two.
VALUE: The system can keep exact track of world state and locate unseen participants, with their existence and connections derived from the framework's geometry and confirmed by later observations.

=== VALORIZED V07 ===
ANCHOR: Hodge split of margins across re-encodings
NAME: Hodge-Proofread Reasoning Charts
MECHANISM: Each reasoning step is scored under several re-encodings of its context, drawn from different kinds of source (paraphrase, formal translation, a different model, a tool run). The margins are treated as edge flows on the graph of encodings and given a Hodge decomposition. The gradient part is a per-encoder bias, estimated across all steps and subtracted. The curl part is inconsistency, and the step is discarded. The harmonic part becomes a local chart with an explicit context variable. The decomposition is trusted only if, after fitting on k encodings, it predicts the step's margin on a new encoding before that encoding is scored. That held-out prediction is the correctness signal, so neither a biased encoder nor an overfit chart can certify itself. A chart whose transition maps keep mispredicting new encodings is dissolved.
VALUE: Long reasoning becomes more reliable without throwing away conclusions that hold only in some contexts, and the system learns where its knowledge splits into separate frames.

=== VALORIZED V08 ===
ANCHOR: bijective layers with ancilla tape
NAME: Reversible Network with Ancilla Audit
MECHANISM: Every layer is a bijection, and every bit a step would discard is written to an ancilla tape, so the network can run backward exactly. To check an output, the system fixes both the actual input and the output and runs backward. The number of ancilla bits that must be invented to reconcile the two is an exact bit count of how much of the output the input does not support, not the model's opinion of it. Zero invented bits means the output follows from its evidence, a high count means it was fabricated, and that count is the training signal. One example's influence is removed by uncomputing its trace. The audit separates grounded content from invented content, but it does not certify that the input itself is true.
VALUE: The system gets exact provenance, a measured count of unsupported information in every claim, exact counterfactual inputs and certified forgetting, none of which an LLM can provide because it discards information at every layer.