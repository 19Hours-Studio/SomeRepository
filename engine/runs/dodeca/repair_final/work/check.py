import math, random
# 1) wall thickness re-derivation (calc.py named in FACT 7 is absent from the folder)
phi=(1+5**0.5)/2
def dodeca(h_mm):
    # h = face-to-face height without knobs = 2*inradius
    r_in_per_a = (250+110*5**0.5)**0.5/20
    a = (h_mm/2)/r_in_per_a
    area = 3*(25+10*5**0.5)**0.5*a*a
    return a, area
rho=8.9e-3 # g/mm^3, leaded bronze ~8.9 g/cm3
for h,m,dmean in [(40,35,11),(80,250,20),(100,580,28),(59,81,16)]:
    a,A=dodeca(h)
    holes=12*math.pi*(dmean/2)**2
    knobs=0.10 # assume knobs ~10% of mass
    t=(m*(1-knobs)/rho)/(A-holes)
    print(f"h={h}mm m={m}g edge={a:.1f}mm area={A/100:.0f}cm2 net={(A-holes)/100:.0f}cm2 -> wall~{t:.2f}mm")
# 2) geometry of resting axes
dihedral=math.degrees(math.acos(-1/5**0.5))
print("dihedral",round(dihedral,3),"axis tilt",round(90-(180-dihedral),3))
# 3) Jublains ringed holes (Sparavigna 2012 after Guillier et al. 2008); B-side 4'-6' = {17,22,22} by FACT 31 sums
A=[21.5,16.5,21,11.5,17]; B=[10.5,15.5,17,22,22]
s=sorted(A+B); gaps=[round(s[i+1]-s[i],2) for i in range(len(s)-1)]
print("sorted",s,"gaps",gaps, "meanA",sum(A)/5,"meanB",sum(B)/5)
cls=lambda d: 'S' if d<14 else ('M' if d<19 else 'L')
print("A classes",sorted(map(cls,A)),"B classes",sorted(map(cls,B)))
# 4) how unusual is 3 tight classes? draw 10 uniform sizes in observed range, ask: the two largest gaps >=4mm AND every class spread <=1.5mm
def trial(lo=10.5,hi=22,q=0.5):
    x=sorted(round(random.uniform(lo,hi)/q)*q for _ in range(10))
    g=[x[i+1]-x[i] for i in range(9)]
    idx=sorted(range(9),key=lambda i:-g[i])[:2]
    if min(g[i] for i in idx)<4: return False
    cuts=sorted(idx); parts=[x[:cuts[0]+1],x[cuts[0]+1:cuts[1]+1],x[cuts[1]+1:]]
    return all(max(p)-min(p)<=1.5 for p in parts)
random.seed(1); N=200000
p=sum(trial() for _ in range(N))/N
print("P(random 10 holes form 3 tight classes like Jublains) ~",p)
