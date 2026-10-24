# Minimal LPDDR sub-channel timing model (FR-FCFS, closed-page per gather). Params ~LPDDR5X/6 class (est.):
import random
tRCD,tRP,tRAS,tFAW,tRRD,tRFCpb_frac = 18.0,18.0,42.0,20.0,5.0,0.05
BANKS=16; BURST_B=32; BW=19.2e9  # one 12-bit LPDDR6 subchannel at 14.4Gbps (half of 38.4 GB/s)
tBURST=BURST_B/BW*1e9
def run(req_bytes,n=200000,q=64,seed=1):
    rnd=random.Random(seed); bank_free=[0.0]*BANKS; acts=[]; bus=0.0; t_last_act=-1e9
    queue=[rnd.randrange(BANKS) for _ in range(q)]; done=0; moved=0
    bursts=-(-req_bytes//BURST_B)
    while done<n:
        # pick request whose bank is ready earliest
        i=min(range(len(queue)),key=lambda k:bank_free[queue[k]]); b=queue.pop(i)
        t=max(bank_free[b], t_last_act+tRRD, (acts[-4]+tFAW) if len(acts)>=4 else 0)
        acts.append(t); t_last_act=t
        start=max(t+tRCD,bus); bus=start+bursts*tBURST
        bank_free[b]=max(t+tRAS,bus)+tRP
        moved+=req_bytes; done+=1; queue.append(rnd.randrange(BANKS))
    return moved/(bus*1e-9)/BW*(1-tRFCpb_frac)
print("known-answer check, 32B random (tFAW bound = 4*32B/20ns /19.2GB/s = %.3f): %.3f"%(4*32/20e-9/BW*(1-tRFCpb_frac),run(32)))
print("sequential-like 4KB:",round(run(4096),3))
for s in (656,):
    print("656B gather efficiency:",round(run(s),3))
