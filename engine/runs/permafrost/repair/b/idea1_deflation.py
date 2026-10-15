"""IDEA 1 - Winter Wind Deflation Placer. Anchor: cold dry wind (+sun) freeze-dries frozen pay gravel by
sublimation, and the freed light grains blow away (no liquid water), leaving heavies as a lag.
Sources (see LOG.md): Buck 1981 ice vapour pressure; bulk transfer C~(k/ln(z/z0))^2;
measured winter sublimation: Siberian taiga midwinter 0.01-0.05 mm/d, Alaska tundra 0.08-0.15 mm/d mean,
CRREL permafrost tunnel dried-silt layer growth 0.058 cm/month (Johansen et al. 1981, CRREL SR 81-8);
saltation threshold Shao & Lu 2000; Yukon placer income model 2008 (fuel 65-130 kL/season), YGS: fuel ~30% of cost."""
import math
SIG=5.67e-8; LS=2.834e6; CP=1005.; P=101325.; KAPPA=0.4
def esat_ice(Tc): return 611.15*math.exp(22.452*Tc/(272.55+Tc))   # Pa, Buck (1981)
def q(e): return 0.622*e/P
def rho_air(Tc): return P/(287.*(Tc+273.15))

def surface_balance(Ta,U,RH,SWabs,eps_sky,Tg,dz_g=0.15,k_g=1.8,z0=2e-3,dry_mm=2.0,phi=0.3):
    """daily-mean surface energy balance with sublimation; solve Ts by bisection.
    G = conduction into cold frozen ground at Tg over dz_g (harrowing keeps re-exposing cold material).
    dry_mm: thickness of the dried layer the vapour must diffuse through (series resistance)."""
    ra=rho_air(Ta); C=(KAPPA/math.log(10/z0))**2
    LWin=eps_sky*SIG*(Ta+273.15)**4
    qa=RH*q(esat_ice(Ta))
    Deff=0.66*phi*2.2e-5                       # m2/s, tortuous molecular diffusion in dry layer
    def fluxes(Ts):
        H=ra*CP*C*U*(Ta-Ts)
        r_aero=1/(ra*C*U)                       # s/m  (kg/m2/s per kg/kg)
        # convert diffusion resistance to same units: E = ra*(qs-qa)/(r_aero + r_dif)
        r_dif=(dry_mm/1000)/Deff
        E=ra*(q(esat_ice(Ts))-qa)/(r_aero+r_dif)  # kg/m2/s (+ = sublimation)
        LW=LWin-0.97*SIG*(Ts+273.15)**4
        G=k_g*(Tg-Ts)/dz_g
        return SWabs+LW+H+G-LS*E, E, H, LW, G
    lo,hi=-70.,10.
    for _ in range(80):
        mid=(lo+hi)/2
        if fluxes(mid)[0]>0: lo=mid
        else: hi=mid
    Ts=(lo+hi)/2; _,E,H,LW,G=fluxes(Ts)
    return Ts,E*86400  # kg/m2/day = mm w.e./day

def freed_mm(E_mmwe,ice_vol):  # mm of gravel freed per day
    return E_mmwe/0.917/ice_vol

print("=== ROUND 1-3: sublimation rate by regime (daily mean energy balance) ===")
cases=[ # name, Ta, U10, RH_ice, SWabs, eps_sky, Tground
 ("R1 C.Yakutia Jan, calm Siberian High (orig. design)",-40,1.5,0.85,0,0.70,-25),
 ("R2 Chukotka coast Jan, windy, polar night",-27,7,0.80,0,0.75,-15),
 ("R3a Chukotka/N.Yakutia March, sun on dark gravel",-20,6,0.70,0.80*130,0.72,-15),
 ("R3b April, sun on dark gravel (alb 0.2)",-12,6,0.65,0.80*230,0.75,-10),
 ("R3c early May, before thaw",-5,6,0.65,0.80*280,0.80,-5),
]
res={}
for n,Ta,U,RH,SW,eps,Tg in cases:
    for dry in (0.5,3.0):
        Ts,E=surface_balance(Ta,U,RH,SW,eps,Tg,dry_mm=dry)
        res[(n,dry)]=(Ts,E)
        print(f"{n:55s} dry layer {dry:3.1f}mm: Ts={Ts:6.1f}C  E={E:6.3f} mm w.e./d  freed(ice 0.30)={freed_mm(max(E,0),0.30):5.2f} mm/d  freed(drained ice 0.15)={freed_mm(max(E,0),0.15):5.2f} mm/d")

