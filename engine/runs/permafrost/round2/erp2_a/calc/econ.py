# Per-unit cost comparisons (assumptions flagged in NOTES.md). CRF 12%/yr.
CRF=0.12
print("=== Idea 1: per t Ni delivered, Kun-Manie-scale 25 kt Ni/yr, Ni price $15,500/t")
Ni=25e3; P=15500
truck=0.10; rail=0.03
# anchor increment vs same carbonyl refinery at PoS/BAM junction shipping pellets by rail
CO=2.53*203
absorber=(50e6+75e6)/2*CRF/Ni
safety_inj=20e6*CRF/Ni
anchor_extra=CO+absorber+safety_inj+50
saved=900*rail*1.0
print(f"anchor extra cost ${anchor_extra:.0f}/t Ni (CO {CO:.0f}, GPP absorber {absorber:.0f}, injection/leak detection {safety_inj:.0f}, stripper/decomposer 50) vs pellet rail freight saved ${saved:.0f}/t Ni")
print(f"break-even pellet freight: {anchor_extra/0.2:.0f} km of winter road at $0.20/t-km, or {anchor_extra/rail:.0f} km of rail")
# whole chain vs best practice (concentrate sale, 8% Ni conc, 70-75% payability)
conc=1/0.08
for pay in [0.70,0.75]:
    C=(1-pay)*P+conc*(340*truck+2500*rail+10)
    print(f"concentrate sale (payability {pay:.2f}): ${C:.0f}/t Ni lost vs LME")
for capint in [30e3,45e3]:
    A=capint*CRF+2000+1.4*340*truck+anchor_extra
    print(f"on-site matte+carbonyl+pipeline (capex ${capint/1e3:.0f}k per annual t): ${A:.0f}/t Ni; same without anchor (rail pellets): ${A-anchor_extra+saved:.0f}")
print()
print("=== Idea 2: per t Cu cathode, 10-16 kt Cu/yr, remote off-grid diesel $0.30/kWh (grid $0.06)")
EW_kWh=2.1
def sxew(p):
    return 240 + EW_kWh*1000*p + 120 + 5000*CRF   # SX opex, EW power, EW other opex, SX-EW capex $5,000 per annual t
for p in [0.30,0.06]:
    print(f"SX-EW baseline at ${p}/kWh: ${sxew(p):.0f}/t Cu")
for c0,ice,frac_ew in [(2.5,496,0.50),(5,243,0.245),(10,117,0.118),(15,77,0.078)]:
    V=1000/c0  # m3 PLS per t Cu
    for fc in [1.5,2.5]:
        freeze=V*fc
        eng_kwh=frac_ew*EW_kWh*1000
        eng_cost=eng_kwh*0.375   # natural-draft incremental tower + ORC, capital charge ~$0.30-0.45/kWh
        diesel=(EW_kWh*1000-eng_kwh)*0.30
        tot=freeze+eng_cost+diesel+120+2500*CRF+60   # EW other opex, EW capex, dissolution of vitriol
        print(f"PLS {c0:4.1f} g/L, freeze ${fc}/m3: freeze ${freeze:.0f}, engine supplies {frac_ew*100:.0f}% of EW, total ${tot:.0f}/t Cu -> ratio vs SX-EW diesel {sxew(0.30)/tot:.2f}")
print()
print("=== Idea 3: per t Li2O in concentrate delivered 700 km by winter road ($0.15/t-km), ore 1.2% Li2O, 1 Mt/yr")
mine=6.0; haul=700*0.15
routes={
 'raw ore haul':(1.0,0.0,0,1.0),
 'DMS (coarse) + haul':(0.60,8.0,50e6,0.012*0.60/0.058),
 'Arctic flotation(+DMS) + haul':(0.80,22.0,130e6,0.012*0.80/0.060),
 'XRT/optical ore sorting + haul':(0.88,3.0,25e6,0.42),
 'self-charging tribo cascade + haul':(0.82,11.0,45e6,0.161),
}
res={}
for k,(rec,opex,capex,mass) in routes.items():
    perore=mine+opex+capex*CRF/1e6+mass*haul
    perLi2O=perore/(0.012*rec)
    res[k]=perLi2O
    print(f"{k:38s}: ${perore:6.1f}/t ore -> ${perLi2O:7.0f}/t Li2O delivered (rec {rec:.2f}, mass pull {mass:.3f})")
best=min(v for k,v in res.items() if 'tribo' not in k)
print(f"best baseline / tribo = {best/res['self-charging tribo cascade + haul']:.2f}")
