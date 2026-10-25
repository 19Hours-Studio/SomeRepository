# Idea 1: decompose ledger A bill into token fractions
w,r,o=47,42,10; fresh=1
W=w/3.75; R=r/0.30
print("write fraction of cached tokens", W/(W+R))          # check vs 92% hit
print("cost/MTok", (0.3*R+3.75*W)/(R+W))                  # ledger says 0.58
# floor write fraction = new tokens per turn / context (assume 5k/100k, 3k/100k)
for nC in (0.05,0.03):
    hidden=max(0,(W/(W+R)-nC)/(W/(W+R)))
    cost=100-w*hidden
    print(f"n/C={nC}: max removable write share {hidden:.2f}, ratio {100/cost:.2f}")
# required: 1.5x => cost 66.7 => remove 33.3 of 47 write
print("required write share removed for 1.5x", (100-100/1.5)/w)
# check idea's example: 100k miss per 50 turns @5k
print("example", 100e3/(50*5e3))
# Idea 2: archetype C, m = share of prefill that is post-divergence suffix
for m in (0.2,0.4,0.6):
  for f in (0.0,0.08,0.3):   # fallback rate
    suf=m*((1-f)*0.025+f)
    load=1.0  # KV load/index overhead, % of cost
    cost=45+55*((1-m)+suf)+load
    print(f"m={m} fallback={f}: ratio {100/cost:.2f}")
# fallback rate allowed for 10x suffix saving
print("max fallback for 10x", (0.1-0.025)/(1-0.025))
# KV load vs recompute: Llama-70B 320KiB/token, 50k tokens, PCIe5 ~50GB/s vs H100 ~600TFLOPs eff
print("load s", 50e3*320*1024/50e9, "prefill s", 2*70e9*50e3/600e12)