# midday melt check for April / May (peak absorbed SW ~ 2.3x daily mean)
for n,Ta,U,RH,SWmean,eps,Tg in [("April noon",-8,6,0.6,0.8*230*2.3,0.75,-10),("May noon",-1,6,0.6,0.8*280*2.1,0.8,-5),("May noon, calm",-1,2,0.6,0.8*280*2.1,0.8,-5)]:
    Ts,E=surface_balance(Ta,U,RH,SWmean,eps,Tg,dz_g=0.05,dry_mm=0.5)
    print(f"melt check {n:18s}: Ts={Ts:5.1f} C  (E rate {E:5.2f} mm/d equiv)  {'MELT RISK' if Ts>-0.5 else 'stays frozen'}")

print("\n=== wind threshold: which grains leave (Shao & Lu 2000) ===")
def ustar_t(d,rho_p):
    AN=0.0111; gam=2.9e-4; ra=1.4
    return math.sqrt(AN*(rho_p/ra*9.81*d+gam/(ra*d)))
z0=2e-3
for U10 in (5,7,10):
    us=KAPPA*U10/math.log(10/z0)
    # largest quartz grain moving
    dq=[d*1e-6 for d in range(10,3000,5) if ustar_t(d*1e-6,2650)<us]
    dmax=max(dq) if dq else 0
    dmin=min(dq) if dq else 0
    # gold / cassiterite: smallest size that stays (i.e. largest that moves)
    dau=max([d*1e-6 for d in range(5,3000,1) if ustar_t(d*1e-6,19300)<us] or [0])
    dsn=max([d*1e-6 for d in range(5,3000,1) if ustar_t(d*1e-6,6900)<us] or [0])
    print(f"U10={U10} m/s u*={us:.2f}: quartz moves {dmin*1e6:.0f}-{dmax*1e6:.0f} um; gold lost below {dau*1e6:.0f} um, cassiterite lost below {dsn*1e6:.0f} um")

print("\n=== pad / in-situ area and residue ===")
# assumed typical Kolyma/Yakutia pay gravel size split (mass): >2mm 55%, 0.5-2mm sand 13%, <0.5mm sand+silt 32%
f_gravel,f_csand,f_fines=0.55,0.13,0.32
season_days=60   # March 15-May 15 sun regime
E_spring=res[("R3b April, sun on dark gravel (alb 0.2)",0.5)][1]
fr=freed_mm(E_spring,0.15)   # in-situ on autumn-drained active layer
print(f"spring sublimation {E_spring:.2f} mm w.e./d -> {fr:.1f} mm/d freed of drained gravel; season depth {fr*season_days/1000:.2f} m")
fr_sat=freed_mm(E_spring,0.30)
V=100000.
for lab,f in (("drained (ice 0.15)",fr),("saturated (ice 0.30)",fr_sat)):
    A=V/(f/1000*season_days)
    print(f"  area for {V:.0f} m3/season, {lab}: {A/1e6:.2f} km2")
A_orig=V/(freed_mm(res[('R1 C.Yakutia Jan, calm Siberian High (orig. design)',0.5)][1] if res[('R1 C.Yakutia Jan, calm Siberian High (orig. design)',0.5)][1]>0 else 1e-3,0.30)/1000*150)
print(f"  original midwinter-Yakutia design area for same volume: {A_orig/1e6:.0f} km2")
residue=f_csand+0.01   # coarse sand + heavies after dry screening off >2mm
print(f"residue to summer wash after dry 2-mm screen: {residue*100:.0f}% of pay gravel")

