"""Where do requests stop matching cache? Bucket missed tokens by relative divergence point d/L (infinite cache)."""
import json, sys
for p in sys.argv[1:]:
    seen=set(); buckets={"no prefix hit (d=0)":0,"0<d/L<0.5":0,"0.5<=d/L<0.9":0,"d/L>=0.9":0}; tot=0
    for l in open(p):
        r=json.loads(l); h=r["hash_ids"]; n=r["input_length"]; tot+=n
        d=0
        while d<len(h) and h[d] in seen: d+=1
        miss=n-min(d*512,n)
        f=d/len(h)
        k="no prefix hit (d=0)" if d==0 else "0<d/L<0.5" if f<0.5 else "0.5<=d/L<0.9" if f<0.9 else "d/L>=0.9"
        buckets[k]+=miss; seen.update(h)
    print(p.split('/')[-1], {k:round(v/tot,4) for k,v in buckets.items()})
