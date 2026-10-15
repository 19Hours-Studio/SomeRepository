"""Idea 1 repair: sun-wind freeze-drying (sublimation) + aeolian removal of fines.
Round 1 = original horizontal in-place field; Round 2 = autumn-built drained pay windrows, south faces.
All inputs labelled: [S]=sourced (see LOG/notes), [A]=assumption, [R]=reviewer number."""
import numpy as np
L_s=2.834e6; sig=5.67e-8; rho_a=1.35; cp=1005.
def qsat_ice(T):  # T in C, specific humidity over ice at 1013 hPa
    e=611.15*np.exp(22.452*T/(272.55+T)); return 0.622*e/101300
# --- Site: Tiksi / Kular (70.6N) climate [S: Tiksi climate normals (Wikipedia/pogoda.ru): Mar -27, Apr -19.5, May -7.6 C mean;
#  mean daily max Apr ~ -11 (R)], wind 10 m mean 5-6 m/s winter-spring [A from Tiksi normals ~5.5 m/s]
lat=np.radians(70.6)
months={'Mar(15-31)':(75,-26.0,9.0),'Apr(1-20)':(100,-19.0,9.0),'Apr(21-30)/May':(118,-13.0,9.0),'May(1-10)':(126,-9.0,8.0)}
def sun(doy,h):
    d=np.radians(23.44)*np.sin(2*np.pi*(284+doy)/365)
    H=np.radians(15*(h-12)); el=np.arcsin(np.sin(lat)*np.sin(d)+np.cos(lat)*np.cos(d)*np.cos(H))
    az=np.arctan2(np.sin(H),np.cos(H)*np.sin(lat)-np.tan(d)*np.cos(lat))  # 0=south
    return el,az
def face_flux(doy,Tmean,dTdiurnal,slope_deg,U10,Ch,albedo,cloud,RHi=0.85,rdry=0.0):
    """hourly energy balance, returns daily sublimation kg/m2, max Ts, hours Ts>-2C"""
    s=np.radians(slope_deg); E=0; Tmax=-99; warmh=0
    for h in np.arange(0,24,0.5):
        el,az=sun(doy,h); Ta=Tmean+dTdiurnal/2*np.cos(2*np.pi*(h-14)/24)
        if el>0:
            tau=0.75*(1-0.65*cloud); Sb=1361*tau**(1/max(np.sin(el),0.05))
            cosi=np.cos(s)*np.sin(el)+np.sin(s)*np.cos(el)*np.cos(az)
            SW=Sb*max(cosi,0)+0.12*1361*np.sin(el)*(0.3+cloud)*(1+np.cos(s))/2
        else: SW=0
        LWin=(0.70+0.25*cloud)*sig*(Ta+273.15)**4*(1+np.cos(s))/2+sig*(Ta+273.15)**4*(1-np.cos(s))/2
        qa=RHi*qsat_ice(Ta); ra=1/(Ch*U10)  # aerodynamic resistance s/m
        lo,hi=-60.,10.
        for _ in range(60):
            Ts=(lo+hi)/2
            LE=L_s*rho_a*max(qsat_ice(min(Ts,0))-qa,0)/(ra+rdry)
            H=rho_a*cp*(Ts-Ta)/ra; G=8.0  # conduction into cold pile [A]
            res=(1-albedo)*SW+LWin-0.95*sig*(Ts+273.15)**4-H-LE-G
            if res>0: lo=Ts
            else: hi=Ts
        E+=LE/L_s*1800; Tmax=max(Tmax,Ts); warmh+=0.5*(Ts>-2)
    return E,Tmax,warmh
print("=== Round 1: original horizontal harrowed field (slope 0) vs Round 2: 37 deg south face (windrow) ===")
for name,(doy,Tm,dT) in months.items():
    for slope in (0,37):
        for cloud in (0.3,0.6):
            E,Tx,wh=face_flux(doy,Tm,dT,slope,6.0,2.0e-3,0.12,cloud)
            print(f"{name:16s} slope{slope:3d} cloud{cloud}: E={E:5.2f} kg/m2/d  noon Ts max={Tx:6.1f}C  hours>-2C={wh:4.1f}")
