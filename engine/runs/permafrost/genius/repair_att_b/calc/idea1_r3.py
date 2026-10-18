import math
exec(open(__file__.replace('idea1_r3.py','idea1_r2.py')).read().split('for R in (6,9):')[0])
for rate in (20,40):
  for c in (0.5,1):
    m,D,f,Cd,cpg,V=run(9,c,rate=rate)
    print(f"rate={rate} m3/h R=9 c={c}: Cd={Cd:.0f} rub/m3 cost={cpg:,.0f} rub/g ; vs cheapest W40 {min(pit(40),dredge(40))/cpg:.1f}x ; W25 {min(pit(25),dredge(25))/cpg:.1f}x ; margin at 12088 rub/g = {(GOLD-cpg)/GOLD:.0%}")
