# Idea 1: Ni(CO)4 carried in a trunk gas line (Power of Siberia, 9.8 MPa, 38 bcm/yr) -> Amur GPP
import math
R=8.314
# Vapour pressure of Ni(CO)4 (NIST/Cheméo fit): ln P[kPa] = 14.5275 - 2837.86/(T-28.762), 228-337 K
def psat(T): return math.exp(14.5275-2837.86/(T-28.762))
print("check bp: P(316K)=%.1f kPa (should be ~101)"%psat(316.0))
P=9.8e3 # kPa
for y in [0.0004,0.0002,0.0001,0.001]:
    pp=y*P
    # dew point
    lo,hi=200,330
    for _ in range(60):
        m=(lo+hi)/2
        if psat(m)>pp: hi=m
        else: lo=m
    print(f"y={y*100:.3f}% pp={pp:.2f} kPa dewpoint {lo-273.15:.1f} C ; sat. ratio at -20C {pp/psat(253.15):.2f}, at -10C {pp/psat(263.15):.2f}")
# Thermo Ni(s)+4CO(g)=Ni(CO)4(g)  NIST-JANAF / NIST WebBook
dH=-602.9-4*(-110.53)   # kJ/mol
dS=(410.6-29.87-4*197.66)/1000
print("dH=%.1f kJ/mol dS=%.4f kJ/molK"%(dH,dS))
def K(T): return math.exp(-(dH-T*dS)/(R/1000*T))  # atm^-3 (std 1 bar~1 atm)
for TC in [20,40,50,60,80]:
    T=TC+273.15
    for y in [0.0004,0.0002]:
        pNi=y*P/101.325
        pCO_eq=(pNi/K(T))**0.25
        print(f"T={TC}C y_Ni(CO)4={y*100:.2f}% -> min CO for stability {pCO_eq*101.325/P*100:.4f} mol% (x1.5 margin {1.5*pCO_eq*101.325/P*100:.4f}%)")
# decomposer equilibrium residual at 200C, CO partial pressure in concentrated stream at 1 atm
for TC,pCO in [(190,1.0),(200,1.0),(200,0.3)]:
    T=TC+273.15; print(f"decomp {TC}C pCO={pCO} atm: eq. Ni(CO)4 partial pressure {K(T)*pCO**4:.2e} atm")
# --- flows
bcm=38e9; Vm=0.022414 # m3/mol at STP (Gazprom uses 20C std: 0.024055)
Vm20=0.024055
n_gas=bcm/Vm20 # mol/yr
for y in [0.0004,0.0002]:
    ni=n_gas*y*58.69/1e9
    print(f"dose {y*100:.2f}% -> {ni:.1f} kt Ni/yr")
# Kun-Manie scale: ~350 kt conc/yr; assume 7 Mt ore *0.6%Ni*75% -> ~30 kt Ni; take 25 kt Ni/yr
Ni_kt=25.0
y_need=Ni_kt*1e9/58.69/n_gas
print("Kun-Manie-scale 25 kt Ni/yr needs dose %.4f mol%%"%(y_need*100))
# CO consumption
CO_stoich=4*28.01/58.69
print("stoichiometric CO %.2f t CO / t Ni"%CO_stoich)
for TC in [45,60,80]:
    T=TC+273.15; pNi=y_need*P/101.325; pCO=1.5*(pNi/K(T))**0.25
    yCO=pCO*101.325/P
    CO_t=n_gas*yCO*28.01/1e6  # t/yr
    print(f"stabiliser for max {TC}C: {yCO*100:.4f}% CO = {CO_t/1e3:.1f} kt/yr = {CO_t/(Ni_kt*1e3):.2f} t CO/t Ni")
# CO cost via partial oxidation of pipeline gas: CH4+0.5O2 -> CO+2H2
O2_per_tCO=0.5*32/28.01; CH4_per_tCO=16.04/28.01
print("O2 %.2f t/tCO, CH4 %.2f t/tCO"%(O2_per_tCO,CH4_per_tCO))
# cost items (sources in NOTES): O2 from small ASU ~250 kWh/t O2 * $0.06 + capex -> ~$45/t O2; POX+ASU capex ~$90M for ~70 kt CO/yr at 12% CRF
CO_tpy=CO_stoich*Ni_kt*1e3*1.25  # with stabiliser ~0.25 extra at 45C -> recomputed below
def CO_cost(CO_tpy,gas_price_GJ=3.0):
    o2=O2_per_tCO*45
    energy_loss=CH4_per_tCO*50*0.20*gas_price_GJ   # 20% of feed LHV lost (cold gas eff ~80%, H2 used for power)
    capex=90e6*(CO_tpy/70e3)**0.65*0.12/CO_tpy
    return o2+energy_loss+capex
T=45+273.15; pNi=y_need*P/101.325; yCO=1.5*(pNi/K(T))**0.25*101.325/P
stab=n_gas*yCO*28.01/1e6/(Ni_kt*1e3)
tot=CO_stoich+stab
c=CO_cost(tot*Ni_kt*1e3)
print(f"CO make-up {tot:.2f} t/t Ni at ${c:.0f}/t CO -> ${tot*c:.0f}/t Ni")
# GPP capture: cold oil absorber vs heating whole stream
m_gas=bcm*0.73/3.156e7 # kg/s (0.73 kg/m3 at 20C)
nV=n_gas/3.156e7 # mol/s
print("gas flow %.0f kg/s, %.0f kmol/s"%(m_gas,nV/1e3))
for TC,Pa in [(5,9.8e3),(-10,9.8e3),(5,7.0e3)]:
    Kv=psat(TC+273.15)/Pa  # Raoult, gamma~1 for nonpolar Ni(CO)4 in paraffin oil
    for A in [2.0,3.0]:
        L=A*Kv*nV  # mol/s
        Lkg=L*0.170 # C12 oil ~170 g/mol
        N=math.log(1/1e-5*(A-1)+1)/math.log(A)-1
        print(f"absorber {TC}C {Pa/1e3:.1f}MPa K={Kv:.2e} A={A}: oil {Lkg:.0f} kg/s, stages for 99.999% {N:.1f}")
# whole-stream heating alternative (original design)
cp=2.6e3; dT=190-5; Q=m_gas*cp*dT; Qnet=m_gas*cp*20
print("whole-stream heating: gross %.0f MW, recuperated net %.0f MW, recuperator UA %.0f MW/K"%(Q/1e6,Qnet/1e6,Q/20/1e6))
# toxicity of residual in sales gas
for capture in [0.9997,0.99999]:
    resid=y_need*(1-capture)
    air=resid*0.01 # gas leak at 1% in room air
    print(f"capture {capture}: residual {resid*1e9:.1f} ppb in gas -> {air*1e9:.3f} ppb in air at 1% gas leak (NIOSH REL 1 ppb)")
# Rupture: dilution of Ni(CO)4 to IDLH 2 ppm
print("dilution factor of line gas to reach IDLH 2 ppm: %.0f"%(y_need/2e-6))
