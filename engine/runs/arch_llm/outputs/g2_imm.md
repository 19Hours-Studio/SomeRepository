**1. Goals (from the center)**
- G1: More learning per FLOP. On this card the limit of about 5B tokens per week caps quality more than the architecture does.
- G2: Knowledge capacity. 200M dense weights cannot hold long-tail facts.
- G3: Tracking state across a long context, with calibrated uncertainty.

**2. Paradigm negated**
Mainstream LMs are one point-estimate network: every weight is fit by backpropagating next-token loss through the whole stack at every step, and the model carries one deterministic hidden state. Three mechanisms are therefore forbidden: backprop through the whole stack on every step, a single deterministic state, and adding capacity only by gradient descent.

**4. Mechanisms from the periphery**
- G1, from molecular dynamics: RESPA multiple-time-stepping. Cheap fast forces are integrated every step. Expensive, smooth slow forces are applied only every k steps, as a k-scaled impulse, and the long-run dynamics are preserved.
- G2, from immunology: germinal-center affinity maturation. A danger signal decides which antigen counts. Clones compete for limited T-cell help, and only helped clones expand. Their mutation rate falls as affinity rises. Unhelped clones die, and clones that keep winning become memory cells.
- G3, from numerical weather prediction: the ensemble Kalman filter. It forecasts an ensemble of states and estimates their sample covariance. It then moves every member toward the observations, with localization and inflation.

**5. Honesty check**
1. Closest work: FreezeOut and other ways of skipping gradients for some layers, plus interlocking backprop. Difference: the full gradient is applied as a k-scaled impulse on a fixed fast/slow split, as in RESPA, rather than layers being frozen or trained greedily. Kept, but it is the nearest to prior work.
2. Closest work: kNN-LM, CLONALG/AIRS and growing neural gas. Against the forbidden families: there is no corpus index (NGRAMIDX), no cached residuals (COMPCACHE) and no frozen teacher (PRIORRES). Clones are added only on surprise and selected competitively without gradients. Kept.
3. Closest work: PF-RNN, the Recurrent Memory Transformer and Kalman-filter layers. Difference: a closed-form EnKF update with no parameters, run on an ensemble of memories using batch rows that are idle during decoding. Kept.

=== IDEAS ===
IDEA 1
NAME: Multiple-Time-Step Split Training
MECHANISM: A 350M transformer runs a full forward pass every step, but backprops only through its top 3 layers, embeddings and readout. This is the cheap fast force. Every k=4 steps it runs one full end-to-end backward pass, and the gradient for the lower layers is applied as a k-scaled impulse, as in RESPA, with momentum split so the average force stays correct. Lower-layer activations from the fast steps need no stored gradients. That cuts both memory and backward FLOPs, to roughly 1.7 compute units per step instead of 3, so about 1.7× more tokens per week fit on 12 GB.
VALUE: On the same card it trains a larger model on more tokens than a transformer that backprops through the whole stack every step.

IDEA 2
NAME: Germinal-Center Clone Memory
MECHANISM: A 150M backbone sits beside a repertoire in VRAM of up to 8M clones. Each clone is an int8 64-d receptor plus a sparse 4-token logit payload, about 640 MB in total. At positions where surprisal exceeds a running threshold (the danger signal), the layer-8 state acts as the antigen. Clones that bind it compete, and only the one whose payload most lowers that token's loss is "helped". Helped clones divide, and the mutation noise on their receptors shrinks as their affinity rises. Clones that go unhelped for N presentations die, and clones that keep winning freeze as memory cells. Selection uses only forward passes and integer arithmetic, so capacity grows where the data is surprising at almost no FLOP cost.
VALUE: It stores long-tail facts one-shot and adds capacity on demand, far beyond what 150M gradient-fit weights can hold.

IDEA 3
NAME: Ensemble-Kalman Assimilated Memory
MECHANISM: A 200M transformer with a 512-token window carries a 32-slot memory from chunk to chunk, kept as 16 perturbed ensemble members that run as batch rows. This is nearly free, because decoding on the RTX 3060 is bandwidth-bound and one read of the weights serves all 16 rows. After each chunk, every member forecasts a summary embedding of it. The actual chunk's embedding is the observation, and a closed-form EnKF update (localized covariance, inflation) moves each member by K(y − Hx). Only the forecast and observation networks are trained, by backprop over short windows. The ensemble spread drives calibration and triggers re-reading, and running it as a smoother lets later evidence revise earlier entity states.
VALUE: It tracks state across long documents while keeping alternative readings alive and reporting its own uncertainty, which a same-budget model with one deterministic state cannot do.