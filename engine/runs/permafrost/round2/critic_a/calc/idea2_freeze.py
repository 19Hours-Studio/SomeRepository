import math
# --- ice per kg Cu (CuSO4 solubility 14.3 g/100 g H2O at 0 C)
cu_sat=14.3*63.546/159.61*10  # g Cu per kg water
W0=1000.0; cu0=2.5; rec=0.80
cu_left=cu0*(1-rec); w_left=cu_left/cu_sat*1000
w_hyd=cu0*rec/63.546*5*18.015
ice=W0-w_left-w_hyd
print("Cu at saturation %.1f g/kg; water left %.1f g; hydrate water %.2f g; ice %.1f g -> %.0f kg ice/kg Cu; concentration factor %.0fx"%(cu_sat,w_left,w_hyd,ice,ice/(cu0*rec),W0/w_left))
for r in (0.8,0.9):
    cl=cu0*(1-r); wl=cl/cu_sat*1000
    print(" rec %.0f%%: concentration factor %.0fx -> acid 2-3 g/L becomes %.0f-%.0f g/kg; Fe 0.5-1 g/L -> %.0f-%.0f g/kg; Mg 1 g/L -> %.0f g/kg (MgSO4 sat ~40 g Mg/kg at 0C)"%(r*100,W0/wl,2*W0/wl,3*W0/wl,0.5*W0/wl,W0/wl,W0/wl))
print(" max Mg in feed before epsomite saturates at 80%% rec: %.2f g/L"%(40/(W0/w_left)))
# --- EW coverage
for kj in (12,15,19):
    e=ice/(cu0*rec)*kj/1000  # MJ per kg Cu
    print("engine %d kJ/kg ice -> %.2f MJ/kg Cu = %.2f kWh/kg Cu (EW needs ~2.0)"%(kj,e,e/3.6))
# --- Carnot check
for Tair in (-35,-40,-45):
    Th=273.15-1.0; Tc=273.15+Tair
    eta=1-Tc/Th
    print("Tair %d: Carnot (liquor -1C to air) %.3f -> %.1f kJ/kg ice; claimed/Carnot=%.2f"%(Tair,eta,eta*334,{-35:12,-40:15,-45:19}[Tair]/(eta*334)))
# --- condenser fan power
Q=127e6; W=4.5e6; Qc=Q-W
for Tair in (-35,-40):
    rho=101325/(287*(273.15+Tair))
    for dTa in (5,8,12):
        m=Qc/(1005*dTa); V=m/rho
        for dp in (100,150):
            P=V*dp/0.65
            print("Tair %d air rise %2d K: air %.0f m3/s, dp %d Pa -> fan %.2f MW (%.0f%% of 4.5 MW gross)"%(Tair,dTa,V,dp,P/1e6,100*P/W))
# --- propane vs propane-hydrate (I-H-V) equilibrium
def p_propane(T): return 10**(4.53678-1149.36/(T+24.906))  # bar, NIST Antoine 230-320K
def p_hyd(T):
    # ln P interpolation between (259.15 K, 1.0 bar) [3-phase at 0.1 MPa, -14 C] and Q1 (273.1 K, 1.72 bar)
    a=(math.log(1.72)-math.log(1.0))/(1/259.15-1/273.1)
    return math.exp(math.log(1.0)-a*(1/T-1/259.15))
for TC in (-2,-5,-8,-12):
    T=273.15+TC
    print("propane boiling at %d C: P=%.2f bar; propane hydrate stable above %.2f bar -> ratio %.1f"%(TC,p_propane(T),p_hyd(T),p_propane(T)/p_hyd(T)))
def p_nbutane(T): return 10**(3.85002-909.65/(T-36.146))
for TC in (-5,-28,-33):
    print("n-butane vapour pressure at %d C: %.2f bar"%(TC,p_nbutane(273.15+TC)))
# propane loss if a fraction of the 'ice' is propane hydrate (C3H8.17H2O)
for frac in (0.01,0.05):
    kgC3=494*frac*44.1/(17*18.015)
    print("if %.0f%% of crystallised water forms hydrate: %.2f kg propane locked per kg Cu = $%.0f/t Cu at $500/t propane"%(frac*100,kgC3,kgC3*500))
# --- baseline with grid power
for p in (0.05,0.07,0.30):
    print("EW power 2.0 kWh/kg at $%.2f/kWh = $%.0f/t Cu"%(p,2000*p))
