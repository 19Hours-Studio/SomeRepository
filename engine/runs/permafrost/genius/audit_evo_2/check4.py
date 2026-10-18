import math
print("=== IDEA 4 ===")
Q=600 # m3/h
for ice_ratio in (0.17,):
    vi=Q*ice_ratio
    for rho,L in ((917,334e3),(910,300e3)):
        P=vi*rho*L/3600
        print("ice m3/h",vi,"melt power MW (rho,L)",rho,L/1e3,round(P/1e6,2))
print("4.3 MW corresponds to ground rate m3/h:",round(4.3e6*3600/(0.17*917*334e3)))
for hi in (1.0,1.5,2.0,2.2,2.5):
    for wd in (4,6,8):
        cut=17-wd
        print("ice",hi,"water depth",wd,"cut thickness",cut,"ice/ground",round(hi/cut,3),"under-ice water gap",round(wd-0.9*hi,2))
print("Dec-Jun days:",31+31+28+31+30+31+30)
print("winter effective days",214-58,"availability", round((214-58)/212,2))
# cost scaling
print("126/(214/58) =",round(126/(214/58),1))
print("126/37=",round(126/37,2)," 126/23=",round(126/23,2)," same-grade seasonal at 0.8:",round(126*0.5/0.8,1)," ratio:",round(126*0.5/0.8/23,2))
print("grade needed to hit 22k and 14k:",round(37*0.5/22,2),round(37*0.5/14,2))
# production
for d in (58,214):
    V=Q*24*d
    print("days",d,"m3/yr",V, "Sn t/yr at 0.5 kg/m3 rec 0.7:",round(V*0.5*0.7/1e3), "at 0.8:",round(V*0.8*0.7/1e3))
# bulking of tailings in under-ice gap
for wd,hi in ((4,2.2),(5,2.2),(6,2.0)):
    cut=17-wd
    for swell in (1.1,1.2,1.3):
        print("wd",wd,"ice",hi,"swell",swell,"excess height over seabed m",round(cut*(swell-1),2),"gap under ice",round(wd-0.9*hi,2))
