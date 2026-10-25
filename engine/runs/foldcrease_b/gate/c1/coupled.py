# fully bonded composite D (OCA 25um x3 assumed rigid shear, E~0) vs decoupled; worst-case cold state
layers=[(30e-6,70e9),(25e-6,0),(50e-6,4e9),(25e-6,0),(30e-6,8e9),(25e-6,0),(50e-6,4e9)]
z=0;zs=[]
for t,E in layers: zs.append((z,z+t,E)); z+=t
zn=sum(E*(b*b-a*a)/2 for a,b,E in zs)/sum(E*(b-a) for a,b,E in zs)
Dc=sum(E*((b-zn)**3-(a-zn)**3)/3 for a,b,E in zs)/(1-0.25**2)
print(f"coupled D={Dc:.3e}  ratio to decoupled 2.761e-4: {Dc/2.761e-4:.1f}x")
lam60=48e-3
for name,D in [('decoupled 60C',2.761e-4),('coupled -20C',Dc)]:
    T20=118*D/2.761e-4; T1=3003*D/2.761e-4
    print(name, f"T20={T20:.0f} N/m peak shear {T20/lam60/1e3:.1f} kPa; T1={T1:.0f} peak {T1/lam60/1e3:.0f} kPa")
