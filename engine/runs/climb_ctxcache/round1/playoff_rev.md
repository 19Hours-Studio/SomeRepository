All four answers reach the same basic conclusion. Once you only ever append to the prompt, about 96–97% of tokens already hit the cache. Most of the remaining bill is re-reading the cached context at 0.1x on every request, so the real saving comes from batching when old tool outputs get dropped, not from raising the hit rate. What separates the answers is how well that claim is supported.

**What I checked**
- **Re-runs:** I re-ran C3's 63-trace replay and C4's 200-trace clearing-rule replay. Both reproduce their saved outputs exactly, and C4's trace-file checksum matches.
- **Delta-view test:** C3 replaces lines the agent has already seen with short back-references ("delta views"), and claims this saves 19.4% on its traces. I applied C3's exact method to C4's newer traces (Claude Sonnet 4 with the current SWE-agent). There it saves only **3.4%**. Most of C3's gain comes from the old SWE-agent reprinting a 100-line file window after every edit, and C3 doesn't mention that. C4's own version of this test misses the file views shown after edits, so its −0.2% is slightly too low.
- **Batch clearing:** the two real-trace answers agree on how much batched clearing of old tool outputs saves against keeping everything: about −18% to −26%. C4's "−45%" headline is measured against the one-per-turn sliding-window clearing, which is a weak baseline. C4 does report the comparison against keeping everything too.

**Ranking**
1. **C4:** It uses the largest and most current sample (200 trajectories). It adds an offline-optimal schedule as a bound, a check that the model always sees at least what the sliding window shows, and a per-edit choice between appending a correction and rewriting in place. It is honest that the hit rate tops out at 97.1%. Its headline baseline is the main weakness.
2. **C3:** It is rigorous: confidence intervals, a cost breakdown, and a comparison against a threshold tuned in hindsight. Its baseline is the fairer one. But its headline −30.4% leans on delta views, and those don't carry over to a modern agent.
3. **C1:** The same core idea, with a clean closed-form batch size. But its headline −47.9% comes from a synthetic workload. On real recorded traces it saves 0%, and its longer real sessions are resampled from short demos.
4. **C2:** It has the most insightful framing: a ceiling on what any hit-rate method can save, batching tool calls into fewer requests, and the physical cost of a cache read. But its −63% needs the provider to cut its read price. Its batching factor comes from a single demo trajectory, and the change in agent behaviour isn't measured.

No answer measured output quality, because none could run a real model.

I saved my notes and check script in the current folder as `review_notes.md` and `check_delta_on_c4_traces.py`.

RANKING: C4 > C3 > C1 > C2
WHY: I re-ran C3's and C4's real-trace replays: both reproduce exactly and agree that batched clearing saves about 18–26% against keeping everything. Applying C3's delta-view method to C4's newer traces saved only 3.4%, not 19.4%, so C3's headline depends on old agent behaviour. That leaves C4's larger, current sample, offline-optimum bound and honest 97.1% ceiling slightly ahead. C1 rests mostly on synthetic or resampled data (0% on real recorded traces), and C2's −63% depends on a provider price change and a batching factor taken from one demo trajectory.