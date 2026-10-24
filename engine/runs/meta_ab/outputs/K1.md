SCORES
ID | O | C | V | R | BASIN | closest
B01 | 3 | 5 | 5 | N | NEW | Razor/ThUnderVolt + ABFT undervolting
B02 | 2 | 4 | 4 | Y | NEW | Dark silicon computational sprinting
B03 | 4 | 4 | 5 | N | NEW | Dynamic precision scaling, shadow sampling
B04 | 2 | 5 | 5 | Y | NEW | LUT-GEMM / T-MAC codebook lookup
B05 | 4 | 5 | 6 | N | NEW | In-DRAM LSH sparse attention
B06 | 6 | 4 | 6 | N | NEW | Optical broadcast weight sharing
B07 | 3 | 4 | 5 | N | NEW | TopoOpt / SiP-ML reconfigurable optics
B08 | 3 | 5 | 6 | N | NEW | AttAcc PIM attention + tiering
B09 | 6 | 5 | 7 | N | NEW | Optical weight broadcast, token-stationary
B10 | 2 | 5 | 6 | Y | NEW | AttAcc / NeuPIMs HBM-PIM attention
B11 | 4 | 6 | 7 | N | NEW | Quest/InfiniGen top-k in HBM base die
B12 | 4 | 5 | 5 | N | NEW | Mixed-precision residual recompute
B13 | 6 | 5 | 5 | N | NEW | Groq determinism + predictive voltage regulation
B14 | 3 | 5 | 5 | N | NEW | ABFT undervolting (B01 duplicate)
B15 | 3 | 4 | 6 | Y | NEW | SeedLM PRNG-seed weights
B16 | 3 | 4 | 5 | N | NEW | TPU OCS / circuit-switched photonics
B17 | 2 | 5 | 5 | Y | NEW | AQLM/LUT-GEMM codebook lookup
B18 | 3 | 4 | 7 | Y | NEW | N3XT monolithic BEOL RRAM
B19 | 3 | 5 | 6 | Y | NEW | QTIP trellis quantization, inline decode
B20 | 2 | 5 | 5 | Y | NEW | LUT-NN / codebook GEMM
B21 | 2 | 4 | 6 | Y | NEW | SeedLM
B22 | 5 | 3 | 7 | N | NEW | Adiabatic charge-recovery logic
B23 | 4 | 5 | 6 | N | NEW | FeFET CAM approximate attention
B24 | 4 | 4 | 5 | N | NEW | Expert parallelism + WDM routing
B25 | 4 | 5 | 6 | N | NEW | PQCache + in-bank PIM
B26 | 3 | 5 | 5 | N | NEW | Bit-serial MSB-first early termination
B27 | 5 | 5 | 6 | N | NEW | Optical weight broadcast (B09 variant)
B28 | 5 | 5 | 6 | N | NEW | ABFT + adaptive precision
B29 | 2 | 4 | 4 | Y | NEW | TPU v4 OCS, resident pipeline slices
B30 | 6 | 5 | 5 | N | NEW | Bit-serial early exit, decision-aware
B31 | 6 | 5 | 6 | N | NEW | SHARP in-network reduction + ring attention
B32 | 5 | 4 | 6 | N | NEW | Optical ring weight circulation
B33 | 3 | 6 | 6 | N | NEW | HBM base-die flash-decoding PIM
B34 | 2 | 6 | 5 | Y | NEW | LUT-GEMM codebook lookup
B35 | 3 | 5 | 6 | N | NEW | LSH sparse attention in HBM PIM
B36 | 3 | 4 | 6 | Y | NEW | Duplex / MoNDE MoE PIM
B37 | 4 | 5 | 6 | N | NEW | PQCache in HBM base die
B38 | 6 | 4 | 6 | N | NEW | Analog optical over-the-air aggregation
B39 | 4 | 6 | 7 | N | NEW | Top-k retrieval + flash-decoding PIM
B40 | 6 | 4 | 5 | N | NEW | FFN memoization / LUT-NN in NAND
B41 | 2 | 5 | 5 | Y | NEW | LUT-GEMM codebook lookup
B42 | 2 | 5 | 7 | Y | NEW | Hybrid-bonded DRAM-on-logic (SeDRAM)
B43 | 3 | 3 | 7 | Y | NEW | Decoupled greedy local learning
B44 | 3 | 5 | 6 | N | NEW | AttAcc PIM + H2O eviction
B45 | 3 | 4 | 7 | N | NEW | 3D FeFET compute-in-memory
B46 | 2 | 3 | 5 | Y | NEW | CXL memory pool with attention engines
B47 | 2 | 5 | 5 | Y | NEW | LUT-GEMM codebook lookup
B48 | 4 | 5 | 5 | N | NEW | Mixed-precision residual recompute (B12 variant)

TOP3:
- B09: Using passive optical fan-out to share each HBM weight read across many token-stationary chips goes straight at the economics of decode bandwidth, and it can be tested with existing photonics.
- B31: Merging partial attention with online softmax inside the switches is a clean, exact, buildable way to spread one context over many chips.
- B39: The HBM base-die design that combines top-k retrieval with exact flash-decoding partials is the most concrete and highest-value version of the crowded near-memory-attention idea.

NOTE: No family codes were provided, so every answer is marked NEW. About 70% of the answers fall into roughly six de facto families: codebook/LUT GEMM (B04/17/20/34/41/47), KV attention in HBM or DRAM (B05/08/10/11/25/33/35/37/39/44/46), optical weight broadcast (B06/09/27/32), ABFT undervolting or error-bounded precision (B01/03/12/14/28/48), seed-generated weights (B15/21), and reconfigurable optics for MoE (B07/16/24/29). Almost none of them commit to target metrics or defend themselves against Rubin, Ironwood or WSE-3 numbers, as the question asks.