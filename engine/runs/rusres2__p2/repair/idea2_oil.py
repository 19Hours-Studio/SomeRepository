# Idea 2 "Size Sever to tankers" - repaired. $ real 2026, RUB 81/$ (assumption)
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
CRF=crf(0.12,25); FX=81.0
BRENT=65*7.33                          # $65/bbl assumption -> $/t
DISC=15*7.33                           # SDN-Rosneft seaborne discount ~$15/bbl (assumption, post FACT 219)
REAL=BRENT-DISC
# ---- north lift
DWT=69e3*0.95                          # Valentin Pikul 69k dwt (gCaptain), 95% cargo
cyc=(12.0,15.5,20.0)                   # idea's 12 d; Carnegie 15-16 d (FACT 146); Yenisei fast-ice winter 20 d
for c in cyc: print(f"Arc hull {c:4.1f} d cycle -> {365/c*DWT/1e6:.2f} Mt/y per hull")
per_hull=365/15.5*DWT/1e6
need30=30/per_hull
print(f"30 Mt/y needs {need30:.0f} hulls at 15.5 d (Carnegie says ~15)")
# summer open-water pickups at Sever (Aug-Oct ~75 d), one berth, 1.5 d per call, 100 kt Aframax
summer=75/1.5*0.1
print(f"summer conventional pickups <= {summer:.1f} Mt/y (berth-limited; ice class 1A+ needed in Kara)")
# ---- south outlet (Vankor-Purpe 25 Mt/y, FACT 361)
VANKOR_23=14.8; decl=0.06
for y in (2026,2027,2028,2030):
    v=VANKOR_23*(1-decl)**(y-2023)
    print(f"{y}: Vankor cluster ~{v:.1f} Mt, Purpe spare {25-v:.1f} Mt/y")
# ---- per-tonne marginal logistics to Asian buyer
tariff_espo=3896.51/FX                 # 2026 ESPO network tariff (investfuture/FAS order)
south=tariff_espo+3+6                  # Kozmino port + short sea to China
arc_day=(250e6*CRF/365+25e3)           # Arc6/7 69k dwt crude shuttle, $250M (assumption)
north_shuttle=arc_day*15.5/DWT
afr_day=45e3+25e3                      # Russian-built Aframax TC + fuel
north_onward=afr_day*2*27/(100e3)+0.5e6/100e3   # Murmansk-China/India via Suez ~27 d one way
north=5+2+north_shuttle+8+2+north_onward       # pumping opex, terminal, shuttle, icebreaker, STS, onward
print(f"south (Purpe-Transneft-Kozmino) marginal ${south:.0f}/t; north (Sever-Murmansk-Suez) marginal ${north:.0f}/t")
print(f"  north components: shuttle ${north_shuttle:.0f}/t onward ${north_onward:.0f}/t")
# ---- full cost incl. idle sunk capex of the northern system
CAPEX_IN=4e12/FX                      # 4 trn RUB invested (Sechin, FACT 52)
for mt in (3,6,10,20,30,50):
    cc=CAPEX_IN*CRF/(mt*1e6)
    print(f"north {mt:2d} Mt/y: sunk capex charge ${cc:5.0f}/t, full ${cc+north+60:5.0f}/t (incl $60/t lifting) vs realised ${REAL:.0f}/t")
# ---- Sever storage buffer: 14 x 30 kt
stor=14*30e3
for lift in (3,6,10,30):
    print(f"lift {lift} Mt/y: Sever tanks = {stor/(lift*1e6/365):.0f} days buffer")
# ---- value of gating Payakha drilling to hull arrivals
cap_per_tpy=800.0                     # $/t/y upstream capacity (assumption, Arctic greenfield)
for defer_mt,yrs in ((15,2),(15,3),(25,3)):
    capex=defer_mt*1e6*cap_per_tpy
    pv=capex*(1-1/1.12**yrs)
    print(f"defer {defer_mt} Mt/y Payakha capacity {yrs} y: capex ${capex/1e9:.0f}bn, PV saving ${pv/1e9:.1f}bn")
