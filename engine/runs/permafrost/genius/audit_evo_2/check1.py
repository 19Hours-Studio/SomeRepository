import math
print("=== IDEA 1 ===")
# Shields: tau* = h S/(1.65 D); constant q, Manning: h ~ S^-0.3 -> tau* ~ S^0.7
print("Shields ratio 1%/0.5% if h const:",2.0," if q const (Manning):",2**0.7, " text:",0.043/0.026)
# pond
A=3e4; P=5.4e6
print("pond flux W/m2:",P/A)
# heat needed per m3 ice-saturated gravel
for n in (0.25,0.30,0.35):
    lat=n*917*334e3
    sens=2.0e6*3  # warm from -3C, vol heat cap ~2 MJ/m3K
    print("porosity",n,"latent MJ/m3",lat/1e6,"total",(lat+sens)/1e6)
cw=4.186e6
for T in (4,7):
    d=7*cw*T
    print("T",T,"delivered MJ/m3 gravel (exit 0C):",d/1e6)
# implied need from 1.27 @4C
need=7*cw*4/1.27
print("implied need MJ/m3",need/1e6," ratio at 7C would be",7*cw*7/need, "text 2.5")
# exit temp implied by both 1.27 and 2.5
# (7-Te)/(4-Te)=2.5/1.27
r=2.5/1.27; Te=(r*4-7)/(r-1); print("exit temp implied",Te)
# season
V=216e3; days=70; t=days*86400
Q=7*V/t; print("water flow m3/s",Q)
print("heat demand MW",V*need/t/1e6)
print("pond can raise flow by K:",P/(Q*cw))
print("flow heat at 7C from 0 MW:",Q*cw*7/1e6)
# July-Aug 62 days vs 70-day season
print("Jul+Aug days",31+31)
# per monitor face
pm=V/days/2
for hpay in (1.0,1.5,2.0,3.0):
    adv=pm/(25*hpay)
    flux=adv/86400*need
    print("pay",hpay,"m: face advance m/day",round(adv,1),"required face heat flux kW/m2",round(flux/1e3,1),"h needed at mean dT 2K kW/m2K",round(flux/2/1e3,1))
# roof bending
g=19e3
for h in (10,12,15,20,30):
    L=25
    print("overburden",h,"fixed-fixed sigma MPa",round(g*L**2/(2*h)/1e6,3),"simply sup",round(3*g*L**2/(4*h)/1e6,3))
# overburden ratio 6 -> overburden thickness
for pay in (1,1.5,2,3): print("pay",pay,"overburden at 6:1",6*pay)
# cost
print("implied recovered grade g/m3",650/620)
for c in (556,650,965):
    g_=c/(650/620)
    print("cost rub/m3",c,"rub/g",round(g_),"ratio vs 1100",round(1100/g_,2),"vs 2650",round(2650/g_,2))
