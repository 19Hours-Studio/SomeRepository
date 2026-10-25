# independent hand re-derivation of answer §4.1 (no model imports)
hid=7168; exp=3*7168*3072; dense=0.35e9+exp; head=129280*7168
lin=2*(6*exp+dense)+2*head/62
f=((0.55-0.30)/(0.75-0.30))**1.3*0.75/0.55; e=(0.55/0.75)**2
F4=64e15*f; F8=32e15*f; s=1.43; eta=0.6; imb=1.07
FPE=128*2*(512+512); att=(1024+128)*FPE; idx=32768*64*128*2
b,k,mm=354,1,2; pos=2; tok=1.8; L=62; n=b*pos
cl=lin/(F4*s); ca=att/F8; ci=idx/F4
hca=(cl+ca)*n*imb/eta/5; csa=(cl+ca+ci)*n*imb/eta/7
tau=(7+3/f)*1e-6; c=max(hca,csa); T=max(mm*c,c+tau)
print(f"f={f:.3f} lin={lin/1e9:.3f}GF  t_lin={cl:.3e} t_att={ca:.3e} t_idx={ci:.3e}")
print(f"HCA c={hca*1e6:.2f}us CSA c={csa*1e6:.2f}us tau={tau*1e6:.2f} T={T*1e6:.2f} spd={tok/(L*T):.0f}")
# slot power
comp=2640*f*e; leak=500*0.55/0.75; wt=614*f
K=(comp+leak+wt+240+144)*1.146+110; S=(comp+leak+wt+144)*1.146+110; H4=(comp+leak+wt+320+144)*1.146+110
W=210*K+160*S+H4; print(f"comp {comp:.0f} leak {leak:.0f} wt {wt:.0f}  K {K:.0f} S {S:.0f} head {H4:.0f} avg {W/371:.0f}")
print(f"eff={0.85*n*tok/T/W:.1f} tok/s/W  users={mm*b*L}")
E=448+128; idxk=32768*64; users=mm*b*L
print(f"idx keys per CSA pkg {users*idxk/7/1e9:.2f} GB; KV HBM per CSA pkg {users*(32768*E+128*E)/7/1e9:.1f} GB (cap {0.9*144:.1f})")
expb=384*exp*4.5/8; db=dense*8.25/8
print(f"CSA SRAM: weights {(expb/7+db)/1e9:.2f} + idx {users*idxk/7/1e9:.2f} = {(expb/7+db+users*idxk/7)/1e9:.2f} of {0.9*18.4:.2f}; replica need {0.125*expb/7/1e9:.2f}")
print(f"HCA SRAM: {(expb/5+db+users*((1024+128)*E)/5)/1e9:.2f} GB")
# W-tier density check
print(f"W-tier: 18.4 GB over 8 tiers = {18.4*8/8*1e3:.0f} Mb... per tier {18.4/8:.2f} GB = {18.4/8*8*1024:.0f} Mbit; at 750 mm2 -> {18.4/8*8*1024/750:.1f} Mb/mm2")
print(f"V-Cache gen1 (N7, 64MB, 41mm2): {64*8/41:.1f} Mb/mm2; N7->N5 HD bitcell 0.027->0.021 um2 scaled: {64*8/41*0.027/0.021:.1f} Mb/mm2")
