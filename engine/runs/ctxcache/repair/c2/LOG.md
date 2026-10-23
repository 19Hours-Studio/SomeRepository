# LOG (c2 repair) — one line per round
| round | idea | change | decisive number | result |
|---|---|---|---|---|
| 0 | both | prior-art check | Claude Code already appends file-change diffs as system-reminders (claudeissues #21650, #20850); Manus = append-only | the plain patch chain is shipped practice, so it must be judged against the chain, not only against inline rewrite |
| 1 | both | model.py: inline vs doc-last vs chain vs ledger, archetypes C/D/E | C, 3 edits: inline/chain 1.50; D (120k, 15 edits): 2.82; E: 3.04 | the cost works; the chain's patch depth per key reaches 3-7 (PI-LLM/DKI: accuracy on the latest value decays with update count) -> quality hazard |
| 2 | I1 | floating depth-1 ledger after the question, never kept in history | E: inline/ledger 4.57, within 6% of the no-edit floor, depth 1 by construction | WORKS in the repeated-edit regime |
| 2 | I2 | chain + depth cap 1 + ski-rental fold + free fold on TTL expiry | C 1.52x, D 2.66x vs inline; E only 2.95x (folds cost money) | WORKS for scattered edits; loses to I1 when the same keys are edited repeatedly |
| 3 | I1 | share-cap sweep 2/5/10/20% | C: cap 5% -> 1.16x, cap 10% -> 1.46x vs inline | use a 10% cap for document sessions |
| 3 | I2 | depth-cap sweep 1/2/3/inf | E: $0.114 / 0.087 / 0.077 / 0.070 | the depth cap is a direct price for quality; keep 1 for documents and hand repeated keys to the I1 ledger |
| 3 | both | TTL expiry 30% of gaps | D gain falls 2.6x -> 1.43x; C 1.5x -> 1.19x | the gain needs gaps under the TTL (or 1-h writes at 2x) |
| 3 | both | hit rate (D) | patched 96.4% token-weighted = 100% of reusable tokens; inline ~70.7% | the near-100% claim holds for edits and insertions only |
| 3 | both | eval size | McNemar, 3-pt drop, discordance 8-15%: 696-1306 paired questions | decides both ideas |
