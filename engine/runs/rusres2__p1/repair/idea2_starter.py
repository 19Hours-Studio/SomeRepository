# Idea 2: diesel-sized starter, nuclear-sized expansion (Baimskaya)
OZ=31.1035; CU=10000.; AU=4000.; USD_RUB=85.
def crf(r,n): return r/(1-(1+r)**-n)
# FS-2021 first-10-yr: 300 kt Cu, 490 koz Au at 70 Mt/y (FACT 12) -> recovered grades
rec_cu=0.88; rec_au=0.65
cu_head_fs = 300e3/70e6/rec_cu; au_head_fs=490e3*OZ/70e6/rec_au
print(f"implied FS first-decade head: {cu_head_fs*100:.2f}% Cu, {au_head_fs:.2f} g/t Au")
DIESEL_T=1100.  # $/t delivered Pevek/site (~RUB 94k/t), assumption; sens 900-1400
SFC=0.215        # t/MWh medium-speed diesel
def starter(tpa, cu, au, kwh_t=30, diesel=DIESEL_T, genset_kw_usd=700, capex_t=180, life=20, r=0.15,
            road_per_t_conc=40, years=None):
    MW = tpa*kwh_t/8000/1e3*1.15        # 15% site load (camp, heat) on top
    GWh = MW*8000/1e3
    fuel_t = GWh*1e3*SFC
    cu_t = tpa*cu*rec_cu; au_oz=tpa*au*rec_au/OZ
    conc_t = cu_t/0.22
    power = fuel_t*diesel + GWh*1e6*0.02     # + $0.02/kWh O&M
    gen_cap = MW*1.3*1e3*genset_kw_usd*crf(r,5)  # N+30%, 5-yr lease-equivalent
    mining = tpa*2.5*2.2                      # strip 1.5:1 -> 2.5 t moved/t ore, $2.2/t moved
    proc = tpa*5.0                            # ex power
    ga = 40e6
    logist = conc_t*(road_per_t_conc+15+45)   # road, port, sea to China
    tc = cu_t*(0.035*CU) + conc_t*80          # payable deduction + TC
    capex_ann = tpa*capex_t*crf(r,life)
    cost = power+gen_cap+mining+proc+ga+logist+tc+capex_ann
    credit = au_oz*0.92*AU
    return dict(MW=MW, fuel_kt=fuel_t/1e3, cu_kt=cu_t/1e3, au_koz=au_oz/1e3, conc_kt=conc_t/1e3,
                power_per_tcu=(power+gen_cap)/cu_t, gross=(cost)/cu_t, net=(cost-credit)/cu_t,
                margin=(cu_t*CU+credit-cost)/1e6, capex=tpa*capex_t/1e6)
# full plan baseline: 70 Mt/y, $8bn (FACT 73), FPU power price unknown: assume $0.12/kWh (deciding unknown)
def fullplan(tpa=70e6, cu=cu_head_fs, au=au_head_fs, kwh_t=25, p_kwh=0.12, capex=8.0e9, r=0.15, life=25):
    cu_t=tpa*cu*rec_cu; au_oz=tpa*au*rec_au/OZ; conc=cu_t/0.25
    cost = tpa*kwh_t*p_kwh + tpa*2.5*1.6 + tpa*3.5 + 150e6 + conc*(10+15+45) + cu_t*0.035*CU + conc*80 + capex*crf(r,life)
    credit=au_oz*0.92*AU
    return dict(gross=cost/cu_t, net=(cost-credit)/cu_t, cu_kt=cu_t/1e3, margin=(cu_t*CU+credit-cost)/1e6)
fp=fullplan(); print("FULL PLAN 70 Mt/y:", {k:round(v) for k,v in fp.items()})
for p in (0.08,0.12,0.20): print(f"  FPU price {p}: net ${fullplan(p_kwh=p)['net']:.0f}/t Cu")
print("STARTER variants (capex $/t annual cap, Cu%, Au g/t):")
for tpa,cu,au,cx in [(6e6,0.0039,0.21,180),(6e6,0.0049,0.33,180),(6e6,0.0049,0.33,250),(6e6,0.0060,0.40,180),(3e6,0.0049,0.33,230),(10e6,0.0049,0.33,160)]:
    s=starter(tpa,cu,au,capex_t=cx)
    print(f" {tpa/1e6:.0f}Mt {cu*100:.2f}%Cu {au}g/t cx{cx}: {s['MW']:.0f} MW, fuel {s['fuel_kt']:.0f} kt, Cu {s['cu_kt']:.0f} kt, Au {s['au_koz']:.0f} koz, conc {s['conc_kt']:.0f} kt | power ${s['power_per_tcu']:.0f}/tCu, gross ${s['gross']:.0f}, NET ${s['net']:.0f}/tCu, margin ${s['margin']:.0f}m/y, capex ${s['capex']:.0f}m")
# energy share of Cu price
s=starter(6e6,0.0049,0.33); print("power share of Cu price:", round(s['power_per_tcu']/CU,3))
# --- logistics check: inbound fuel+consumables vs outbound conc; winter road vs all-season road
s=starter(6e6,0.0049,0.33); inbound=s['fuel_kt']+6*1.2+6*0.6+5  # media 1.2 kg/t, lime/reagents 0.6 kg/t, misc 5 kt
print(f"inbound {inbound:.0f} kt, outbound {s['conc_kt']:.0f} kt; loads @40t: in {inbound*1e3/40:.0f}, out {s['conc_kt']*1e3/40:.0f}; with backhaul trips = {max(inbound,s['conc_kt'])*1e3/40:.0f}")
print(" TCWR record ~10,922 loads/season (~305 kt in 2018 with 8,300 loads); Kupol 2008 1,944 loads")
# fuel storage for 12 months if supplied in 4-5 month Pevek navigation: 
print(f" diesel tankage needed ~{s['fuel_kt']*1.2/0.84:.0f} k m3 (12 months + 20%)")
# Nagleynyn 1.842 Mt/y terminal: starter conc share
print(f" starter conc / Nagleynyn capacity = {s['conc_kt']/1842:.2%}")
# --- value of bridging: FPU slip scenarios. starter online T0 (when?), FPU full power at T0+slip
for slip in (0,1,2,3):
    pv = sum(s['margin']/(1.15)**t for t in range(slip))
    print(f" FPU late by {slip} y beyond starter start: PV of starter margin before FPUs ${pv:.0f}m vs starter capex ${s['capex']:.0f}m (capex reused as line 3)")
