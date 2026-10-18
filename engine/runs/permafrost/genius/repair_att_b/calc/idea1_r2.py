# IDEA 1 round 2: self-consistent Cd(V_hole) with jet reach R; find regime where anchor strongest
import math
GOLD=12088
def run(R,c,hp=1.5,gp=2.5,drill=10000,depth=55,team_cost=(24*100*25000+40e6),rate=20,units=2,avail=0.75,days=100):
    P0=math.pi*R*R*hp; best=None
    for i in range(1,300):
        D=i*0.05; V=D*P0
        f=1-math.exp(-D/(1+c))
        prod=units*rate*24*days*avail          # m3 drawn per season
        Cd=depth*drill/V + 7*22 + team_cost/prod
        gold=P0*gp*f*0.85*0.85
        cost=Cd*V; m=gold*GOLD-cost
        if best is None or m>best[0]: best=(m,D,f,Cd,cost/gold,V)
    return best
def pit(W,H=50,hp=1.5,slope=2.0,cs=250,wash=400,gp=2.5,rec=0.85):
    SR=H*(W+slope*H)/(W*hp); return (SR*cs+wash)/(gp*rec)
def dredge(W,H=53,hp=1.5,m=3.0,cl=100,gp=2.5,rec=0.80):
    SR=H*(W+m*H)/(W*hp); return SR*cl/(gp*rec)
for R in (6,9):
  for c in (0.5,1,2):
    m,D,f,Cd,cpg,V=run(R,c)
    r40=min(pit(40),dredge(40))/cpg; r80=min(pit(80),dredge(80))/cpg
    print(f"R={R} c={c}: D*={D:.2f} V_hole={V:.0f} m3 extraction={f:.2f} Cd={Cd:.0f} rub/m3 cost={cpg:,.0f} rub/g ; vs cheapest baseline W40 {r40:.1f}x, W80 {r80:.1f}x")
# thicker pay (3 m) and richer narrow channel
for hp,gp in ((3.0,2.5),(1.5,4.0)):
    m,D,f,Cd,cpg,V=run(9,1,hp=hp,gp=gp)
    print(f"R=9 c=1 hp={hp} gp={gp}: cost={cpg:,.0f} rub/g ; baseline W40 pit {pit(40,hp=hp,gp=gp):,.0f} dredge {dredge(40,hp=hp,gp=gp):,.0f} -> {min(pit(40,hp=hp,gp=gp),dredge(40,hp=hp,gp=gp))/cpg:.1f}x")
