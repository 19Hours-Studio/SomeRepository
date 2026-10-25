# Idea 2 repaired regime: diesel-sized FIRST LINE (bridge) of the already-built plant; nuclear-sized expansion when FPUs arrive
OZ=31.1035; CU=10000.; AU=4000.
def crf(r,n): return r/(1-(1+r)**-n)
DIESEL=1100.; SFC=0.215
CAPEX=8.0e9; R=0.15
idle_carry = CAPEX*R          # carrying cost of a finished, unpowered plant per year
print(f"carrying cost of idle $8bn plant: ${idle_carry/1e9:.2f}bn/yr")
def bridge(MW_gen=80, util=0.85, kwh_t=25*1.1, cu=0.0049*1.05, au=0.33, rec_cu=0.85, rec_au=0.60):
    # cu: grade-control on highest-grade benches +5% vs FS first-decade head (assumption); coarse grind -3 pts recovery
    site_MW = 15
    MWh = (MW_gen*util)*8000*1.0
    ore = (MW_gen*util - site_MW)*8000*1e3/kwh_t
    fuel = MWh*SFC
    cu_t = ore*cu*rec_cu; au_oz = ore*au*rec_au/OZ; conc = cu_t/0.24
    power = fuel*DIESEL + MWh*1e3*0.025 + MW_gen*1.25*1e3*700*crf(R,5)   # fuel+O&M+genset (N+25%)
    tank = 80e6*crf(R,10)                                                # 1-yr tank farm on permafrost pads w/ thermosyphons
    mining = ore*2.5*1.8; proc = ore*3.5; ga=120e6
    logist = conc*(25+15+45); tc = cu_t*0.035*CU + conc*80
    cash = power+tank+mining+proc+ga+logist+tc
    credit = au_oz*0.92*AU
    return dict(ore_Mt=ore/1e6, fuel_kt=fuel/1e3, cu_kt=cu_t/1e3, au_koz=au_oz/1e3, conc_kt=conc/1e3,
                kwh_price=power/(MWh*1e3), cash_net_tcu=(cash-credit)/cu_t, margin=(cu_t*CU*0.965+credit-cash)/1e6,
                power_tcu=power/cu_t)
for MW in (40,80,120):
    b=bridge(MW)
    print(f"gensets {MW} MW: ore {b['ore_Mt']:.1f} Mt/y, fuel {b['fuel_kt']:.0f} kt/y, Cu {b['cu_kt']:.0f} kt, Au {b['au_koz']:.0f} koz, conc {b['conc_kt']:.0f} kt,"
          f" power ${b['kwh_price']:.3f}/kWh = ${b['power_tcu']:.0f}/tCu, C1 net ${b['cash_net_tcu']:.0f}/tCu, cash margin ${b['margin']:.0f}m/y")
# sensitivity to diesel price and Cu/Au price
for d in (900,1400):
    DIESEL=d; b=bridge(80); print(f" diesel ${d}/t: margin ${b['margin']:.0f}m/y")
DIESEL=1100.
for cu,au in ((8000,2800),(9000,3200)):
    CU,AU=cu,au; b=bridge(80); print(f" Cu {cu} Au {au}: margin ${b['margin']:.0f}m/y, C1 net ${b['cash_net_tcu']:.0f}/tCu")
CU,AU=10000.,4000.
b=bridge(80)
# logistics & consistency
loads = max(b['fuel_kt']+15, b['conc_kt'])*1e3/40
print(f"\nloads/yr with fuel-in/conc-out backhaul: {loads:.0f}; all-season road: {loads/350:.0f}/day; winter-road-only 90 d: {loads/90:.0f}/day (TCWR record ~168/day)")
print(f"Chukotka 2025 petroleum delivery 152 kt -> bridge adds {b['fuel_kt']/152:.0%}; tankage {b['fuel_kt']*1.25/0.84:.0f} k m3")
print(f"tanker calls (20 kt) in 4-5 month Pevek window: {b['fuel_kt']/20:.0f}")
print(f"conc share of Nagleynyn 1,842 kt/y: {b['conc_kt']/1842:.0%}")
# time-to-full-rate: Natalka took ~2 y from first dore to full rate (FACT 287). Bridge does commissioning+ramp on diesel.
# value per FPU-slip scenario, starting end-2028 with plant mechanically complete
print("\nFPU slip vs plant completion | no bridge: cash 0 during slip, then 2-y ramp | bridge: cash during slip, ramp absorbed")
full_margin = 2396e6   # from idea2_starter fullplan() at 70 Mt/y
for slip in (0,1,2,3):
    ramp_loss_nobridge = full_margin*0.5*2      # ~50% avg of full margin lost over 2-y ramp
    ramp_loss_bridge = full_margin*0.5*1        # ramp of line 1 already done -> ~1 y ramp of line 2
    gain = b['margin']*1e6*slip + (ramp_loss_nobridge-ramp_loss_bridge) - (80e3*1.25*700 if slip==0 else 0)
    print(f" slip {slip} y: bridge gain ${gain/1e9:.2f}bn undiscounted; first metal at T0 vs T0+{slip} y")
