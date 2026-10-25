Continuum-9 holds up as about **1.6× Rubin and 1.2× a same-date 4-die Ultra at ≥1,000 tok/s/user, 128K context**. Correcting a mistake in the link model brings the number down from 1.63 to **1.59**, and the worst adverse pairs fall below the answer's floor. All of this is still model output. The full write-up is `critique.md`; scripts are in `src/` and outputs in `out/`.

## 1. Re-run and re-derived numbers

I copied the author's scripts into critic2 and re-ran `all9`, `sens9`, `c8pairs`, `om1m` and `sweep9b`. All five outputs match the author's files byte-for-byte.

| Claim | My result | Holds? |
|---|---|---|
| D(13), CSA link time | 4.96, 8.1 µs | ✓ |
| Cycle time T, speed, efficiency | 22.8 µs, 1,274 tok/s/user, 59.7 tok/s/W | ✓ |
| Against Rubin, all tiers | 1.22 / 1.35 / 1.63 / 1.81 / 2.67 | ✓ |
| Against 4-die bottom-up Ultra | 1.11 / 1.11 / 1.23 / 1.27 / 1.34 | ✓ |
| 90 adverse pairs at ≥1,000 | worst 1.19 (η = 0.5 + leakage ×2), median 1.41 | ✓ |
| Worst pair at ≥200 | 0.89 | ✓ |
| Continuum-8 worst pair | 1.10 | ✓ |
| 1M context, ω = 1 | 15.4 tok/s/W | ✓ |
| Tokens per HBM GB | 8.6× | ✓ |
| SoIC wafer passes per GW | 77k | ✓ |
| "1.15 × hid" link bytes | 1.21 × hid once the 1.07 imbalance is included | Minor slip; the 8.1 µs is right |

## 2. Unfair or unsupported points

1. **The residual hand-off between stages is missing (the decisive error).**
   - V4's config sets `hc_mult = 4`: its mHC residual keeps four copies of the hidden state.
   - Continuum puts one layer on each pipeline stage, so all four copies cross a package link at every layer. In BF16 that is 8 × hid bytes per position; the model charges 1 × hid.
   - Rubin keeps the residual on the GPU, so this cost falls on Continuum only.
   - At 64 lanes, ≥1,000 drops from **1.63 to 1.46**.
   - Re-optimised at 88 lanes:
     - against Rubin, **1.19 / 1.31 / 1.59 / 1.76 / 2.59**;
     - against Ultra, **1.08 / 1.08 / 1.20 / 1.23 / 1.30**.
   - The worst pair at ≥1,000 falls from 1.19 to **about 1.15** against Rubin. Against Ultra it is **0.87**, a loss.
   - At 1M context: 1.38 → 1.33 against Rubin at ≥1,000; 0.90 → 0.87 against Ultra at bulk.
   - With an FP32 residual: 1.52.
2. **The calibration condition is misstated.** "Continuum realises ≥62% of the GPU decode fraction" is the break-even point (1/1.63 = 0.61), where the ratio is 1.0. Getting 1.6× needs Continuum to realise the *same* fraction as GPUs.
3. **The Feynman risk is understated.** It is called "unspecified", but GTC 2026 reports describe stacked logic dies and custom HBM for 2028. That is Continuum's own main advantage, so the margin over a same-date competitor is at risk.
4. **Minor inconsistency.** §3.1 lists 120 W of host power per slot, but the model and the slot formula use 110 W.

**Where the answer undersells itself:**

- **The failure cost is 1,000× too high.** Re-prefilling 6.8k users × 128K tokens is 8.9e8 tokens × 12.5 mJ = 11 MJ. That is about **7 s** of the pod per failure, not 1.9 h, so the annual loss is **0.0027%, not 2.7%**. The KV mirror (10 W per slot, 0.44%) is not needed. Dropping it gives back +0.4%.
- **The memory margins are already in the model.** HBM "99.4% full" means 99.4% of a 90% cap, which is 89.5% of physical capacity. The CSA SRAM "95%" is about 86% of physical. The §8 row "cap at 90% → about −3%" counts that cap twice; strike it.
- **Cold spares are correct.** They cost 0 to 0.01.

## 3. Where a larger honest gain could be found

- **Biggest unused lever: per-layer collective latency.** It binds at the base point (c + τ = 22.8 µs > 2c = 22.1 µs). Cutting the fixed part from 7 µs to 4 µs, for example with a static point-to-point fabric between stage neighbours, gives:
  - 1.59 → **1.64** at ≥1,000;
  - 1.76 → 1.95 at ≥1,500;
  - 2.59 → 2.88 at ≥2,000.
  
  Going below 4 µs adds nothing. This is unproven and should be the kill target in test 2.
- **Best regime: the premium speed tiers (≥1,500 to 2,000 tok/s/user).** That is where the margin is largest and survives the worst pairs (about 1.8× Rubin). Against the same-date Ultra, though, it is only 1.23–1.30×.
- **Bulk speeds and 1M context are not wins.** Against Ultra they come out at 0.87–1.08.

HONEST GAIN: ~1.6× Rubin (1.59; 1.15 worst pair) and ~1.2× same-date 4-die Ultra in decode tok/s per provisioned W at ≥1,000 tok/s/user, 128K, model output only

Sources:
- [HF DeepSeek-V4-Pro-Base config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Pro-Base/blob/main/config.json)
- [NVIDIA NeMo DeepSeek-V4 config](https://docs.nvidia.com/nemo/automodel/nemo-automodel/nemo_automodel/components/models/deepseek_v4/config)
- [arXiv DeepSeek-V4](https://arxiv.org/pdf/2606.19348)
- [aman.ai V4 primer](https://aman.ai/primers/ai/deepseek-v4/)
- [Klockwood V4-Pro](https://glennklockwood.com/garden/DeepSeek-V4-Pro)
- [Tweaktown Feynman](https://www.tweaktown.com/news/110521/nvidia-updates-roadmap-with-new-details-on-its-next-gen-gpu-architecture-coming-in-2028/index.html)
- [igorsLAB Feynman stacking](https://www.igorslab.de/nvidia-stapelt-ab-2028-offenbar-erstmals-echte-logik-dies-in-feynman-und-damit-wird-aus-25d-ploetzlich-ein-thermischer-drahtseilakt/)
- [Wikipedia Feynman](https://en.wikipedia.org/wiki/Feynman_(microarchitecture))
- [hwbusters Feynman](https://hwbusters.com/news/nvidia-may-unveil-first-1-6nm-feynman-chips-at-gtc-2026/)

HONEST GAIN: ~1.6× Rubin (1.59 after the mHC hand-off fix; worst pair ~1.15) and ~1.2× same-date 4-die Ultra in decode tok/s per provisioned W at ≥1,000 tok/s/user, 128K — model output only