# Decisive-number checks for the remaining idea attempts (Germany-scale unless stated).
import math
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
need_GW=61; heat_extra_GW=56   # s02 daily-mean peak deficit; + future heat-pump load in cold spell (est. below)
print("=== I5 dormant boilers (negative-load discharge) ===")
heat_TWh=600; peak_factor=2.6   # space+DHW heat; cold-spell heat power / annual mean
P_heat=heat_TWh*1e3/8766*peak_factor; cop_cold=2.2; hp_share=0.7
P_hp=P_heat*hp_share/cop_cold
print(f"cold-spell heat {P_heat:.0f} GW_th, heat-pump electric load {P_hp:.0f} GW_e (if 70% HP)")
boilers_GW=19e6*20/1e6
print(f"existing boiler fleet ~{boilers_GW:.0f} GW_th vs needed {P_heat*hp_share:.0f} GW_th")
for cop in (2.2,3.0):
    print(f"  fuel->displaced-electricity eff boiler/COP at COP {cop}: {0.92/cop:.2f}  (H2 turbine 0.40)")
print("=== I8 farm machinery PTO gensets on PV-export farm feeders ===")
tractors=1.0e6; kW=80; farms_export=250e3; per_farm_export=60
print(f"tractor shaft power {tractors*kW/1e6:.0f} GW; export-limited {farms_export*per_farm_export/1e6:.0f} GW")
tank_L=3000; fuel_kwh=tank_L*9.8; eta=0.33; el=fuel_kwh*eta
print(f"farm diesel tank {tank_L} L -> {el/1e3:.1f} MWh_e -> {el/per_farm_export:.0f} h at {per_farm_export} kW")
pto_gen=150; print(f"PTO generator ${pto_gen}/kW -> {pto_gen*(crf(.07,20)+.02)/600:.3f} $/kWh at 600 h/yr")
print("=== I9 electrolyser grid interface reused by discharge DC sources ===")
ely_GW=55; interface=250  # $/kW transformer+rectifier->bidirectional+grid connection share
print(f"electrolyser fleet {ely_GW} GW (s03, OVER1.5,RTE.18) ~ discharge need {need_GW} GW; "
      f"interface ${interface}/kW saved = {ely_GW*1e6*interface/1e9:.0f} B$ capex, "
      f"{interface*(crf(.07,25)+.015)/900:.3f} $/kWh at 900 h; bidirectional premium ~$40/kW")
print("=== I10 wind turbine tip-jet discharge ===")
v_tip=80; v_jet=500; prop=2*v_tip/(v_tip+v_jet)   # Froude-type propulsive eff of tip jet
print(f"tip-jet propulsive efficiency {prop:.2f} x nozzle/expansion ~0.6 x gen 0.95 => {prop*0.6*0.95:.2f} -> DROP")
print("=== I11 ship-to-grid in ports ===")
print(f"ships at berth (DE ports) ~60 x 5 MW aux = {60*5/1e3:.1f} GW vs {need_GW} GW -> DROP")
print("=== I12 truck V2G energy ===")
print(f"6e6 EU trucks x 600 kWh x 0.3 usable = {6e6*600*0.3/1e9:.1f} TWh vs EU drought need 351 TWh -> DROP")
print("=== I13 car alternator fleet ===")
eta_idle=0.10*0.55
print(f"49M cars x 2 kW = {49e6*2/1e6:.0f} GW but idle-engine->alternator eff {eta_idle:.3f}: "
      f"fuel for 55 TWh = {55/eta_idle:.0f} TWh -> DROP")
print("=== I14 hemispheric powership rotation ===")
season=120; transit=2*17
print(f"utilisation gain {(2*season)/(season):.1f}x minus transit -> available {365-transit-2*season:.0f} spare days; "
      f"powership capex ~$1000/kW -> per-kWh at 2x900h: {1000*(crf(.07,25)+.03)/1800:.3f} $/kWh vs fixed turbine {900*(crf(.07,30)+.025)/900:.3f}")
print("=== I16 low-current-density 'battery field' ===")
for j in (10,50,200):  # A/m2
    Pm2=j*1.0; print(f"  j={j} A/m2 -> {Pm2:.0f} W/m2; for $100/kW need cell area cost <= ${100*Pm2/1000:.1f}/m2 (geomembrane ~$3-5/m2, felt ~$20/m2)")
print("=== I17 dual-shaft heat pump (H2 engine on the open-drive compressor's second shaft end) ===")
eta_sh=0.40; rec=0.45; cop=3.0
heat=eta_sh*cop+rec; disp=heat/cop
print(f"1 kWh fuel -> {heat:.2f} kWh heat; displaces {disp:.2f} kWh grid electricity (turbine 0.40, boiler/COP {0.92/cop:.2f})")
print(f"effective RTE with electrolysis 0.65: {0.65*disp:.2f} vs H2 turbine {0.65*0.40:.2f}")
eng=150; perkWe=eng/(1/ eta_sh * disp)   # $/kW_shaft -> per kW_e displaced
print(f"engine ${eng}/kW_shaft -> ${perkWe:.0f}/kW of displaced electric load (vs turbine $900/kW)")
dh_GW_th=20; print(f"scale: large open-drive HPs in DE district heat ~{dh_GW_th} GW_th -> {dh_GW_th/cop*disp/ (eta_sh*cop/ cop) /1:.0f}?")
P_e_motor=dh_GW_th/cop; P_disp=P_e_motor*(disp/eta_sh)/ (1/1)  # per kW shaft = per kW motor
print(f"   motor load {P_e_motor:.1f} GW_e; displaced incl. waste heat {P_e_motor*disp/eta_sh/ (cop/ cop)/ (1):.1f} GW_e-equivalent")
print("=== I18 summer event-rental genset fleets idle in winter ===")
print("Europe rental/event genset fleet ~5-10 GW (Aggreko ~10 GW world) vs EU need ~300+ GW -> minor, DROP")
