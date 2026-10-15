# Estimate hours per winter below thresholds from monthly means, assuming hourly T ~ Normal(monthly mean, sd)
import math
def Phi(z): return 0.5*(1+math.erf(z/math.sqrt(2)))
hours={'Oct':744,'Nov':720,'Dec':744,'Jan':744,'Feb':672,'Mar':744,'Apr':720}
sites={
 # Udachny monthly daily means (Wikipedia/climate-data.org via search): Nov -29.8 Dec -36.0 Jan -39.4 Feb -35.2 Mar -24.3; Oct, Apr assumed
 'Udachny':{'Oct':-12,'Nov':-29.8,'Dec':-36.0,'Jan':-39.4,'Feb':-35.2,'Mar':-24.3,'Apr':-11},
 # Chara (Udokan) Jan -31.8 (Wikipedia via search); other months assumed from Kupi (~-28 Dec) and continental profile
 'Chara':{'Oct':-6,'Nov':-19,'Dec':-28,'Jan':-31.8,'Feb':-27,'Mar':-16,'Apr':-4},
}
for site,mm in sites.items():
    for sd in (5,6.5,8):
        out=[]
        for thr in (-35,-40,-45):
            h=sum(hours[m]*Phi((thr-mm[m])/sd) for m in mm)
            out.append("<=%d C: %4.0f h"%(thr,h))
        print(site,"sd=%.1f"%sd," | ".join(out))
# Idea 2 requirement
ice=494*10e6  # kg/yr for 10 kt Cu
Q=127e6
t=ice*334e3/Q
print("Idea2: 127 MW freezes %.2f Mt ice in %.0f h (%.0f days) of continuous operation"%(ice/1e9,t/3600,t/86400))
# Season-average engine output using the idea's own curve: 12,15,19 kJ/kg at -35,-40,-45 C -> linear fit
import statistics
xs=[-35,-40,-45]; ys=[12,15,19]
mx=sum(xs)/3; my=sum(ys)/3
b=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs); a=my-b*mx
T0=-a/b
print("fit E = %.2f + %.3f*T kJ/kg ; zero output at %.1f C"%(a,b,T0))
def E(T): return max(0.0,a+b*T)
months5=['Nov','Dec','Jan','Feb','Mar']
for site,mm in sites.items():
    for sd in (6.5,):
        # expected E over the 151-day Nov-Mar season (numerical integration over normal)
        tot=0; hrs=0
        for m in months5:
            mu=mm[m]; n=2000
            acc=0
            for i in range(n):
                z=-5+10*(i+0.5)/n
                w=math.exp(-z*z/2)/math.sqrt(2*math.pi)*10/n
                acc+=w*E(mu+sd*z)
            tot+=acc*hours[m]; hrs+=hours[m]
        Eav=tot/hrs
        print("%s: Nov-Mar mean output %.1f kJ/kg ice -> %.2f kWh/kg Cu = %.0f%% of 2.0 kWh/kg EW"%(site,Eav,Eav*494/3600,100*Eav*494/3600/2.0))
