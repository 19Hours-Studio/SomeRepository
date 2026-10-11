The 3060 gives you very little compute, but it sits next to 32 GB of system RAM and an open-weight model that fits in memory. A same-budget transformer has to keep all of its knowledge in about 200M dense weights and has to recompute every answer from scratch. All three proposals below move capacity, computation or learning into cheap memory instead of into FLOPs.

**1. Self-memoizing depth.** The model has a cheap 4-layer "fast path" and a deep 24-layer "slow path." Whenever the slow path runs, its net effect on the residual stream gets stored, so the next time the same situation comes up the model looks it up instead of recomputing it.

**2. Foreign-neuron retrieval.** An open 7B–13B model's feed-forward layers are broken into individual (key, value) neurons and indexed in RAM. A small trainable model fetches only the few thousand neurons relevant to each token, so it draws on a large model's knowledge at small-model cost.

**3. Sleep-grown sparse slots.** The model never stops learning. During use it logs surprising episodes. When the PC is idle it replays them into sparse weight slots that it allocates as needed and that can grow until RAM is full, so it learns without overwriting old skills.

=== IDEAS ===
IDEA 1
NAME: Self-Memoizing Depth Cache
MECHANISM: Each token first passes through a 4-layer fast path. A learned locality-sensitive hash of its residual state then queries a RAM-resident table of up to about 1B int8 entries. Each entry stores a compressed delta ("this is what layers 5–24 would have added"). On a confident hit the 20 deep layers are skipped and the delta is added. On a miss the slow path runs and its delta is written back as a new entry. Training does three things together: it distills the slow path into the cache entries, it shapes the hash so that states with similar deltas share buckets, and it calibrates a hit-confidence gate. Lookups cost bytes rather than FLOPs, so the 32 GB of RAM becomes stored computation, and PCIe only carries the few kilobytes each token needs.
VALUE: Effective depth and throughput keep improving with use and data seen, not with parameters, so a fixed-FLOP transformer cannot match it on recurring computations.

IDEA 2
NAME: Foreign-Neuron Retrieval Model
MECHANISM: Every feed-forward neuron of a frozen open 7B–13B model is extracted as a (key, value) pair and quantized to 4 bits. The roughly 2B-vector index lives in RAM, behind a product-quantized nearest-neighbour index. A trainable 200M "host" model learns per-layer projections from its own residual into the teacher's residual coordinates. With those it retrieves the top 2–8k neurons for each token, applies the teacher's activation function to those neurons only, and maps the summed values back into its own stream. The projections are trained by distillation: the retrieval-augmented output has to match the full teacher's output. The neuron selection is made differentiable through a straight-through top-k. Each token then costs only a few megabytes of RAM reads and about 2% of the teacher's feed-forward FLOPs.
VALUE: The model gets close to a 7–13B model's factual and associative capacity while training and running at roughly the compute and VRAM cost of a 200M model.

IDEA 3
NAME: Sleep-Consolidated Growing Slots
MECHANISM: While the model is in use, any token span with high loss or user correction is stored in a RAM episodic buffer as compact latent states plus targets. During idle hours the GPU replays these episodes into a pool of sparse weight "slots": small rank-4 adapters keyed by a content hash, with up to millions of them in RAM. A slot is allocated only when its gradient conflicts with existing slots (measured as gradient cosine below zero), so new learning goes into new capacity instead of overwriting old capacity. While the model runs, a router loads only the 8–32 slots that match the current context into VRAM. The dense core stays mostly frozen, with interleaved replay from a reservoir sample of old episodes.
VALUE: The model keeps learning new facts and skills indefinitely after deployment without catastrophic forgetting or full retraining, while a same-budget transformer is fixed after its weekly training run.