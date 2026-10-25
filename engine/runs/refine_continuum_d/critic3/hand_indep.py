"""Independent re-derivation of the >=1000 128K point (no model imports): capacity, per-layer times, cycle, speed, tok/s/W."""
hid=7168; exp_p=3*7168*3072; dense_p=0.35e9+exp_p
b_exp=exp_p*4.5/8; b_dense=dense_p*8.25/8
G,h,b,k,mm=16,2,1084,1,2; p=0.8
pos=1+k; tok=1+p; L=62; S=L-30; users=mm*b*S
E=448+64*2; ctx=131072
csa_kvs=ctx/4*E+128*E; hca_kvs=ctx/128*E+128*E; idx=ctx/4*64
f=((0.55-0.3)/0.45)**1.3*0.75/0.55; e=(0.55/0.75)**2
F4=64e15*f; F8=32e15*f; s=1.43; eta=0.6; imb=1.07
srambw=512e12*0.7*f; link=1.8e12*0.85*72/64
print(f"f={f:.3f} F4={F4/1e15:.1f}PF srambw={srambw/1e12:.0f}TB/s link={link/1e12:.2f}TB/s users={users}")
upk=users/G
print(f"SRAM {2*(384*b_exp/G+b_dense)/1e9+upk*idx/1e9:.2f} GB of {0.9*18.4:.2f}; HBM {upk*(csa_kvs+hca_kvs)/1e9:.1f} of {0.9*h*48:.1f}")
n=b*pos
lin=2*(6*exp_p+dense_p)+2*129280*7168/L
FPE=128*2*1024
touched=384*(1-(1-6/384)**n)
D=G*(1-(1-1/G)**6)
def layer(kvr,f8,f4,idxr):
    cL=n*imb*lin/(F4*s)/eta/G; cA=n*imb*(f8/F8+f4/F4)/eta/G
    sw=(imb*touched*b_exp/G+b_dense)/srambw + b*idxr/G/srambw
    hk=b*kvr/G/(h*2.5e12)
    lk=imb*n/G*hid*3*D*(G-1)/G/link
    return sw,hk,cL+cA,lk
c=layer((1024+128)*E,(1024+128)*FPE,ctx/4*64*128*2,ctx/4*64)
hh=layer((ctx/128+128)*E,(ctx/128+128)*FPE,0,0)
ho=imb*8*n/G*hid/link
cp=max(c[0],c[1],c[2],c[3]+ho)+max(hh)
tau=(7+3/f)*1e-6; T=max(mm*cp,cp+2*tau)
print("CSA us",[round(x*1e6,2) for x in c],"ho",round(ho*1e6,2)," HCA us",[round(x*1e6,2) for x in hh])
# power
comp=2640*f*e; leak=500*0.55/0.75; wt=(614-100)*0.7*f; chip0=2640+500+514*0.7+80*h+144*72/64+100
chip=comp+leak+wt+80*h+144*72/64+100
P=chip0*1.146+110-1.146*(chip0-chip)
print(f"chip {chip:.0f} W slot {P:.0f} W; c_pair {cp*1e6:.2f} T {T*1e6:.1f} speed {tok/(S*T):.0f}")
npk=497; Wavg=2303
print(f"eff (pod avg slot {Wavg}) {0.85*mm*b*tok/T/(npk*Wavg):.1f} tok/s/W")
