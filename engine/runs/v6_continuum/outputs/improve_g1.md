=== IDEAS ===
IDEA 1
NAME: N6 SRAM-chiplet pipeline, NVFP4-sized
MECHANISM: Weights and KV cache stay entirely in SRAM, on ~100 mm² N6 chiplets with 32 per organic package, and a compiler pipelines layers across them. Only ~8 KB of activations per token crosses package links. The fix sizes the design to the measured 14.2 Mb/mm² of AMD's V-Cache die and applies it only to an 80 mm² SRAM region, with 20 mm² left for logic. That gives 142 MB per die. The design also stores 70B weights and KV in NVFP4 (4.5 bits), which is current Blackwell/Rubin practice, instead of FP8. Capacity needed drops from 111.6 GB to 62.8 GB for 31 users at 8K context, so the build is 448 dies in 14 packages, not 512 dies on an unshipped 17.5 Mb/mm². Compute is 6.8 PF FP8 against the 5.0 PF needed for 31×1,000 tok/s (margin 1.35). Under a 2× vendor markup the system price is ~$226k, or ~$3.5k/GB. That fails the old $/GB test, but that test was a stand-in for cost per token. The deciding number is now $/Mtok, which comes to ≈$0.068 including energy (14.6 kW).
VALUE: At measured SRAM density and a 2× vendor markup, it serves 70B at ~1,000 tok/s/user for ≈$0.068/Mtok. That is about GB300's ~$0.07/Mtok cost at ~20× the per-user speed, with no HBM or CoWoS. The cost margin is only ~1.03×, and it assumes 4-year, fully utilised amortisation.

IDEA 2
NAME: Half-density hybrid-bonded DRAM decode package
MECHANISM: The target is unchanged: decode for 1T-total/32B-active MoE at 8K–128K context, measured in tokens/s per kW at a per-user speed floor. The package has four ~400 mm² N2 logic chiplets, each hybrid-bonded onto a 4-high custom DRAM stack, with no HBM. The fix halves the DRAM areal density the design demands, from 0.20 Gb/mm² (commodity DRAM with no room left over) to 0.10 Gb/mm². That leaves half of each layer for SeDRAM-style wide I/O periphery and for the power TSVs that feed the logic above. Those TSVs need about 67k per chiplet at 10 mA each (667 A at 0.75 V), which is ~15% of a layer at 30 µm pitch. The package then holds 80 GB instead of 160 GB at the same 64 TB/s. That needs 100 GB/s/Gb against UniIC's measured 135, and energy is taken at the measured 0.88 pJ/bit (IEDM 2020), so DRAM power is 450 W and the package ~2.04 kW. Because decode throughput per package tends to BW ÷ KV bytes once weights are spread out, losing half the capacity costs only weight-amortisation. Against Rubin on the same roofline model, the gain is 2.13× tokens/s/kW at 32 packages and 2.36× at 64, at both 8K and 128K. At 16 packages it is 1.64×. The per-user ceiling rises to 800 tok/s (1.25 ms step).
VALUE: Modelled decode tokens per kW are ~2.1–2.4× Rubin for GQA MoE models, in scale-up domains of ≥32 packages, without needing 160 GB per package of unproven DRAM. MLA models still get only ~1.1–1.3×. The remaining unmeasured number is whether a hybrid-bonded wide-I/O DRAM reaches 0.10 Gb/mm².

