# eval_g2_re r1 recheck
Own sims in sim.py (Zipf 100k chunks, 5 docs, popularity order, window N requests). Anthropic multipliers 0.1/1.25/2.0.
Idea1 gated single-breakpoint: ratio vs uncached 1.01-1.44 (claim 1.33/1.5/1.9); margin 0.58-0.91.
Idea2: Mooncake rewrite ceilings 1.112x/1.081x (FACT 20/23) vs 1.15x claimed: margin 0.94-0.97 (on gain: 0.75/0.54).
Idea3: doc-token hit 0.337-0.818 (FACT 29, reproduced 0.338-0.713 at 1k window) vs ~0.95 target.
Idea4: max leaf-path P per window 0.000-0.083 at 10-100 req/window vs 0.087 break-even.
Idea5: m_max for 1.5x 0.15-0.25 in 3/6 regimes, none in 3 (45 fixed/55 prefill model).
