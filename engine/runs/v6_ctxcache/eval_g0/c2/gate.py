# Idea 1: edit vs erratum (100k ctx, 1k new suffix, Anthropic multipliers)
C,s=100e3,1e3
cached=C*0.1+s*1.25
inplace=C/2*0.1+C/2*1.25+s*1.25
errat=cached+200*1.25
print("I1 inplace/cached %.2f erratum/cached %.3f"%(inplace/cached,errat/cached))
# Idea 1 upper bound vs best practice: all 8% misses avoidable (unrealistic)
print("I1 UB ratio if all misses became reads:",0.58/(0.58-0.08*(3.75-0.30)))
# Idea 4: check bill shares claim (50 turns, 20k base, +2k/turn, 300 out)
r=w=o=0
for t in range(50):
    ctx=20e3+2e3*t; r+=ctx*0.30; w+=2e3*3.75; o+=300*15
T=r+w+o; print("I4 shares read %.1f write %.1f out %.1f"%(100*r/T,100*w/T,100*o/T))
# Idea 4 killer: PCIe fetch per decode step, Llama-3-8B KV/token
kv=32*8*128*2*2; assert kv==131072
for budget in (2048,4096):
    per_tok=budget*kv/1e9  # GB per decode step per sequence
    pcie=50.0  # GB/s effective PCIe5 x16 (64 GB/s theoretical)
    itl=0.030  # 30 ms target ITL
    B_max=pcie*itl/per_tok
    print("I4 budget %d: %.3f GB/step/seq, max batch at 30ms ITL = %.2f, margin vs batch 32 = %.3f"%(budget,per_tok,B_max,B_max/32))
# Idea 2 chain (Archetype C)
for f in (23.2,27.9):
    pf=(f+1.0)/83.0
    print("I2 with %.1f%%: prefill factor %.3f RATIO %.2f"%(f,pf,1/(0.45+0.55*pf)))
# Idea 3: required duplicate share of write+read tokens for 1.5x
req=(1-1/1.5)/0.89
print("I3 required dup share %.2f; avail 0.26*f(0.6)*0.9=%.3f; CORVUS 9-50%%"%(req,0.26*0.6*0.9))
for d in (0.09,0.14,0.25,0.50): print("  input cut",d,"RATIO %.2f"%(1/(1-0.89*d)))
