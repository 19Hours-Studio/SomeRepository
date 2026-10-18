import math
print("--- Idea 3: ice sheet edge stress from hull uplift ---")
Awp=2878; L=130.8; B=22.0; per=2*(L+B)
for burn in (1.0,3.0):  # kt
  P=burn*1e6*9.81/per
  for h in (1.0,1.5,2.0):
    for E in (1e9,5e9):
      D=E*h**3/(12*(1-0.33**2)); k=1000*9.81
      beta=(k/(4*D))**0.25
      Mfree=0.3224*P/beta; Mclamp=P/(2*beta)
      print(f"uplift {burn} kt P={P/1e3:.0f} kN/m h={h} E={E/1e9:.0f}GPa  sigma free-edge {6*Mfree/h**2/1e6:.2f} MPa clamped {6*Mclamp/h**2/1e6:.2f} MPa")
# uplift needed to crack 0.5-0.8 MPa (free edge, h=1.5,E=5)
h=1.5;E=5e9;D=E*h**3/(12*(1-0.33**2));beta=(9810/(4*D))**0.25
for s in (0.5,0.8):
    P=s*1e6*h**2/6*beta/0.3224
    print("crack at sigma",s,"needs P kN/m",round(P/1e3,1),"= coal burned t",round(P*per/9.81/1e3))
print("--- Idea 1: Vyalov creep time to failure sigma=beta/ln(t/B) ---")
for s_short,t_short in ((1.0,60),(1.5,60),(2.0,60)):
  for s_long in (0.2,0.35,0.5):
    t_long=50*3.156e7
    r=s_short/s_long
    lnB=(math.log(t_long)-r*math.log(t_short))/(1-r)
    beta=s_short*(math.log(t_short)-lnB)
    out=[]
    for s in (0.30,0.40,0.50,0.58):
        if s<=s_long: out.append((s,'never(<long-term)')); continue
        lt=beta/s+lnB
        out.append((s,f"{math.exp(lt)/86400:.3g} d"))
    print("short",s_short,"long",s_long,out)
print("--- Idea 1: heat transfer coefficients ---")
nu=1.57e-6; kw=0.57; Pr=11.6
for U in (0.5,1,2,3):
  for Dh in (0.1,0.2):
    Re=U*Dh/nu; f=(0.79*math.log(Re)-1.64)**-2
    Nu=(f/8)*(Re-1000)*Pr/(1+12.7*(f/8)**0.5*(Pr**(2/3)-1))
    h=Nu*kw/Dh
    print(f"sheet U={U} Dh={Dh}: h smooth {h/1e3:.1f} kW/m2K, x3 rough {3*h/1e3:.1f}")
for v,d in ((10,0.05),(15,0.05),(20,0.075)):
    Re=v*d/nu; Nu=0.715*Re**0.5*Pr**0.4; print(f"jet stagnation v={v} d={d}: h={Nu*kw/d/1e3:.1f} kW/m2K (stagnation point only)")
# NTU required for 4C water to exit at 0.9C, per monitor
mc=0.125*4.186e6; eps=(4-0.9)/4; NTU=-math.log(1-eps)
print("per-monitor mc kW/K",mc/1e3,"NTU needed",round(NTU,2),"hA needed kW/K",round(NTU*mc/1e3))
for h in (3e3,6e3,15e3):
    print(" h",h/1e3,"kW/m2K -> wetted frozen area per monitor m2",round(NTU*mc/h), " vs pay face 25x2=50 m2")
print("--- Idea 1: insolation TOA 63N ---")
def toa(lat,doy):
    S=1361; dec=23.44*math.sin(math.radians(360*(284+doy)/365)); phi=math.radians(lat); d=math.radians(dec)
    x=-math.tan(phi)*math.tan(d); x=max(-1,min(1,x)); ws=math.acos(x)
    return S/math.pi*(1+0.033*math.cos(2*math.pi*doy/365))*(ws*math.sin(phi)*math.sin(d)+math.cos(phi)*math.cos(d)*math.sin(ws))
for m,doy in (("Jul",196),("Aug",227),("early Sep",250)):
    T=toa(62.8,doy); print(m,"TOA W/m2",round(T),"surface at Kt 0.40/0.45:",round(0.40*T),round(0.45*T))
def pond(SW,Ta,Tw=7,RH=0.7,U=3,c=0.7):
    sig=5.67e-8
    es=lambda T:6.112*math.exp(17.67*T/(T+243.5))
    ea=RH*es(Ta); Tk=Ta+273.15
    eps=1.24*(ea/Tk)**(1/7)*(1+0.22*c*c)
    LWnet=0.97*eps*sig*Tk**4-0.97*sig*(Tw+273.15)**4
    H=1.2*1005*1.3e-3*U*(Ta-Tw)
    LE=1.2*2.5e6*1.3e-3*U*0.622*(ea-es(Tw))/1013
    return 0.93*SW+LWnet+H+LE,(0.93*SW,LWnet,H,LE)
for m,doy,Ta in (("Jul",196,14.9),("Aug",227,10.9)):
    for Kt in (0.40,0.45):
        SW=Kt*toa(62.8,doy)
        for Tw in (4,7):
            q,parts=pond(SW,Ta,Tw)
            print(m,"Kt",Kt,"pond",Tw,"C net W/m2",round(q),[round(p) for p in parts],"-> 3 ha MW",round(q*3e4/1e6,2))
