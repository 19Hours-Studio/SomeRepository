# Review of answer.md (Continuum-7)

**Reproduction.** I reran all seven round-7 scripts (`check7`, `run7`, `run7b`, `run7c`, `run7d`, `run7e`, `calib7`). Every output matches the stored `.txt` byte for byte. The tables in the answer match `run7d.txt`, and the hand check in §4.2 is arithmetically correct.

**Like-for-like probe** (`probe_same_node_vs_ultra.py`). Figures are output tok/s per provisioned W, as a ratio, with every system on the same V/f law. Speed floors are tok/s/user.

| 128K context | ≥200 | ≥500 | ≥1,000 | ≥1,500 | ≥2,000 |
|---|---|---|---|---|---|
| Continuum vs Rubin NVL72 (answer's headline) | 1.17 | 1.29 | 1.57 | 1.70 | 2.47 |
| Same node vs Rubin | 1.06 | 1.17 | 1.42 | 1.56 | 2.25 |
| Same node, η 0.5, vs Rubin | 0.88 | 0.98 | 1.19 | 1.28 | 1.87 |
| Same node vs Rubin Ultra (bottom-up power) | 0.93 | 0.93 | 1.03 | 1.04 | 1.08 |
| Same node, η 0.5, vs Rubin Ultra | 0.78 | 0.78 | 0.86 | 0.86 | 0.90 |

At 1M context, same node vs Rubin Ultra: 0.82 / 0.82 / 0.99 / 1.13 / 1.21.

**Findings**
1. **Bulk speeds.** The gain at bulk speeds comes from the process node (N2 against N3P), not from the architecture. On the same node it is 1.06×. A 2028 Nvidia part would also be on N2/A16.
2. **Fair rival.** Continuum ships in 2028 at the earliest. The fair rival is Rubin Ultra, which SemiAnalysis reportedly says has slipped to 2028, or Feynman. Against Ultra on the same node and the same law, the result is a tie (0.93–1.08×) at 128K and a loss at 1M below 1,000 tok/s/user.
3. **Calibration.** The calibration has no anchor. The measured 12k tok/s/GPU is either 0.19× or 1.70× the model, depending on whether InferenceX counts input tokens, and that is unconfirmed. The calibration rows also do not change with p or τ, because the model picks k = 0, yet the measured run used MTP. No Continuum figure is anchored to a measurement.
4. **What does hold.** Tokens per HBM stack improve 3–4×, by simple arithmetic: the weights sit in SRAM. That is paid for with about 1.4× more leading-edge logic and about 68k SoIC passes per GW.
5. **Rubin+LPX baseline.** The model puts it at about 1/7 of plain Rubin. That is physically explainable: FP8 weights in 0.5 GB chips need about 3,500 LP30s. It does contradict Nvidia's projected claim of "up to 35× per MW", so this comparison should not be read as a real-world ranking.
