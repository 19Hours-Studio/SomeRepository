import numpy as np
pi=np.pi
# ---------- shared ----------
TARGET_DEPTH=20e-6   # assumed "invisible" target (< 60 um "good" grade and < 143 um mean perception threshold, SNU study)
def slip(d): return pi*d                 # interlayer slip for a 180 deg fold, midplane separation d
print("check slip: d=50um ->", slip(50e-6)*1e6, "um (idea 1 states 157 um)")
def sag(theta,L): return L*theta/8       # circular-arc sag of a band of length L turned through theta (small angle)

# ---------- Idea 1: gel band, OCA outside band carries slip at band edges ----------
R1=1.5e-3; L1=pi*R1; d1=50e-6
theta_max=8*TARGET_DEPTH/L1; dr_max=theta_max*d1
print("\nIDEA1 band L=%.1f mm, allowed residual rotation %.3f rad -> residual slip <= %.2f um of %.0f um = %.2f%%"%(L1*1e3,theta_max,dr_max*1e6,slip(d1)*1e6,100*dr_max/slip(d1)))
for r in (0.10,0.15):
    print("  OCA residual %.0f%% -> margin %.2f"%(r*100,(dr_max/slip(d1))/r))
# shear-lag length of OCA next to band (CPI 50um, E=6GPa; OCA 25um, G'=5e4 Pa @60C)
lam=np.sqrt(6e9*50e-6*25e-6/5e4); print("  shear-lag length beyond band %.1f mm; peak OCA shear strain %.0f%%"%(lam*1e3,100*slip(d1)/25e-6))

# ---------- Idea 2 ----------
t2=60e-6; R2=5e-3
eps2=t2/(2*R2); print("\nIDEA2 strain bonded 60um at R=5mm: %.2f%%; CPI zero-residual threshold ~5mm*(50um film)->%.2f%%; margin %.2f"%(eps2*100,50e-6/(2*5e-3)*100,(50e-6/(2*5e-3))/eps2))
spine=2*R2+2*t2+2*0.8e-3; print("  spine thickness >= %.1f mm (2R+2t+2x0.8mm walls) vs claimed 10 mm vs Fold7 8.9 mm"%(spine*1e3))
L2=pi*R2; print("  idea's own 0.05%% residual strain, free 60um film: sag %.0f um"%( (2*5e-4/t2)*L2**2/8*1e6))
print("  residual strain fraction allowed for 20um: %.2f%%"%(100*(8*TARGET_DEPTH/L2)/pi))

# ---------- Idea 3: unbonded layers bonded outside zone ----------
R3=2e-3; L3=pi*R3
for name,d in (("glass-OLED",15e-6+5e-6+10e-6),("glass-plate",15e-6+5e-6+20e-6+5e-6+37e-6)):
    D=slip(d); A=(2/pi)*np.sqrt(L3*D); area=(2/pi)*A*L3
    print("\nIDEA3 %s d=%.0fum: length mismatch %.0f um = membrane strain %.2f%%; buckle amp %.0f um; extra fluid %.2f mm^2/mm vs available %.3f"%(name,d*1e6,D*1e6,100*D/L3,A*1e6,area*1e6,5e-6*15e-3*1e6))
    print("   fluid-volume margin %.3f"%((5e-6*15e-3)/area))
# squeeze film: stylus 1N, a=2mm, mu=1 Pa.s, 5->4.5 um
mu=1.0;F=1.0;a=2e-3
ts=3*pi*mu*a**4/(4*F)*(1/4.5e-6**2-1/5e-6**2); print("   squeeze 5->4.5um under 1N stylus: %.2f s"%ts)

# ---------- Idea 4: tension flattening, beam-column with imperfection ----------
def fd_beam(T,D,L,w0amp,n=400):
    # D w'''' - T w'' = D w0''''  (initial imperfection w0 = amp sin(pi x/L)), simply supported
    x=np.linspace(0,L,n+2)[1:-1]; h=L/(n+1)
    I=np.eye(n); D2=(np.diag(-2*np.ones(n))+np.diag(np.ones(n-1),1)+np.diag(np.ones(n-1),-1))/h**2
    D4=D2@D2
    w0=w0amp*np.sin(pi*x/L)
    w=np.linalg.solve(D*D4-T*D2, D*D4@w0)
    return w.max()
Dstack=70e9*(45e-6)**3/(12*(1-0.22**2))+1e-4   # 45um UTG (Fold7, ZDNet Korea) + ~1e-4 polymers
print("\nIDEA4 D=%.2e N.m"%Dstack)
print("  FD check T=0: w/w0=%.3f (expect 1)"%(fd_beam(0,Dstack,9.4e-3,1)))
T01=0.001*(70e9*45e-6+400e3*1e-3*1)  # 0.1% x (UTG 3150 + ~400 N/m polymers)
T01=0.001*70e9*45e-6+400.0
lamg=np.sqrt(70e9*45e-6*25e-6/5e4)
print("  T at 0.1%% = %.0f N/m; force over 151mm fold line = %.0f N; glass shear-lag %.0f mm; peak OCA shear %.0f kPa vs G'(60C) 45-65 kPa"%(T01,T01*0.151,lamg*1e3,T01/lamg/1e3))
Tav=0.5*T01  # after 40-50% stress relaxation of OCA at 60C (Samsung patent)
for L in (9.4e-3,4e-3):
    Tcr=pi**2*Dstack/L**2
    fa=1/(1+Tav/Tcr); fn=fd_beam(Tav,Dstack,L,1)
    Tneed=4*Tcr
    print("  L=%.1fmm Tcr=%.0f N/m; reduction x%.1f (analytic) x%.1f (FD); T needed for x5 = %.0f N/m; margin %.2f; 50um->%.1f um"%(L*1e3,Tcr,1/fa,1/fn,Tneed,Tav/Tneed,50*fn))
