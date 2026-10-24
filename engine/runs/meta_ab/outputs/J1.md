SCORES
ID | O | C | V | R | BASIN | closest
A01 | 4 | 5 | 7 | N | NEW | MagicPIG LSH + PIM attention
A02 | 6 | 5 | 5 | N | NEW | Compiler-directed voltage-emergency prediction
A03 | 4 | 6 | 7 | N | NEW | Quest/SparQ top-k in HBM-PIM
A04 | 3 | 4 | 5 | N | NEW | TPU v4 optical circuit switches
A05 | 4 | 6 | 7 | N | NEW | PQCache, near-memory ANN search
A06 | 6 | 5 | 6 | N | NEW | Weight streaming over optical ring
A07 | 4 | 7 | 7 | N | NEW | PQ-LUT attention in HBM-PIM
A08 | 5 | 4 | 5 | N | NEW | AWGR wavelength-routed optical MoE
A09 | 6 | 6 | 6 | N | NEW | ABFT plus adaptive mixed precision
A10 | 5 | 5 | 6 | N | NEW | Error-bounded residual quantization correction
A11 | 2 | 6 | 5 | Y | NEW | LUT-NN / AQLM / MADDNESS
A12 | 3 | 5 | 6 | N | NEW | MoE on HBM-PIM (Duplex)
A13 | 3 | 4 | 5 | Y | NEW | Groq scheduled network + OCS
A14 | 3 | 6 | 5 | Y | NEW | MSB-first bit-serial early termination
A15 | 6 | 6 | 6 | N | NEW | SHARP in-network reduction, tree attention
A16 | 3 | 4 | 6 | N | NEW | HBM-PIM attention (AttAcc/NeuPIMs)
A17 | 2 | 4 | 6 | Y | NEW | FeFET 3D compute-in-memory
A18 | 2 | 6 | 5 | Y | NEW | LUT-NN codebook matmul

TOP3:
- A15: The switches merge partial attention results using the online-softmax rule as packets pass through. That cleanly removes the KV all-gather for very long contexts, and existing switch logic could test it.
- A02: It uses deterministic execution to remove the voltage guardband. Few people have explored this, it costs no extra area, and it builds on Groq-style determinism.
- A07: This is the most concrete version of the near-memory KV top-k idea. A team could prototype the query-to-codeword tables and in-stack table-lookup scoring on an HBM4 base die.

NOTE: Five answers (A01, A03, A05, A07, A16) are the same basin: approximate KV top-k inside the memory stack. Two more pairs are duplicates: codebook/LUT weights (A11, A18) and optical MoE or circuit-switched fabrics (A04, A08, A13). The set therefore covers only about 7 distinct mechanisms, and the error-bounded adaptive-precision ideas (A09, A10, A14) also overlap. None of the answers sets out target workloads or metrics, or a full-stack defence against Rubin, Ironwood, WSE-3 or the Groq LPU, as the question asks; each is a single mechanism rather than an architecture.