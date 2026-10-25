=== RECHECK ===
IDEA 1: per-user DRAM bandwidth while layers are pipelined | required 39 TB/s for one user at 1,000 tok/s, reading 39 GB of weights per token (arithmetic from the idea's own 39 GB) | available 1.32 TB/s per active chiplet, from 135 GB/s/Gb × 9.75 Gbit (UniIC VLSI 2023, FACT 8). The 42 TB/s total is reached only if all 32 chiplets serve one token at once. In a pipeline a token visits one stage at a time. | MARGIN 0.034

IDEA 2: DRAM areal density for 80 GB on 2 chiplets × 4 layers | required 0.20 Gb/mm² (640 Gb over 3,200 mm², using the assumed 400 mm² chiplet) | available 0.064 Gb/mm², the only measured hybrid-bonded logic-to-DRAM density (Niu et al., ISSCC 2022 title confirmed by search; affiliation not confirmed). Commodity HBM3E reaches ≥0.198 Gb/mm² (Micron 11×11 mm package, FACT 16), but that leaves no room for wide-I/O periphery or power TSVs. | MARGIN 0.32 (0.99 against commodity density)

IDEA 3: wide-I/O hybrid-bonded DRAM areal density per layer | required 0.10 Gb/mm² (the idea's own figure) | available 0.064 Gb/mm² (same measured source as Idea 2). Commodity density is higher, but the idea reserves half the layer for periphery and power TSVs. | MARGIN 0.64

IDEA 4: per-user decode speed with SRAM-resident weights pipelined layer by layer | required 1.0 ms/token step (1,000 tok/s). | available 1.65 ms, from L·F/P = 80 × 140 GFLOP / 6.8 PF, which is about 607 tok/s per user. This assumes 100% of peak FP8 compute and the idea's own 6.8 PF. | MARGIN 0.61

IDEA 5: share of Rubin HBM time per step spent reading weights, at 300 tok/s/user, with 545 GB spread over 72 packages | required 28.6% to reach the claimed 1.4× (1 − 1/1.4) | available 10.3%: 7.57 GB / 22 TB/s = 0.344 ms against a 3.33 ms step (FACT 12 for 22 TB/s; FACT 19). The maximum gain is 1.115×. | MARGIN 0.36. It is 1.13 against the low end of the claim (1.1×).

IDEA 6: same weight-read share of HBM time at 300 tok/s/user | required 29.1% for the claimed 1.41× at 8K (1 − 1/1.41) | available 10.3% (same arithmetic as Idea 5) | MARGIN 0.355

I ran only 2 searches, in parallel. They confirmed the 64 Mb/mm² paper title but not its affiliation, and found no 24Gb HBM3E die area. The other inputs are the idea statements and the supplied facts. I wrote the margins to `recheck.txt` in the working directory and committed nothing.

Sources:
- [MDPI: process-heterogeneous stacked eDRAM (cites the ISSCC 2022 64 Mb/mm² paper)](https://mdpi.com/2151526)
- [Micron HBM3E product brief](https://micron.net/content/dam/micron/global/public/documents/products/product-flyer/hbm3e-product-brief.pdf)