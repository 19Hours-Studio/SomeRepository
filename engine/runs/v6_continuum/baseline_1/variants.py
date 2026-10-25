"""Package-variant sensitivity: what Continuum memory mix wins at long context? (all EST)"""
import roofline as R
R.chips.update({
  "C-A 2hi+4HBM":   dict(cf=80,  bf=64, tf="stack", cs=192, bs=10, ts="hbm", f4=32, f8=16, kw=2.2, lat=3.0),
  "C-B 2hi only":   dict(cf=80,  bf=64, tf="stack", cs=0,   bs=0,  ts="hbm", f4=32, f8=16, kw=1.9, lat=3.0),
  "C-C 4hi only":   dict(cf=160, bf=64, tf="stack", cs=0,   bs=0,  ts="hbm", f4=32, f8=16, kw=2.0, lat=3.0),
  "C-D 4hi+2HBM":   dict(cf=160, bf=64, tf="stack", cs=96,  bs=5,  ts="hbm", f4=32, f8=16, kw=2.1, lat=3.0),
})
for k in ["Ironwood (TPU)", "WSE-3 (wafer)", "Groq LP30", "Continuum"]: R.chips.pop(k)
import itertools
def sweep(L, slos=(100, 400, 800)):
    print(f"\ncontext {L}: best tok/s/kW (n,B) at SLO; B up to 16384")
    for ch in R.chips:
        out=[]
        for slo in slos:
            best=None
            for n in [2,3,4,6,8,12,16,24,32,48,64,96,128,192,256,384,512,1024]:
                for B in [2**i for i in range(15)]:
                    r=R.step(ch,B,L,n_force=n)
                    if r and r["tps_user"]>=slo and (best is None or r["tps_per_kW_tdp"]>best[0]):
                        best=(r["tps_per_kW_tdp"],n,B,r["tok_per_J"])
            out.append(f"{best[0]:6.0f}({best[1]},{best[2]}) {best[3]:.1f}tok/J" if best else "-")
        print(f"{ch:14s} | "+" | ".join(out))
for L in (8192, 32768, 131072): sweep(L)
