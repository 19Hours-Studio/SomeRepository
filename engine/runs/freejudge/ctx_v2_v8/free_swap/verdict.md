**A is clearly better.** I ran both sides' scripts again from copies, and every number in both answers came out the same. So neither answer misquotes its own outputs. What separates them is how strong the evidence is and how good the baselines are.

**Evidence and baselines.**
- **A** works from 42 real Claude Sonnet 4 SWE-agent sessions on SWE-bench Verified, re-tokenized with a real Claude tokenizer (the legacy one).
  - It compares against the strongest current option in each setting:
    - Claude Code's whole-file re-read stub;
    - Anthropic's `clear_tool_uses` context editing, swept over its full set of settings;
    - vLLM's official suffix-decoding code, tuned, with FP8 KV and cascade attention included in the baseline.
  - It also withdraws its own earlier drafter result after finding that the baseline it had used was too weak. That kind of self-correction is a good sign.
- **B** models a synthetic 50-turn agent. Its only replay uses 3 small demo trajectories, with token counts guessed as characters ÷ 4 and a median observation of 65 tokens.
  - Its main measured result, "server splice gives 0.62× input cost", is compared with append-only and naive elision. It is not compared with the provider's context editing, which already exists.
  - The splice itself is approximate, and its quality is untested.

**What each adds beyond prior art.**
- **A's main idea** ("reference, don't repeat") works on the client side and keeps all the information. Any run of 4 or more lines already sent in the request is replaced by a pointer. I read `dedup.py`. Line numbers are part of each match and the rewrite is saved once, so the cached prefix stays intact. Repeated text is 18.1% of the final context. Since cache reads and writes are 78% of the bill, a bill of 0.881× is consistent with that, against 0.993× for the existing stub.
  - A is honest about the limits:
    - its hit rate is already 97%;
    - its exact gains are modest;
    - its large runner-side gains (0.53–0.60× with sparse attention) apply only at long context, and their quality on agent tasks has not been tested.
- **B's main content** is the cache-stable layout:
  - append-only errata;
  - a volatile tail at the end;
  - ordering blocks by p/((1−p)·s), where p is the chance a block changes and s its size;
  - ski-rental compaction.
  - Most of this is already known (Manus, Anthropic's docs, *Don't Break the Cache*). The new ordering rule beats the usual one by a median of only 1%. Its 98% hit rate comes from a made-up layout. A also includes all of B's ideas 1–4.

**What neither can do.** Neither answer gets close to 100% exact hits after an in-place middle edit. Both say so correctly.

Quality claims for every idea in both answers still need a real model. Neither answer ran a resolve-rate test, so the agent-task gains are unproven in both.

WINNER: A
HOW MUCH BETTER: By a wide margin. A includes everything B has, then adds a new exact method measured on real traces, plus fair, tuned baselines and honest self-corrections. B's numbers mostly come from synthetic models or toy traces, and its approximate splice is compared only with weak baselines.
REAL GAIN A: About a 12% cut in the API bill (0.881× against 0.993× for the best existing re-read stub) while keeping all information, provided resolve rate holds up. Batched clearing, which drops content on purpose, gives about 0.80× against about 1.0× for Anthropic's context editing at keep 10. On a self-hosted runner the exact gain is about 0.88× over tuned suffix decoding. Larger runner gains are approximate and unverified.
REAL GAIN B: Close to none that is verified. Its layout advice is mostly prior art, and the new ordering rule is about 1% better at the median. Its 0.62× splice figure is approximate, comes from tiny traces, and is not compared with the provider's existing context editing.