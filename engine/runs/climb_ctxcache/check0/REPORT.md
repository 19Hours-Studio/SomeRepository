# Check of vs_ctxcache/baseline answer
Files: calc_orig.py (author's copy, reproduces every printed number), replay_fixed.py/.out, checks.py/.out.

## Decisive numbers
- Break-even 1238 / 50 turns: reproduce; correct incremental cost (rewrite replaces a 0.1x read) gives 1137 / 45. Conclusion unchanged.
- Replay 92.9% -> 99.75%, 604k -> 365k (-40%): reproduces for seed 0 only, and has a billing bug:
  each turn's new tool result + assistant output (2300 tok) is counted as a cache READ. It is new input (a 1.25x write).
  Fixed, 200 seeds: inplace 88.7% / 762k; erratum (1000 tok) 96.3% / 506k (-33.6%); erratum of full size (2300 tok) 96.3% / 548k (-28.0%).
  Edits to recent entries (mean 2 entries back): -0.9% (e=1000), +7.5% MORE expensive (e=2300).
  Floor with no edits at all = 96.3%: no append-growing session reaches ~100% token hit; the ~3.7% miss is new content.
- Ski-rental compaction never fires in the replay (erratum == erratum+ski); the "2x competitive" claim is not exercised.
- Hash-sorted doc order: one new doc invalidates 50% of the doc tokens on average; first-seen (append) order invalidates 0.
- Storage $/M tok-h (8.19 / 1.64 / 0.07), 320/160/69 KB/tok, 6.6 s PCIe: reproduce. Recompute $0.175/M ignores attention:
  $0.227 at 32k, $0.338 at 100k context -> DRAM break-even reuse interval 8-12 min, NVMe 3.5-5.2 h (answer undersells).
- Prior art missed for Idea 2: Leyline (arXiv 2606.01065) - explicit replace/remove-span directives with RoPE correction in SGLang (+11.2 pp hit rate);
  llama.cpp seq_rm/seq_add already removes spans by explicit API call.
