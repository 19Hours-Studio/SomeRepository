# extra numbers for final notes
# Idea 4: 1.2 m tall pod, 5.0x1.2 frontal, Cd 1.1 (box) -> CdA 6.6
for U in (0.2,0.3):
    D=0.5*1000*6.6*U**2; Bmax=D/0.15/9.81
    for dT,bl in ((0.03,11.0),(0.05,18.4)):
        T=0.9*Bmax/bl; print(f"I4 low pod U={U}: drag {D:.0f} N Bmax {Bmax:.0f} kg; +{dT}K -> {T:.0f} d, {T*86400*U/1000:.0f} km")
# early-winter window: ice 0.6-1.0 m -> draft 0.55-0.92 -> depth needed 1.75-2.1 m
print("I4 early-winter depth need:",round(1.2+0.917*0.6,2),"-",round(1.2+0.917*1.0,2),"m")
# Idea 1 cost per gram (grade 0.7 g/m3, rec 0.85) for repaired flat/ridge regime vs baseline
grade,rec=0.7,0.85
area=100000/0.11/1e6  # km2 at 0.11 m/season (6% ice, lag cleared daily)
harrow=(0.85*area/0.48, 3.0*area/0.48)   # scale reviewer's $0.85-3.0/m3 at 0.48 km2
print(f"I1 area {area:.2f} km2; harrow ${harrow[0]:.1f}-{harrow[1]:.1f}/m3")
idea=(harrow[0]+0.27+0.75*1.4+0.5+1.0, harrow[1]+0.66+2.1*1.4+0.8+2.0)  # +lag loading, residue wash (70-90% residue), pre-drain/thaw, windrow/stage
base=(1.7,6.0)
print(f"I1 processing $/m3 idea {idea[0]:.1f}-{idea[1]:.1f} vs baseline wash {base}; per g idea {idea[0]/(grade*rec):.1f}-{idea[1]/(grade*rec):.1f} vs {base[0]/(grade*rec):.1f}-{base[1]/(grade*rec):.1f} $/g")
# dust: suspended fraction (<70-100 um quartz) 10-30% of 100,000 m3 at 1.6 t/m3
print("I1 dust leaving site t/season:",[round(100000*f*1.6) for f in (0.1,0.3)])
