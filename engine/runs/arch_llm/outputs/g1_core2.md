**1. Goals (picked for importance, not originality)**
- G1: More learning per FLOP than backprop SGD, which costs about 6N FLOPs per token.
- G2: A working memory far larger than 12 GB of KV cache allows.
- G3: Answer quality close to a 7-8B model at a cost close to a small model's.

**2. Paradigm negation**
Mainstream LMs are a single dense network trained by end-to-end backprop of next-token cross-entropy, and they run the same full graph for every token. Both global backprop-SGD and uniform dense per-token execution are forbidden as mechanisms.

**3. Forbidden families**
None of the ideas below uses NGRAMIDX, SLEEP, COMPCACHE, RAMBANK, NEURORET, PRIORRES, SSM, LOWBIT, LOOPDEPTH, DIFFUSE, HIERLAT or TOOLSYM.

**4. Mechanisms from the periphery**
- G1 → Geodesy, Helmert blocking (the method used for the NAD83 adjustment with about 1M unknowns). Stream the observations, accumulate normal equations per block, remove the interior unknowns by Schur complement onto shared junction unknowns, solve once, then back-substitute.
- G2 → Video coding (the H.264 GOP structure). I-frames are stored in full. P-frames are stored as a motion vector to a reference frame plus a quantized residual, chosen by rate-distortion optimization.
- G3 → Power-grid economic dispatch and unit commitment. Units run in merit order against a system price λ. Slow units have startup costs and minimum up-times, so whether to switch them on is decided from forecast demand.

**5. Honesty check**
- My first G2 candidate was spaced-repetition data scheduling. It is essentially Amiri et al. 2017 (Leitner-queue training), so I discarded it.
- Idea 1's closest work is extreme learning machines and random-feature ridge regression. The difference is an exact solve over the whole corpus of a cell-partitioned head of about 0.5B parameters, using Schur elimination onto a shared vocabulary factor.
- Idea 2's closest work is KV-cache compression (MiniCache, KIVI, InfLLM). The difference is that chunks are coded against references with a residual, and no tokens are evicted or retrieved.
- Idea 3's closest work is Co-LLM (per-token deferral), FrugalGPT cascades and speculative decoding. The difference is a dual price that clears the budget, plus commitment state with startup costs and minimum up-times.

=== IDEAS ===
IDEA 1
NAME: Helmert-Blocked Closed-Form Training
MECHANISM: A briefly trained 120M trunk is frozen, and above it sits a head of 4096 cells, each a 512×256 linear map. Each token is routed to one cell by k-means on the trunk state, and every cell maps into a shared 256-d vocabulary factor taken from a PCA of a 1.5B open model's logits. The head is trained in one streaming pass: for each token, the GPU adds rank-1 updates to that cell's normal equations (XᵀX, and XᵀY where Y is the teacher's logits in the PCA basis), which take about 6 GB. The cell unknowns are removed by Schur complement onto the shared factor, which is solved by Cholesky; the cells are then back-substituted, and two or three such alternations replace SGD entirely.
VALUE: The head reaches the exact least-squares optimum without backward passes, learning rates or activation memory, so it takes in several times more tokens per week than a backprop-trained model of the same size.

IDEA 2
NAME: Motion-Compensated KV Coding
MECHANISM: The context is split into 64-token chunks grouped into GOPs. I-chunks keep their full fp16 K/V. Each P-chunk stores, per head, a motion vector (a reference chunk plus token alignment, found by matching key sketches) and a quantized low-rank residual. An encoder chooses between I and P coding and sets the residual rank by Lagrangian rate-distortion optimization, with distortion measured as attention-output error on probe queries. Attention rebuilds P-chunks from their references in shared memory, so the GPU mostly reads small residuals.
VALUE: Repetitive material such as code, logs and long documents gets million-token working memory in 12 GB, with every token still exactly addressable where a same-budget transformer would have to truncate or evict.

IDEA 3
NAME: Merit-Order Compute Dispatch
MECHANISM: Three units share one tokenizer: a 200M student (baseload), a 1.5B open model (mid-merit) and a 4-bit 8B open model (peaker). A 5M forecaster reads the student's hidden state and predicts how much each unit would reduce loss over the next 16 tokens; it is trained by regression on logged realized reductions. A dual price λ is updated by subgradient so that compute spending clears the latency budget. A unit is committed only when its forecast gain is larger than λ times its running cost plus its startup cost (catch-up prefill of the tokens it skipped). A minimum up-time keeps the 8B's KV cache warm across hard spans, and it is idled across easy ones.
VALUE: It delivers near-8B quality on the hard tokens at about 2-3× the cost of the small model, a cost-quality point that no single same-budget transformer can reach.