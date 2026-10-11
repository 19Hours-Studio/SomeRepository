**1. Structural engineering: rigidity counting (Maxwell–Calladine).** Engineers compute the rank of a frame's rigidity matrix. A zero mode, or floppy mechanism, means the frame is under-braced. A state of self-stress means the frame has redundant members that are fighting each other.
- *Port:* Treat each concept embedding as a joint. Treat each learned relation as a bar that holds two joints at a set distance or offset.
- *Closed loop:* A floppy mode means the concept is underdetermined, so the system creates a brace: a new anchoring relation that it gets by targeted querying or reading. A self-stress means the concept conflates two things, so the system splits the node along the eigenvector of the stress and gives each half the constraints it satisfies.
- *Honesty:* The closest work is TMS and graph-realization embeddings. TMS retracts beliefs; this splits and braces concepts using spectral structure, so it differs.

**2. Metrology: Allan variance.** For a clock, Allan deviation is plotted against averaging time τ. If it rises at some τ, there is hidden drift at that timescale.
- *Port:* Compute the Allan deviation of the model's prediction residuals over context position, at log-spaced τ.
- *Closed loop:* Wherever the deviation rises, the system creates a new recurrent state variable with time constant τ\*, feeds it the residual, and keeps it only if the rise flattens.
- *Honesty:* The closest work is multi-timescale SSMs and Clockwork RNNs. Their timescales are fixed in advance; here a noise-spectrum test grows them on demand.

**3. Population genetics: Hardy–Weinberg / Wahlund deficit.** A shortage of heterozygotes compared with Hardy–Weinberg proportions reveals that two hidden subpopulations have been pooled together.
- *Port:* Within each module, check whether paired feature co-activations match what the features' marginal frequencies predict.
- *Closed loop:* A Wahlund-type deficit splits the module into two children. The system assigns inputs to them by admixture inference and then fits a router between them.
- *Honesty:* The closest work is MoE and SAE polysemanticity analysis. MoE fixes its expert count in advance and SAEs only report. Here a population-genetics statistic decides when and where to split.

=== IDEAS ===
IDEA 1
NAME: Rigidity-Braced Concept Frames
MECHANISM: Concepts are joints and learned relations are bars. The system periodically computes the spectrum of the rigidity matrix. Floppy modes trigger acquisition of new bracing relations, and self-stress states split the node along the eigenvector of the stress. The concept frame is stored, and it grows or splits as these spectral tests fire.
VALUE: The system can find for itself which concepts are underdetermined and which are conflated, and repair them.

IDEA 2
NAME: Allan-Grown Memory Timescales
MECHANISM: The system computes the Allan deviation of its prediction residuals across context lag. When the deviation rises at τ\*, it creates a new recurrent state with time constant τ\*. It keeps that state only if the rise in deviation flattens afterwards.
VALUE: Memory gets exactly the timescales that the data's hidden drift requires.

IDEA 3
NAME: Wahlund-Split Module Growth
MECHANISM: For each module, the system tests whether paired feature co-activations match the products of their marginal frequencies. A heterozygote-like deficit indicates two pooled subpopulations, so the module splits in two, inputs are assigned by admixture inference, and a router is learned. Over time, splits build a lineage tree of specialized modules.
VALUE: The architecture adds specialists when a statistic shows a module has been mixing two input types.