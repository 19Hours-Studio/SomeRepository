import json,sys
# Replays Mooncake trace: per 512-token block prefix, track last-use time; compare 5m TTL vs infinite TTL vs 1h TTL.
def run(fn):
    R=[json.loads(l) for l in open(fn)]
    last={}  # prefix tuple-key -> last ts (ms)
    gaps=[]; tot_in=0; hit_inf=0; hit5=0; hit60=0
    for r in R:
        t=r['timestamp']; h=r['hash_ids']; L=r['input_length']; nb=len(h)
        key=();m_inf=0;m5=0;m60=0;g=None
        for i,b in enumerate(h):
            key=key+(b,)
            k=hash(key)
            if k in last:
                m_inf=i+1
                if t-last[k]<=300e3: m5=i+1
                if t-last[k]<=3600e3: m60=i+1
                if i>=1: g=t-last[k]
            last[k]=t
        tok=lambda m: min(m*512,L)
        tot_in+=L; hit_inf+=tok(m_inf); hit5+=tok(m5); hit60+=tok(m60)
        if m_inf>m5: gaps.append(g)
    print(fn,'n',len(R),'span_h',R[-1]['timestamp']/3.6e6,'hit_inf %.3f hit5 %.3f hit1h %.3f'%(hit_inf/tot_in,hit5/tot_in,hit60/tot_in),
          'expired-reuse tokens share of input %.3f'%((hit_inf-hit5)/tot_in))
    # cost model (input only, Anthropic multipliers): write 1.25 miss, 0.1 hit
    c=lambda h:(tot_in-h)*1.25+h*0.1
    print('  input cost ratio 5m/inf %.3f'%(c(hit5)/c(hit_inf)))
for f in sys.argv[1:]: run(f)
