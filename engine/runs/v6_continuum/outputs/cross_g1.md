Three combined designs follow, one per pair. All figures are my estimates and use 4.5-bit weights.

- **Pair 1 (fixed):** B's stacked DRAM replaces A's SRAM, which removes A's density gap. Hybrid-bonded DRAM reaches ~0.1–0.2 Gb/mm², against 14.2 Mb/mm² for shipped dense SRAM (FACT 1, ~7–14× denser). UniIC's 135 GB/s/Gb bandwidth (FACT 8) also covers the speed target. A 39 GB set of 70B weights gives 42 TB/s, against 39 TB/s needed for 1,000 tok/s/user.
- **Pair 2 (partly fixed):** B's pipelining lets A's capacity spread over twice as many smaller packages. Each package then holds 80 GB, which is at the mature limit. Current per stack falls by half to about 340 A. Delivering that current through the stack still needs testing.
- **Pair 3 (best improvement, not a full fix):** At the true 14.2 Mb/mm², A needs 192 packages instead of 144. B's ~8–14 KB activation hops make the larger pipeline cheap. The net gain holds only if the extra HBM is filled with KV cache.

=== IDEAS ===
IDEA 1
NAME: Stacked-eDRAM pipeline chiplet packages
MECHANISM: Each ~100 mm² N6 logic chiplet carries a hybrid-bonded multilayer embedded-DRAM stack instead of on-die SRAM. The stack delivers ~135 GB/s per Gbit at ~0.66 pJ/bit, and its density is about 7–14× that of dense SRAM. Thirty-two chiplets sit on each organic package. A compiler pipelines the layers so that only ~8 KB of activations per token crosses the package links. Weights and KV cache stay resident in the stacked DRAM. For a 70B model, 39 GB of weights spread over 312 Gbit yields ~42 TB/s, against ~39 TB/s needed for 1,000 tok/s/user.
VALUE: It serves a 70B model at ~1,000 tok/s/user with no HBM and no CoWoS. Its cost per GB no longer depends on an SRAM density that no one has shipped.

IDEA 2
NAME: Half-size DRAM-on-logic pipeline packages
MECHANISM: The design targets decode for sparse-MoE LLMs. Each package has two N2 logic chiplets, each hybrid-bonded to a 4-high DRAM stack, for 80 GB at 32 TB/s and ~1 kW per package. Layers are pipelined across twice as many packages. Each hop carries only ~14 KB of activations per token, so link energy is under 1% of the energy spent reading DRAM. The 80 GB per package is within mature hybrid-bonding capacity. Current per stack falls by half, to about 340 A.
VALUE: It keeps the modelled ~2.2–2.7× tokens/s per kW over Rubin on GQA models. Each package stays within the capacity and current limits that have already been shown.

IDEA 3
NAME: Wider-pipeline SRAM-weight HBM-KV domain
MECHANISM: Each compute die sits face-to-face on an SRAM base die at a realistic ~14 Mb/mm², which gives ~1.4 GB per die and ~2.8 GB per package. The 545 GB of model weights are pinned across a 192-package pipeline instead of 144, with ~14 KB of activations crossing each hop. Each package's HBM holds only KV cache. The 33% larger HBM pool raises the number of concurrent users, which offsets the cost of the extra packages.
VALUE: The weight-in-SRAM, KV-in-HBM split fits at shipped SRAM densities. It keeps a ~1.1–1.4× per-MW advantage at interactive speeds, but only if the extra KV capacity is filled with users.