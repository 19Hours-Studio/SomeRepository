**1. Goals**
- G1: Store more knowledge than about 200M dense weights can hold.
- G2: Learn more from each token, since 5B tokens a week is the real limit.
- G3: Do multi-step reasoning reliably without a bigger model.

**2. Paradigm negation**
Mainstream models keep everything in one dense weight vector, train it by first-order backprop on next-token loss, and answer with feed-forward similarity matching. That combination is not allowed as the mechanism here.

**3/4. Mechanisms from far fields**
- G1 comes from coding theory. An LDPC code recovers a noisy or partial word by passing messages over a sparse parity graph, and its capacity grows with code length.
- G2 comes from robot mapping (SLAM, iSAM2). Every past measurement stays as a factor in a sparse square-root information matrix, and only variables that have drifted are relinearized.
- G3 comes from phase retrieval in crystallography. Elser's difference map finds points that satisfy two non-convex constraint sets at once, and it escapes traps where plain alternating projection gets stuck.

**5. Honesty check**
- Idea 1: the closest work is coded neural associative memories (Salavati and Karbasi), product-key memory and Hopfield layers. Retrieval here works by error-correcting decoding, not key similarity, and it has not been used inside a language model. Kept.
- Idea 2: the closest work is K-FAC, Shampoo and online Laplace/EWC. Those use curvature only as a decaying preconditioner. Here past batches are kept as factors and solved for the best overall estimate. This is the closest of the three to known work.
- Idea 3: the closest work is deep equilibrium models and looped transformers. My first draft, "iterate one block to a fixed point," was the forbidden LOOPDEPTH family, so I discarded it. The kept version needs two distinct projections and difference-map dynamics.

=== IDEAS ===
IDEA 1
NAME: LDPC-Coded Fact Memory
MECHANISM: Facts are stored as sparse binary words (8192 bits, 64 active). Together they form the null space of a large sparse constraint graph held in host RAM (10-20 GB of edge lists), learned incrementally with a Karbasi-style null-space rule over spans the model encodes from the corpus. At chosen layers the model emits a noisy partial word from its hidden state. The CPU runs 5-10 rounds of min-sum decoding to reach the nearest stored codeword, and a learned projection adds that codeword back into the residual stream. The query head is trained with a straight-through estimator. Decoding is sparse integer work on the CPU that overlaps with GPU compute, so capacity grows with code length rather than VRAM.
VALUE: It recalls whole facts from corrupted or half-given cues, at a capacity well beyond what 200M dense weights hold.

IDEA 2
NAME: Incremental-Smoothing Weight Estimation
MECHANISM: Weight blocks (heads, FFN slabs) are treated as SLAM variables. Each batch adds a linearized factor (Kronecker-factored information plus residual) to a sparse square-root information matrix kept in fp32 in host RAM. Cross-block factors are kept only between blocks that are strongly co-activated. A Bayes tree updates only the affected cliques. A block's Jacobians are recomputed on a stored mini-sample only when its estimate drifts past a threshold; otherwise it is solved by cheap back-substitution. The GPU computes forward passes and Jacobian sketches, and the CPU does the sparse Cholesky updates. Each token's information is kept rather than fading out through momentum.
VALUE: It reaches a target loss on far fewer tokens than first-order training, which matters most when data is the binding limit.

IDEA 3
NAME: Difference-Map Constraint Reasoning
MECHANISM: A slot-based reasoning latent x is refined by Elser's difference map: x <- x + beta[P_A(f_B(x)) - P_B(f_A(x))]. P_A is a small transformer that projects onto logically consistent states. P_B projects onto knowledge-consistent states through Idea 1's decoder or a layer of a frozen quantized open model. Both are trained with an idempotence loss plus task loss, using implicit differentiation at the fixed point, so memory use stays constant however many iterations run. Iteration stops when the two projections agree. Each step is cheap enough to run hundreds of times on the 3060.
VALUE: It solves constraint-heavy multi-step problems where single-pass or single-loop models get stuck at wrong fixed points.