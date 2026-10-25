import time, model8 as e8
q=e8.q
L=("0.55V wt","0.60V wt","0.65V wt","0.55V","0.60V")
t=time.time()
A=e8.c8_env(e8.C8,e8.C8_PARTS,q.C128,labels=L,hs_csa=(4,),hs_hca=(4,),idx_opts=(False,),hca_sram_opts=(False,),imb_fixed=1.12)
print("uniform per-layer (critic 46.8 46.8 46.8 46.8 42.3):",e8.fmt(A), time.time()-t)
print(A[1000][1])
