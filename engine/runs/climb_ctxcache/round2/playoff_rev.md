**C1 is the better answer for the asker, though not by much.** Both answers' numbers match their output files. The parts I re-ran gave byte-identical results: C1's `copyspec.py` and `agent_gpu_spec.py`, and C2's `decode_dilute.py`.

**C1 (`fresh/`)**
- **Evidence base:** it is the only answer that measures how often the question's four cases happen in real traffic. It replays 269,681 Bailian production requests plus the 200 SWE-agent sessions.
  - Mid-prompt changes inside sessions cost 0.00% of input.
  - Content reused at a non-prefix position is 1.2% of chat input and 6.8% of API input. The exact cache ceilings are 46–71% on production traffic and 97.9% on agents.
  - So it tells the asker, with data, that a near-100% hit rate is impossible and that the mid-prompt case is a small prize.
- **What it offers instead:** savings that leave the output exactly as full recomputation would give, set out by where they can run.
  - Copy-speculation cuts GPU time by 21–34% on your own stack. It doesn't pay on MLA models, and C1 says so.
  - Keeping the KV of the model's own reply, so the next turn hits it, cuts billed input by 6–10%.
  - Choosing retention by cost saves money, and C1 shows that "keep everything" raises cost by 55–178% on MoE models.
  - OpenAI's `24h` retention flag cuts billed input by about 17% on chat and coder, with no server access needed.
- **Weaknesses:**
  - The headline idea (speculative decoding) is prior art (Prompt Lookup Decoding, SuffixDecoding) and sits next to caching rather than inside it.
  - The one approximate idea, reusing segments at a different position, has no quality measurement.
  - Its tokens-per-pass figure uses a proxy tokenizer.

**C2 (`fix/`)**
- **Strengths:**
  - It does what the question literally asks for one case: it splices deleted tool outputs out of the server-side KV cache.
  - It actually measures quality against full recomputation on a real model, SmolLM2-135M. KL divergence is 0.006–0.013, top-1 agreement about 98%, and there is no harm on the next message. Its sanity checks hold (splice and re-insert reproduces the cache to 1e-5; the right RoPE convention scores NLL 3.24 against 4.74).
  - It saves 33–42% of GPU-hours against append-only.
- **Weaknesses:**
  - It covers only agent tool-output deletion.
  - Its client-side gain is essentially SWE-agent's existing `polling` setting (about 3.6% better, relative).
  - The quality evidence is from a 135M model on about 1.5k-token contexts.
  - Per its own summary, the splice is worse than the one-output-longer window reference at 29 of 44 points, so "about the same size" is a little generous.
  - It cites an `idea4.out` file that isn't in its folder; the file exists only under `round1/`.
  - It opens with a reply to a reviewer ("changes in response to the check"), not with an answer for the asker.

RANKING: C1 > C2
WHY: I re-ran scripts from both answers and cross-checked every headline figure against their output files. All held up, and C2 still points to a file that isn't in its folder. C1 wins because it checks the question's premise against 270k real production requests: mid-prompt changes are worth about 0% inside sessions and 1–7% across requests. It then gives exact, measured savings for client-only use, your own stack, and the provider. C2 has the stronger quality experiment, but only for one case (deleting agent tool outputs), on a 135M model, and its client-side gain is mostly existing prior art.