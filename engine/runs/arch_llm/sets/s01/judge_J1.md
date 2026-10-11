SCORES
ID | O | C | V | R | BASIN | closest
A01 | 5 | 7 | 3 | N | NEW | Closed-form piecewise least-squares distillation heads
A02 | 6 | 7 | 5 | N | NEW | CacheGen-style delta KV-cache compression
A03 | 6 | 4 | 4 | N | NEW | K-FAC / EKF training plus iSAM2
A04 | 3 | 8 | 5 | Y | NEW | RHO-LOSS plus learning-progress curriculum
A05 | 4 | 6 | 4 | N | NEW | MMI reranking; Belief State Transformer
A06 | 4 | 6 | 3 | N | NEW | Markov Logic Networks / MaxWalkSAT
A07 | 4 | 7 | 5 | N | NEW | Reverse training; bidirectional consistency
A08 | 5 | 7 | 5 | N | NEW | FrugalGPT / model-cascade routing
A09 | 5 | 3 | 3 | N | NEW | Kuramoto binding (AKOrN, temporal binding)
A10 | 5 | 3 | 2 | N | NEW | Example-based MT / analogical proportions
A11 | 2 | 8 | 4 | Y | NEW | Interchange Intervention Training (Geiger)
A12 | 4 | 7 | 5 | N | NEW | EntNet / dynamic entity-state LMs
A13 | 6 | 6 | 3 | N | NEW | LightRNN 2D softmax plus growing MoE
A14 | 6 | 6 | 4 | N | NEW | Relation-aware attention with cycle consistency
A15 | 6 | 4 | 4 | N | LOOPDEPTH | DEQ plus Elser difference map
A16 | 6 | 6 | 4 | N | NEW | Learned sparse attention via Granger tests
A17 | 3 | 7 | 5 | Y | NEW | PRANC / SeedLM / NOLA seed weights
A18 | 6 | 5 | 4 | N | NEW | Karbasi neural associative memory; memory layers

TOP3:
- A02: You could build and measure it directly. It goes after the real bottleneck on 12 GB (KV memory for long context), and the rate-distortion criterion based on attention-output error is a sound, testable idea.
- A12: A cheap explicit entity/state graph aimed at a weakness small transformers really have (tracking state over many transfers). It has a clear auxiliary loss and an obvious benchmark.
- A16: Growing long-range heads where statistical tests say they are needed is a new way to allocate attention compute, and it is easy to test against sliding-window baselines.

NOTE: Almost every answer avoided the listed families, but most of the novelty is in the cross-domain framing (SLAM, unit commitment, population genetics, video codecs, surveying) rather than the mechanism. Several turn out to be existing methods (RHO-LOSS, IIT, PRANC/SeedLM, MMI reranking), and only a few address the 3060's memory and bandwidth limits directly.