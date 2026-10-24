**Continuum** targets data-center frontier-model work: decode-heavy inference first, training second. It is judged on joules per token and TCO dollars per token at a fixed interactivity floor (≥200 tokens/s/user). No CONTEXT figures came with this request, so the comparisons below are qualitative.

**Physical and economic limits**
- **HBM bandwidth** grows slower than logic. GPUs and TPUs like Rubin and Ironwood stay bandwidth-bound in decode.
- **SRAM density** has nearly stopped scaling. Cerebras and Groq buy speed with wafers or racks of SRAM, at high cost per GB.
- **Switching energy** follows CV² per transition. Nobody recovers that charge.

**Architecture**
- **Compute and memory:** compute is cheap, while bytes and joules are expensive.
- **Interconnect:** co-packaged optics links reticle chiplets. Their traffic is mostly seeds and activations, not weights.
- **Numerics:** a seed-plus-low-rank weight format, with FP8 accumulation.
- **Programming model:** a JAX-like graph language. The compiler emits generator programs.
- **Packaging:** 2.5D, with a resonant-inductor interposer.
- **Power:** an adiabatic core at a 0.5–1 GHz clock rail.

**What must be true**
- Seed-based generation must keep frontier accuracy within about 1%.
- On-die inductors must reach a Q of about 10 or better.
- Local-loss training must close the gap with backpropagation at large scale. Today it does not.

Each idea below fails or succeeds on its own.

=== IDEAS ===
IDEA 1
NAME: Synthesized, Never-Fetched Weights
MECHANISM: Each weight tile is stored as a few bytes: a pseudo-random generator seed, a handful of mixing coefficients and a tiny low-rank correction. Hardware generators beside every tensor array expand these into full weights at the moment of use. Training updates only the coefficients and corrections, using gradients projected onto each seed's basis, and re-searches seeds when error grows.
VALUE: Turns the decode memory wall into spare compute, so a trillion-parameter model's weights fit in on-chip SRAM without wafer-scale cost or HBM bandwidth limits.

IDEA 2
NAME: Charge-Recycling Resonant Tensor Arrays
MECHANISM: The multiply-accumulate arrays use adiabatic logic driven by sinusoidal power-clocks. These come from LC resonators built into the package interposer. Charge moved onto the wires is steered back into the resonator rather than dumped to ground, recovering most of the energy each switching transition would otherwise waste. Slower clocks are offset by far wider arrays, because AI workloads are massively parallel and tolerate higher latency per operation.
VALUE: Breaks the CV² energy floor that all current accelerators pay, aiming for several-fold lower joules per operation at equal silicon area.

IDEA 3
NAME: Backprop-Free Pipeline Silicon
MECHANISM: Each chip trains its block of layers against a local learned objective, so no backward pass crosses chip boundaries. No full-model activations are stored, and no global all-reduce is needed. Chips stream activations forward only and keep short-lived local state. The hardware has no global synchronization and no large activation memory, and blocks retune their local objectives by checking periodically against a small end-to-end signal.
VALUE: Training scales linearly to millions of chips over cheap one-way optical links, removing the collective-communication and activation-memory costs that dominate frontier training clusters.