print("\n=== cost per m3 of pay gravel (excavate+feed+wash stage only; stripping unchanged) ===")
diesel=1.5  # $/L delivered to roadless Yakutia/Chukotka (winter-road delivered), assumption
# Yukon placer income model 2008: medium op 130 kL diesel for 40-200k m3 moved -> ~1.0-1.5 L/m3 moved; fuel ~30% of cost (YGS)
wash_L=1.2  # L/m3 pay for dig+feed+pump+tailings (pumps = 60-100% of plant energy, trud.igduran 2023)
cur=wash_L*diesel/0.30
print(f"current: {wash_L} L/m3 x ${diesel}/L / 0.30 fuel share = ${cur:.1f}/m3 pay")
A=V/(fr/1000*season_days)
harrow_L_day=25*(A/1e4)/8.0   # tractor 25 L/h, 8 ha/h (10 m harrow at 8 km/h)
scrape_L_day=25*(A/1e4)/2.4/5 # grader every 5 days, 2.4 ha/h
fuel_def=(harrow_L_day+scrape_L_day)*season_days/V
ops_def=fuel_def*diesel/0.30
screen=0.3   # $/m3 for dry screening residue windrows (mobile screen) applied to all pay
new=ops_def+screen*residue*3+residue*cur   # screening of lag (lag = residue+gravel ~ 0.7 of volume? use 3x residue)
print(f"in-situ deflation ops fuel {fuel_def:.3f} L/m3 -> ${ops_def:.2f}/m3; + screening + washing {residue*100:.0f}% -> total ${new:.2f}/m3")
print(f"RATIO current/new = {cur/new:.1f}x")
print("\nDust: fines emitted per 100k m3 pay:", round(V*f_fines*1.7/1000), "kt (<0.5 mm, of which silt ~", round(V*0.18*1.7/1000),"kt)")

print("\n=== ROUND 4: season integral, lag raked daily into windrows (effective fine dry layer 1 mm) ===")
season=[("Mar15-31",17,-20,6,0.70,0.80*130,0.72,-15),("April",30,-12,6,0.65,0.80*230,0.75,-10),("May1-10",10,-6,6,0.65,0.80*270,0.80,-6)]
tot_we=0
for n,days,Ta,U,RH,SW,eps,Tg in season:
    Ts,E=surface_balance(Ta,U,RH,SW,eps,Tg,dry_mm=1.0)
    tot_we+=E*days
    print(f"  {n:9s}: Ts={Ts:5.1f} E={E:.2f} mm w.e./d")
for ice in (0.15,0.30):
    depth=tot_we/0.917/ice/1000
    print(f"  season (57 d) sublimation {tot_we:.0f} mm w.e. -> deflated depth {depth:.2f} m (ice {ice}); area per 100k m3 = {100000/depth/1e6:.2f} km2")
# midwinter windy-coast add-on (Dec-Feb, 90 d) as bonus
Ts,E=surface_balance(-27,7,0.80,0,0.75,-15,dry_mm=1.0)
print(f"  midwinter windy coast bonus: {E:.3f} mm w.e./d x 90 d = {E*90:.0f} mm w.e. ({E*90/0.917/0.15:.0f} mm drained gravel)")

print("\n=== ROUND 5: honest cost with -10 mm residue (keeps nuggets 2-10 mm) and two deployment modes ===")
diesel=1.5; cur=1.2*diesel/0.30
season_depth=0.16+0.046       # spring + midwinter windy-coast bonus, drained ground (m/yr)
resid=0.25                    # 0.5-10 mm lag fraction sent to washing (13% coarse sand + ~12% fine gravel)
lag=0.68                      # gravel + coarse sand left as lag -> scraped & dry-screened
ops=0.53                      # harrow/rake fuel+labour-equivalent from round 3 ($/m3)
scrape_screen=0.6*lag         # $0.6 per m3 of lag (grader windrow + loader + mobile dry screen)
wash_clean=0.5*cur            # silt-free, pre-sized, dry residue: no scrubbing/clay, little water -> ~half unit cost
insitu=ops+scrape_screen+resid*wash_clean
pad=insitu+1.2                # autumn excavation of thawed drained pay + spreading 0.2 m layer on a pad
print(f"current excavate+feed+wash ${cur:.2f}/m3")
print(f"in-situ (stripped thin-overburden placer or old tailings dump): ${insitu:.2f}/m3 -> {cur/insitu:.1f}x ; depth {season_depth:.2f} m/yr")
print(f"pad mode (virgin thick pay, autumn-spread 0.2 m): ${pad:.2f}/m3 -> {cur/pad:.1f}x")
print(f"area for 100k m3/yr: {100000/season_depth/1e6:.2f} km2")
