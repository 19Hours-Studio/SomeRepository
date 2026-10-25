# eval_g2/c2 gate notes (Idea 1: popularity-ordered probe-routed KV reuse)
- gate_c2.py: 100k chunks, top-5 Zipf, 100k req. Known-answer check: identical requests -> reuse 0.999 (printed 0.01 is /N scaling with N=100k vs 1k reqs).
  doc-token exact reuse hash-canonical / popularity / chunk-level KV hit:
  s1.05 inf .201/.448/.890; W1k .100/.337/.646 | s1.2 inf .295/.598/.933; W1k .153/.477/.793 | s1.5 inf .607/.818/.980; W1k .354/.696/.930
- chain_c2.py (Archetype C shares: prefill 55 at baseline, other 45 fixed; prefill ∝ uncached tokens; blend = 15% recompute + 1/32 layer-1 probe; missing chunks fully prefilled):
  whole-bill ratio vs hash-canonical APC at m=0.25: 1.27-1.44; at m=0: 1.32-1.52; m allowed for 1.5x: <=0.03-0.04 in 2/6 regimes, none in 4/6.
  Prefill-only ratio at m=0.25: 1.62-2.24 (the idea's 1.46-1.55 is closer to a prefill-only figure than a whole-bill one).
- Popularity ordering alone (m=1) gives 1.14-1.33x; if the baseline already adopts it, the blending/probe increment is smaller still.
- Quality: probe recall and blended-path quality not measurable here (HF blocked); needs 2WikiMQA/MuSiQue + long-context runs vs full recompute.
