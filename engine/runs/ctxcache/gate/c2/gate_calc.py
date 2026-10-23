# Exact arithmetic for the 4-idea gate. Prices: Sonnet $3/M in, $15/M out, write 1.25x, read 0.1x.
P=3e-6; W=1.25*P; R=0.1*P; O=15e-6
# --- Ideas 1/3: archetype C session (50k doc, 10 Qs, mid-doc edit at 25k) ---
base=50e3*W + 10*(50e3*R + 300*P + 500*O)
edit_rewrite = 25e3*W - 25e3*R          # extra vs a normal read of that suffix
edit_patch   = 1e3*W + 5*1e3*R          # 1k patch write + ~5 later reads
print("C session base $%.4f, rewrite extra $%.4f, patch $%.4f"%(base,edit_rewrite,edit_patch))
for k in [0.5,1,2,3,5]:
    print(" edits/session %.1f ratio %.2f"%(k,(base+k*edit_rewrite)/(base+k*edit_patch)))
# k needed for 1.5x
k=(1.5*base-base)/(edit_rewrite-1.5*edit_patch); print(" edits needed for 1.5x: %.2f"%k)
# --- Idea 2: archetype A, 40 turns, ctx 20k + 2k/turn (1.4k tool output), 0.5k out ---
def task(stub, every=10, keep=5, stub_tok=50):
    turns=[]; cost=0; cached=20e3; cost+=20e3*W
    for t in range(1,41):
        # rewrite step
        if stub and t%every==0:
            new=[]
            first=None
            for i,tok in enumerate(turns):
                age=t-i
                if age>keep and tok['tool']>stub_tok:
                    if first is None: first=i
                    tok['tool']=stub_tok
            if first is not None:
                suffix=sum(x['tool']+x['other'] for x in turns[first:])
                cost+=suffix*W; cached=20e3+sum(x['tool']+x['other'] for x in turns)
        ctx=20e3+sum(x['tool']+x['other'] for x in turns)
        cost+=ctx*R + 2e3*W + 500*O
        turns.append({'tool':1400.0,'other':600.0})
    return cost, ctx
b,_=task(False); s,_=task(True)
print("A task base $%.3f stub $%.3f ratio %.2f"%(b,s,b/s))
# --- Idea 4: KV size and load time, Llama-3-70B (80 layers, 8 KV heads, d=128) ---
kv=80*8*128*2*1; print("FP8 KV bytes/token",kv,"=",kv/1024,"KiB; 6k tok GB",6e3*kv/1e9,"load s @10GB/s",6e3*kv/1e10)
flop=2*70e9*6e3; print("full prefill 6k tok on 2xH100 @40pct MFU s: %.2f"%(flop/(2*989e12*0.4)))
for r in [0.10,0.15]:
    D=0.45+0.55*(r+0.02+0.02)   # +2% calibration sample, +2% load/overhead
    B=0.29+0.71*(r+0.02+0.03)
    print("recompute %.0f%%: D ratio %.2f  B ratio %.2f"%(r*100,1/D,1/B))
print("vs CacheBlend@15%%: D ratio %.3f"%((0.45+0.55*(0.15+0.02))/(0.45+0.55*(0.10+0.04))))
# breakdown for idea 2
def detail(stub, every=10, keep=5, stub_tok=50):
    turns=[]; rd=wr=rw=0; ctxs=[]
    for t in range(1,41):
        if stub and t%every==0:
            first=None
            for i,tok in enumerate(turns):
                if t-i>keep and tok['tool']>stub_tok:
                    if first is None: first=i
                    tok['tool']=stub_tok
            if first is not None: rw+=sum(x['tool']+x['other'] for x in turns[first:])*W
        ctx=20e3+sum(x['tool']+x['other'] for x in turns); ctxs.append(ctx)
        rd+=ctx*R; wr+=2e3*W
        turns.append({'tool':1400.0,'other':600.0})
    return rd,wr,rw,sum(ctxs)/len(ctxs)
for s in (False,True):
    for e in ([10] if not s else [5,10,20]):
        rd,wr,rw,avg=detail(s,every=e)
        print("stub",s,"every",e,"reads $%.3f writes $%.3f rewrites $%.3f avgctx %.0fk total(+out $0.30) $%.3f"%(rd,wr,rw,avg/1e3,rd+wr+rw+0.3+20e3*W))
