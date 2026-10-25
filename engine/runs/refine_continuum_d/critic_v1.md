The `sens8` re-run has now finished, and it agrees with the author's results.

- **Byte-identical:** all 64 lines of the author's `sens8.txt` match my run exactly, including the p = 0.6 rows (128K: 1.11 / 1.38 / 2.60 / 9.06 / 98.37).
- **Rows the author's run never reached:** it hit the 10-minute limit before the NVFP4-KV rows. My complete run produced them, and they match the answer's `fp4kv8` files: 128K 1.15 / 1.28 / 1.45 / 1.60 / 2.21, and 1M 1.05 / 1.13 / 1.39 / 1.97 / 3.42.

Every one of the author's outputs is now confirmed. I've updated `critique.md` to say so. None of the findings or numbers in my earlier review change.

HONEST GAIN: ~1.45× Rubin (trimmed) in output tok/s per provisioned W at ≥1,000 tok/s/user (128K, decode pod, modelled, with spares counted); 1.10 under the worst untested pair, ~1.14 vs same-date bottom-up Ultra, and the bulk tier is a tie (~1.0–1.1)