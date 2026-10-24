import numpy as np
pi=np.pi
def Dpl(E,t,nu=0.22): return E*t**3/(12*(1-nu**2))
# ---------- IDEA 1 ----------
print("== IDEA1")
r=3.3/20; print("kill: T/D/k^2 at 600 =",1/r-1)
Dk2=600/(1/r-1); print("D*k^2 =",Dk2)
k_slope=2.3e-3/3.3e-6; print("slope/amp implied k =",k_slope,"1/m -> lambda",2*pi/k_slope*1e3,"mm")
D=Dk2/k_slope**2; print("implied D",D)
for wt,lab in [(1,'1um'),]:
    print("T to reach 1um:",Dk2*(20/1-1))
# set geometry: set curvature f/R over arc L=pi R; w0 = kappa L^2/8
def w0(f,R): return f*pi**2*R/8
for R in [1.5e-3,4.5e-3]:
  for f in [0.025,0.08]:
    k=pi/(pi*R)  # half-wave over arc length
    w=w0(f,R); 
    for T in [1000]:
      ratio=k**2/(k**2+T/D)
      print(f"R={R*1e3}mm f={f} w0={w*1e6:.0f}um  k={k:.0f} resid={w*ratio*1e6:.2f}um slope~{w*ratio*k*1e3:.2f}mrad")
# T needed at 1.5mm for 1um with f=8%
R=1.5e-3;k=1/R;print("T needed R1.5 f8%:",D*k**2*(w0(0.08,R)/1e-6-1)/1e3,"kN/m")
# glass strain
print("glass strain 30um UTG:",1000/30e-6/70e9*100,"%")
# adhesive margin
print("shear margin",10.5/9.4)
# thermal: Ti vs display mismatch
for name,a in [("Ti",8.6e-6),("Al",23e-6)]:
  for ad in [3.2e-6,8e-6]:
    d=(a-ad)*60*0.15; print(name,"disp mismatch over 60K, alpha_disp",ad, d*1e6,"um vs elastic elong",1000/30e-6/70e9*0.15*1e6,"um")
# ---------- IDEA 2 ----------
print("== IDEA2")
Dg=Dpl(70e9,30e-6); print("D glass30",Dg)
print("buckling L for 0.34 N/m:",np.sqrt(pi**2*Dg/0.34)*1e3,"mm")
print("slip pi*d for 149um -> d=",149/pi,"um")
print("gravity wedge 40um/150mm",40e-6/0.15*1e3,"mrad")
rho=1.1e3;g=9.81;h=20e-6
for mu in [0.05,0.1,0.5]:
  u=h**2*rho*g/(12*mu); print(f"mu={mu} drain vel {u*1e6:.2f} um/s  time 75mm {0.075/u/3600:.2f} h")
print("hydrostatic dp over 150mm",rho*g*0.15,"Pa; glass long-wave stiffness D k^4 (lam=300mm)",Dg*(2*pi/0.3)**4,"Pa/m")
print("short-wave 3mm bridging sag",rho*g*0.15/(Dg*(2*pi/3e-3)**4)*1e6,"um")
# levelling time vs wavelength
for mu in [0.05,0.1,0.4]:
  for lam in [3e-3,10e-3,20e-3]:
    k=2*pi/lam; rate=h**3*Dg*k**6/(12*mu); print(f"mu={mu} lam={lam*1e3}mm tau={1/rate:.3g}s")
# finger squeeze: disk a=5mm 1N, gap 20->10um
for mu in [0.05,0.1]:
  a=5e-3;F=1
  t=3*pi*mu*a**4/(4*F)*(1/(10e-6)**2-1/(20e-6)**2); print("finger 1N halving gap time",t,"s (rigid-disk bound)")
n1,n2=1.51,1.53; print("reflectance dn=0.02",((n1-n2)/(n1+n2))**2, "dn=0.04",((1.49-1.53)/(3.02))**2)
# panel set vs fluid gap: set at R=3mm
for f in [0.02,0.08]: print("panel set depth R=3mm f",f,w0(f,3e-3)*1e6,"um vs gap 20um")
print("thermal fluid expansion 60K, beta 9.5e-4:",20*9.5e-4*60,"um")
print("glass strain 30um R3",15e-6/3e-3*100,"%  stress MPa",70e3*15e-6/3e-3)
# ---------- IDEA 3 ----------
print("== IDEA3")
print("25um at R4.2:",25e-6/(2*4.2e-3)*100,"%")
for f in [0.3,0.5]:
  frac=0.024*f; print(f"poly share 2.4% x set {f}: stack set frac {frac:.4f} -> free depth {w0(frac,4.2e-3)*1e6:.1f} um")
print("hinge cost implied 7/0.08, 33/0.47:",7/0.08,33/0.47)
print("CPI 25um vs glass 30 share", (6*25**3)/(6*25**3+70*30**3))
# ---------- IDEA 4 ----------
print("== IDEA4")
print("sigma",2000/45e-6/1e6,"MPa strain",2000/45e-6/70e9*100,"% total",2000*0.15,"N")
Dimp=2000*(0.57e-3)**2; print("D implied by sqrt(D/T)=0.57mm:",Dimp," UTG45 D:",Dpl(70e9,45e-6))
R=3e-3; L=pi*R+4e-3; k=pi/L
for Dx in [Dimp,3*Dimp]:
  ratio=k**2/(k**2+2000/Dx); print(f"D={Dx:.2e} L={L*1e3:.1f}mm resid 180um -> {180*ratio:.2f} um, slope {180e-6*ratio*k*1e3:.2f} mrad")
# gel cavitation and confined modulus
G=2e3;E=3*G; print("gel cavitation ~5E/6 =",5*E/6,"Pa")
for hg in [25e-6,50e-6]:
  print("gel thickness",hg*1e6,"um must absorb 180um crease: thickness change ratio",180e-6/hg)
# glass CT with membrane tension
CS,DOL,t=700e6,5e-6,45e-6; CT=CS*DOL/(t-2*DOL); print("CT",CT/1e6,"MPa ; with tension",(CT+44e6)/1e6)
print("bending stress folded R3:",70e3*22.5e-6/3e-3,"MPa")
