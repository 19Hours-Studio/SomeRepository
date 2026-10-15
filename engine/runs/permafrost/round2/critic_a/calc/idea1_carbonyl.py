import math
R=8.314
# --- throughput
V=38e9  # m3/yr; Russian standard 20C, 101.325 kPa
vm20=R*293.15/101325; vm0=R*273.15/101325
for lab,vm in (("20C std",vm20),("0C std",vm0)):
    n=V/vm; nNi=n*4e-4
    print(lab,"gas mol/yr %.3e"%n,"Ni kt/yr %.1f"%(nNi*58.693/1e9),"Ni(CO)4 kg/s %.2f"%(nNi*170.73/1000/3.156e7))
n=V/vm20; nNi=n*4e-4; Ni_t=nNi*58.693/1e6
# --- vapour pressure (Clausius-Clapeyron through bp 316.15 K and 318 mmHg at 20 C)
dHR=math.log(760/318)/(1/293.15-1/316.15)
print("dHvap = %.1f kJ/mol"%(dHR*R/1000))
def psat(T): return 101.325*math.exp(-dHR*(1/T-1/316.15))  # kPa
for x,P in ((1e-3,9800),(4e-4,9800),(4e-4,7500),(4e-4,5000)):
    pp=x*P
    Tsat=1/(1/316.15 - math.log(pp/101.325)/dHR)
    print("x=%.4f P=%d kPa pp=%.2f kPa dew/frost T=%.1f C ; sat ratio at -20C=%.2f"%(x,P,pp,Tsat-273.15,pp/psat(253.15)))
# --- decomposition thermo  Ni(CO)4(g) -> Ni + 4CO ; dH, dS
for dH,dS in ((160.9e3,410.1),(158e3,413)):
    def Kp(T): return math.exp(-(dH-T*dS)/(R*T))  # bar^3
    P=98.0; pNi=4e-4*P; pCO=1.5e-3*P
    Q=pCO**4/pNi
    Tst=dH/(dS-R*math.log(Q))
    print("dH=%.0f dS=%.0f: stability limit (decomp starts above) T=%.1f C"%(dH/1e3,dS,Tst-273.15))
    for TC in (180,200):
        T=TC+273.15; pCOend=(1.5e-3+4*4e-4)*P
        peq=pCOend**4/Kp(T)
        print("   %d C at 98 bar: eq. residual fraction=%.2e -> max removal %.4f%%"%(TC,peq/pNi,100*(1-peq/pNi)))
        P2=60.0; pNi2=4e-4*P2; pCO2=(1.5e-3+1.6e-3)*P2
        print("   %d C at 60 bar: residual fraction=%.2e"%(TC,(pCO2**4/Kp(T))/pNi2))
# --- residual Ni(CO)4 in sales gas
res=4e-4*3e-4
print("residual Ni(CO)4 in sales gas = %.3f ppm; in air at 1%% gas = %.2f ppb, at LEL 4.4%% = %.1f ppb (TLV/PEL 1 ppb)"%(res*1e6,res*0.01*1e9,res*0.044*1e9))
# --- CO budget
nCO_dose=n*1.5e-3; nCO_carb=4*nNi
print("CO dose %.0f kt/yr + CO bound in carbonyl %.0f kt/yr = %.0f kt/yr ; per t Ni = %.2f t CO"%(nCO_dose*28e-9,nCO_carb*28e-9,(nCO_dose+nCO_carb)*28e-9,(nCO_dose+nCO_carb)*28e-6/Ni_t))
print("CO in sales gas after decomposer: %.2f mol%%"%(100*(1.5e-3+1.6e-3)))
# --- decomposer heat duty
mdot=n*0.0172/3.156e7  # kg/s (M~17.2 g/mol pipeline gas)
cp=2.6  # kJ/kgK methane at ~7-10 MPa, 0-200C average
LHV=V*34.0e6/3.156e7/1e6  # MW (34 MJ/m3 at 20C std)
for dT in (180,200):
    Q=mdot*cp*dT/1000  # MW
    for eff in (0.8,0.85,0.9):
        print("mdot=%.0f kg/s dT=%d: gross heat %.0f MW, recup eff %.2f -> net %.0f MW = %.3f%% of line gas"%(mdot,dT,Q,eff,Q*(1-eff),100*Q*(1-eff)/LHV))
fuel_needed=0.0012*LHV
print("0.12%% of gas = %.1f MW; implies recuperator effectiveness >= %.3f (dT 190K, no losses)"%(fuel_needed,1-fuel_needed/(mdot*cp*190/1000)))
# recuperator area
Q=mdot*cp*190/1000*0.885
for U in (300,500):
    print("recuperator duty %.0f MW, approach ~22K, U=%d -> area %.0f m2"%(Q,U,Q*1e6/(U*22)))
# --- line inventory
L=2159e3; D=1.42-2*0.0215; A=math.pi*D**2/4
rho=80.0 # kg/m3 methane ~9.8->7 MPa, ~0-5C
gas_mol=L*A*rho/0.0172
inv=gas_mol*4e-4*170.73/1e6
print("linepack %.0f kt gas, Ni(CO)4 in line %.0f t; per 30 km valve section %.1f t"%(L*A*rho/1e6,inv,inv*30/2159))
for vent in (2.7e6,0.9e6):
    m=vent/vm20*4e-4*170.73/1e6
    print("vent %.1f Mm3 (Gazprom 2021 repair) carries %.1f t Ni(CO)4 = %.1e m3 of air at IDLH 2 ppm (14 mg/m3)"%(vent/1e6,m,m*1e9/14))
# --- Fe(CO)5 equilibrium on steel wall: Fe + 5CO -> Fe(CO)5(g)
dH=-733.8+5*110.53; dS=445.3-27.28-5*197.66
for TC in (0,15,30):
    T=TC+273.15; K=math.exp(-(dH*1e3-T*dS)/(R*T))
    print("Fe(CO)5 eq. pressure at %d C with pCO=0.147 bar: %.3g bar (vs Ni(CO)4 pp 0.039 bar)"%(TC,K*0.147**5))
# --- pipeline capacity share
share=4e-4+1.5e-3
print("molar capacity used by Ni(CO)4+CO = %.2f%%; displaced gas %.0f Mm3/yr"%(share*100,share*V/1e6))
for price in (100,250):
    lost=share*V/1000*price
    # CO returns heating value: 0.31% CO * 283/890 of methane HHV
    credit=(3.1e-3*283/890)*V/1000*price
    print(" gas price $%d/1000m3: displaced value $%.1fM/yr, CO fuel credit $%.1fM, net $%.0f/t Ni"%(price,lost/1e6,credit/1e6,(lost-credit)/Ni_t))
print("Ni t/yr",round(Ni_t))
# --- transport baseline
for grade in (0.10,0.12,0.70,0.99):
    print("truck+rail $1067/t Ni corresponds to $%.0f per t of product at %.0f%% Ni"%(1067*grade,grade*100))
# stability limit vs pressure (x_Ni=4e-4, x_CO=1.5e-3)
for P in (98,75,55):
    Q=(1.5e-3*P)**4/(4e-4*P)
    for dH,dS in ((160.9e3,410.1),(158e3,413)):
        print("P=%d bar: decomposition becomes favourable above %.1f C (dH=%.0f)"%(P,dH/(dS-R*math.log(Q))-273.15,dH/1e3))