IDEA 3
NAME: Stacked-SRAM weights, 224-package interactive tier
MECHANISM: Each compute die sits on an 800 mm² hybrid-bonded SRAM base die, and HBM4 (288 GB, 22 TB/s) carries only KV cache. The fix accepts the measured 14.2 Mb/mm² instead of 30 Mb/mm²: 2.84 GB raw per package, 2.56 GB after 10% for TSVs. The 545 GB of weights therefore need 213 packages, and the domain grows from 144 to 224. Per-package decode throughput is set by HBM bandwidth ÷ KV bytes, not by where the weights sit. So tokens/s per MW is unchanged by the larger domain. MoE all-to-all is ~14 MB per token, ≈0.6 TB/s per package, well under NVLink-6-class ~3.6 TB/s. The design is offered only for the ≥300 tok/s/user tier. There the per-MW gain of 1.41× (8K) and 1.58× (128K) still survives a 5–15% capex premium (base-die silicon is only ~$370 per package), giving 1.23–1.34× at 8K and 1.37–1.50× at 128K. At ≥100 tok/s/user the net is 0.97–1.09×, which is not a win, so that tier is dropped.
VALUE: It gives a modelled ~1.2–1.5× lower cost per token than Rubin NVL72 for interactive serving at ≥300 tok/s/user, at shipped SRAM density. The cost is a 224-package scale-up domain, still ~4.8× fewer packages than Groq LP30's 1,064. This is the smallest honest version: it does not beat Rubin at ≥100 tok/s/user.

=== NOTES ===
- **IDEA 1:**
  - **What changed:** the measured density now applies only to the SRAM part of each die (142 MB per die). Weights and KV are stored in NVFP4, which needs 62.8 GB. The build is 448 dies in 14 packages. The deciding metric moved from $/GB to $/Mtok under a 2× markup.
  - **New deciding number:** ≈$0.068/Mtok at 1,000 tok/s/user, a margin of about 1.03 against $0.07.
  - **Sources:** AMD V-Cache, 64 MB in 36 mm² (FACT 1, TechPowerUp ISSCC); the Llama-3-70B config; NVFP4 at 4.5 bits (user notes).
  - **Estimates, not sourced:** the $10k N6 wafer, the $7.5k per-package overhead, 25 W per die and $0.08/kWh.
  - **Caveat:** the cost margin is thin and depends on utilisation.
- **IDEA 2:**
  - **What changed:** the DRAM density the design needs is halved to 0.10 Gb/mm², which gives 80 GB per package. Energy is set to the measured 0.88 pJ/bit. The power-TSV area is now computed (15%). The domain is at least 32 packages.
  - **New deciding number:** 2.13× tokens/s/kW against Rubin at 32 packages (2.36× at 64). The bandwidth-density margin is 135/100 = 1.35.
  - **Sources:** UniIC SeDRAM at 135 GB/s/Gb and 0.66 pJ/bit (VLSI 2023), and at 34 GB/s/Gb and 0.88 pJ/bit (IEDM 2020) (FACT 8); Rubin at 288 GB and 22 TB/s (FACT 12).
  - **Not published:** SeDRAM's areal density. A search found only XMC's 64 MB–8 GB capacity range.
  - **Estimates, not sourced:** the TSV current limit and the TSV pitch.
- **IDEA 3:**
  - **What changed:** the measured SRAM density replaces 30 Mb/mm². The domain grows from 144 to 224 packages. The scope is cut to the ≥300 tok/s/user tier.
  - **New deciding number:** a net cost-per-token gain of 1.23–1.50×. This is the answer's own per-MW ratios divided by 1.05–1.15 for capex.
  - **Sources:** FACT 1 for density; the answer's own per-MW model; the NVLink-6 bandwidth is a vendor figure.
  - **Estimates, not sourced:** the wafer price and the SoIC premium.

All three numbers come from roofline and cost arithmetic, not from a simulator or silicon. Calculations are in `improve_calc.py` and `improve_calc.out`. The text above is also saved as `answer.md`. All files are in `/home/user/SomeRepository/engine/runs/v6_continuum/improve_g1/`, and nothing was committed.

Sources:
- [XMC on UniIC SeDRAM](https://xmcwh.com/en/site/details/300?details=1)
- [MDPI, stacked embedded DRAM via hybrid bonding](https://mdpi.com/2151526)
- [Chips and Cheese on the 9800X3D V-Cache](https://chipsandcheese.com/p/amds-9800x3d-2nd-generation-v-cache/comments)
- [Zen 5 on Wikipedia](https://en.wikipedia.org/wiki/Zen_5)
- [TechPowerUp on V-Cache at ISSCC](https://www.techpowerup.com/292256/amd-details-its-3d-v-cache-design-at-isscc)
- [chinaflashmarket on UniIC VLSI 2023](https://chinaflashmarket.com/a/179680)