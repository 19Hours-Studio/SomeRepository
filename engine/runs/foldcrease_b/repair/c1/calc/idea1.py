# Idea 1: tensioned drumhead hinge. Plate under tension with eigen-curvature (set).
# Fourier: W(k) = K0(k)/(k^2 + T/D)  -> reduction factor 1/(1+T/(D k^2)) per harmonic.
import numpy as np
D_list=[3.9e-4, 1.0e-3]            # N*m, kill-test floor and a partly-coupled stack
# crease geometry: HTX Duo 167um, 1.24deg after 3000 folds (FACT 5); cosine width w = pi*h/slope
h=167e-6; th=np.radians(1.24); w=np.pi*h/th
print(f"HTX-implied crease full width w = {w*1e3:.1f} mm")
# visibility targets (see LOG/NOTES): depth<=2um, slope<=0.3 mrad, curvature<=0.5 1/m, haptic < Louw thr
def louw(width_m):  # Louw 2000: A = a*w^1.3, fitted to 8 mm at 240 mm
    a=8e-3/(0.240**1.3); return a*width_m**1.3
def profile(x, comps):  # sum of raised-cosine bumps (h, w)
    z=np.zeros_like(x)
    for hh,ww in comps:
        m=np.abs(x)<ww/2; z[m]+=hh/2*(1+np.cos(2*np.pi*x[m]/ww))
    return z
N=2**16; L=0.15; x=np.linspace(-L/2,L/2,N,endpoint=False); dx=x[1]-x[0]
k=2*np.pi*np.fft.fftfreq(N,dx)
def flatten(z,T,D):
    Z=np.fft.fft(z); f=1/(1+T/(D*np.where(k==0,1e-12,k)**2)); f[0]=1/(1+T/D*1e24)
    zz=np.real(np.fft.ifft(Z*f)); zz-=zz.min(); return zz
def metrics(z):
    s=np.gradient(z,dx); c=np.gradient(s,dx); return z.max()-z.min(), np.abs(s).max(), np.abs(c).max()
cases={"new Duo-like 48um wide":[(48e-6,w)],
       "3000-fold 167um wide":[(167e-6,w)],
       "48um wide + 10um narrow ridge 3mm":[(48e-6,w),(10e-6,3e-3)]}
# OCA shear limit: shear-lag lambda = sqrt(E t h/G)
E,t,hO,G=5e9,30e-6,25e-6,9e4   # PI 30um, OCA 25um, G' 25C (FACT 12)
for lam in [np.sqrt(E*t*hO/G), 15e-3]:
    for gam in [0.5,3.0]:
        print(f"lambda={lam*1e3:.1f}mm gamma_allow={gam:.0%}: T_max={gam*G*lam:.0f} N/m -> {gam*G*lam*0.151:.0f} N over 151 mm")
for name,c in cases.items():
    z=profile(x,c); d,s,cu=metrics(z)
    print(f"\n{name}: depth {d*1e6:.1f}um slope {s*1e3:.2f}mrad curv {cu:.2f}/m")
    for D in D_list:
        for T in [300,675,3900]:
            zz=flatten(z,T,D); d2,s2,c2=metrics(zz)
            ok = d2<=2e-6 and s2<=0.3e-3 and c2<=0.5
            print(f"  D={D:.1e} T={T:5d}N/m: depth {d2*1e6:6.2f}um slope {s2*1e3:6.3f}mrad curv {c2:6.3f}/m  INVISIBLE={ok}")
print(f"\nLouw haptic threshold: w=3mm {louw(3e-3)*1e6:.0f}um, w=10mm {louw(10e-3)*1e6:.0f}um, w=24mm {louw(24e-3)*1e6:.0f}um")
# stretch needed and thermal error (why closed loop / series spring)
EA=70e9*30e-6+5e9*150e-6; Lspan=30e-3
for T in [300,675]:
    d=T/EA*Lspan; print(f"T={T}: panel strain {T/EA*100:.4f}%  stretch over 30mm span {d*1e6:.2f}um")
dCTE=10e-6; dT=40; print(f"thermal mismatch over span, 40K: {dCTE*dT*Lspan*1e6:.1f}um  -> open-loop cam tension error >100%")
kser=675*0.151/100e-6; print(f"series spring for 100um travel: {kser/1e3:.0f} N/mm (whole fold)")
# reverse-creep budget: OCA sustained shear stress at T=675 lam=15mm
print(f"OCA tau at T=675, lam=15mm: {675/15e-3:.0f} Pa, gamma {675/15e-3/G:.2f}")
