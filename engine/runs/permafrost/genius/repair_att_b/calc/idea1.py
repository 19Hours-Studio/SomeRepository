# IDEA 1: Ice-deck borehole talik mining. All money in rub; gold price CBR Jan-2026 12,088 rub/g.
import math
G=9.81; GOLD=12088
print("=== R1: ice bearing (Gold's formula P=A h^2, A=3.5..7 kg/cm2, TAC/Barrette review) ===")
for h in (120,150,180,200):
    for A in (3.5,7.0):
        print(f" h={h}cm A={A}: P_short={A*h*h/1000:.0f} t ; stationary (x0.5 creep derate, assumption) {A*h*h/2000:.0f} t")
# characteristic length of floating ice plate
E=5e9; nu=0.33; rho_w=1000
for h in (1.2,1.8):
    l=(E*h**3/(12*(1-nu**2)*rho_w*G))**0.25
    print(f" h={h} m: characteristic length l={l:.1f} m -> modules spaced >2.5l={2.5*l:.0f} m act independently")
# loads: drill rig 20 t, mining unit (airlift compressor+jet pump+genset) 25 t, jig/sluice plant in heated tent 20 t
print(" module loads 20/25/20 t; each needs <= stationary capacity")

print("=== R1: thaw energy avoided (frozen gravel, ice 250 kg/m3) ===")
L=334e3; ice=250; ds=1.9e3; cs=800; ci=2100; dT=3
q=ice*L+ (ds*cs+ice*ci)*dT
print(f" thaw energy {q/1e6:.0f} MJ/m3 = {q/3.6e6:.0f} kWh/m3 ; in a talik = 0")

print("=== R1: heat margin of on-ice plant: talik water +2 C carries heat above 0 C ===")
Qw=200/3600  # m3/s process water
print(f" sensible heat above 0C in 200 m3/h at +2C: {Qw*1000*4190*2/1e3:.0f} kW vs tent loss ~ U1*A760*dT40 = {1*760*40/1e3:.0f} kW -> OK if closed loop")

print("=== R2: dilution / extraction model (well-mixed cave zone) ===")
# pay within jet reach R: P0 = pi R^2 h_p.  Drawn volume V. Cave mixing ratio c = caved overburden mixed per unit pay.
# P(V)=P0*exp(-V/(P0*(1+c)))  -> extracted fraction f=1-exp(-D/(1+c)), D=V/P0
def econ(c, R=6.0, hp=1.5, gp=2.5, Cd=1500, bedrock_loss=0.15, plant=0.85):
    P0=math.pi*R*R*hp
    best=None
    for i in range(1,200):
        D=i*0.05
        f=1-math.exp(-D/(1+c))
        gold=P0*gp*f*(1-bedrock_loss)*plant
        cost=Cd*D*P0
        m=gold*GOLD-cost
        if best is None or m>best[0]: best=(m,D,f,gold,cost)
    m,D,f,gold,cost=best
    return D,f,cost/gold, gold, P0
for c in (0.5,1,2,4):
    for Cd in (1000,1500,2500):
        D,f,cpg,gold,P0=econ(c,Cd=Cd)
        print(f" c={c} Cd={Cd}: optimal D={D:.2f} extraction={f:.2f} cost={cpg:,.0f} rub/g ; gold/hole={gold:.0f} g (P0={P0:.0f} m3)")

print("=== R2: cost per m3 drawn (Cd) build-up ===")
depth=55  # 2 m ice + 5 m water + 48 m talik gravel
for drill in (6000,10000,15000):
    D=3; P0=math.pi*36*1.5; V=D*P0
    hole=depth*drill
    energy=7*22   # 7 kWh/m3 (airlift + 1 MPa fluidizing jet in loose gravel; BHM water:solids 8-10:1 TPU) x 22 rub/kWh diesel
    team=(24*100*25000+40e6)/(2*20*24*100*0.75)  # 24 people x 100 d, 40M equipment; 2 mining units 20 m3/h (TPU 10-40 m3/h)
    print(f" drill {drill} rub/m: hole {hole/1e3:.0f}k rub -> {hole/V:.0f} rub/m3; energy {energy:.0f}; team {team:.0f}; Cd={hole/V+energy+team:.0f} rub/m3")
print(" season production per team:",2*20*24*100*0.75,"m3 drawn")

print("=== R3: baselines (same deposit: buried channel W wide, pay 1.5 m, 48 m talik cover + 5 m water) ===")
def pit(W,H=50,hp=1.5,slope=2.0,cs=250,wash=400,gp=2.5,rec=0.85):
    area=H*(W+slope*H)  # trapezoid cross-section, slope 1:2 in dewatered thawed gravel
    SR=area/(W*hp)
    c=SR*cs+wash
    return SR,c,c/(gp*rec)
def dredge(W,H=53,hp=1.5,m=3.0,cl=100,wash=0,gp=2.5,rec=0.80):
    area=H*(W+m*H)   # underwater slope 1:3, everything lifted (submersible-pump suction dredge, to 80 m: booksite)
    SR=area/(W*hp); c=SR*cl
    return SR,c,c/(gp*rec)
for W in (40,80,150,300):
    s1,c1,g1=pit(W); s2,c2,g2=dredge(W)
    D,f,cpg,gold,P0=econ(1,Cd=1500)
    print(f" W={W} m: drain+pit SR={s1:.0f} -> {g1:,.0f} rub/g | pontoon suction dredge lift ratio={s2:.0f} -> {g2:,.0f} rub/g | BHM(c=1,Cd=1500) {cpg:,.0f} rub/g -> ratio vs cheapest {min(g1,g2)/cpg:.1f}x")
print("=== R3: consistency: ice season vs holes ===")
P0=math.pi*36*1.5; V=3*P0; t_draw=V/20; holes=2*20*24*100*0.75/V
print(f" per hole drawn {V:.0f} m3 (TPU per-well 1.2-3.5k m3 -> within range) ; draw {t_draw:.0f} h at 20 m3/h ; holes/season/team {holes:.0f} ; area {holes*math.pi*36/1e4:.2f} ha (hole spacing 2R=12 m)")
print(f" drilling need {holes*55:.0f} m/season = {holes*55/100:.0f} m/day with 100-day ice window")
