The RTX 3060 setup is unbalanced in ways a dense transformer ignores. Training compute is the bottleneck. Host RAM is about 2.7 times larger than VRAM. The CPU sits idle. The PC is also free most of the day. All three designs below use these gaps instead of adding FLOPs.

=== IDEAS ===
IDEA 1
NAME: Co-Access Paged Host Memory
MECHANISM: A 200M-parameter GPU controller is paired with a sparse key-value memory of about 20B int8 rows kept in the 32 GB of host RAM. Rows are grouped into 64 KB pages. A cheap first pass over each 256-token chunk predicts which pages the chunk needs, about 64 pages or 4 MB. That set is copied over PCIe 4.0 (about 25 GB/s) while the GPU is still working on the previous chunk, so the transfer time is hidden. During training, only the rows that were touched get gradients, and CPU threads apply sparse Adam updates to them in RAM. Every night a CPU job re-clusters rows into pages using the co-access graph, so each page fetch serves many tokens. This keeps bandwidth use high while VRAM holds only the controller and the active pages.
VALUE: It gives the model a 20B-parameter knowledge store at the per-token compute cost of a 200M model, a capacity no dense same-budget transformer can hold in 12 GB.

IDEA 2
NAME: Frozen-Prior Surprise Delta Model
MECHANISM: An open-weight 3B model quantized to 4-bit (about 2 GB VRAM) stays frozen and supplies a prior distribution plus hidden states at every position. The trainable network is a small recurrent side model (about 150M parameters). It reads those hidden states and outputs only a gated additive correction to the prior's logits. It is trained only on high-loss tokens, where the prior's loss is high and the corrected output could still improve. These tokens are found by running the frozen prior forward once at inference cost, and they are about 15% of the corpus. At inference a learned gate skips the side model on confident tokens, and on those tokens the prior's later layers exit early. As a result, the backward pass and most FLOPs go only to new information.
VALUE: The 5B-token weekly budget acts like roughly 30B tokens of useful signal on top of a stronger prior, without ever paying training cost for what the prior already knows.

IDEA 3
NAME: Idle-Time Sleep Consolidation
MECHANISM: During use, the model writes episodic traces into a ring buffer in RAM: the context, its own outputs, user corrections and high-surprise spans. When the PC is idle, a "sleep" job replays these traces mixed with samples from its normal training data, which guards against forgetting. Any rewritten answers produced during replay are checked by the frozen open-weight model from Idea 2 before they are kept. The job then distils the result into the memory pages of Idea 1 and the side model's low-rank adapters. Updates are confined to sparse rows and adapters. That keeps a nightly session to a few GPU-hours and makes it reversible: the job keeps checkpoints, and a validation probe rolls back any update that hurts held-out perplexity.
VALUE: The model keeps learning the owner's documents and tasks on the same PC indefinitely, while a same-budget transformer stays frozen at the end of training.