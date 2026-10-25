import random, hashlib, math
# --- Idea 1: ledger A shares; write tokens vs read tokens
W,R,O=0.47,0.42,0.10
print("write share of cached tokens", (W/3.75)/((W/3.75)+(R/0.30)))
for f in [0.2,0.4,0.71,1.0]:
    # remove f of writes, replace with pings at 0.1x of rewritten prefix (~0.08 of write cost each), assume 1 ping avg
    saved=W*f*(1-0.1/1.25)
    print("I1 f",f,"ratio",round(1/(1-saved),3))
# --- Idea 2: arithmetic check and RAG hash-sorted prefix hit rate
N,p,e=100_000,30_000,400
print("rewrite",p*0.1+(N-p)*1.25,"append",N*0.1+e*1.25)
def sim(M=100_000,k=5,Q=20000,zipf=1.0,chunk=800,cache=10**9):
    w=[1/(i+1)**zipf for i in range(M)]
    trie=set(); hit=tot=0
    h=lambda c:hashlib.md5(str(c).encode()).hexdigest()
    for q in range(Q):
        s=set()
        while len(s)<k: s.add(random.choices(range(M),weights=w)[0] if False else None) if False else s.add(int(M*random.random()**(1/(1-0.0))) if zipf==0 else sample())
        pass
    return None
# simpler: Zipf via numpy
import numpy as np
rng=np.random.default_rng(0)
def sim2(M=100_000,k=5,Q=20000,a=1.1):
    trie=set();hit=0
    for _ in range(Q):
        s=set()
        while len(s)<k:
            x=rng.zipf(a)-1
            if x<M: s.add(int(x))
        order=sorted(s,key=lambda c:hashlib.md5(str(c).encode()).hexdigest())
        pre=();h=0;miss=False
        for c in order:
            pre=pre+(c,)
            if not miss and pre in trie: h+=1
            else: miss=True
            trie.add(pre)
        hit+=h/k
    return hit/Q
for a in [1.05,1.2,1.5]:
    print("I2 RAG doc-token hit, zipf",a, round(sim2(a=a),3))
# --- Idea 3: Llama-3-70B: 80 layers, 64 q heads, 8 kv heads, d=128
L,n=100_000,2_000; layers,Hq,Hkv,d=80,64,8,128
kv=L*layers*2*Hkv*d*2; qo=n*layers*2*Hq*d*2
print("KV fetch GB",kv/1e9,"q+o GB",qo/1e9,"ratio",kv/qo)
bw=8*50e9  # 8x400Gb/s NICs
flops=2*70e9*n + 4*n*L*Hq*d*layers
print("transfer s",kv/bw,"prefill s at 8xH100 ~40% of 7.9PF",flops/(0.4*7.9e15))
print("I3 ceiling ratio if KV transfer share 5% removed",1/(1-0.05))
# --- Idea 4: ledger C, prefill 55%; doc tokens ~ (4k of 5.2k) as in B
for keep in [0.10,0.15,0.25]:
    pre=0.55*( (1.2/5.2) + (4/5.2)*keep )   # system+question still computed vs prefix cache: system cached in both
    base=0.55*(4.2/5.2)/(4.2/5.2)  # baseline prefill (system cached already)
    # baseline prefill = docs+question; idea = docs*keep + question
    b=0.55; i=0.55*((4*keep+0.2)/4.2)
    print("I4 recompute",keep,"ratio",round(1/(1-b+i),3))
