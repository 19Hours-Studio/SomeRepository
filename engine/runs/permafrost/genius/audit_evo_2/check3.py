import math
print("=== IDEA 3 ===")
print("winters:",7.4/3.5,8/2)
Awp=8000/(3.3-0.52)/1.0
print("waterplane m2 (fresh water):",round(Awp))
print("e.g. L x B:",round(Awp/22.0,1),"x 22 ;",round(Awp/16.5,1),"x16.5")
for burn in (2.0,3.0,3.5):
    print("burn",burn,"kt -> rise m",round(burn*1000/Awp,2))
light=0.52*Awp
print("light displacement t",round(light))
print("gravel pad pressure kPa (8 kt + light):",round((8000+light)*9.81/Awp,1), " light only",round(light*9.81/Awp,1))
print("3.3% of 2.3 MW =",0.033*2.3e6/1e3,"kW")
# moat open-water heat loss at -40C
def openwater(Ta,u):
    h=5.7+3.8*u
    sens=h*(0-Ta)
    lw=0.97*5.67e-8*273.15**4 - 0.75*5.67e-8*(273.15+Ta)**4  # crude clear-sky
    e_s=611; e_a=611*math.exp(22.46*Ta/(272.62+Ta))*0.8
    lat=h/1005*0.622/101325*2.5e6*(e_s-e_a)
    return sens+lw+lat,sens,lw,lat
for Ta in (-20,-30,-40,-45):
    for u in (1,3,5):
        q=openwater(Ta,u)
        A=76e3/q[0]
        print("Ta",Ta,"u",u,"open-water loss W/m2",round(q[0]),"76 kW keeps open m2",round(A),"=> moat width on perimeter",round(A/(2*(Awp/22+22)),2),"m")
# coal void O2
for bd in (0.8,0.85,0.9):
    vol=8000/bd
    void=vol*(1-bd/1.35)
    print("bulk dens",bd,"coal vol m3",round(vol),"void m3",round(void),"O2 in void t (0.30 kg/m3)",round(void*0.30/1e3,2))
print("1.4 t O2 x 12.3 MJ/kg / (8kt x 1.1 kJ/kgK) =",round(1.4e3*12.3e6/(8e6*1.1e3),2),"K")
print("80 kg O2/day x 12.3 MJ/kg =",round(80*12.3e6/86400/1e3,1),"kW")
print("80 kg O2/day as air m3/day:",round(80/0.30),"; fraction of void per day",round(80/0.30/3500,3))
print("over 200-day winter: heat GJ",round(80*12.3e6*200/1e9), "if into 200 t surface layer K rise (no loss):",round(80*12.3e6*200/(200e3*1.1e3)))
# cost
base=8080
for f in (0.12,0.29,0.5):
    rem=f*base
    print("removable fraction",f,"=",round(rem),"rub/t; vs bunker 2800 -> bunker/removable",round(2800/rem,2),"; net change rub/t",round(2800-rem), "; total cost ratio new/old",round((base-rem+2800)/base,3))
# failure villages: needed premium
for p in (0.2,0.3):
  for f in (0.12,0.29):
    gap=2800-f*base
    print("p",p,"rem",f,"breakeven failure premium rub/t:",round(gap/p))
# draft/ice
for ice in (1.5,2.0,2.3):
    print("ice",ice,"m + loaded draught 3.3 + 0.5 clearance -> water depth needed under winter low water:",ice+3.3+0.5 - ice*0.0)
