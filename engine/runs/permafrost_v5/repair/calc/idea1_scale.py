# Round 2: find regime where anchor is strongest: scale (one bluff serving several villages), thicker seam, municipal dozer reuse
rho=1250; rec=0.9
def cost(need, seam, retreat, km, shared_fleet=False):
    capex=57e6; own=0.20*capex*(0.5 if shared_fleet else 1); rep=0.08*capex
    days=85; hours=8 if need<=8000 else 16
    fuel=days*2*hours*12*95; crew=(4 if hours==8 else 8)*4*250e3; regul=6e6
    pit=(own+rep+fuel+crew+regul)/need
    haul=km*0.2e6/ (need) + km*30 + 300
    face=need/(seam*retreat*rho/1000*rec)
    return pit, haul, face
for need,seam,km,sh in ((6000,3,30,False),(6000,3,30,True),(20000,6,30,False),(20000,6,60,False),(40000,6,60,False)):
    pit,haul,face=cost(need,seam,3.5,km,sh)
    tot=pit+haul; g=tot/3.5/0.65
    print(f"need {need} t, seam {seam} m, haul {km} km, shared fleet {sh}: pit {pit:.0f} haul {haul:.0f} total {tot:.0f} rub/t; face {face:.0f} m; {g:.0f} rub/useful Gcal; ratio vs 3846/5897: {3846/g:.2f}-{5897/g:.2f}")
