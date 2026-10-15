"""IDEA 2 - Self-feeding ore-ice dam. Anchor: the frozen ore pile IS the water-retaining structure, and stored
warm water run over its face melts the ice cement at a flow-set rate, self-dosing gravel into a riffled chute.
Sources: latent heat 334 kJ/kg; Douglas et al. 2023 JGR-ES (ablation-limited permafrost erosion, rates ~3x
smooth-wall theory due to grain roughness; erosion linear in water T, inverse in pore ice);
zolotodb.ru/article/213 (2.2 m3 water per m3 sands in a working placer); trud.igduran 2023 (water supply =
60-100% of wash-plant energy); Yukon placer income model 2008 & YGS (fuel ~30% of cost)."""
import math
Li=334e3; rho_i=917; cw=4.19e6  # J/m3K
def heat_per_m3(n=0.30,T0=-5):
    ice=n*rho_i
    return ice*Li + (1.9e6)*(0-T0)     # J per m3 of frozen saturated gravel (latent + sensible)
print("=== R1: melt heat vs washing water ratio ===")
for n in (0.25,0.30,0.40):
    Qg=heat_per_m3(n)
    for Tw in (5,8,12):
        for eff in (0.4,0.7):
            r=Qg/(cw*Tw*eff)
            print(f"ice frac {n:.2f}: {Qg/1e6:5.0f} MJ/m3 | Tw={Tw:2d}C eff={eff}: water/gravel = {r:4.1f} m3/m3")
print("-> sluicing needs ~2-15 m3 water per m3 (2.2 in zolotodb example); melt-set ratio falls inside the range: self-dosing works thermally")

print("\n=== R1: face area needed (heat-transfer rate) ===")
# turbulent film heat transfer h = St*rho*cp*U ; smooth St~0.0015-0.002, Douglas 2023 rough ~3x
for St in (0.0015,0.005):
    for U in (0.5,1.5):
        h=St*cw*U
        for Tw in (5,10):
            qflux=h*Tw; rate=qflux/heat_per_m3(0.30)   # m/s face retreat
            feed=70/3600  # m3/s target (70 m3/h)
            print(f"St={St} U={U} Tw={Tw}: h={h:6.0f} W/m2K q={qflux/1e3:5.1f} kW/m2 retreat={rate*3600:5.2f} m/h -> face for 70 m3/h: {feed/rate:6.0f} m2")

print("\n=== R2: season water & heat budget, unattended feed ===")
V=60000.  # m3 pay per season (small roadless placer)
days=90; feed=V/(days*24); Tw=8; eff=0.5
r=heat_per_m3(0.30)/(cw*Tw*eff)
Q=feed*r/3600
print(f"{V:.0f} m3 over {days} d = {feed:.1f} m3/h; water ratio {r:.1f} -> {Q*1000:.0f} L/s steady creek/basin outflow")
SWE=0.12; runoff=0.7
print(f"if ALL water from stored snowmelt: catchment {V*r/(SWE*runoff)/1e6:.1f} km2, basin {V*r/1e6:.2f} Mm3 (dam-break hazard) ")
# instead: creek baseflow routed through a small forebay; summer specific runoff Kolyma uplands ~ 5-10 L/s/km2
for qs in (5,10):
    print(f"creek baseflow at {qs} L/s/km2 needs catchment {Q*1000/qs:.0f} km2 (forebay only buffers a few days)")
# solar warming of forebay: need heat feed*Qg; net summer gain of shallow pond ~100 W/m2
P=feed/3600*heat_per_m3(0.30)
print(f"melt power {P/1e3:.0f} kW; if creek water too cold, sun-warming forebay area at 100 W/m2 net: {P/100/1e4:.1f} ha")

print("\n=== R3: keep a sacrificial ore buttress on a permanent frozen core: thaw depth under peat (Stefan) ===")
def stefan(k,dT,days,Lvol): return math.sqrt(2*k*dT*days*86400/Lvol)
# saturated peat: water ~0.85 vol -> L = 0.85*917*334e3; thawed k ~0.5 W/mK
Lpeat=0.85*917*334e3
for dT in (8,12):
    print(f"upstream face under {dT}C water, 100 d: thaw into saturated peat = {stefan(0.5,dT,100,Lpeat):.2f} m ; crest in air (mean 12C, peat k 0.5) = {stefan(0.5,12,100,Lpeat):.2f} m")
