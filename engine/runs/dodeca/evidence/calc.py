import math
# regular dodecahedron geometry
phi=(1+5**.5)/2
def edge_from_height(h):  # h = face-to-face distance = 2*inradius
    ri=h/2
    return ri/(math.sqrt(250+110*5**.5)/20)
def area(a): return 3*math.sqrt(25+10*5**.5)*a*a
for name,h_mm,m_g,dens in [("Newhall",59,81,8.8),("NortonDisney",80,245,8.8),("NortonDisney_Pb18",80,245,9.0)]:
    a=edge_from_height(h_mm)/10  # cm
    A=area(a)
    V=m_g/dens
    print(name,"edge cm %.2f area cm2 %.0f shell-equivalent thickness mm %.2f"%(a,A,V/A*10))
# size/weight range implied thickness bounds
for h,m in [(40,35),(100,580)]:
    a=edge_from_height(h)/10;A=area(a);print("h",h,"m",m,"thk mm %.2f"%(m/8.8/A*10))
# shares
print("Britain 33/134 = %.1f%%, 33/129 = %.1f%%, 33/130=%.1f%%"%(33/134*100,33/129*100,33/130*100))
print("20%% of 130 = %.0f ; 70%% of 130 = %.0f"%(.2*130,.7*130))
print("8.5%% of 130 = %.1f"%(.085*130))
# hole ratios
print("max possible small/large hole ratio within object: %.1f ; Newhall circles ratio %.2f"%(40/6,22/10.5))
print("height range ratio %.1f ; weight ratio %.1f ; weight 35-580 ; volume ratio of heights %.1f"%(100/40,580/35,(100/40)**3))
# timespan
print("span years 2nd-4th c ~ up to 300 yrs; per-year find rate: %.2f per decade since 1739 -> %.1f finds/decade over %d yrs (116 by ~2013)"%(0,116/((2013-1739)/10),2013-1739))
# Norton Disney NDHAG: 33 British / ~275 yrs
print("British finds per decade since 1739 to 2023: %.2f"%(33/((2023-1739)/10)))
