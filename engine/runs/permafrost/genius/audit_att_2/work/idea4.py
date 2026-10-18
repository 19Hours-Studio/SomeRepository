import math
print("=== IDEA 4: Ice-deck borehole talik mining ===")
print("90 MJ =", 90/3.6, "kWh")
# Gold P = A h^2 (A kg/cm2, h cm) -> kg
A=3.5
for h in (120,150,180):
    P=A*h*h/1000
    print(f"h={h} cm: short-term {P:.0f} t, 'parked' (x0.5) {P/2:.0f} t, parked at hole/edge (x0.5 again) {P/4:.0f} t")
# flooded ice: 0.6 m of flooded layer counted at 50%
for nat,fl in ((1.2,0.6),(1.4,0.4)):
    he=(nat+0.5*fl)*100
    P=A*he*he/1000
    print(f"natural {nat} + flooded {fl}: effective {he:.0f} cm -> {P:.0f} t short, {P/2:.0f} t parked, {P/4:.0f} t parked at hole")
# characteristic length & spacing
E=4e9; nu=0.33; k=1e4
for h in (1.5,1.8):
    D=E*h**3/(12*(1-nu**2)); l=(D/k)**0.25
    w=245e3/(8*math.sqrt(k*D))
    print(f"h={h}: char length {l:.1f} m, 57 m = {57/l:.1f} l; 25 t elastic deflection {w*1000:.1f} mm; freeboard {h*(1-0.917)*100:.0f} cm")
# coverage of 18 m square grid by R=9 m circles
print("circle/cell coverage pi/4 =", math.pi/4, "; uncovered", 1-math.pi/4)
# triangular grid would need spacing R*sqrt(3) for full coverage
print("full-coverage square spacing = R*sqrt2 =", 9*math.sqrt(2), "m -> holes per area x", (18/(9*math.sqrt(2)))**2)
# submerged jet centreline decay u_c = 6.2 d/x u0  (x>~6d)
for p_MPa,d_mm in ((4,20),(10,25),(15,30)):
    u0=math.sqrt(2*p_MPa*1e6/1000)*0.95
    uc=6.2*(d_mm/1000)/9*u0
    print(f"p={p_MPa} MPa d={d_mm} mm: u0={u0:.0f} m/s, centreline u at 9 m = {uc:.1f} m/s, dyn pressure {0.5*1000*uc**2/1e3:.1f} kPa")
# critical velocity for gravel (approx. u_c ~ 1.4*sqrt(g*(s-1)*d)*... use Shields-based near-bed ~ sqrt(theta*(s-1)*g*d)*~8 depth-avg)
for dm in (0.02,0.05,0.15):
    ustar=math.sqrt(0.05*1.65*9.81*dm)
    print(f"gravel {dm*100:.0f} cm: critical shear velocity {ustar:.2f} m/s, mean-flow critical ~{ustar*8:.1f} m/s")
# cost/g consistency: rub/m3 drawn x D / recovery -> rub per m3 pay recovered
combos=[(1130,3.4,0.89),(1130,3.9,0.86),(1970,3.4,0.89),(1970,3.9,0.86)]
for c,D,r in combos:
    print(f"cost {c} D {D} rec {r}: {c*D:.0f} rub/m3 pay; per m3 recovered-pay {c*D/r:.0f}")
lo=1130*3.4/0.89; hi=1970*3.9/0.86
print("max spread ratio", hi/lo, "claimed 4800/3000=", 4800/3000)
print("implied recovered gold per m3 pay at 3000 rub/g (low combo):", 1130*3.4/3000, "; at 4800 (high combo):", 1970*3.9/4800)
# baseline ratios
print("8800/4800 =", 8800/4800, " 8800/3000 =", 8800/3000, " needed alt cost for 4.4x at 3000:", 4.4*3000)
# season and per-hole time
for thick in (1.0,2.0,3.0):
    pay=18*18*thick
    for D in (3.4,3.9):
        drawn=pay*D
        for q in (20,40):
            h=drawn/q
            print(f"pay {thick} m: {pay:.0f} m3 pay/hole, {drawn:.0f} m3 drawn, at {q} m3/h = {h:.0f} h = {h/24/0.7:.1f} d at 70% util")
# Dilution: waste fraction of drawn
for D,r in ((3.4,0.89),(3.9,0.86)):
    print(f"D={D}: pay in drawn = {r/D:.0%}, waste = {1-r/D:.0%}")
# well-mixed reservoir recovery 1-exp(-D) vs claim
for D in (3.4,3.9):
    print(f"well-mixed R=1-exp(-D) = {1-math.exp(-D):.3f}")
