# R3: winter-idle fleet barge (survey/maintenance paid by fleet anyway); natural backwater; bank boiler within 150 m
Q=2500; hulls=2
for label, site_capex, maint in (("natural backwater, bank boiler", 4e6+10e6, 0.3e6), ("dredged basin, bank boiler", 12e6+10e6+10e6, 0.3e6)):
    opp = hulls*25e6*0.15*0.15         # 15% of the year (spring/autumn weeks) lost from summer service
    moat_fuel = 82*240*24/1e3*0.0      # moat+hold heat from flue-gas waste heat: ~0 fuel
    ann = opp + hulls*maint + site_capex*0.12
    print(f"R3 {label:32s}: {ann/Q:,.0f} rub/t vs avoided 1,105-3,440 rub/t -> ratio {1105/(ann/Q):.1f}-{3440/(ann/Q):.1f}x")
# summer gap: central Yakutia heating season ~240 d; Arctic coast ~300-365 d -> need small bin or relay
for heat_days in (240, 330):
    gap = 365-heat_days; print(f"heating {heat_days} d: summer gap {gap} d; hull out ~ice-out (early Jun) to last voyage (late Aug) = ~80 d -> {'OK' if gap>=80 else 'needs relay hull or day-bin'}")
