# Idea 3: DSA decode bytes per token (DeepSeek-V3.2: 61 layers, indexer key 128B FP8, MLA entry 656B FP8, top-k 2048)
L,ctx,ik,kv,k=61,131072,128,656,2048
idx=L*ctx*ik; gat=L*k*kv; dense=L*ctx*kv
print("indexer GB/tok",idx/1e9,"gather GB/tok",gat/1e9,"dense GB/tok",dense/1e9)
print("vs dense",dense/(idx+gat),"vs sparse-on-HBM best practice",(idx+gat)/idx)
# SLA 100 tok/s, B200-class 8 TB/s HBM, weights/GPU 9.3GB (671B FP8 /72)
hbm=8e12; step=0.01; wts=9.3e9
print("users/GPU bandwidth-limited (idea)",(hbm*step-wts)/idx)
print("users/GPU capacity-limited (HBM-only, 186GB-9.3-20)",(186e9-9.3e9-20e9)/(L*ctx*(ik+kv)))
# LPDDR6 subchannel: 12 pins x 10.667 Gbps = 16 GB/s; 656B gather transfer time vs activate limit
bw=12*10.667e9/8; t=656/bw; print("656B xfer ns",t*1e9,"; 4 ACT/tFAW(~20ns) limit GB/s",4/20e-9*656/1e9)
print("burst-alignment efficiency (32B bursts)",656/(np.ceil(656/32)*32) if False else 656/(21*32))
# Idea 1: BOM per dense FP8 PF
b200=6400/4.5
for p in (10,15,20):
    cont=(600+256*p+300)/2.0
    print(f"LPDDR ${p}/GB: Continuum $/PF {cont:.0f} vs B200 {b200:.0f} -> RATIO {b200/cont:.2f}")
print("LPDDR $/GB needed for 1.5x:",((b200/1.5)*2-900)/256)
# Idea 4: run-cost ratio from goodput 0.90->0.98 on time-proportional share (hw 44+net 13+energy 4=61)
print("run ratio",1/(0.39+0.61*0.90/0.98))
