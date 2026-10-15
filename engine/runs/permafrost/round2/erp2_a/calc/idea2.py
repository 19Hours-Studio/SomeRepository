# Idea 2: freeze-engine vitriol winning. Freezing heat of stored Cu PLS drives an ORC that rejects to Arctic air.
import math, random
L_ice=334.0 # kJ/kg
MCu,MCuSO4,MPenta=63.55,159.61,249.69
w_e=0.119   # CuSO4 wt fraction at CuSO4-H2O eutectic, -1.6 C (Van der Ham et al. 1998, Delft: 12 wt% stream)
def ice_per_kgCu(c0_gL,R):
    w0=c0_gL/1000/1.01*MCuSO4/MCu         # CuSO4 wt fraction in PLS
    sol=1/(c0_gL/1000/1.01)                 # kg solution per kg Cu
    CuSO4=sol*w0
    m_e=CuSO4/w_e
    ice_pre=sol-m_e
    ice_eut_perCu=(1-w_e-w_e*(MPenta-MCuSO4)/MCuSO4)/(w_e*MCu/MCuSO4)  # ice per kg Cu crystallised at eutectic
    return (ice_pre+R*ice_eut_perCu)/R, sol/1.0 # per kg Cu recovered; also impurity concentration factor ~ sol/(liquid left)
for c0 in [1.0,2.5,5,10,20,40]:
    ice,_=ice_per_kgCu(c0,0.8)
    # concentration factor of non-crystallising impurities (Mg, Al, Fe, acid) at end of freezing
    sol=1/(c0/1000/1.01); CuSO4=sol*c0/1000/1.01*MCuSO4/MCu; m_e=CuSO4/w_e
    left=m_e*(1-0.8*(1+ (1-w_e-w_e*(MPenta-MCuSO4)/MCuSO4)/w_e*0+0))  # rough: liquid left after eutectic freezing of 80% Cu
    left=m_e*0.2
    print(f"PLS {c0:5.1f} g/L Cu: ice {ice:6.0f} kg/kg Cu; impurity concentration factor ~{sol/left:5.0f}x")
# --- ORC / engine, n-butane direct-contact evaporator (propane would form sII hydrate: propane-hydrate 3-phase T at 0.1 MPa is -14 C)
T_ev=-8.0+273.15   # butane boiling in liquor at eutectic -1.6 C minus acid/Fe depression (~2 K) minus 4 K driving force
def engine(Ta,dT_air=6.0,approach=4.0,eta2=0.55):
    Tc=Ta+273.15+dT_air+approach
    if Tc>=T_ev-1: return 0.0,0.0
    carnot=1-Tc/T_ev
    w=L_ice*carnot*eta2   # kJ el per kg ice, gross
    q_rej=L_ice-w
    # fan power for dry air condenser: volume = q_rej/(rho cp dT_air); dp 150 Pa, fan+motor eff 0.6
    rho=101325/(287*(Ta+273.15))
    V=q_rej/(1.005*dT_air)/rho  # m3 air per kg ice
    fan=V*150/0.6/1000           # kJ per kg ice
    return w,fan
print("\nTa   gross kJ/kg-ice  fan kJ/kg-ice  net (fan-driven dry ACC, 6K air rise) | 10K air rise variant")
for Ta in [-20,-25,-30,-35,-40,-45]:
    w,f=engine(Ta)
    w2,f2=engine(Ta,dT_air=10,approach=4)
    print(f"{Ta:4d}  {w:6.1f}  {f:5.1f}  {w-f:6.1f}   | 10K rise: gross {w2:5.1f} fan {f2:4.1f} net {w2-f2:5.1f}")
# --- season at Yakutsk (normals: Jan -38.6, Feb -31.2..-33.8, Mar -20.1, Nov -27.0, Dec -36.5 C; intra-month hourly SD ~5 K)
months={'Nov':(-27.0,30),'Dec':(-36.5,31),'Jan':(-38.6,31),'Feb':(-32.5,28),'Mar':(-20.1,31)}
random.seed(1)
SD=5.0

def season(UA, dT_air=8.0, fan_on=True, eta2=0.55):
    random.seed(1)
    E_net=0; ice=0; E_gross=0; hrs_pos=0
    for m,(mu,d) in months.items():
        for h in range(d*24):
            Ta=random.gauss(mu,SD)
            best=None
            Tc_C=Ta+dT_air/2+0.5
            while Tc_C < T_ev-273.15-0.5:
                Tc=Tc_C+273.15
                lmtd=Tc_C-Ta-dT_air/2
                Qrej=UA*lmtd
                eff=max(0,1-Tc/T_ev)*eta2
                Qin=Qrej/(1-eff); W=Qin*eff
                rho=101325/(287*(Ta+273.15))
                fan=(Qrej*1e3/(1.005*dT_air)/rho*150/0.6/1e6) if fan_on else 0.0
                score=W-fan + 0.002*Qin   # prefer power, tiny weight on ice
                if best is None or score>best[0]: best=(score,W-fan,Qin,W)
                Tc_C+=0.5
            if best is None: continue
            E_net+=best[1]; ice+=best[2]*3600/334.0; E_gross+=best[3]
            if best[1]>0: hrs_pos+=1
    return E_net/1e3, ice/1e6, E_gross/1e3, hrs_pos
for UA in [10,20,30]:
    for fan_on in [True,False]:
        E,ice,Eg,hp=season(UA,fan_on=fan_on)
        need_Cu=ice*1e9/496/1e6   # kt Cu supported at 2.5 g/L
        print(f"UA {UA} MW/K fans={fan_on}: ice {ice:5.2f} Mt/season -> {need_Cu:5.1f} kt Cu at 2.5 g/L; net el {E:5.1f} GWh (gross {Eg:5.1f}); hours net>0: {hp}; EW need {need_Cu*1e6*2.1/1e6:5.1f} GWh at 2.1 kWh/kg")
