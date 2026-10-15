import math
h=6.626e-34; c=2.998e8; k=1.381e-23; s=5.670e-8
def band(T,l1,l2,n=20000):
    tot=0; dl=(l2-l1)/n
    for i in range(n):
        l=l1+(i+0.5)*dl
        tot+=2*math.pi*h*c**2/l**5/(math.exp(h*c/(l*k*T))-1)*dl
    return tot
for TC in (-40,-48,-50,-52):
    T=273.15+TC
    B=band(T,8e-6,13e-6); bb=s*T**4
    print("T=%d C: blackbody %.1f W/m2, 8-13um %.1f W/m2 (%.1f%%)"%(TC,bb,B,100*B/bb))
# implied Li grade of brine
area=11600; kg=55
Li_per_tLCE=1000*2*6.94/73.89
print("Li per t LCE %.1f kg; brine frozen %.0f t/yr -> implied Li %.0f mg/kg (100%% recovery)"%(Li_per_tLCE,area*kg/1000,Li_per_tLCE/(area*kg)*1e6))
print("cost $55,000/t LCE over 11,600 m2 -> $%.2f per m2 per year"%(55000/11600))
# niche: eluate freezing
for Li_g_L in (0.3,0.5,1.0):
    eluate=Li_per_tLCE/Li_g_L  # m3
    ice=eluate*(1-1/30)  # t
    per_m2=ice/100
    print("eluate %.1f g/L Li: %.0f m3/t LCE, ice %.0f t -> %.1f t ice per m2 per winter (100 m2/t LCE); heat %.2f GJ/m2"%(Li_g_L,eluate,ice,per_m2,per_m2*334e-3))
# Stefan limit for ice growth on a quiescent tray: thickness for given freezing degree-days
for FDD in (4000,6000):
    for a in (2.0,2.7):
        print("Stefan/empirical: FDD %d C-d, coeff %.1f -> %.2f m ice (%.1f t/m2)"%(FDD,a,a*math.sqrt(FDD)/100,a*math.sqrt(FDD)/100*0.917))
# heat flux needed
for per_m2 in (1.85,3.1,6.1):
    for days in (120,150):
        print(" %.1f t/m2 in %d days needs mean %.0f W/m2"%(per_m2,days,per_m2*1000*334e3/(days*86400)))
# Li lost in ice for progressive freezing (C_L/C0 = f^(K-1); fraction kept in liquid = f^K), f=1/30
f=1/30
for K in (0.02,0.05,0.1,0.2):
    print("K_eff=%.2f: concentration %.1fx, Li kept in liquor %.0f%% (lost to ice %.0f%%)"%(K,f**(K-1),100*f**K,100*(1-f**K)))
# RO competitor: osmotic pressure of LiCl solution (van't Hoff, phi~1)
for g_L in (2,5,10):
    M=g_L/6.94
    print("LiCl at %.0f g/L Li (%.2f M): osmotic ~%.0f bar"%(g_L,M,2*M*0.08314*293))
