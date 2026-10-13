# K1: plug-in range-extender (EREV/PHEV) fleet as the dark-spell discharge converter (Germany).
cars=49e6
for share in (0.10,0.15,0.25):
  n=cars*share; plugged=0.5; p_out=11  # kW bidirectional AC wallbox
  P=n*plugged*p_out/1e6               # GW
  print(f"EREV share {share:.2f}: {n/1e6:.1f} M cars, export capacity {P:.0f} GW (needed ~61 GW daily-mean peak)")
# Per-car duty if fleet delivers the whole 55 TWh/yr deficit with 15% share
n=cars*0.15; E=55e9  # kWh/yr
e_car=E/n; eta_eng=0.36; p_eng=40  # kW at best-efficiency point, engine charges battery, battery exports
h_eng=e_car/p_eng
print(f"per car: {e_car:.0f} kWh_e/yr exported, engine hours {h_eng:.0f} h/yr at {p_eng} kW; "
      f"fuel {e_car/eta_eng:.0f} kWh/yr = {e_car/eta_eng/8.9:.0f} L gasoline-equiv")
life_h=6000; drive_h=0.4*300  # engine-on hours/yr from driving (EREV)
print(f"engine life used: {(h_eng+drive_h)/life_h*100:.1f}%/yr -> {life_h/(h_eng+drive_h):.0f} yr life")
# converter costs per delivered kWh: bidirectional charger premium + engine wear + owner payment
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
charger_premium=800  # $ per car for 11 kW bidirectional vs unidirectional
ann=charger_premium*crf(0.07,12)
wear=4000/life_h*h_eng   # $ engine replacement cost pro-rata
print(f"converter cost: charger {ann/e_car:.3f} $/kWh + wear {wear/e_car:.3f} $/kWh = {(ann+wear)/e_car:.3f} $/kWh "
      f"vs H2 turbine at 900 h: {900*(crf(0.07,30)+0.025)/900:.3f} $/kWh")
print(f"equivalent converter capex: {charger_premium/p_out:.0f} $/kW (export side)")
# RTE: PtL 0.5 x engine 0.36
print(f"RTE = {0.5*0.36:.2f}; s03 shows this needs overbuild ~1.5 with a 55 GW charge converter at CF 0.47")
