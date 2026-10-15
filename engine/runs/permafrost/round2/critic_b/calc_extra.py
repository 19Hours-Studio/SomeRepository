"""Extra checks: idea 4 shell-melt sensitivity; idea 1 cost tally; idea 3 pilot statistics."""
import math
# Ashton-type coefficient h = 1622 V^0.8 / D^0.2 (W/m2/K)
for V, D in ((0.2, 3.0), (0.3, 3.0), (0.5, 5.0)):
    h = 1622*V**0.8/D**0.2
    print(f"V={V} D={D}: h={h:.0f} W/m2K")
    for dT in (0.01, 0.03, 0.05, 0.1):
        q = h*dT
        for t in (0.08, 0.10):
            days = t*917*334e3/q/86400
            print(f"   water +{dT} K: {q:.1f} W/m2 -> {t*100:.0f} cm shell gone in {days:.0f} d")
# idea 1 cost tally ($/m3 of pay)
items = {
 "harrow+rake (0.85-3.0)": (0.85, 3.0),
 "load/haul +10mm lag (0.27-0.66)": (0.27, 0.66),
 "wash -10mm residue (0.75-2.1)": (0.75, 2.1),
 "strip pre-existing snowpack 166,600 m3 at $0.3-0.5/m3": (166600*0.3/1e5, 166600*0.5/1e5),
}
lo = sum(v[0] for v in items.values()); hi = sum(v[1] for v in items.values())
for k, v in items.items(): print(f" {k}: {v[0]:.2f}-{v[1]:.2f}")
print(f" total {lo:.2f}-{hi:.2f} $/m3 (claim 1.7) -> ratio vs $6.0 = {6/hi:.1f}-{6/lo:.1f}x (claim 3.6x)")
# if pore ice is 0.30 (undrained/fine tailings): area doubles -> harrow doubles
print(f" with pore ice 0.30: harrow 1.7-6.0 -> total {lo+0.85:.2f}-{hi+3.0:.2f}")
# idea 3: probability a 3-winter pilot sees 3/3 successes if per-winter P=0.3-0.55
for P in (0.3, 0.4, 0.55):
    print(f" per-winter success {P}: P(3/3) = {P**3:.3f}; winters to estimate P within +-0.15 (95%) = {1.96**2*P*(1-P)/0.15**2:.0f}")
# idea 4: pods needed to bound loss
for obs, n in ((0, 60), (0, 300)):
    print(f" {obs} losses in {n} pods -> 95% upper bound {3/n:.3f}")
p = 0.05
print(" pods to estimate 5% loss within +-2% (95%):", round(1.96**2*p*(1-p)/0.02**2))
