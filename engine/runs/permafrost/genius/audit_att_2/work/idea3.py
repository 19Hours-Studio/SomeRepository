import math
print("=== IDEA 3: Wintering barge bunker ===")
g=9.81
# 1. oxidation from 1800 m3 air
for T in (273.15,243.15):
    n_air=101325*1800/(8.314*T); nO2=0.209*n_air
    for dH in (300e3,400e3):
        E=nO2*dH
        for days in (200,240):
            print(f"T={T-273.15:.0f}C dH={dH/1e3:.0f} kJ/molO2: {E/1e9:.1f} GJ over {days} d = {E/(days*86400)/1e3:.2f} kW")
# air volume vs cargo
for rho_b in (0.8,0.85,0.9):
    print(f"bulk {rho_b}: 660 t occupies {660/rho_b:.0f} m3 ; 1500 t occupies {1500/rho_b:.0f} m3")
# 2. buoyancy line load
for L,B in ((75,17.2),(80,14)):
    P=2*(L+B)
    for t in (660,1500):
        print(f"hull {L}x{B}, perimeter {P:.0f} m, {t} t drawn -> {t*1000*g/P/1e3:.0f} kN/m")
# 3. ice plate stress for line load P at a long edge (semi-infinite floating plate, load at edge of a crack-free plate approximated by infinite plate line load: M=P/(4 beta))
E=4e9; nu=0.33; k=1e4
for h in (1.4,1.67):
    D=E*h**3/(12*(1-nu**2)); beta=(k/(4*D))**0.25
    for P in (34e3,40e3,78e3):
        M=P/(4*beta); s=6*M/h**2
        print(f"h={h} P={P/1e3:.0f} kN/m: M={M/1e3:.0f} kNm/m, sigma={s/1e6:.2f} MPa (ice flexural 0.5-0.7)")
# 4. measured end-of-April ice thickness (AARI): Chokurdakh 167 cm, Yubileynaya 152 cm, Chersky 142 cm ; claimed water 1.2 m
for site,h in (("Indigirka Chokurdakh",1.67),("Yana Yubileynaya",1.52),("Kolyma Chersky",1.42)):
    print(f"{site}: mean ice {h} m vs berth water 1.2 m -> water left under ice {1.2-h:+.2f} m (before winter level drop)")
# 5. annual coal need of a 2.4 MW boiler
for Tdes,Tmean,days in ((-48,-19,305),(-45,-17,290)):
    lf=(18-Tmean)/(18-Tdes)
    for cap_used in (1.0,0.6):
        heat=2.4*cap_used*lf*days*24  # MWh
        gcal=heat/1.163
        for eta in (0.6,0.7):
            coal=gcal/eta/5.3
            print(f"Tdes={Tdes} Tmean={Tmean} {days}d peak={2.4*cap_used:.2f}MW eta={eta}: heat {gcal:.0f} Gcal, coal {coal:.0f} t/yr -> one 660 t hull covers {660/coal:.0%}")
# 6. 3.4% check and heat-loss plausibility
print("(55+27)/2400 =", (55+27)/2400)
# open water slot heat loss at -40 C
for w in (0.2,0.3,0.5):
    for q in (700,1000):
        P=184*w*q/1e3
        print(f"slot {w} m wide, {q} W/m2: {P:.0f} kW for 184 m perimeter")
# hold heat losses: hatch/deck 1290 m2, freeboard sides above ice ~ (3.5-1.2) m x 184 m
deck=75*17.2; sides=(3.5-1.2)*184
for Ud,Us in ((0.45,6.0),(0.45,1.0),(2.0,6.0)):
    Q=deck*Ud*40+sides*Us*40
    print(f"U_deck={Ud} U_side={Us}: hold at 0C vs -40C loses {Q/1e3:.0f} kW (claim 27 kW)")
# 7. value ratio and net
print("ratio", 1100/1360, 3400/1360, "net rub/t", 1100-1360, 3400-1360)
# 8. 150 m conveyor/handling capex per tonne
for capex_mrub in (15,30,60):
    crf=0.12/(1-1.12**-15)
    for t in (660,1500):
        print(f"capex {capex_mrub} M rub, CRF {crf:.3f}: {capex_mrub*1e6*crf/t:.0f} rub/t at {t} t/yr")
# 9. 150 m glycol line for 82 kW heat
