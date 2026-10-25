import math
nu=0.25
def D(E,t): return E*t**3/(12*(1-nu**2))
# check on a known case: Idea 4's UTG D (stated 1.6e-4) and bonded strain t/2R (Idea 2: 160um ->4%)
print("check D_UTG30", D(70e9,30e-6), " check t/2R 160um,R2mm", 160e-6/(2*2e-3))
R=2e-3
# --- Ideas 1/2: unbonded zone, layers pinned at zone ends -> equal free lengths
for name,d,L in [("I1 glass-PI",30e-6,15e-3),("I2 UTG-pol",45e-6,10e-3),("I2 pol-PI",45e-6,10e-3)]:
    print(name,"fold-induced membrane mismatch pi*d/L =",round(math.pi*d/L*100,2),"%")
for name,t,L in [("I1 PI20 L15",20e-6,15e-3),("I2 PI20 L10",20e-6,10e-3),("I2 pol50 L10",50e-6,10e-3)]:
    ecr=math.pi**2*t**2/(3*L**2)   # clamped-clamped Euler strain
    for dcte in (1e-6,3.5e-6):
        em=dcte*40
        print(name,"eps_cr=%.2e"%ecr,"dCTE=%.1fppm eps_th=%.1e margin=%.3f"%(dcte*1e6,em,ecr/em))
    em=3.5e-6*40; A=2.5e-6; lam=math.pi*A/math.sqrt(em)
    print("   gap-limited wrinkle: lambda=%.0f um slope=%.1f mrad"%(lam*1e6,2*math.sqrt(em)*1e3))
# --- Ideas 3/4: tension flattening, sinusoidal dent width w
Dst=D(3e9,80e-6)+D(70e9,30e-6)+D(4e9,40e-6)+D(8e9,30e-6)+D(4e9,50e-6)  # decoupled lower bound
print("stack D lower bound",Dst)
w=3e-3;k=math.pi/w
for T in (600,2000,4000):
    for Dv,lab in ((D(70e9,30e-6),"UTG only"),(Dst,"stack")):
        r=Dv*k**2/(Dv*k**2+T); print("T=%d %s residual ratio %.2f  167um->%.0f um"%(T,lab,r,167*r))
Treq=Dst*k**2*(20/2-1); print("T for 20->2um:",round(Treq),"N/m; force over 0.151m:",round(Treq*0.151),"N")
EtUTG=70e9*30e-6
for G,lab in ((9e4,"25C"),(9e4*0.59,"80C")):
    Tav=3.0*math.sqrt(G*EtUTG*25e-6); print("OCA",lab,"T_avail at gamma=300%%: %.0f N/m margin %.2f"%(Tav,Tav/Treq))
# Idea 4: cam displacement control
Etot=EtUTG+0.5e6; T=600; span=0.136
stroke=T/Etot*span; print("I4 stroke um",stroke*1e6,"; +-30% T tol ->",0.3*stroke*1e6,"um")
print("I4 thermal drift Al(23)-UTG(8.7) 40K um",(23-8.7)*1e-6*40*span*1e6)
print("I4 margin assembly only",0.3*stroke/30e-6," with Al thermal",0.3*stroke/(30e-6+(23-8.7)*1e-6*40*span))
