import numpy as np
# IDEA1
r,w,h=0.1,1.25,1.0
full=100*r+1*w; edit=50*r+51*w; err=100*r+1.2*w
print('I1 edit/full %.3f err/full %.4f'%(edit/full,err/full))
for ka in (1.0,1.1):
    need=2.4; # bill: output .1 fixed, input .9
    inp_new=(1/need-0.1)/0.9; red=1/inp_new
    print('input reduction needed %.2fx'%red)
    # edit share e needed with keep-alive factor ka
    tgt=red/ka
    # (1+(6.11-1)e)/(1+(1.022-1)e)=tgt
    e=(tgt-1)/((edit/full-1)-(err/full-1)*tgt)
    print(' ka',ka,'edit-turn share needed %.3f'%e)
for ceil in (1.112,1.081): print(' whole-bill ceiling keepalive only %.3f'%(1/(0.9/ceil+0.1)))
# IDEA2 sim
rng=np.random.default_rng(0)
def sim(a,N=300000,K=5,C=100000):
    p=1/np.arange(1,C+1)**a; p/=p.sum()
    trie={}; hit=0; tot=0
    draws=rng.choice(C,size=(N,K*2),p=p)
    for row in draws:
        docs=[];s=set()
        for d in row:
            if d not in s: s.add(d);docs.append(d)
            if len(docs)==K:break
        docs.sort()  # popularity order = rank id ascending
        node=trie;m=0;ok=True
        for d in docs:
            if ok and d in node: m+=1;node=node[d]
            else:
                ok=False; node=node.setdefault(d,{}) if False else node
                nn={}; node[d]=nn; node=nn
        hit+=m;tot+=K
    return hit/tot
for a in (1.05,1.2,1.5): print('I2 zipf',a,'prefix reuse (inf cache, doc-count weight) %.3f'%sim(a))
u=(1.25-1/1.5)/1.15; print('I2 required reuse for 1.5x (all tokens are docs): %.3f'%u)
# fit k from idea's own numbers
for uu,ratio in ((.40,1.17),(.546,1.35),(.768,1.78)):
    print(' idea claim u=%.3f ratio %.2f implied eff reuse %.3f'%(uu,ratio,(1.25-1/ratio)/1.15))
# IDEA3
for hh in (0.15,0.325,0.5):
    B=0.45+0.55*(1-hh); bl=0.45+0.55*0.15; sh=0.01*0.55
    mx=B/(bl+sh); tgt=B/1.5
    a=(B+sh-tgt)/(B-bl) if tgt>=bl+sh else float('nan')
    print('I3 h=%.3f base %.3f maxratio(a=1) %.2f accept needed %.3f'%(hh,B,mx,a))
# IDEA5/6 whole-bill
def bill(m,b=0.242,e=0.83,extra=0.031,sh=0.01,fixed=0.45,pre=0.55,base=0.83):
    cost=fixed+pre*((1-m)*b+m*(e+extra))+pre*sh
    return (fixed+pre*base)/cost
for m in (0,0.02,0.1,0.2,0.3,0.5): print('I5/6 m=%.2f ratio %.3f'%(m,bill(m)), ' idea6(extra=0) %.3f'%bill(m,extra=0))
import scipy.optimize as so
f=lambda m,ex:bill(m,extra=ex)-1.5
for ex in (0.031,0): 
    print('m for 1.5x extra',ex, so.brentq(lambda m:f(m,ex),0,1))
# alt: baseline whole = 1.0 normalised with fixed .45 + prefill .55*... idea5 style where exact path = 83%+3.1% of full compute
def bill2(m,b=0.242,e=0.83,ex=0.031,sh=0.01):
    cost=(1-m)*b+m*(e+ex)+sh*1.0; return 0.83/cost
for m in (0,0.1,0.3): print('compute-only ratio m=%.1f %.3f'%(m,bill2(m)))
print('m for 1.5x compute-only',so.brentq(lambda m:bill2(m)-1.5,0,1))
