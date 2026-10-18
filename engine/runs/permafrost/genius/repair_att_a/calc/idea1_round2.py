# Round 2/3: submerged concentration (lift only concentrate), lower power, year-round use of one crawler;
# compare with summer-only suction dredge on the same lake and drain-lake dozer-sluice.
grade, pay_frac, Q = 0.5, 2/7, 150.0      # g/m3 sands, pay share of dig, m3/h bank [E]
avail, diesel, crew_pp = 0.75, 90, 2.2e6
def run(days, rec, capex, P_kW, crew_n, mob, crf=0.20, label=""):
    hours = 20*days*avail
    V = Q*hours; Au = V*pay_frac*grade*rec/1000
    annual = capex*crf + 0.26*P_kW*hours*diesel + crew_n*crew_pp*(days/365*1.3) + 0.10*capex + mob
    print(f"{label:48s} days {days:3d} dig {V/1e3:6.0f}k m3 Au {Au:5.1f} kg -> {annual/(Au*1e3):6,.0f} rub/g")
    return annual/(Au*1e3)
cap_crawler = 60e6+30e6+30e6     # crawler, surface power/hut (small: only concentrate lifted), submerged jig module [E]
w  = run(170, 0.75, cap_crawler, 330, 12, 15e6, label="R2 winter-only under-ice crawler, submerged jig")
yr = run(270, 0.77, cap_crawler, 330, 12, 15e6, label="R3 same crawler year-round (winter+summer)")
sd = run(100, 0.85, 50e6+30e6, 330, 10, 15e6, label="baseline: summer-only suction dredge+sluice")
drain = 1932  # from round 1 bottom-up (drainable lake, thawed talik, dozer+sluice)
print(f"ratios: year-round/summer-dredge {yr/sd:.2f}; year-round/drain-lake {yr/drain:.2f}; winter-only/summer-dredge {w/sd:.2f}")
# lake size consistency: year-round dig volume vs lake area at 7 m dig depth
V_yr = Q*20*270*avail; print(f"year-round dig {V_yr/1e3:.0f}k m3 needs {V_yr/7/1e4:.1f} ha lake floor per year")
# silt-curtain cell under ice: closed water volume vs fines released
lake_area, water_depth = 8e4, 2.0   # 8 ha, 2 m of liquid water under 2 m ice in March [E]
fines = Q*20*avail*0.15*1.6e3       # kg/day of <0.075 mm fines (15% of bank, 1.6 t/m3) [E]
print(f"fines released {fines/1e3:.0f} t/day into {lake_area*water_depth/1e3:.0f}k m3 water -> {fines*1e3/(lake_area*water_depth):.0f} mg/L per day if fully mixed")
