# Gate notes (c1)
Arithmetic: gate_calc.py -> gate_calc.out
Known-answer check: the script reproduces idea 4's own 62.8 GB and 5.0 PF.
Key new anchors:
- ISSCC 2022 (Niu et al., Alibaba): 64 Mb/mm2 hybrid-bonded logic-to-DRAM. This is the only measured HB logic-DRAM areal density found.
- TechInsights: D1b 16Gb commodity DRAM is 0.431-0.447 Gb/mm2.
- Micron HBM3E brief: 24GB 8-high in an 11x11 mm package, so a 24Gb core die is <=121 mm2, i.e. >=0.198 Gb/mm2.
- List prices for Llama 3.3 70B output: Groq $0.79/Mtok, Cerebras $1.20/Mtok (one source says ~$0.60).
Layer-serial bound: if a die or package holds only its own layers, per-user time = L * F/P_total. Aggregate compute or bandwidth is not per-user speed.
