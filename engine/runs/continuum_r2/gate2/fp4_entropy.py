# NVFP4-style: E2M1 with block-16 scale; entropy of 4-bit codes (Gaussian weights)
import numpy as np
rng=np.random.default_rng(0); w=rng.standard_normal(2**22).reshape(-1,16)
grid=np.array([0,0.5,1,1.5,2,3,4,6])
s=np.abs(w).max(1,keepdims=True)/6; a=np.abs(w/s)
idx=np.abs(a[...,None]-grid).argmin(-1); code=idx+8*(w<0)
_,c=np.unique(code,return_counts=True); p=c/c.sum()
print("NVFP4 code entropy ratio", -(p*np.log2(p)).sum()/4)
