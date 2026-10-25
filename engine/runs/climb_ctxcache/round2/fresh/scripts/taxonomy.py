# Classify block-aligned non-prefix reuse in Bailian traces A and B (per-block content hashes).
# For each request: prefix part, then maximal runs (>=2 blocks) of blocks seen before. Each run is
# traced to the most recent earlier request containing its first block.
#   shifted-same-source : run comes from the same earlier request as the prefix, at a later offset
#                         -> an insertion / replacement / deletion in the middle of a known prompt
#   reordered           : run comes from a known request but appears out of the order it had there
#   other-source        : run comes from a different request than the prefix (content mixed in, RAG-like)
# Also: the length of the new gap between the prefix end and the first reused run.
import json, sys, collections
for fn in sys.argv[1:]:
    where = {}            # block -> (req index, position) of latest occurrence
    pref = set(); tot = 0; cls = collections.Counter(); gaps = collections.Counter(); prefsrc_n = 0
    first_gap_blocks = []
    for ri, line in enumerate(open(fn)):
        r = json.loads(line); h = r["hash_ids"]; n = len(h); tot += n
        key = 0; p = 0
        for b in h:
            key = hash((key, b))
            if key not in pref: break
            p += 1
        src = where.get(h[p - 1]) if p else None
        i = p; last_src_pos = {}; first = True
        while i < n:
            if h[i] not in where: i += 1; continue
            j = i
            while j < n and h[j] in where: j += 1
            L = j - i
            if L >= 2:
                sreq, spos = where[h[i]]
                if src and sreq == src[0]:
                    c = "shifted-same-source" if spos > src[1] else "reordered"
                elif sreq in last_src_pos and spos < last_src_pos[sreq]:
                    c = "reordered"
                else:
                    c = "other-source"
                cls[c] += L; last_src_pos[sreq] = spos
                if first: gaps[min(i - p, 64)] += 1; first_gap_blocks.append(i - p); first = False
            i = j
        key = 0
        for pos, b in enumerate(h):
            key = hash((key, b)); pref.add(key); where[b] = (ri, pos)
    s = sum(cls.values())
    print(f"{fn.split('/')[-1]}: non-prefix reused blocks in runs>=2: {s/tot:.1%} of input")
    for c, v in cls.most_common(): print(f"   {c:22s} {v/tot:5.1%} of input ({v/s:.0%} of non-prefix reuse)")
    fg = sorted(first_gap_blocks)
    if fg: print(f"   new blocks between prefix end and first reused run: p25 {fg[len(fg)//4]} median {fg[len(fg)//2]} p75 {fg[3*len(fg)//4]} (blocks of 16 tokens)")
