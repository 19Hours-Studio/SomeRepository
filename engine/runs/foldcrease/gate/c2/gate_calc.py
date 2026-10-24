import numpy as np
# plate with natural (set) shape w0 under in-plane tension T:
# energy D/2 (w''-w0'')^2 + T/2 w'^2  ->  w_k = w0_k * D k^2/(D k^2 + T)
def flatten(w0, dx, D, T):
    k = 2*np.pi*np.fft.fftfreq(len(w0), dx)
    W = np.fft.fft(w0)
    f = np.where(k==0, 0.0, D*k**2/(D*k**2+T+1e-300))
    return np.real(np.fft.ifft(W*f))
x = np.linspace(-0.1,0.1,2**16); dx=x[1]-x[0]
# CHECK on known case: single sinusoid, analytic ratio
lam=6e-3; D=1.66e-4; T=600
w0=1e-6*np.cos(2*np.pi*x/lam*0+2*np.pi*np.round(0.2/lam)*x/0.2)  # periodic in box
k=2*np.pi*np.round(0.2/lam)/0.2
w=flatten(w0,dx,D,T); print("check sinusoid num/analytic", w.max()/1e-6, D*k**2/(D*k**2+T))
def Dplate(E,t,nu=0.3): return E*t**3/(12*(1-nu**2))
layers = {"UTG 30um":Dplate(70e9,30e-6,0.22),"PET protect 65um":Dplate(4e9,65e-6,0.38),
          "pol/touch 50um":Dplate(5e9,50e-6,0.35),"OLED/PI 30um":Dplate(8e9,30e-6,0.34),
          "back film 50um":Dplate(4e9,50e-6,0.38)}
for n,v in layers.items(): print(f"D {n}: {v:.2e} N m")
Dsum=sum(layers.values()); print(f"D stack decoupled sum (no plate): {Dsum:.2e}")
def gauss(A,fwhm): s=fwhm/2.3548; return -A*np.exp(-x**2/(2*s**2))
def report(A,fwhm,D,T):
    w=flatten(gauss(A,fwhm),dx,D,T); sl=np.abs(np.gradient(w,dx)).max()
    return abs(w.min()-w.max())*1e6, sl*1e3
for A,fw,lab in [(20e-6,3e-3,"idea1 set 20um/3mm"),(50e-6,3e-3,"Oppo-level 50um/3mm"),(50e-6,1e-3,"sharp 50um/1mm")]:
    for D in (layers["UTG 30um"],Dsum):
        for T in (0,600,3000,1e4):
            d,s=report(A,fw,D,T); print(f"{lab} D={D:.1e} T={T:6.0f} N/m -> depth {d:6.2f} um, max slope {s:5.2f} mrad")
# tension needed for depth<=1um and slope<=0.5 mrad
def Tneed(A,fw,D):
    for T in np.logspace(0,6,400):
        d,s=report(A,fw,D,T)
        if d<=1 and s<=0.5: return T
for A,fw in [(20e-6,3e-3),(50e-6,3e-3),(50e-6,1e-3)]:
    for D in (layers["UTG 30um"],Dsum):
        print(f"Tneed A={A*1e6:.0f}um fwhm={fw*1e3}mm D={D:.1e}: {Tneed(A,fw,D):.0f} N/m")
# OCA shear lag to carry tension into UTG from layer below
G=9e4; h=25e-6; EtU=70e9*30e-6
for T in (600,3000):
    lamb=np.sqrt(EtU*h/G); tau=T/lamb; print(f"T={T}: shear lag {lamb*1e3:.1f} mm, tau {tau/1e3:.1f} kPa, gamma {tau/G:.2f}")
# edge grip if UTG clamped over 3 mm bond
for T in (600,3000): print(f"edge grip 3mm, T={T}: tau {T/3e-3/1e3:.0f} kPa")
print("UTG membrane stress at 600 N/m:", 600/30e-6/1e6, "MPa")
# Idea 3: slip between UTG and OLED midplanes across 180deg fold
for d in (100e-6,150e-6,200e-6):
    slip=np.pi*d; print(f"midplane sep {d*1e6:.0f}um -> slip {slip*1e6:.0f} um; seal/OCA 25um shear strain {slip/25e-6:.1f}; 50um {slip/50e-6:.1f}")
print("--- OCA-limited tension: tau 10.5 kPa (patent test stress) x shear lag")
Tmax=10.5e3*np.sqrt(EtU*h/G); print("Tmax", Tmax)
for A in (20e-6,50e-6):
    for D in (layers["UTG 30um"],Dsum):
        d,s=report(A,3e-3,D,Tmax); print(f"A={A*1e6:.0f} D={D:.1e}: depth {d:.1f} um slope {s:.1f} mrad ratio {A*1e6/d:.2f}")
for D in (layers["UTG 30um"],Dsum):
    d,s=report(50e-6,3e-3,D,600); print(f"idea4 T=600 on 50um: depth {d:.1f} ratio {50/d:.2f}")
