I wrote `compress.py` and `decompress.py`. The official self-check gives a **score of 2.977**: 98,621 bytes of compressed data plus 2,796 bytes for xz -9 of `decompress.py`, against xz -9e's 301,956 bytes. The scorer confirmed that decompression gives back `data.log` byte for byte. Each step takes about 2 seconds, well under the 120 s limit.

**Approach:** each log line is split into its fields, and each field is coded with an adaptive arithmetic (range) coder written in pure Python. Both scripts share one model, so the compressor and decompressor make exactly the same predictions. While analysing the log I found that it is mostly random draws plus some per-client structure:

- **Timestamps** arrive at random intervals (a Poisson process), so they're coded with an exponential distribution whose mean is learned as it goes. This costs about 30.5 KB and is already at its theoretical minimum; it's the largest single cost.
- **IP address:** one bit says whether this line has the same IP as the previous line. If not, the IP is picked by how often it has appeared before. Each brand-new IP costs about 27 bits.
- **Per-IP memory:** the user agent and the cart user ID are predicted from that IP's earlier lines. The referer is almost always either `-` (about 30% of the time, at random) or the IP's previous path, so it costs about one bit.
- **Request:** the method and path type are coded together. Then come the parts that vary: item IDs (each IP's own favourite items blended with overall popularity), review page, image/JS name, and search words.
- **Response size** is almost always fixed by the path and status, so usually only a "same as before" bit is coded. Search results follow size = 800 + 37 × query length + a small remainder, and only the remainder is coded.
- **Latency** is coded with a lognormal distribution per request type, learned as it goes.
- **Fallback:** any line that doesn't fit the expected format is stored as a plain string, so the code still works on other inputs.
- **Decoder size:** `decompress.py` is written compactly because its xz size counts in the score. The line parser lives only in `compress.py`.

Most fields are now within a few percent of the minimum size their randomness allows, so there's little left to gain from better modelling.