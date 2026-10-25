import json,collections
for name in ['conversation','toolagent']:
    rows=[json.loads(l) for l in open(f'data/{name}_trace.jsonl')]
    T=max(r['timestamp'] for r in rows)/1000
    acc=collections.defaultdict(list)
    for i,r in enumerate(rows):
        for h in r['hash_ids']: acc[h].append(r['timestamp']/1000)
    S,W=300,600; ret=gt=op=0; w=0
    for r in rows:
        t=r['timestamp']/1000; b=r['hash_ids'][-1]
        if T-t<W: continue   # need full window observed
        nxt=[x for x in acc[b] if x>t]
        n=min(nxt) if nxt else None
        if n is None or n-t>S:
            gt+=1
            if n is not None and n-t<=W: ret+=1
    print(name,'requests idle>5m',gt,'return in 5-10m',ret,'hazard %.4f'%(ret/gt))
