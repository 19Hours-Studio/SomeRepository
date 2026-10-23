# Exact arithmetic for the 4-idea gate. Shares from the ledger; recompute fractions from papers.
# sanity check: Llama-70B KV bytes/token = 80 layers*8 kv heads*128 dim*2(K,V)*2 B
kv=80*8*128*2*2; print("KV/token FP16 KiB", kv/1024)            # known: 320 KiB
hid=80*8192*2; print("full hidden states/token FP16 KiB", hid/1024)
# IDEA 1, archetype C session (10 q, Sonnet $3/M): base 0.042*10, one mid-doc edit
base=0.042*10; rewrite=25e3*1.25*3/1e6; patch=500*1.25*3/1e6 + 10*500*0.3/1e6
print("I1 rewrite $",rewrite,"patch $",patch,"ratio 1 edit/session",(base+rewrite)/(base+patch))
for f in (0.1,0.3):
    print("  ratio if fraction",f,"of sessions edited",(base+f*rewrite)/(base+f*patch))
# IDEA 2, archetype D: prefill-missed 0.55, rest 0.45
cb=0.45+0.55*0.15; i2=0.45+0.55*(0.03+0.03)   # 3% recompute + ~3% probe
print("I2 vs prefix-only",1/i2,"vs CacheBlend",cb/i2)
i2real=0.45+0.55*(0.20+0.03)  # ProphetKV needs 20% for 96-101% accuracy
print("I2 at ProphetKV 20%: vs CacheBlend",cb/i2real)
# IDEA 3, archetype A: reads 54%
print("I3 2x fewer turns",1/(1-0.54/2),"; CodeAct 30% fewer",1/(1-0.54*0.3))
print("I3 margin",(1/0.7)/2)
# IDEA 4, archetype D edited requests: 5% recompute + early-layer pass (4/80 layers of post-edit tokens)
i4=0.45+0.55*(0.05+4/80); print("I4 vs prefix recompute",1/i4,"vs CacheBlend15%",cb/i4)
i4real=0.45+0.55*(0.15+4/80); print("I4 at 15% (CacheBlend-observed)",1/i4real, cb/i4real)
