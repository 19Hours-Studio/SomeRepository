# LOG — repair c2 (Continuum r2)
| round | idea | change | decisive number | result |
|---|---|---|---|---|
| 1 | I1 tiered KV | recompute vs FlashMLA-sparse baseline | HBM bytes/step 1.137 vs 1.055 GB -> 1.08x; energy/token 31.3 vs 31.7 mJ | bandwidth/energy claim FALSE (kill test confirmed) |
| 2 | I1 | reframe as capacity: idx 132B (scanned every step, 100/s touch rate) in HBM, latent 656B in LPDDR | users/HBM stack @128K: 19.6 vs 5.0 all-HBM Rubin (3.9x) | capacity win real |
| 3 | I1 | add best practice: Rubin+Vera with HiSparse LRU (87% hit) | Vera 17.9/stack vs Continuum 18.4/stack (1.03x); $/user 86-100 vs 102 (2026) | parity with best practice when top-k hit >=0.7 |
| 4 | I1 | hit-rate sweep; retarget to chips w/o big coherent host memory (TPU-class) | Continuum 1.9x/stack when hit<=0.4 (GVR raw overlap 35-50%); Ironwood+tier 47.7 vs 26.6 users/chip (1.8x), 89.5 w/ MTP (3.4x) | NICHE |
| 1 | I2 prefill die | fix threshold: ridge 17.5PF/1.4TB/s = 12,500 FLOP/B (idea said 300) | MoE expert-stationary act intensity fixed ~2F=4096 < ridge | LPDDR-only die memory-bound: 33.7% of compute @128K with 256 MB SRAM |
| 2 | I2 | whole-model NVFP4 replica (377 GB) per package in 512 GB LPDDR -> no EP all-to-all | CPX-like EP3 over 200 GB/s NIC: network-bound 30 ktok/s vs 76 compute | replica removes network bind |
| 3 | I2 | add hybrid-bonded SRAM token-tile buffer | >=0.75 GB/die -> compute-bound @128K, >=1.0 GB @32K; needs >=64K tokens/pass (~1 s) | parity with Rubin per PF, 0 HBM stacks |
| 4 | I2 | BOM/energy | $/ktok/s 115 vs Rubin 114 (2026), 187 (2027 HBM $1300) -> 1.0-1.6x; energy 23.8 vs 24.2 mJ/token | NICHE (throughput-tier long-context prefill when HBM is supply-bound) |
