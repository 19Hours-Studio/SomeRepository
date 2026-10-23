**The usual 8 answers:** provider prefix caching, append-only layout, vLLM/SGLang radix caches, cache-key routing, longer TTLs, CPU/SSD offload, CacheBlend/EPIC recompute, and APE/position re-encoding. **Shared paradigm:** make each new request's tokens match a stored KV state, either exactly or by repairing the approximation.

The three answers below instead change the request itself. They aim only at archetypes A, C and D. B's ceiling is 3.6x, so no answer can reach 3x there.

**Notes per answer**

1. **Patch log**
   - Covers middle edits, insertions and replaced tool output.
   - Hit rate is about 100% on the prefix.
   - In C, a mid-document edit now costs about 200 patch tokens instead of a 1.25× rewrite of about 25k tokens. That saves about $0.09 per edit.
   - Runs on the client only. It adds no storage and only patch-length latency.
   - Quality risk: the model may misapply stacked patches. Test it on edit-tracking QA (questions on edited facts) against a fully rewritten prompt, at 1–50 patches.

2. **Turn collapsing**
   - Targets A's cache reads, which are 54% of its cost.
   - Reads scale with turns times average context: 40 turns × 60k tokens is about $0.72 per task.
   - Cutting to 15 turns is my estimate, not measured. It would save about $0.45, roughly 35% of the task.
   - Runs on the client only. Latency per turn goes up, wall-clock time goes down.
   - Quality risk: the agent adapts less between steps. Test task success on SWE-bench at a matched budget.

3. **Canonical global order**
   - Targets D (own stack) and RAG reordering. Insertions and edits are not covered.
   - Hit rate depends on retrieval skew. Under Zipf-like popularity (Zipf is a long-tailed popularity distribution) I'd guess 40–70%, unmeasured. It does not reach 100%.
   - Runs on your own serving stack. It costs radix memory under the existing LMCache tiers.
   - Quality risk: document order affects answers (lost-in-the-middle). Test accuracy against relevance-ordered documents on NQ and HotpotQA.

**Cannot reach about 100% under these constraints:** new or reordered documents (B), and exact reuse after an arbitrary edit made inside the token stream. No exact method exists for these, because the KV of later tokens depends on all earlier tokens.

=== IDEAS ===
IDEA 1
NAME: Append-only patch log
MECHANISM: The client never edits earlier prompt text. It appends a compact patch instead, such as "doc X, §4 now reads …" or "tool output #12 is superseded by …", so the cached prefix stays byte-identical. Once the patches exceed a set fraction ε of the document, the client compacts them into one fresh cached copy. The closest prior art is Manus's append-only discipline, which forbids mid-prompt edits; this approach turns those edits into appends instead of forbidding them. The deciding quantity is how accurately the model applies patches as their number grows.
VALUE: Mid-document edits and replaced tool outputs no longer trigger 1.25× rewrites, so near-100% prefix hits are possible on hosted APIs with no model access.

IDEA 2
NAME: Read-cost-gated turn collapsing
MECHANISM: Read cost grows with turns times context length. The agent is therefore prompted to emit multi-step scripts or batched tool calls, and to stop and observe only when the predicted branch uncertainty is worth one more full context read. The closest prior art is CodeAct and parallel tool calling, which aim at task success. This approach adds explicit gating on cost per read. The deciding quantity is how much task success drops at 2–3x fewer turns.
VALUE: It cuts the dominant cache-read term of long agent sessions by about 2x, beyond what any hit-rate gain can do.

IDEA 3
NAME: Canonical global document order
MECHANISM: Every retrieved chunk is placed in one fixed corpus-wide order, such as popularity-ranked ID, not in per-query relevance order. Overlapping document sets then become shared prefixes in a radix cache, and requests are routed by their first document ID. The closest prior art is CacheWeaver and RAGCache, which order documents per request and miss when the same set arrives in another order. Here the order is fixed by the corpus, so a repeated set always forms the same prefix. The deciding quantity is the retrieval popularity skew.
VALUE: Prefill compute on reordered RAG requests is reused exactly on your own stack, with no attention approximation.