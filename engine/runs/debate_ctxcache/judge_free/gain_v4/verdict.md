# Verdict on answer.md (round 4)

Reproduced: trace5.out, rag5.out, hitrate5.out all regenerate byte-identically (441 real trajectories).
Own check: sensitivity_check.py (boundary-recompute k, RAG pool/drift).

| Claim | Baseline used | vs best current practice | Status |
|---|---|---|---|
| Polling −29…−52% | per-step LastN (known cache-breaker) | −0.4% vs append-only; batching = Anthropic `clear_at_least`, SWE-agent `polling` | prior art, no gain |
| Span ops −42.5% | per-step LastN | −11…−14% vs batched clearing (k=32); −12% at k=128, −4% at k=512, +26% at k=2000 | modelled only, provider-side, quality untested; mechanism ≈ Budgeted KV-Cache Repair (2610.17338), KVEraser |
| RAG tail −35% | LangChain sys-prompt layout | tail = provider docs' "variable content last" | prior art |
| RAG cap12 −0.7…−20.5% vs tail | tail | +4…+5% (worse) with pool 200/1000 or drift 0.6 | not robust |
| RAG tail_span −30…−50% vs tail | tail | −16…−50% depending on synthetic params; −2…−46% at kb=256 | synthetic, provider, quality untested |
| Batching −9.7…−10.8% | single-command mini-SWE-agent | parallel tool calls are standard | replay estimate only, not new |
