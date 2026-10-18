import math
rho=1000; cp=4186
# creek heat
Q=0.1; dT=5
P_creek=Q*rho*cp*dT
print("creek MW",P_creek/1e6)
E=107e6 # J/m3 pay
for P in [P_creek,3.7e6,5.1e6]:
    print("P %.2f MW -> pay m3/h at 30%%: %.1f"%(P/1e6, P*0.3*3600/E))
# pond
for w in [80,150]:
    print("pond MW",2e4*w/1e6, "total", (P_creek+2e4*w)/1e6)
# grade implied
for c,g in [(1200,550),(1400,660)]:
    print("implied grade g/m3",c/g)
# face heat flux needed
for rate in [35,45]:
  for v in [3.7,8]:
    A=rate/v
    q=rate*E/3600/A
    print(f"rate {rate} m3/h adv {v} m/h section {A:.1f} m2 face flux {q/1e3:.0f} kW/m2 ; h needed at dT 3/5 K: {q/3:.0f} / {q/5:.0f} W/m2K")
# impinging jet stagnation h
nu=1.57e-6; k=0.57; Pr=11.4
for d,vj in [(0.08,40),(0.06,30),(0.1,20)]:
    Re=vj*d/nu
    Nu=0.745*Re**0.5*Pr**0.33
    h=Nu*k/d
    print(f"jet d={d} v={vj} Re={Re:.2e} Nu0={Nu:.0f} h0={h:.0f} W/m2K -> stag thaw rate at dT5 {h*5/E*3600:.2f} m/h")
# water needed: heat supplied per m3 pay at 30%
need=E/0.3
print("heat supplied MJ/m3",need/1e6,"water m3 per m3 pay at dT5:",need/(rho*cp*5))
for rate in [35,45]:
    qw=rate*need/(rho*cp*5)/3600
    print("water flow L/s",qw*1000)
# effectiveness of single pass over face
m=0.19*1000*cp
for hA in [18000,50000,100000]:
    print("hA",hA,"eff",1-math.exp(-hA/m))
# hydro-elevator + jet power
def elev(Q1,H,Hn_ratio=7,alpha=0.7,eta_p=0.75,rho_s=1100):
    Hn=H*Hn_ratio
    Q0=Q1/alpha
    P=Q0*1000*9.81*Hn/eta_p
    return P,Q0,Hn
for H in [25,35]:
  for Q1 in [0.15,0.2]:
    P,Q0,Hn=elev(Q1,H)
    print(f"lift {H} m suction {Q1} m3/s: work flow {Q0:.2f} m3/s at {Hn} m -> {P/1e3:.0f} kW")
# jet pump
for Qj,Hj in [(0.15,60),(0.19,100),(0.19,150)]:
    print("jet pump kW",Qj*9810*Hj/0.75/1e3)
# energy cost per m3 pay
for kW in [500,900,1200]:
  for rub in [25,40]:
    print(kW,"kW",rub,"rub/kWh ->", kW*rub/40,"rub/m3 at 40 m3/h")
# pillar stress
for H in [20,30,40,50]:
  for e in [0.5,0.67]:
    s=2000*9.81*H/(1-e)/1e6
    print(f"cover {H} extraction {e}: pillar stress {s:.2f} MPa")
# roof thaw by humid air
h=10
for Ta in [2,4]:
  esat=lambda T:611*math.exp(17.27*T/(T+237.3))
  dw=0.622*(esat(Ta)-esat(0))/101325
  qc=h*2.5e6*dw/1005
  qs=h*Ta
  for t in [25,45]:
    print(f"air {Ta}C: flux {qs+qc:.0f} W/m2 -> thaw in {t} h: {(qs+qc)*t*3600/E*100:.1f} cm")
# season volume
for r in [35,45]:
    print("season m3",r*24*90)
# adit length
for v,t in [(3.7,45),(8,25),(3.7,25),(8,45)]:
    print("adit length",v*t)
