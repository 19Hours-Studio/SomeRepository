import math
Pe=0.3; eb=0.80; eo=0.16
Pf=Pe/(eb*eo); Pth=Pf*eb; rej=Pth-Pe
print(f"fuel {Pf:.3f} MW, boiler out {Pth:.3f}, reject {rej:.3f} MW")
disp=1.54/0.65
print("displaced boiler-house coal MW:",disp," net extra fuel MW:",Pf-disp)
for bh in [0.65,0.70,0.75,0.80]:
    net=Pf-1.54/bh
    print(f"boiler house eff {bh}: net extra coal per kWh_e {net/Pe:.2f} kWh -> rub/kWh at 10k rub/t, 22 MJ/kg: {net/Pe*3.6/22*10:.2f}")
for LHV in [15,18,22,23.5]:
    kg=1/(eb*eo)*3.6/LHV
    print(f"LHV {LHV} MJ/kg: {kg:.2f} kg coal/kWh_e -> {kg*10:.1f} rub/kWh electric-only; coal per winter at 194 d: {Pf*1e6*194*86400/(LHV*1e6)/1e3:.0f} t")
LHV=22.1
t=1780e3*LHV*1e6/(Pf*1e6)
print("1780 t lasts days at full load:",t/86400)
for d in [230,250,270]:
    print(f"frozen-in {d} d at full load needs {Pf*1e6*d*86400/(LHV*1e6)/1e3:.0f} t")
print("1 MWe coal per same 194 d:",1780/0.3,"t")
# ash
for ash,rho in [(0.15,0.7),(0.20,0.8),(0.25,0.8)]:
    print(f"ash {ash} density {rho}: {1780*ash/rho:.0f} m3; freed hold {1780/0.85:.0f} m3")
# moat heat
def q(Ta,v=2.0):
    h=5.7+3.8*v
    sig=5.67e-8
    ql=0.97*sig*273.15**4-0.65*sig*(273.15+Ta)**4
    es=lambda T:611*math.exp(21.87*T/(T+265.5)) if T<0 else 611
    qe=h*(2.5e6/1005)*0.622/101325*(611-0.8*es(Ta))
    return h*(0-Ta)+ql+qe
for L,B in [(75,15),(86,15)]:
    per=2*(L+B)
    for Ta in [-40,-50]:
        qq=q(Ta)
        A=104e3/qq
        print(f"hull {L}x{B} perimeter {per} m; Ta {Ta}: {qq:.0f} W/m2 -> 104 kW keeps {A:.0f} m2 = moat width {A/per:.2f} m")
# hold heat
deck=75*15; sides=2*(75+15)*2.0
for U_deck,U_side in [(0.4,0.6),(2.0,5.0),(5.0,20.0)]:
    print(f"U deck {U_deck} side {U_side}: hold loss at -45 C {(deck*U_deck+sides*U_side)*45/1e3:.0f} kW")
# buoyancy change as coal burned
wp=75*15*0.9
print("draft change m when 1780 t burned:",1780/(wp*1.0))
# levelized cost
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
for cap in [132e6,237e6]:
  for r,n in [(0.10,15),(0.15,15)]:
    for hrs in [4662,5500]:
      E=Pe*1e3*hrs
      for staff_cost in [0,15e6]:
        c=(cap*crf(r,n)+staff_cost)/E
        print(f"capex {cap/1e6:.0f}M r={r} n={n} hrs {hrs}: staff {staff_cost/1e6:.0f}M -> {c:.1f} rub/kWh")
# diesel avoided fuel cost
for sfc in [0.28,0.30,0.33]:
  for price in [66,90,120]:
    print(f"diesel sfc {sfc} kg/kWh price {price} k rub/t -> fuel {sfc*price:.1f} rub/kWh")
# ratio stated
for d in [45,60,75,88]:
  for c in [14,19,32]:
    print(f"diesel {d} / CHP {c} = {d/c:.2f}")
