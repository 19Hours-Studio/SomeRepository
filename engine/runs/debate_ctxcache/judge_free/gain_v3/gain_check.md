# Gain check of answer.md (round 3)

Reproduction: `round3/trace4.py`, rerun on the 441 downloaded trajectories plus the Claude Opus 4.6 trajectory, gives output byte-identical to `trace4.out`.

Findings:
- The baseline (mini-SWE-agent, append-only, exact prefix caching) already gets 99.4% hits on re-sent tokens. The question's "~100% hits" target is already met there, so the open question is cost.
- Batching (−5.7% to −8.8%):
  - Parallel tool calls are an existing provider/harness feature (prior art).
  - The harness prompt in these trajectories already says "You can make MULTIPLE tool calls in a single response when the commands are independent" and gives an example. Even so, 19,514 of 19,514 responses contain exactly one tool call.
  - So prompting, the client-side mechanism the answer offers, was already tried here and gave 0%. The saving is an upper bound that depends on enforcement, and the answer does not specify that enforcement. Quality is untested.
- Back-references (−3.7%): measured on real traces. The ≥20-character line-dedup rule, with a 12-token cost per run, is conservative. This is the only new measured saving over best practice. Quality is untested. Related prior art is observation masking (Lindenbauer et al. 2025, about −50% vs a raw agent on SWE-bench Verified), which the answer does not cite.
- Errata −32.6%: synthetic, and measured against an in-place-mutation baseline that is already known to be bad practice (Manus guidance). Against append-full it is −9.6%, also synthetic.
- RAG first-seen −36% to −44%: synthetic, and not information-matched (final context 1.8–2.5x larger).
- Span ops: simulation only, and the gain is 0 on the real traces.
- Selective 1h TTL: unverified.
- Operator items: prior art.
- No output-quality measurement on any model.

Honest gain: about −4% of total cost (back-references, measured, quality unverified). The −12% figure needs batching that this model did not do under the existing prompt.
