# Repair of K1: sunk low-RTE converters (EREV fleet) take only the TOP SLICE of the deficit duration curve,
# efficient H2 turbines take the base. Germany daily system OVER=1.3.
import importlib.util, io, contextlib
spec=importlib.util.spec_from_file_location("s02","s02_deficit_shape.py")
with contextlib.redirect_stdout(io.StringIO()):
    s02=importlib.util.module_from_spec(spec); spec.loader.exec_module(s02)
R=s02.run(1.3,quiet=True); ny=len(R)/365.25
P=[max(0,-x)/24 for x in R]  # GW daily-mean deficit
Pmax=max(P)
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
turb_ann=900*(crf(.07,30)+.025)*1e6     # $/GW-yr
erev_ann=73*(crf(.07,12))*1e6 + 0      # charger premium per GW-yr
# marginal cost of energy delivered: surplus electricity value ~0.01 $/kWh at margin + fuel-chain extra
def energy_cost(rte, extra_fuel, eta_conv): return (0.01/rte + extra_fuel/eta_conv)  # $/kWh_e
cA=energy_cost(0.26,0.0,0.40); cB=energy_cost(0.18,0.035,0.36)+0.017  # + engine wear
print(f"marginal energy cost: H2-turbine {cA:.3f} $/kWh, EREV {cB:.3f} $/kWh")
best=None
for f in [i/20 for i in range(0,21)]:
    cap=f*Pmax
    Ebase=sum(min(p,cap) for p in P)*24/ny*1e6   # kWh/yr
    Etop=sum(max(0,p-cap) for p in P)*24/ny*1e6
    hrs_top=sum(1 for p in P if p>cap)*24/ny
    cost=cap*turb_ann + (Pmax-cap)*erev_ann + Ebase*cA + Etop*cB
    print(f"turbines {f:.2f} of peak: base {Ebase/1e9:5.1f} TWh, top slice {Etop/1e9:5.2f} TWh over {hrs_top:5.0f} h/yr, cost {cost/1e9:5.2f} B$/yr")
    if best is None or cost<best[1]: best=(f,cost)
print("best split", best, "vs all-turbine", Pmax*turb_ann/1e9 + sum(P)*24/ny*1e6*cA/1e9)
