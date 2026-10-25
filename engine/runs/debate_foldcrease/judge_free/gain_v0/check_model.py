"""Audit of the baseline crease_model.py (same formulas, varied assumptions)."""
import math
GPa=1e9
def D(E,t): return E*t**3/12
def depth(R,layers,Lfac=1.5):
    L=math.pi*R*Lfac; Dt=sum(D(E,t) for E,t,_ in layers)
    k=sum(D(E,t)*p for E,t,p in layers)/R/Dt; return k*L**2/8*1e6, 4*k*L**2/8/L*1e3
cur=lambda phi:[(4*GPa,60e-6,phi),(72*GPa,45e-6,0),(6*GPa,30e-6,phi/2),(4*GPa,50e-6,phi),(4*GPa,100e-6,0)]
new=lambda phi,pg=0,pm=0:[(72*GPa,70e-6,pg),(6*GPa,25e-6,phi/2),(100*GPa,40e-6,pm)]
print("1) Radius dependence at phi=0.05 (model says depth ~ R):")
for R in (1.5e-3,2e-3,3e-3,4e-3,5.5e-3):
    print(f"   R={R*1e3:.1f}mm current-like {depth(R,cur(.05))[0]:6.1f} um | proposed {depth(R,new(.05))[0]:5.2f} um")
print("2) What phi does the current-like stack need to match HTX iPhone Duo?")
for target in (48,167):
    phi=target/depth(2e-3,cur(1.0))[0]; print(f"   {target} um -> phi={phi:.2f}")
print("3) Proposed stack if panel polymer set reaches the HTX-implied level (phi from 2):")
for phi in (0.07,0.25,0.5,1.0):
    print(f"   phi={phi}: {depth(4e-3,new(phi))[0]:.2f} um, slope {depth(4e-3,new(phi))[1]:.2f} mrad")
print("4) Sensitivity to small set in 'non-creeping' layers (glass relaxation / Ti microplasticity):")
for pg,pm in ((0.001,0),(0,0.005),(0,0.02),(0.001,0.01)):
    d,s=depth(4e-3,new(0.05,pg,pm)); print(f"   glass {pg*100:.1f}%, Ti {pm*100:.1f}% set: {d:.1f} um, {s:.2f} mrad")
print("5) Missing layers: add a 25um OCA (G~1e5 Pa -> E~3e5) and a 2nd OCA panel/Ti; also a top")
print("   hard-coat 5um acrylic (E 4GPa) -- bending-stiffness share only (decoupled):")
extra=new(0.05)+[(3e5,25e-6,0.10),(3e5,25e-6,0.10),(4*GPa,5e-6,0.05)]
print(f"   depth {depth(4e-3,extra)[0]:.2f} um  (OCA bending share negligible; its shear set is NOT in the model)")
print("6) Coupled (bonded) limit: panel set as a membrane strain offset at its distance from neutral axis")
# fully bonded composite: neutral axis z0, residual moment from set strain phi*eps_i in each polymer layer
lay=[("UTG",72*GPa,70e-6,0),("OCA",3e5,25e-6,0),("panel",6*GPa,25e-6,0.05),("OCA2",3e5,25e-6,0),("Ti",100*GPa,40e-6,0)]
z=0;geo=[]
for n,E,t,p in lay: geo.append((n,E,t,p,z+t/2)); z+=t
z0=sum(E*t*zc for _,E,t,_,zc in geo)/sum(E*t for _,E,t,_,_ in geo)
Dc=sum(E*(t**3/12+t*(zc-z0)**2) for _,E,t,_,zc in geo); R=4e-3
M=sum(E*t*p*abs(zc-z0)/R*(zc-z0) for _,E,t,p,zc in geo)
k=abs(M)/Dc; L=1.5*math.pi*R
print(f"   NA at {z0*1e6:.0f}um, panel {abs(geo[2][4]-z0)*1e6:.0f}um from NA, strain {abs(geo[2][4]-z0)/R*100:.2f}%  depth {k*L**2/8*1e6:.2f} um")
print("7) Is 0.4 mrad / ~100 mD invisible on bare glossy glass?")
for s in (0.4e-3,):
    for dist in (0.5,2.0):
        print(f"   slope {s*1e3} mrad, reflected object at {dist} m: image shift {2*s*dist*1e3:.1f} mm")
print("   HTX new Duo slope <0.1 deg =",round(math.radians(0.1)*1e3,2),"mrad; after 3000 folds 1.24 deg =",round(math.radians(1.24)*1e3,1),"mrad")
print("8) UTG stress incl. plate factor 1/(1-nu^2), nu=0.22, R=4mm, t=70um:",
      round(72e9*70e-6/(2*4e-3)/(1-0.22**2)/1e6),"MPa; at 10um depth (DOL, CS~0):",
      round(72e9*(35e-6-10e-6)/4e-3/(1-0.22**2)/1e6),"MPa net tension below the CS layer")
