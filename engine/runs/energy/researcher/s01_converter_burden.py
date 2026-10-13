# Baseline: cost per delivered kWh contributed by the discharge converter vs full-load hours/yr,
# and by round-trip loss (cost of charging energy / RTE).
def crf(r, n): return r*(1+r)**n/((1+r)**n-1)
r=0.07
cases = {  # name: ($/kW installed, life yrs, fixed O&M frac/yr)
 "OCGT/H2 turbine": (900, 30, 0.025),
 "PEM fuel cell stationary": (1500, 15, 0.03),
 "rSOC stack+BOP": (2000, 10, 0.03),
 "auto engine genset": (120, 15, 0.04),
 "existing (sunk) converter": (0, 20, 0.02),
}
print("converter $/kWh_e delivered at full-load hours H")
for name,(c,n,om) in cases.items():
    ann = c*(crf(r,n)+om)
    row=[f"{name:28s}"]+[f"H={H}: {ann/H:7.3f}" for H in (200,500,1000,2000)]
    print("  ".join(row))
print("\ncharging-energy cost per delivered kWh = p_charge/RTE")
for p in (0.0,0.01,0.02,0.04):
    print(f"p={p:.2f} $/kWh:", "  ".join(f"RTE {e:.2f}: {p/e:.3f}" for e in (0.25,0.4,0.6,0.8)))
