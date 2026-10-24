exec(open('idea2_prefill.py').read().split('cfgs =')[0])
print("SRAM sweep, 1 die 17.5PF, 1.4 TB/s LPDDR, L=32K/128K, 128K tokens/pass")
for sr in [0.256e9,0.5e9,0.75e9,1.0e9,1.45e9,2.0e9]:
    out=[]
    for L in [32768,131072]:
        r,b,T=prefill(L,131072,17.5e15,1.4e12,sr); rc=1/(NL*(flops_per_token(L)[0]/17.5e15+sum(flops_per_token(L)[1:])/(8.75e15))/0.6)
        out.append(f"L={L//1024}K {r/rc*100:5.1f}% of compute ({b})")
    print(f"  SRAM {sr/1e9:4.2f} GB:", " | ".join(out))
print("tokens/pass sweep with 1.45 GB SRAM, L=8K prompts packed:")
for S in [8192,32768,65536,131072,262144]:
    r,b,T=prefill(8192,S,17.5e15,1.4e12,1.45e9); print(f"  S={S:6d}: {r/1e3:6.1f} ktok/s ({b}); pass latency {S/r:5.2f} s")
# BOM per package (assumptions, USD): die N3 ~$700, SRAM die ~$400, SoIC bond+test ~$500/die, CoWoS-L ~$2000, substrate $500
for yr,h in [("2026",600),("2027",1300)]:
    rubin = 2*700 + 8*h + 2000 + 500
    cont  = 2*700 + 2*400 + 2*500 + 500 + 512*10
    rr,_,_=prefill(131072,131072,35e15,22e12,400e6,a2a_bw=1.8e12,ep=2); rc,_,_=prefill(131072,131072,35e15,2.8e12,2.9e9)
    print(f"{yr}: BOM Rubin ${rubin}  Continuum-P2 ${cont}  | $ per ktok/s @128K: Rubin {rubin/(rr/1e3):.0f}  Cont {cont/(rc/1e3):.0f}  ratio {rubin/(rr/1e3)/(cont/(rc/1e3)):.2f}")
# energy/token @128K: assume same compute energy (same node, same engine): 2 dies ~1.8 kW at full load; memory: HBM4 ~3.0 pJ/b, LPDDR 3.6 pJ/b
d,i,a=flops_per_token(131072)
rc,_,T=prefill(131072,131072,35e15,2.8e12,2.9e9)
passes=math.ceil(131072/T); bytes_c=(WL*passes*NL/131072 + NL*D*3 + NL*788*1.5)
rr,_,_=prefill(131072,131072,35e15,22e12,400e6,a2a_bw=1.8e12,ep=2)
bytes_r=(WL/2*math.ceil(131072/((400e6-100e6)/(D*6)))*NL/131072 + NL*D*3 + NL*788)
nvl = NMOE*8*D*3*0.5*8*1.0e-12     # NVLink ~1 pJ/b assumed
e_comp = 1800/rr
print(f"bytes/token: Rubin {bytes_r/1e6:.1f} MB (+NVLink a2a {NMOE*8*D*3*0.5/1e6:.1f} MB) ; Continuum {bytes_c/1e6:.1f} MB")
print(f"energy/token: compute {e_comp*1e3:.1f} mJ both; mem Rubin {bytes_r*8*3.0e-12*1e3:.2f}+NVL {nvl*1e3:.2f} mJ ; Cont {bytes_c*8*3.6e-12*1e3:.2f} mJ")