print("-> 0.8-1.0 m saturated peat (or peat + 0.3 m ice-rich silt) keeps the core frozen all summer")

print("\n=== R2/R3: buttress geometry & feed self-regulation ===")
H=6.; L=60.; crest_core=6.  # dam height, crest length, core top width
Vb=V; width_b=Vb/(H*L)  # buttress horizontal thickness
print(f"buttress for {V:.0f} m3 at H={H} m, L={L} m: {width_b:.0f} m thick (retreats {width_b/days:.2f} m/day)")
# face area ~ L * H/sin(35deg)
Af=L*H/math.sin(math.radians(35))
for St,U in ((0.0015,0.5),(0.005,1.0)):
    rate=St*cw*U*Tw/heat_per_m3(0.30)*3600
    print(f"  heat-transfer-limited capacity St={St},U={U}: {rate*Af:.0f} m3/h on {Af:.0f} m2 face vs needed {feed:.0f} m3/h -> {'heat supply (flow x T) controls, as anchor claims' if rate*Af>feed else 'face too small'}")

print("\n=== COST per m3 of pay, washing stage (feed+water+wash+tailings), roadless placer ===")
diesel=1.8   # $/L air/winter-road delivered roadless site (assumption)
cur_L=1.2    # L/m3 (dozer feed ~0.4, pumps ~0.6, tailings ~0.2)
cur=cur_L*diesel/0.30
# new: autumn build: dozer places thawed pay from cut directly into dam layers (~= feed push, 0.4 L/m3),
# winter spray pump 0.05 L/m3, peat cover, tailings dozer at chute end 0.15 L/m3, weekly cleanup crew 2 vs 8-10
new_L=0.4+0.05+0.15
labour_cur=8*120*days/V*1.0  # 8 people x $120/day
labour_new=2*120*days/V + 3*120*40/V  # 2 summer + 3 for 40 days autumn build
cap_cur=1.5; cap_new=0.6   # $/m3 equipment ownership (pumps+plant+dozer) vs gate+chute+peat
c_cur=cur_L*diesel+labour_cur+cap_cur; c_new=new_L*diesel+labour_new+cap_new
print(f"current: fuel ${cur_L*diesel:.2f} + labour ${labour_cur:.2f} + equipment ${cap_cur:.2f} = ${c_cur:.2f}/m3 (fuel share {cur_L*diesel/c_cur*100:.0f}%)")
print(f"ore-ice dam: fuel ${new_L*diesel:.2f} + labour ${labour_new:.2f} + equipment ${cap_new:.2f} = ${c_new:.2f}/m3")
print(f"RATIO = {c_cur/c_new:.1f}x on the washing stage (stripping unchanged)")

print("\n=== R4: strongest regime = winter (underground/winter-mined) placer whose hoist already builds a frozen stockpile ===")
# current practice for winter-mined sands: frozen stockpile must be thawed (sprinkling) / ripped, dozed to hopper, water pumped
cur_L=0.5+0.4+0.6+0.2   # rip frozen stockpile + feed + pumps + tailings (L/m3)
lab_cur=10*120*days/V
c_cur=cur_L*diesel+lab_cur+1.8
new_L=0.05+0.15         # spray pump during building + occasional tailings dozing; hoist conveyor lays the layers
lab_new=2*120*days/V
c_new=new_L*diesel+lab_new+0.6
print(f"current (thaw/rip frozen stockpile, feed, pump): ${c_cur:.2f}/m3 ; ore-ice dam: ${c_new:.2f}/m3 ; RATIO {c_cur/c_new:.1f}x")
H=10.; L=80.
print(f"geometry H={H} m, L={L} m: buttress {V/(H*L):.0f} m thick, retreat {V/(H*L)/days:.2f} m/day (chute head advanced weekly)")

print("\n=== HAZARD: dam-break peak outflow (Froehlich 1995: Qp=0.607 V^0.295 H^1.24) ===")
for Vr,Hd,lab in ((0.36e6,10,"full-season snowmelt reservoir (original)"),(0.04e6,6,"forebay only, creek baseflow routed through (repaired)")):
    print(f"{lab:50s}: V={Vr/1e6:.2f} Mm3 H={Hd} m -> Qp={0.607*Vr**0.295*Hd**1.24:.0f} m3/s")
