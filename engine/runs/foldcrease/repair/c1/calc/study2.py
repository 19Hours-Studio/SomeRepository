import numpy as np, crease, strain
from study1 import smooth, solve_lin
from crease import teardrop_profile, metrics, EI
base_stack=list(strain.stack)
idea2_stack=[("hard coat (on UTG)",5,5.0,True),("UTG",45,70.0,False),("silicone OCA",25,0.00003,True),
             ("POL-less CF+touch+TFE",15,5.0,True),("OLED/TFT on CPI",20,8.0,True),("CPI back film",25,5.0,True)]
def kres(stack,R,phi,eps_c):
    D=sum(EI(t,E) for _,t,E,_ in stack); num=0
    for n,t,E,c in stack:
        if not c or E<0.01: continue
        num+=EI(t,E)*phi*max(0,t*1e-3/(2*R)-eps_c)/(t*1e-6/2)
    return num/D*(R*1e-3), D
def depth(stack,R,phi,eps_c,sm=2.0,T=0):
    c,D=kres(stack,R,phi,eps_c); x,k=teardrop_profile(R,n=700); k=smooth(x,k,sm)
    w,s,cu=solve_lin(x,c*k,T,D=D); return metrics(x,w,s,cu)
# calibrate phi on base stack: R=2, sharp, untensioned = 60 or 150 um, at eps_c (same eps_c used for both)
for eps_c in [0.0,0.0025,0.003,0.005]:
  for base in [60,150]:
    lo,hi=1e-4,50
    for _ in range(50):
        phi=np.sqrt(lo*hi); d=depth(base_stack,2.0,phi,eps_c,sm=0)['depth_um']; lo,hi=(phi,hi) if d<base else (lo,phi)
    row=[]
    for R in [3.0,4.2,5.0]:
        m=depth(idea2_stack,R,phi,eps_c); row.append(f"R{R}: {m['depth_um']:.2f}um/{m['slope_mrad']:.2f}mrad")
    print(f"eps_c={eps_c*100:.2f}% base={base} phi={phi:.3f} | idea2 stack untensioned, 2mm clothoid: "+" | ".join(row))
D1=sum(EI(t,E) for _,t,E,_ in base_stack); D2=sum(EI(t,E) for _,t,E,_ in idea2_stack)
poly=lambda st: sum(EI(t,E) for _,t,E,c in st if c and E>0.01)
print(f"polymer share of bending stiffness: base {poly(base_stack)/D1*100:.1f}%  idea2 {poly(idea2_stack)/D2*100:.1f}%")
