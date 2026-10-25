Pair 1 and Pair 2 are only partly fixed by their B mechanisms. The numbers say so below. Pair 3 changes the most: B's "don't move reused spans" principle, applied on the client, brings in a cost that keep-alive alone can't touch.

- **Pair 1:** Canonical order gives 15–50% exact-prefix reuse (FACT 5). The recovered quality gap rises from 0.53 to 0.53 + p·0.47, about 0.60–0.77 at p = 0.15–0.5. That is still short of 0.95. The real gain is that a gate failure no longer costs a full recompute. It costs (1−p), about 50–85% of full compute.
- **Pair 2:** The shadow gate makes the disputed multi-hop loss measurable and bounded, but it does not remove the loss. Suppose 30% of traffic fails the gate. Cost is then about 0.7·0.156 + 0.3·1 + 0.01 ≈ 0.42 of full compute, against 0.83 for prefix caching. That is about 2×, with quality at the SLO.
- **Pair 3:** A uniform-position edit costs 6.11× a cached turn, while an appended erratum costs 1.022× (FACT 6). Assume 20% of turns contain mid-prompt edits (my assumption, not measured). A turn then averages 2.02 → 1.00, a 2.0× saving. Combined with the 1.18× from keep-alive, the total is about 2.4×, client-only. This clears the threshold that A needed f ≈ 0.8 to reach. Quality risk is low: appended corrections are robust (FACT 18). Test it by replaying logged edits as errata against in-place edits and comparing the KL of the outputs.

Still not reachable at about 100% with full quality: multi-hop reasoning over reordered or blended chunks (repair recovers 0.6–0.77 at best), and mid-prompt edits on third-party APIs when the edit must be applied in place.

=== IDEAS ===
IDEA 1
NAME: Canonical-prefix fallback for blended KV
MECHANISM: Runs on your own stack or provider-side. Spans are stored by content hash in a rolling-hash, position-independent KV store and repaired with EPIC/CacheBlend. Retrieved documents are sorted canonically first, so 15–50% of tokens become lossless exact-prefix hits. When the shadow-KL gate rejects a blended request, it is recomputed only after the last canonically matched document, not from the start.
VALUE: The quality loss from blending is confined to the non-canonical remainder, raising the recovered multi-source gap to about 0.6–0.77, and exact fallback costs 50–85% of full prefill instead of 100%.

IDEA 2
NAME: SLO-gated canonical chunk blending
MECHANISM: Retrieved documents are sorted by stable ID so most reorders hit exactly. The remainder is assembled from per-chunk KV with a shared-system-prompt prefix (APE), plus EPIC and selective recompute. On 1% of traffic, a full recompute runs in shadow and the KL of the first 32 output tokens is compared. This learns the recompute ratio r per query type and document type, and routes the classes that fail, such as multi-hop, to exact recompute.
VALUE: The disputed multi-hop quality loss becomes a measured, bounded SLO, at about 0.42 of full compute even if 30% of traffic falls back, against 0.83 for prefix caching.

IDEA 3
NAME: Priced prefix-preserving client
MECHANISM: Runs client-only, against any API. The client fits a survival curve over the idle gaps of each session. It sends a 1-token keep-alive read only when P(return) × 1.25 × prefix exceeds 0.1 × prefix. Instead of editing earlier content in place, it appends errata that reference the original span, so the cached prefix never changes. It compacts and rewrites the prompt only when the accumulated errata cost more than one rewrite.
VALUE: Edited turns cost about 1.02× instead of 6.11× a cached turn, which together with keep-alive gives about a 2.4× lower bill with no server changes.