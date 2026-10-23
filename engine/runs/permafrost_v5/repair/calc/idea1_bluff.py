# Idea 1: river-bluff lignite with layer-by-layer natural thaw (scrape thawed skin every few days)
import math
L_ice = 334e3            # J/kg
rho_lig = 1250           # kg/m3 frozen lignite (bulk, typical brown coal 1.2-1.3)
for w in (0.25, 0.35):   # total moisture mass fraction (Yakutian brown coals ~20-40%; assumption)
  Lv = rho_lig*w*L_ice   # J/m3 latent per m3
  for k in (0.33, 0.5):  # thawed wet lignite W/mK (Herrin&Deming 1996 matrix mean 0.33; wet higher)
    for Ts in (8, 12):   # mean surface temp of dark exposed face above 0C, Jun-Aug (air ~13-16C July Zyryanka/Srednekolymsk; face lower)
      for d in (0.10, 0.20):     # thawed skin removed each cycle (m)
        t = Lv*d*d/(2*k*Ts)      # Stefan time to thaw d from 0
        rate = d/(t/86400)       # m/day
        q = Lv*d/t               # mean flux W/m2 needed
        # surface energy cap: assume <=110 W/m2 net into ground for a dark face (Jul net rad ~120-150 W/m2 daily mean)
        cap = 110/Lv*86400
        r = min(rate, cap)
        print(f"w={w} k={k} Ts={Ts} d={d}: Stefan {rate*100:.1f} cm/d (q={q:.0f} W/m2), capped {r*100:.1f} cm/d, season(85 d) {r*85:.1f} m")
# Field anchor: freshly exposed placer surface thaws ~4 in (10 cm)/day in Yukon/Alaska summer (AIME 1951 'Solar thawing...') -> gravel, k~2, lower ice
print("one-shot face thaw (kill test): 0.9-1.35 m/yr")
# Required face length for village need
need = 6000.0  # t lignite/yr (~3,000 tce at 3,500 kcal) for ~1,000 people (idea's figure)
seam = 3.0
for retreat in (2.5, 3.5, 5.0):
  per_m = seam*retreat*rho_lig/1000*0.9   # 90% recovery
  print(f"retreat {retreat} m/season -> {per_m:.1f} t per m face -> face length {need/per_m:.0f} m")
# Cost per tonne (rub, 2025), conventional small-equipment micro-pit costs, assumptions flagged
exc=25e6; doz=20e6; ldr=12e6          # excavator 20-25t, D6-class dozer, loader (new, rub, assumption)
capex=exc+doz+ldr; crf=0.20           # 8 yr life, ~12% rate
own=capex*crf
crew=4*0.35e6*1.0                     # 4 people x ~4 months x ~350k/month incl. northern allowances? -> per person season
crew=4*4*250e3
fuel=90*2*8*12*0.85*90                # 90 days x 2 machines x 8 h x 12 L/h x 0.85 kg/L... -> use L x price
fuel=90*2*8*12*95                     # L x 95 rub/L arctic diesel (assumption)
repairs=0.08*capex
regul=6e6                             # licence, mine survey, Rostekhnadzor, project docs amortised per yr (assumption)
strip=1.0                             # m3 overburden per m3 coal (site-selection limit: overburden <= seam)
pit=(own+crew+fuel+repairs+regul)
print(f"pit cost {pit/1e6:.1f} M rub/yr -> {pit/need:.0f} rub/t lignite (strip ratio {strip} handled by same fleet)")
# Winter haul 30 km: ice/snow road 30 km construction+maint ~0.15-0.3 M rub/km/season (assumption), trucking 25-40 rub/t-km
for road_km_cost, tkm in ((0.15e6,25),(0.3e6,40)):
  haul = 30*road_km_cost/need + 30*tkm + 300  # + 300 rub/t loading/stockpile
  tot=pit/need+haul
  print(f" road {road_km_cost/1e6} M/km, {tkm} rub/tkm: haul {haul:.0f}, total {tot:.0f} rub/t lignite -> {tot/3.5:.0f} rub/Gcal(fuel)")
# Baselines per Gcal of fuel heat (boiler efficiency penalty for lignite: 0.65 vs 0.75 hard coal, assumption)
for name, price, kcal, eff in (("imported hard coal delivered, low",15000,5200,0.75),("imported hard coal delivered, high (run baseline)",23000,5200,0.75)):
  print(f"{name}: {price/(kcal/1000)/eff:.0f} rub per useful Gcal")
for tot in (pit/need+30*0.15e6/need+30*25+300, pit/need+30*0.3e6/need+30*40+300):
  print(f"local lignite: {tot/3.5/0.65:.0f} rub per useful Gcal")
