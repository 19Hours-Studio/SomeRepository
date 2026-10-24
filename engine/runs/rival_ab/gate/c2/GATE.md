# Gate c2 — results (arithmetic in gate_calc.py / gate_calc.out)

Shared per-bit path model (pJ/bit): HBM3E device 3.44 (I/O 0.25) [arXiv 2602.18568];
host PHY+interposer 0.3 (est.), host NoC/L2 ~1.0 (est.) -> GPU path 4.74.
Base-die path: 3.19 + 0.2 local + 0.54 logic (GQA g=8, FP8, 0.22 pJ/FLOP from B200 1000 W / 4.5 PF) -> 3.93.
Ratio 1.21x per KV bit. KV-attributable energy at 16K = 180 mJ (differential of 107/242 mJ, arXiv 2605.11999).
Token-energy ratio vs best practice: 1.04–1.05.

| Idea | Killer margin | Chain ratio | Verdict |
|---|---|---|---|
| 1 Base-die FP4 KV | 0.80 (needs 1.5x/bit, gets ~1.2x) | ~1.05 (NVFP4 KV already on GPUs) | DEAD |
| 2 Attention in HBM4 base die | 0.5 (needs 2x bytes/s; TSV BW ≈ PHY BW) | ~1.05 | DEAD |
| 3 Half-HBM training die | 2.5 (dense: non-GEMM/FA ~6% vs 15% limit) | ≤1.10 at full BOM pass-through | DEAD (borderline) |
| 4 Attention inside memory base | 1.85 (0.54 vs ≤1 pJ/bit, GQA only; MLA 7.1) | ~1.05 (needs 1.6) | DEAD |
