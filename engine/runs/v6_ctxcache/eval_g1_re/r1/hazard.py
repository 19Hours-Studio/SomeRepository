import json,sys,collections
for name in ['conversation','toolagent']:
    rows=[json.loads(l) for l in open(f'data/{name}_trace.jsonl')]
    T=max(r['timestamp'] for r in rows)/1000
    last={}  # block-> last time
    gaps=[];  # (gap) token-weighted by 512 tokens
    for r in rows:
        t=r['timestamp']/1000
        for h in r['hash_ids']:
            if h in last: gaps.append(t-last[h])
            last[h]=t
    surv_open=[T-t for t in last.values()]  # no further access
    S=300; W=600
    ret=sum(1 for g in gaps if S<g<=W)
    # survivors past 5min: gaps>5min plus open ends with >5min elapsed; windows fully observed only if remaining>=W
    gap_gt=sum(1 for g in gaps if g>S)
    open_obs=sum(1 for e in surv_open if e>=W)  # observed full window w/o return
    open_part=sum(1 for e in surv_open if S<e<W)
    h=ret/(gap_gt+open_obs)  # conservative-ish
    h2=ret/(gap_gt+open_obs+open_part)
    print(name,'T=%.0fs'%T,'ret',ret,'gap>5m',gap_gt,'open>=10m',open_obs,'hazard %.4f / %.4f'%(h,h2))
    # request-level: fraction of blocks idle>5min that return at all
    print(' gaps>5m share of all reuses: %.4f'%(gap_gt/len(gaps)))
