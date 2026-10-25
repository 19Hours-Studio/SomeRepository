**Candidates**
1. Always use the 1-hour TTL | P 0.35
2. Fixed keep-alive ping every 4.5 min | P 0.30
3. Append-only context and stable header | P 0.60 (this is already the baseline)
4. Self-hosted chunk-KV blending | P 0.50 (another direction covers it)
5. Speculative pre-write of the predicted next suffix | P 0.12 (it moves latency, not cost, because the write still costs 1.25×)
6. Keep-alive controller driven by measured idle-gap statistics | P 0.08
7. Write-anchor audit plus write-skipping for tokens that are never read again | P 0.06
8. Provider-side shared cache for public content, billed per content hash | P 0.07

I develop candidates 6–8.

**Arithmetic used throughout.** Writes are 47% of the bill at $3.75/MTok, so about 8% of input tokens are written. A full rewrite of a 100k-token prefix costs 1.25 × 100k. Keeping it alive costs 0.1 × 100k per 5-minute window, so pinging pays for up to about 12 windows (about 1 hour).

**Scope.** None of these three covers a middle edit, an insertion, a changed early tool output or reordering. Under exact-prefix APIs, those cases stay uncached. This direction touches only the write term. Even a 10× cut of that term gives at most 1.73×, so the 3× target also needs the read term, which is outside this direction.

**Quality and testing.** All three reuse a bit-identical prefix, so output quality is unchanged. To test, diff the `cache_creation_input_tokens` field in the API's usage data against a replayed trace.

=== IDEAS ===
IDEA 1
NAME: Return-hazard priced keep-alive
MECHANISM: The client logs the gaps between turns per user and per tool, including long test runs. From this it fits a survival curve, S(t) = the probability the user has not yet returned after t minutes. Just before a 5-minute expiry, it sends a 1-output-token read of the whole prefix only if the expected cost of rewriting (P(return soon) × 1.25 × prefix) exceeds 0.1 × prefix. It uses the 1-hour TTL only on the stable header when parallel sub-agents will read it. The closest prior art is fixed keep-alive scripts and the blanket 1-hour TTL. Those either ping dead sessions forever or pay +0.75× on every write, whereas this rule prices each gap. Deciding quantity: the share f of write tokens that are rewrites after expiry. If f = 0.4, the saving is about 15% of the bill (about 1.18×). It runs client-only and adds roughly zero latency; time-to-first-token after an idle gap also improves.
VALUE: It removes rewrites after expiry and during tool waits for about 0.1× per window, without changing output.

IDEA 2
NAME: Write-anchor audit and skip
MECHANISM: The client scans usage logs for write spikes larger than half the context. These are full rewrites caused by a turn adding more than about 20 blocks (for example, parallel tool results) past the provider's lookback limit. It fixes them by always keeping a second breakpoint at the end of the previous request and by merging tool-result blocks. It also places tokens that will never be read again after the last breakpoint, so they are billed at 1.0× instead of 1.25×. Examples are a sub-agent's final call and outputs that are about to be cleared. The closest prior art is Anthropic's breakpoint guidance, which states the lookback rule but does not detect or price the misses. Deciding quantity: the miss rate per turn. At 5k new tokens per turn, one 100k-token miss every 50 turns adds 40% to the write term.
VALUE: It removes hidden full-prefix rewrites, which can be a large share of the 47% write term.

IDEA 3
NAME: Per-hash public prefix pool
MECHANISM: The provider keeps one KV entry for byte-identical content that has been registered as public: widely used agent system prompts, tool schemas and public documentation. The entry is keyed by a hash of the content plus the model version. The first write is amortised across tenants, so every tenant pays only the 0.1× read rate plus a small per-hash fee. Entries are admitted only once at least k tenants use them, and latency is padded, which blocks the cross-tenant timing leak found in prompt-cache audits. The closest prior art is per-organisation isolation by Anthropic and OpenAI. That isolation exists for privacy, and the privacy reason does not apply to content that is public by declaration. Deciding quantity: the share of written tokens that are public across tenants. An assumed 20k-token header in a 250k-token-write session gives about 3% of the bill. The share is larger for short sub-agent calls. It runs provider-side only, and the extra storage is one copy per hash.
VALUE: It removes cold-start and post-expiry writes of the shared header for every tenant.