# IDEA 4: wintering coal CHP barge (bunker barge burns its own cargo; thermal-oil boiler + ORC; heat-led)
kWh_per_kg=5300*4.1868/3600     # 5,300 kcal/kg hard coal (assumption) -> 6.16 kWh/kg
eta_b=0.80; eta_orc=0.16; eta_bh=0.65  # barge thermal-oil boiler; ORC net (UK 17%, Lienz 18% ORC/15% plant); village boiler house (assumption)
print("=== R1: fuel cost per kWh_e ===")
for pc in (5000,10000,20000):
    c_th=pc/1000/kWh_per_kg         # rub per kWh_th of coal
    elec_only=c_th/(eta_b*eta_orc)
    # heat-led CHP: per kWh_e, coal in = 1/(eta_b*eta_orc); heat delivered = (1-eta_orc-0.02)/eta_orc kWh; displaces boiler-house coal heat/eta_bh
    q_in=1/(eta_b*eta_orc); heat=(1-eta_orc-0.02)/eta_orc
    net=c_th*(q_in-heat/eta_bh)
    print(f" coal {pc} rub/t: {c_th:.2f} rub/kWh_th ; electric-only {elec_only:.1f} rub/kWh_e ; heat-led CHP net fuel {net:.1f} rub/kWh_e (heat {heat:.1f} kWh_th per kWh_e)")
for pd in (90,120,150):
    print(f" diesel {pd} rub/kg x 0.30 kg/kWh = {pd*0.30:.0f} rub/kWh fuel; full cost if fuel=60% (Sakhaenergo) = {pd*0.30/0.6:.0f} rub/kWh")
print(" -> parent's '1-2 rub vs 30-45 rub, 20-30x' compares kWh_th of coal with kWh_e of diesel: wrong. Electric-only ratio is ~2-3x, heat-led CHP ratio >10x")
print("=== R2: capex, LCOE (0.3 MWe, winter only) ===")
def lcoe(capex_M, P=0.3, hours=5500*0.85, crf=0.147, om_frac=0.02, crew_M=5, pc=12000, pd=120, heat_led=True):
    E=P*1e3*hours   # kWh
    c_th=pc/1000/kWh_per_kg
    if heat_led:
        q_in=1/(eta_b*eta_orc); heat=(1-eta_orc-0.02)/eta_orc; fuel=c_th*(q_in-heat/eta_bh)
    else: fuel=c_th/(eta_b*eta_orc)
    cap=capex_M*1e6*crf/E; om=(capex_M*1e6*om_frac+crew_M*1e6)/E
    diesel_full=pd*0.30/0.6
    return E, cap, om, fuel, cap+om+fuel, diesel_full
for orc_eur in (1500,2500,5000):
    capex=0.3e3*orc_eur*100/1e6 + 30 + 15 + 30 + 12   # ORC + boiler 30M + used barge 15M + integration 30M + heat link 12M
    for hl in (True,False):
        E,cap,om,fuel,tot,dfull=lcoe(capex,heat_led=hl)
        print(f" ORC {orc_eur} EUR/kW -> capex {capex:.0f} M rub ; {'CHP heat-led' if hl else 'electric-only'}: {E/1e6:.2f} GWh/winter; capex {cap:.1f} + O&M {om:.1f} + fuel {fuel:.1f} = {tot:.1f} rub/kWh vs diesel full {dfull:.0f} rub/kWh -> {dfull/tot:.1f}x")
print("=== R3: scale-up 1.0 MWe for district centres (ORC 2,000 EUR/kW, boiler 70M, barge 25M, integration 45M, heat link 15M) ===")
capex=1e3*2000*100/1e6+70+25+45+15
E,cap,om,fuel,tot,dfull=lcoe(capex,P=1.0,crew_M=7)
print(f" capex {capex:.0f} M rub ; {E/1e6:.2f} GWh ; LCOE {tot:.1f} rub/kWh (capex {cap:.1f}, O&M {om:.1f}, fuel {fuel:.1f}) vs diesel full {dfull:.0f} -> {dfull/tot:.1f}x ; vs 88 rub/kWh districts -> {88/tot:.1f}x")
print("=== Consistency: bunker, hold, ash, ice moat, heat sink ===")
for P in (0.3,1.0):
    Qin=P/(eta_b*eta_orc)    # MW_th fuel
    coal=Qin*1e3*5500*0.85/kWh_per_kg/1e3
    heat=P*(1-eta_orc-0.02)/eta_orc
    print(f" {P} MWe: fuel {Qin:.2f} MW_th, coal/winter {coal:,.0f} t (river barges 1,000-3,000 t), ash 15% {coal*0.15:,.0f} t = {coal*0.15/0.7:,.0f} m3 vs coal volume freed {coal/0.85:,.0f} m3 ; reject heat {heat:.2f} MW to village net")
moat=2*(60+14)*1.0*0.7   # 1 m open ring, 700 W/m2 open-water loss at -40C
hold=2*(50*12+50*6+12*6)*0.5*45/1e3  # hold surfaces U 0.5, dT 45 K
print(f" ice moat around 60x14 m hull: {moat:.0f} kW ; keeping 2,500 m3 hold >0 C: {hold:.0f} kW -> both << reject heat")
