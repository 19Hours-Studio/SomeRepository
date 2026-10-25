import random, statistics as st
W,R=1.25,0.10
print("== break-even turns: answer's formula vs incremental (rewrite replaces a 0.1x read of the suffix) ==")
for N,p,e in [(100_000,50_000,500),(100_000,90_000,2_000)]:
    a=(W*(N-p)-W*e)/(R*e); b=((W-R)*(N-p)-W*e)/(R*e)
    print(N,p,e,f"answer={a:.0f} corrected={b:.0f}")
print("== doc ordering: insert 1 new doc into n cached docs; fraction of doc tokens recomputed ==")
for n in (5,10,20,50):
    rng=random.Random(1); hs=[];fs=[]
    for _ in range(20000):
        docs=[rng.random() for _ in range(n)]; new=rng.random()
        hs.append(sum(d>new for d in docs)/n)   # hash order: everything after the new doc's slot
        fs.append(0.0)                          # first-seen (append) order
    print(f"n={n}: hash-sort recompute={st.mean(hs):.3f}  first-seen-order recompute={st.mean(fs):.3f}")
print("== prefill cost incl. attention, Llama-3-70B (80L, d=8192), H100 $2/h 45% MFU ==")
lin=2*70e9
for ctx in (8_000,32_000,100_000):
    attn=4*80*8192*ctx/2      # QK^T + AV, causal average over the prefill
    usd=(lin+attn)/(0.45*989e12)*2/3600*1e6
    print(f"ctx={ctx}: attn/linear={attn/lin:.2f}  recompute=${usd:.3f}/M tok  DRAM breakeven reuse interval={60*usd/1.64:.1f} min  NVMe={usd/0.0655:.1f} h")
