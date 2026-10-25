# Idea 2: fluid (shear-free, normal-locked) interlayers; panel is the only creeping layer, sandwiched by
# N fluid-decoupled UTG leaves. Composite eigen-curvature = sum(D_i k_i)/sum(D_i). Clamped-clamped band.
import numpy as np
def Dp(E,t,nu): return E*t**3/(12*(1-nu**2))
Dg=Dp(70e9,30e-6,0.22)
R=2.5e-3
print(f"D UTG30 = {Dg:.2e}; strain UTG30 at R={R*1e3}mm: {15e-6/R:.2%}, stress {70e9*15e-6/R/1e6:.0f} MPa (CS 500-1000 MPa, Schott)")
for tp in [20e-6,30e-6]:
    print(f"panel {tp*1e6:.0f}um strain own midplane {tp/2/R:.2%}")
# coupled comparison: UTG30 + OCA + panel coupled would put panel far from neutral axis; skip, use HTX data as baseline
Lb=np.pi*R  # bend arc length
n=4001; s=np.linspace(0,Lb,n); ds=s[1]-s[0]
kap_fold=np.sin(np.pi*s/Lb)**2*2/R   # smooth fold curvature distribution, integral = pi/R*... normalize to 180deg
kap_fold*=np.pi/np.trapezoid(kap_fold,s)
def residual(f_set,tp,Ep,Nleaf):
    D_p=Dp(Ep,tp,0.34); D_tot=D_p+Nleaf*Dg
    kc=f_set*kap_fold*D_p/D_tot
    # clamped-clamped, symmetric: subtract mean curvature (slope 0 both ends, equal heights by symmetry)
    k=kc-kc.mean()
    slope=np.cumsum(k)*ds; z=np.cumsum(slope)*ds
    return D_p/D_tot,(z.max()-z.min()),abs(slope).max(),abs(k).max()
print("\nf_set = residual natural curvature of free panel / applied (unknown; PU ~0.6-0.7 per FACT 7, PI assumed lower)")
for f in [0.05,0.1,0.2,0.4]:
    for tp,Ep in [(20e-6,6e9),(30e-6,6e9)]:
        for Nl in [1,2,3,5]:
            r,d,sl,c=residual(f,tp,Ep,Nl)
            ok=d<=2e-6 and sl<=0.3e-3 and c<=0.5
            print(f"f={f:.2f} panel {tp*1e6:.0f}um leaves={Nl}: ratio {r:.4f} depth {d*1e6:6.2f}um slope {sl*1e3:6.3f}mrad curv {c:7.3f}/m {'INVISIBLE' if ok else ''}")
# free-panel residual angle equivalent: f*180deg
# slip at free edges, viscous drag, squeeze-flow (drainage) times, optics
d_mid=30e-6+10e-6
print(f"\nslip per interface at each free edge (pinned centreline): {np.pi*d_mid/2*1e6:.0f} um; whole stack 5 leaves+panel ~{np.pi*6*d_mid/2*1e6:.0f} um")
mu=1.0; hgap=10e-6; v=np.pi*d_mid/2/0.5
print(f"viscous shear stress during 0.5 s fold: {mu*v/hgap:.1f} Pa (OCA would be ~{9e4*np.pi*d_mid/2/25e-6:.0f} Pa)")
for p,Lf,lab in [(1.5e3,75e-3,'gravity head, phone upright'),(2e3,5e-3,'panel set pressure'),(5e4,5e-3,'finger 0.5 N on 10 mm2')]:
    tau=12*mu*Lf**2/(p*hgap**3); print(f"squeeze-flow time [{lab}]: {tau:.2e} s = {tau/86400:.1e} days")
n1,n2=1.51,1.50; print(f"interface reflectance UTG/fluid: {((n1-n2)/(n1+n2))**2:.1e} (air gap would be {((1.51-1)/2.51)**2:.3f})")
print(f"fluid thermal: CTE_v 9.6e-4/K x 60K x 10um = {9.6e-4*60*10:.2f} um uniform gap change per film")
# mass/thickness
A=0.150*0.140; print(f"mass per 30um leaf {A*30e-6*2500*1e3:.2f} g; stack thickness 5 leaves+panel+6 films: {(5*30+30+6*10)} um")
