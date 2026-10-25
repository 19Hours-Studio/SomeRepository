# eval_g1/c1 gate notes
- ttl_replay.py (Mooncake FAST25 conversation/toolagent traces, 512-tok blocks): hit inf-TTL 0.374/0.571, 5m 0.293/0.529, 1h = inf (trace ~1h long, censored).
  Input-cost ceiling of perfect TTL vs 5m: 1.112x / 1.081x (Anthropic 1.25/0.1 multipliers, free keep-alive assumed).
- pop_order_ttl.py (100k chunks, top-5 Zipf, 100k requests, TTL as W requests per 5 min, '4bp' = breakpoints after docs 2..5):
  Zipf1.05: inf 0.416->1.19x; W=1k 0.267->1.04x; W=100 0.156->0.95x
  Zipf1.2 : inf 0.589->1.42x; W=1k 0.449->1.22x; W=100 0.327->1.10x
  Zipf1.5 : inf 0.818->1.91x; W=1k 0.693->1.61x; W=100 0.579->1.40x
  reuse needed for 1.5x per request = 0.637; break-even 0.217.
- Idea 3: ratio vs APC+canonical order = (0.45+0.55(1-r))/(0.45+0.55(1-r)(1-0.85a)); need acceptance a>=0.77 (r=.15), 0.85 (r=.3), >1 (r=.5).