# dry-skin resistance (reviewer defect 4)
D=2.0e-5; phi=0.35; tau_=1.5; Deff=D*phi/tau_
print("\nDry-layer resistance r=L/Deff (s/m):",{L:round(L/Deff) for L in (1e-3,3e-3,10e-3)}, " aero ra=1/(Ch*U)=",round(1/(2e-3*6)))
E_r,_,_=face_flux(100,-19,9,37,6.0,2.0e-3,0.12,0.45,rdry=0.5e-3/Deff)
E_0,_,_=face_flux(100,-19,9,37,6.0,2.0e-3,0.12,0.45,rdry=0)
E_3,_,_=face_flux(100,-19,9,37,6.0,2.0e-3,0.12,0.45,rdry=3e-3/Deff)
print(f"Apr face E: bare {E_0:.2f}, 0.5 mm skin {E_r:.2f}, 3 mm lag {E_3:.2f} kg/m2/d")
# --- Round 2 production: face self-clears (37 deg = repose; freed grains roll to toe) => skin <= ~1 grain (0.5 mm) [A]
# ice content of autumn-drained windrow: field capacity of sandy gravel 0.06-0.12 vol water [S: typical FC of sand/gravel 0.05-0.12]
season=[(75,-26,9,17),(100,-19,9,20)]  # (doy,Tmean,dT,days) Mar15-Apr20 only (liquid-water cut-off)
for cloud in (0.45,):
    Etot=sum(face_flux(d,T,dT,37,6.0,2e-3,0.12,cloud,rdry=0.5e-3/Deff)[0]*n for d,T,dT,n in season)
snow_loss=0.15  # ~6 snow days Mar15-Apr20 (Tiksi ~4/month) each costing ~1 day of sublimating fresh snow [A from R: 4 snow days in Apr]
Etot*=1-snow_loss
print(f"\nSeason Mar15-Apr20 (37 days) face sublimation = {Etot:.1f} kg/m2 (after {snow_loss:.0%} snow-day loss)")
for ice in (0.06,0.10,0.15,0.30):
    retreat=Etot/(ice*917)
    # windrow: 3 m high, 37deg faces; south face 5.0 m2 per m; volume 3*(3/tan37)=11.9 m3/m
    face_per_m=3/np.sin(np.radians(37)); vol_per_m=3*3/np.tan(np.radians(37))
    released=min(retreat*face_per_m,vol_per_m)
    km=100000/released/1000
    spacing=3/np.tan(np.radians(12))+8  # no-shading spacing at 12 deg sun (mid-March noon at 70.6N ~ 16 deg)
    print(f"pore ice {ice:.2f}: retreat {retreat:5.2f} m/season; released {released:5.2f} m3 per m ridge; ridge for 100,000 m3 = {km:6.1f} km; footprint {km*1000*spacing/1e6:5.2f} km2")
# --- Aeolian sorting (defect 2): Shao & Lu (2000) threshold + suspension criterion; design keeps saltation fraction on site
AN=0.0123
def ustar_t(rho_p,d,g=1.65e-4): return np.sqrt(AN*(rho_p/1.23*9.81*d+g/(1.23*d)))
def ws(rho_p,d):  # Stokes+Oseen-ish settling in air
    mu=1.6e-5; w=rho_p*9.81*d**2/(18*mu)
    for _ in range(30):
        Re=1.23*w*d/mu; w=rho_p*9.81*d**2/(18*mu*(1+0.15*Re**0.687))
    return w
print("\nThresholds u*t (m/s), gamma 1.65e-4..5e-4:")
for d in (25e-6,40e-6,70e-6,100e-6,200e-6,500e-6,1e-3):
    print(f" d={d*1e6:5.0f}um quartz {ustar_t(2650,d):.2f}-{ustar_t(2650,d,5e-4):.2f}  gold {ustar_t(17500,d):.2f}-{ustar_t(17500,d,5e-4):.2f}  ws quartz {ws(2650,d):.2f} gold {ws(17500,d):.2f}")
for us in (0.3,0.45,0.6):
    # largest gold that can be suspended (ws<u*) => leaves site; quartz suspended
    ds=np.logspace(-6,-3,400)
    g_s=max(d for d in ds if ws(17500,d)<us); q_s=max(d for d in ds if ws(2650,d)<us)
    g_m=max([d for d in ds if ustar_t(17500,d)<us] or [0])
    print(f" u*={us}: suspended (leaves site) quartz<{q_s*1e6:.0f}um, gold<{g_s*1e6:.0f}um; gold mobile(saltation/creep, stays in trough) up to {g_m*1e6:.0f}um")
# gold loss accounting (assumptions flagged): fraction of gold mass <30um in primary (virgin) placer [A]=0.5-2%;
# baseline sluice recovers <30um gold at ~0-20% [S: fine-gold losses 40-50% in sluices, Langeri/Sakhalin, Obogashchenie Rud 2019]
for f in (0.005,0.02):
    for rec in (0.0,0.2):
        print(f" net gold loss vs sluice if f(<30um)={f:.1%}, sluice recovery of it {rec:.0%}: {f*(1-0)-f*(1-rec) if False else f*rec:.2%} of gold")
