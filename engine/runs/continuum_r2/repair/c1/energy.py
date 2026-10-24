"""J/token at the Idea-1 target point (128K DSA, 200 tok/s/user) and per-die power build-up."""
from systems import *
cd = continuum_d(); t_cd = cd_tps(cd, 1/200, 131072, True)[0]
t_vr = max(vr_hbm(1/200, 131072, True)[0], vr_ess(1/200, 131072, True)[0])
# bottom-up die power (EST): FP8 at 0.3 pJ/FLOP (B200 ~0.22 pJ/FLOP at TDP), LPDDR 3.6 pJ/b (FACT 5), SRAM leak 1 W/64MB (EST)
rd, fl, ft = per_token(131072, True)
tok_die = t_cd / cd['active']
p = dict(compute=tok_die*fl*0.3e-12, lpddr=tok_die*rd*8*3.6e-12, sram_leak=1024/64*1.0, serdes=10, misc=20)
tot = sum(p.values()) * 1.1
print("die power W:", {k: round(v,1) for k,v in p.items()}, "total", round(tot))
for label, w in (("bottom-up", tot), ("budget 300W", 300)):
    print(f"Continuum-D {label}: {cd['n']*w*1.15*PUE/t_cd:.2f} J/token (facility)")
print(f"VR NVL72 best: {VR['kw']*1e3*PUE/t_vr:.2f} J/token at {t_vr:.0f} tok/s; Cont-D {t_cd:.0f} tok/s")
print(f"capex per TB/s of KV bandwidth: Cont-D ${cd['capex']/(cd['active']*1.0):.0f}k-ish -> ${cd['capex']/(cd['active']*cd['bw']/1e12)/1e3:.1f}k, VR ${VR['capex']/(72*22)/1e3:.1f}k")
