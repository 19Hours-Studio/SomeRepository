# Repair of K1 (EREV fleet): use sunk, low-RTE converters only for the inter-annual TAIL.
# Per heating-year (Jul-Jun) deficit & storage need in the German daily system (OVER=1.3, wind 0.65).
import importlib.util, io, contextlib
spec=importlib.util.spec_from_file_location("s02","s02_deficit_shape.py")
with contextlib.redirect_stdout(io.StringIO()):
    s02=importlib.util.module_from_spec(spec); spec.loader.exec_module(s02)
R=s02.run(1.3,quiet=True); D=s02.D
years={}
for d,x in zip(D,R):
    y=int(d[:4]); m=int(d[5:7]); hy=y if m>=7 else y-1
    years.setdefault(hy,[]).append(x)
print("heating-year  deficit_TWh  maxRunDeficit_TWh(storage need, RTE=1 within-year surplus netted)")
needs=[]
for hy,xs in sorted(years.items()):
    if len(xs)<360: continue
    # storage need with perfect efficiency: max drawdown of cumulative residual
    c=0; peak=0; dd=0
    for x in xs:
        c+=x; peak=max(peak,c); dd=max(dd,peak-c)
    dfc=sum(max(0,-x) for x in xs)
    needs.append(dd); print(f"  {hy}/{hy+1}   {dfc/1000:6.1f}       {dd/1000:6.1f}")
mean=sum(needs)/len(needs); mx=max(needs)
print(f"storage need mean {mean/1000:.1f} TWh, worst {mx/1000:.1f} TWh (ratio {mx/mean:.2f}) -- 6 yrs only")
# Cost of covering the tail energy (worst-mean) once per ~6 years
tail=(mx-mean)*1e6   # GWh -> kWh_e
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
# Option H2: extra cavern + electrolyser-hours exist; extra fuel bought at RTE .26 from surplus; converters already sized
# The point: tail ENERGY costs storage capacity that sits full for years.
h2_store=tail/0.40*0.5*(crf(0.07,40)+0.01)        # $/yr cavern capacity
meoh_store=tail/0.36*0.02*(crf(0.07,40)+0.01)       # tank farm capacity (or sunk SPR-type)
meoh_carry=tail/0.36*0.10*0.07                    # inventory carrying cost of e-methanol at 0.10 $/kWh fuel
h2_carry=tail/0.40*0.06*0.07                     # inventory carrying cost of H2 at 0.06 $/kWh
print(f"tail {tail/1e9:.1f} TWh_e: H2 cavern {h2_store/1e9:.2f}+carry {h2_carry/1e9:.2f} B$/yr; "
      f"e-MeOH tanks {meoh_store/1e9:.2f}+carry {meoh_carry/1e9:.2f} B$/yr")
