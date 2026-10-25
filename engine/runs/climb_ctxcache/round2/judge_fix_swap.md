I'd pick **A**, and it's clearly better. B is the round-1 answer and A is its revision, so I compared them mainly on whether A's corrections hold up in the code and data.

**What I checked**
- **A's numbers match its outputs.** `billing2.out` and `decode_dilute.out` contain the figures A cites. I re-ran `spliceq_sum.py` and its output was byte-identical to the stored file. I also checked the decode-compute figure by hand: about 0.24 GPU-hours for 2.7M output tokens on a 70B model at 45% MFU, which is right.
- **B's headline compares against a weak baseline.** The 45–47% saving is measured against sliding-window clearing, which costs 39.7% *more* than just appending everything. Against append-only (what the agent actually ran), B's horizon rule saves 23.7%. SWE-agent's existing `polling=10` setting already saves 23.2%, so the rule adds about 0.5 points over existing practice.
- **B misses Anthropic's 20-block lookback.** A's breakpoint model (`billing2.out` (a)) shows that with only one breakpoint at the end of the prompt, B's horizon rule costs 55.9% more than exact billing. That puts it at **+19% against append-only**, worse than doing nothing. Placing four breakpoints brings every policy back to within 0.6–1.6% of exact billing. B's numbers silently assume that fix.
- **A measured splice quality; B didn't.** A checked its setup first: splicing tokens out and back in reproduces the cache to about 1e-5, the correct RoPE convention scores clearly better (NLL 3.24 vs 4.74), and the noise floor is KL 2.5e-8. The spliced cache's error against full recompute is KL 0.0128 with 97.9% top-1 agreement. That is about the size of moving the window by one output, and there is no measured harm on the real next message. Without the key shift the error is 33% larger. B only proposed this test.
- **A costed the splice honestly.** It counts GPU-hours including the key re-rotation and the decode weight compute, and it shows that a fixed refresh schedule throws away most of the gain. B's −58% is at API prices that no provider actually offers.

**Limits of A's evidence**
- The quality results come from a 135M model on contexts of about 1.5k tokens, not a frontier model at full trace length.
- A's own client-side gain over prior art is small.
- Neither answer reaches about 100% hit rate on non-identical prefixes, and both say so: the measured ceiling is 97.1% because new content is always a miss.

WINNER: A
MARGIN: clearly
WHY: I re-ran A's summaries and checked its billing and decode outputs. They show that B's headline is measured against a sliding-window baseline that costs more than append-only, and that B's "new" horizon rule only matches SWE-agent `polling` (−23.7% vs −23.2%). Under Anthropic's 20-block lookback with one breakpoint, B's rule costs 19% more than append-only, a flaw B never mentions. A also replaced B's untested splice-quality claim with a checked real-model measurement (KL about 0.013, 98% top-1, no NLL harm), though only on a 135M model.
REAL GAIN A: Client side, about 3.6% relative over SWE-agent `polling=10` (fixed 5k batch, −26.0% vs −23.2% against append-only), and only if breakpoints are placed for the lookback. On your own serving stack, the splice saves about 11–14 more points of GPU-hours (−33% to −42% vs −23% to −28%), with quality evidence only from a 135M model.
REAL GAIN B: About 0.5 points over existing SWE-agent `polling` (−23.7% vs −23.2% against append-only), and negative (+19% against append-only) under Anthropic's real single-breakpoint billing. The splice is unvalidated.