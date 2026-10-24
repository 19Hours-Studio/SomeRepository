SCORES
ID | O | C | V | R | BASIN | closest
B01 | 3 | 5 | 6 | Y | NEW | Razor undervolting with ABFT checksums
B02 | 3 | 4 | 4 | Y | NEW | Dark silicon, computational sprinting, activity migration
B03 | 4 | 4 | 5 | N | NEW | Dynamic precision scaling, shadow sampling
B04 | 3 | 6 | 5 | Y | NEW | LUT-GEMM / T-MAC codebook lookup
B05 | 4 | 5 | 6 | N | NEW | Reformer LSH plus DRAM-PIM
B06 | 6 | 4 | 6 | N | NEW | Optical broadcast weight sharing
B07 | 3 | 4 | 5 | Y | NEW | TPU OCS / TopoOpt reconfigurable topology
B08 | 4 | 5 | 6 | N | NEW | AttAcc / NeuPIMs KV PIM
B09 | 6 | 5 | 6 | N | NEW | Photonic broadcast, token-stationary batching
B10 | 2 | 5 | 6 | Y | NEW | AttAcc attention PIM
B11 | 4 | 6 | 6 | N | NEW | Quest/InfiniGen top-k in HBM base die
B12 | 4 | 5 | 5 | N | NEW | Mixed-precision recompute of outlier rows
B13 | 5 | 5 | 4 | N | NEW | Groq determinism plus predictive voltage regulation
B14 | 3 | 5 | 6 | Y | NEW | ABFT near-threshold timing speculation
B15 | 3 | 5 | 5 | Y | NEW | SeedLM PRNG-seed weights
B16 | 3 | 4 | 5 | Y | NEW | Compiler-scheduled optical circuit switching
B17 | 2 | 6 | 5 | Y | NEW | AQLM codebook quantization, LUT GEMM
B18 | 3 | 4 | 6 | Y | NEW | Monolithic 3D RRAM (N3XT)
B19 | 2 | 6 | 5 | Y | NEW | QTIP trellis-coded quantization decoder
B20 | 2 | 5 | 5 | Y | NEW | AQLM / LUT-based VQ inference
B21 | 2 | 5 | 5 | Y | NEW | SeedLM
B22 | 4 | 3 | 6 | Y | NEW | Adiabatic resonant-clock computing (Vaire)
B23 | 5 | 5 | 6 | N | NEW | FeFET CAM attention retrieval
B24 | 4 | 4 | 5 | N | NEW | Expert parallelism over WDM optics
B25 | 4 | 5 | 6 | N | NEW | PQ KV cache in DRAM-PIM
B26 | 4 | 5 | 5 | Y | NEW | MSB-first bit-serial early termination
B27 | 5 | 5 | 6 | N | NEW | Optical splitter weight broadcast
B28 | 5 | 5 | 5 | N | NEW | ABFT-guided adaptive precision
B29 | 3 | 4 | 5 | Y | NEW | OCS phase-reconfigured pipeline parallelism
B30 | 5 | 5 | 5 | N | NEW | Bit-serial interval arithmetic early exit
B31 | 6 | 6 | 6 | N | NEW | SHARP in-network reduction plus ring attention
B32 | 5 | 4 | 6 | N | NEW | Optical ring weight circulation
B33 | 3 | 6 | 6 | Y | NEW | HBM-PIM flash-decoding partials
B34 | 2 | 7 | 5 | Y | NEW | LUT-GEMM codebook lookup
B35 | 3 | 5 | 6 | N | NEW | LSH KV retrieval in HBM base die
B36 | 4 | 4 | 6 | N | NEW | Duplex / MoE DRAM-PIM
B37 | 4 | 6 | 6 | N | NEW | PQCache in HBM logic die
B38 | 6 | 4 | 6 | N | NEW | Analog over-the-air aggregation, optical
B39 | 4 | 6 | 6 | N | NEW | Quest plus flash-decoding in HBM PIM
B40 | 6 | 4 | 5 | N | NEW | FFN output memoization in NAND
B41 | 2 | 5 | 5 | Y | NEW | LUT-GEMM VQ inference
B42 | 2 | 4 | 7 | Y | NEW | Hybrid-bonded DRAM-on-logic stacking
B43 | 3 | 3 | 7 | Y | NEW | Decoupled greedy local learning
B44 | 2 | 5 | 6 | Y | NEW | AttAcc KV PIM
B45 | 2 | 4 | 6 | Y | NEW | FeFET analog compute-in-memory
B46 | 3 | 3 | 5 | Y | NEW | CXL memory pool with attention offload
B47 | 2 | 6 | 5 | Y | NEW | LUT-GEMM / T-MAC
B48 | 4 | 5 | 5 | N | NEW | Low-bit compute with bounded recompute

TOP3:
- B31: Merging online-softmax partials inside the switches is a clean, testable fix for spreading one context across many chips. It builds on existing in-network reduction rather than reinventing it.
- B09: Splitting one HBM weight read optically across a group of token-stationary chips attacks decode's weight-bandwidth limit directly. It also avoids wafer-scale SRAM costs.
- B30: Stopping a computation once the argmax or router choice is mathematically settled gives a certified way to save compute. That goes beyond plain bit-serial early termination.

NOTE: About 40% of the set falls into two crowded basins: KV-attention offloaded into HBM or DRAM logic (B05/08/10/11/25/33/35/37/39/44) and codebook/LUT weight quantization (B04/17/19/20/34/41/47). Undervolting with ABFT, optical weight broadcast and SeedLM-style seed weights each also show up more than once. None of the answers sets out target workloads and metrics, or compares itself against Rubin, Ironwood, WSE-3 or Groq, as the question required.