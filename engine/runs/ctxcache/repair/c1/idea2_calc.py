"""Idea 2: read-cost-gated turn collapsing. Session cost under Anthropic-style pricing (FACT2 / docs):
base input p, 5-min write 1.25p, read 0.1p, output 5p (Sonnet $3/$15).  Session shape: SWE-agent-like."""
p=3e-6
def session(S=8000, T=40, obs=1200, act=250, merge=None, filt=1.0, think=150):
    """merge(t)->True if step t is folded into the previous turn (no model read between them).
    filt: fraction of raw observation kept in context (in-script filtering of outputs)."""
    C=S; read=write=out=0.0; turns=0
    write+=S*1.25*p
    pend=0
    for t in range(T):
        folded = merge is not None and t>0 and merge(t,C)
        if not folded:
            turns+=1
            read+=C*0.1*p             # re-read whole cached context
            write+=pend*1.25*p        # tokens appended since last read get written now
            out+=think*5*p
            C+=pend; pend=0
        out+=act*5*p                  # action tokens emitted either way (inside script if folded)
        pend+=act+obs*filt
    read+=C*0.1*p; write+=pend*1.25*p; turns+=1   # final read
    tot=read+write+out
    return dict(turns=turns,read=read,write=write,out=out,tot=tot)
b=session()
print("baseline: turns %d  total $%.3f  read %.0f%% write %.0f%% out %.0f%%"%(b['turns'],b['tot'],100*b['read']/b['tot'],100*b['write']/b['tot'],100*b['out']/b['tot']))
def show(name,r):
    print(f"{name:55s} turns {r['turns']:3d}  ${r['tot']:.3f}  x{b['tot']/r['tot']:.2f}")
show("uniform pairs merged (2x fewer turns)", session(merge=lambda t,C: t%2==1))
show("CodeAct-measured 30% fewer turns", session(merge=lambda t,C: t%10 in (1,4,7)))
# Anchor: gate on read cost. observe only if VOI > C*0.1p.  Model VOI as constant v per step;
# so threshold is context length: fold steps when C > C*.  (late, expensive turns are collapsed)
for Cstar in (20000,30000):
    for k in (2,3):
        show(f"gated: fold to {k} steps/turn when C>{Cstar}", session(merge=lambda t,C,k=k,Cs=Cstar: C>Cs and t%k!=0))
# second lever inside the anchor: script returns filtered observation (decision-relevant lines)
for f in (0.5,0.3):
    show(f"in-script obs filtering keep {f:.0%} (no merge)", session(filt=f))
    show(f"gated k=3 C>20k + filter {f:.0%}", session(merge=lambda t,C: C>20000 and t%3!=0, filt=f))
# long sessions where reads dominate (Claude-Code-like, many small obs, 150 turns)
bl=session(S=20000,T=150,obs=600,act=120)
print("long session baseline $%.2f read share %.0f%%"%(bl['tot'],100*bl['read']/bl['tot']))
g=session(S=20000,T=150,obs=600,act=120,merge=lambda t,C: C>40000 and t%3!=0)
print("long session gated k=3 C>40k: turns %d $%.2f x%.2f"%(g['turns'],g['tot'],bl['tot']/g['tot']))
g2=session(S=20000,T=150,obs=600,act=120,merge=lambda t,C: C>40000 and t%3!=0,filt=0.5)
print("long + filter 50%%: $%.2f x%.2f"%(g2['tot'],bl['tot']/g2['tot']))
# Break-even success loss: cost saving must exceed the expected cost of a failed task
for task_value in (1.0,5.0):
    r=session(merge=lambda t,C: C>20000 and t%3!=0, filt=0.5)
    print(f"task value ${task_value}: saving ${b['tot']-r['tot']:.3f}/task -> tolerable success drop {100*(b['tot']-r['tot'])/task_value:.1f} pts")
# baseline: observation masking (FACT9: -52%) but it breaks cache (FACT10); model it as keeping last 10 obs
def masking(S=8000,T=40,obs=1200,act=250,window=10,think=150,clear_every=10):
    # clear old obs every clear_every turns (clear_at_least batching) -> full rewrite of remaining context
    hist=[];read=write=out=0.0; write+=S*1.25*p; C=S
    for t in range(T):
        read+=C*0.1*p; out+=(think+act)*5*p
        hist.append(act+obs); write+=(act+obs)*1.25*p; C+=act+obs
        if (t+1)%clear_every==0:
            keep=hist[-window:]; masked=[act+40 for _ in hist[:-window]]
            hist=masked+keep; C=S+sum(hist); write+=(C-S)*1.25*p  # rewrite after the edit point
    read+=C*0.1*p
    return read+write+out
m=masking(); print("obs masking w/ clear_at_least-style batching: $%.3f x%.2f"%(m,b['tot']/m))
# paired (McNemar) sample size to detect a success drop d, discordant fraction pd
for d in (0.02,0.03,0.05):
    n=(1.96+0.84)**2*0.15/d**2
    print(f"detect {d:.0%} success drop (15% discordant pairs): {n:.0f} paired tasks")
