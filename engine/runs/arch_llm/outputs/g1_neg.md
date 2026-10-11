**My 12 most probable answers:**
1. Mixture-of-experts with routing
2. Retrieval-augmented generation (RETRO/kNN-LM)
3. Distillation from a larger open model
4. SSM or linear-attention backbones
5. Ternary or low-bit training
6. Recurrent depth with adaptive computation
7. Product-key or large memory layers
8. Sparse or compressed long-context attention
9. Test-time training or fast weights
10. Byte-level hierarchical patching
11. Diffusion language models
12. Tool use or neurosymbolic offloading

**Shared paradigm:** they keep the standard next-token objective on raw text and only move, sparsify, compress or offload where the parameters and the computation live.

I forbid all of these, everything next to them, and the listed families (NGRAMIDX, SLEEP, COMPCACHE, RAMBANK, NEURORET, PRIORRES, SSM, LOWBIT, LOOPDEPTH, DIFFUSE, HIERLAT, TOOLSYM). The ideas below change something else: how the hidden state is organised and what the training signal says. Capacity and compute stay roughly fixed.

=== IDEAS ===
IDEA 1
NAME: Typed Relational State Machine
MECHANISM: Next to a small transformer, the model keeps an explicit per-context graph of at most 64 entity slots, each with a typed attribute vector, plus a sparse relation matrix between slots. At each token a small controller emits discrete edit operations: create, bind, update attribute, add or remove relation, or no-op. These are trained with straight-through Gumbel estimates, so next-token loss reaches the operations through a graph readout that the decoder attends to. A small auxiliary loss rewards edits that make later references predictable, such as pronouns, quantities and possession changes. The graph is a few kilobytes per sequence and the controller adds about 5% compute, so this fits easily on a 3060.
VALUE: It gives exact, length-independent tracking of entities and state (who holds what after 40 transfers), which a 200M transformer can only approximate in its attention patterns and loses as the context grows.

IDEA 2
NAME: Counterfactually Factorized Hidden State
MECHANISM: The residual stream is split into named subspaces such as tense, number, speaker, topic, numeric value and polarity. Training adds interchange-intervention losses: the model runs on a pair of inputs that differ in one factor, the matching subspace is swapped between the two runs, and the output must change exactly as the counterfactual text predicts. The counterfactual pairs are generated on the CPU by templated and rule-based perturbations of the corpus, for example number inflection, entity swaps and digit edits. That costs nothing on the GPU, and roughly every third training batch is a paired batch.
VALUE: The model generalises systematically, recombining factors in ways it never saw together, and it can be edited reliably by setting a subspace directly. An unconstrained same-budget transformer only gets there with far more data.

IDEA 3
NAME: Bidirectional Joint-Likelihood Consistency
MECHANISM: One shared network is trained to factorise each sequence both left-to-right and right-to-left, with a learned direction embedding selecting the order. A consistency loss penalises any disagreement between the two total sequence log-likelihoods, which must be equal for a coherent joint distribution. Disagreement on a sequence also flags it as a high-information sample, and those samples are reweighted in later epochs. The cost is about 1.6 times the compute per token, but every token gives two prediction targets plus a consistency constraint, which raises data efficiency within the 5B-token weekly budget.
VALUE: It removes the reversal curse ("A is B" implies "B is A") and gives better-calibrated probabilities over whole sequences, which a one-directional transformer trained on the same budget cannot achieve.