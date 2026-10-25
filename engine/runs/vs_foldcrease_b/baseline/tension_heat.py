import math
# Idea 2: in-plane tension T flattens a residual-curvature dip: w ~ (D/T)*kappa0 when L >> l=sqrt(D/T)
for name,Dtot,k0,L in (("current-like",1.0e-3,6.0,9.4e-3),("proposed",2.6e-3,0.038*1.0,18.8e-3)):
    w0=k0*L**2/8
    for T in (250,500,1000,2000):
        l=math.sqrt(Dtot/T); w=min(w0,(Dtot/T)*k0)
        print(f"{name:12s} T={T:5d} N/m  l={l*1e3:.2f}mm  depth {w0*1e6:6.1f} -> {w*1e6:6.2f} um   hinge force over 150mm width {T*0.15:5.0f} N  glass stress {T/70e-6/1e6:.0f} MPa (70um)")
# Idea 3: WLF shift factor (universal constants, Tref=Tg) -> recovery speed-up from heating
def logaT(T,Tg,C1=17.44,C2=51.6): return -C1*(T-Tg)/(C2+T-Tg)
for mat,Tg in (("acrylic OCA",-30),("TPU top film",-40)):
    for Th in (45,60):
        print(f"{mat:12s} Tg={Tg:4d}C heat 25->{Th}C speeds relaxation x{10**(logaT(25,Tg)-logaT(Th,Tg)):.0f}" + (" (WLF invalid below Tg; Arrhenius regime)" if Tg>25 else ""))
print("heater energy 1.5 W x 45 s =",1.5*45,"J =",round(1.5*45/(6000e-3*3.85*3600)*100,3),"% of a 6000 mAh cell")
