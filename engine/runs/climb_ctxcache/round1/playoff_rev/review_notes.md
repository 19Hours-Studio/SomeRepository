# Review notes
- C3 `lever/replay.py` and C4 `fix/rule.py` re-run: outputs identical to the shipped .out files; C4 trace sha256 OK.
- C3-style delta views (runs of >=3 already-seen lines vs any earlier view), applied to C4's 200 Claude-Sonnet-4 / SWE-agent 1.x traces
  (`check_delta_on_c4_traces.py`): append-only billed input -3.4% (C3 reports -19.4% on 2024 SWE-agent 0.x / Sonnet-3.5 traces).
  So most of C3's delta-view gain comes from old SWE-agent reprinting its 100-line window, not from a general property of agents.
- C4's own delta test misses "cat -n on a snippet of" edit outputs (regex), so its -0.2% is slightly too low (about -3.4%).
- Masking-schedule gain vs append-only agrees across C3 and C4: about -18% to -26%. C4's "-45%" is measured against sliding-window clearing, a weak baseline.
