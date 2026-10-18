import math
print("=== IDEA 1: Thermal drift-and-drop ===")
g=9.81
# 1. clamped beam under self weight: sigma = gamma*t*L^2/12 / (t^2/6) = gamma*L^2/(2t)
def span(t, sigma, gamma=20e3, t_eff=None):
    # load from full thickness t, resisting section t_eff
    if t_eff is None: t_eff=t
    # sigma = (gamma*t*L^2/12)/(t_eff^2/6) = gamma*t*L^2/(2 t_eff^2)
    return math.sqrt(2*t_eff**2*sigma/(gamma*t))
for gamma in (20e3,22e3):
    for t in (6,8,10,15):
        print(f"gamma={gamma/1e3:.0f} t={t}: L(0.2)={span(t,0.2e6,gamma):.1f} L(0.5)={span(t,0.5e6,gamma):.1f} L(1.0)={span(t,1.0e6,gamma):.1f}")
# active layer (thawed, zero tensile) reduces resisting section
for t in (6,10,15):
    for a in (0.5,1.5,2.5):
        print(f"t={t} active={a}: L(1.0MPa)={span(t,1e6,20e3,t-a):.1f}  L(0.5)={span(t,0.5e6,20e3,t-a):.1f}")

# 2. Vyalov time-dependence sigma(t)=beta/ln(t/B), fitted through designer's own numbers
t0=30.0           # s, conditionally instantaneous (20-30 s test)
tinf=50*365*86400 # s, 'long-term' service horizon
for s_inf in (0.2,0.35,0.5):
    # beta/ln(t0/B)=1 ; beta/ln(tinf/B)=s_inf
    x=(s_inf*math.log(tinf)-math.log(t0))/(1-s_inf)   # x=-lnB
    B=math.exp(-x); beta=math.log(t0/B)
    out=[]
    for days in (1/24,1,2.3,7,30,77):
        tt=days*86400
        out.append((days,beta/math.log(tt/B)))
    print(f"long-term={s_inf}: "+", ".join(f"{d:g}d:{s:.2f}MPa" for d,s in out))
    # span at 6 m and 10 m cover with strength at 7 and 30 days
    for d in (7,30):
        s=beta/math.log(d*86400/B)*1e6
        print(f"   span at {d} d: t=6 {span(6,s):.1f} m, t=10 {span(10,s):.1f} m")

# 3. working time windows
for rate in (0.15,1,5):
    widen=(25-2)/2/rate
    drive30=30/rate; drive60=60/rate
    print(f"thaw {rate} m/d: widen 2->25 m {widen:.1f} d ; drive 30-60 m drift {drive30:.0f}-{drive60:.0f} d")

# 4. heat penetration into roof from warm drift
alpha=1.0e-6
for d in (2.3,7,30,77):
    print(f"heat penetration sqrt(4 a t) after {d} d = {math.sqrt(4*alpha*d*86400):.2f} m")

# 5. thaw-water heat balance
for wi in (0.2,0.3):
    Q= wi*917*334e3 + 2.0e6*3   # latent + sensible (-3C to 0)
    for dT in (4,7,10):
        print(f"ice {wi}: thaw heat {Q/1e6:.0f} MJ/m3 ; water at dT={dT}: {Q/(4.18e6*dT):.1f} m3/m3 at 100% eff, {Q/(4.18e6*dT*0.6):.1f} at 60%")

# 6. trench fraction
for L in (30,60):
    for b in (4,8):
        for sides in (1,2):
            H=10
            vert=b/(b+sides*L)
            slope=((b+5)*H)/((b+sides*L)*H)   # 1:0.5 slopes, top width b+10
            print(f"L={L} b={b} sides={sides}: trench share vertical {vert*100:.0f}% sloped {slope*100:.0f}%")

# 7. fuel check
for cv in (0.08,0.12):
    slurry=1/cv
    mass=slurry*1000+1000*1.65  # water + solids excess
    H=20
    E=mass*g*H/0.2/0.75/3.6e6  # kWh shaft for hydroelevator
    mon=8*0.6e6/0.75/3.6e6
    L=(E+mon)*0.27
    print(f"cv={cv}: hydroelevator {E:.1f} kWh + monitor {mon:.1f} kWh => {L:.2f} L diesel => {L*80:.0f}-{L*110:.0f} rub/m3 (claim 60)")

# 8. ratios
print("ratios open cut", 2270/1930, 3980/1930, " underground", 3500/1930, 7000/1930)
for rec_loss in (0.1,0.2,0.3):
    c=1930/(1-rec_loss)
    print(f"if recovery {1-rec_loss:.0%} vs open-cut equal: cost {c:.0f} -> ratio {2270/c:.2f}-{3980/c:.2f}")
# 62 m3/m guess
print("62 m3/m = e.g. 10 m x 5 m x swell", 62/50)
