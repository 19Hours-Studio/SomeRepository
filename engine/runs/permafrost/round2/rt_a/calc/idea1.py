# Idea 1: Ni(CO)4 carried in a trunk gas line. Repair rounds.
import math
R=8.314
M_Ni, M_CO, M_NiCO4 = 58.69, 28.01, 170.73
# --- line data (Power of Siberia, reviewer + Gazprom public): 38 bcm/yr, 1420 mm, ~9.8 MPa, 2159 km
Q_std = 38e9            # m3/yr at 20 C, 1 atm
mol_per_m3 = 101325/(R*293.15)
D=1.42-2*0.0215; A=math.pi*D**2/4
x_Ni=0.0004             # mol fraction Ni(CO)4
nNi = Q_std*mol_per_m3*x_Ni
print(f"Ni carried {nNi*M_Ni/1e9:.1f} kt/yr")
# transit time: mean pressure ~8 MPa, T 280 K, Z 0.85
P,T,Z=8.0e6,280,0.85
Qact = Q_std/(365*86400)*(101325/P)*(T/293.15)*Z
v = Qact/A
L=2159e3
print(f"actual flow {Qact:.1f} m3/s, velocity {v:.2f} m/s, transit {L/v/86400:.1f} d")
inv_t = nNi*M_NiCO4/1e6/365/ (86400) * (L/v)  # t Ni(CO)4 inventory
print(f"inventory full length {inv_t:.0f} t Ni(CO)4 = {inv_t/(L/1e3):.2f} t/km; 30 km section {inv_t/(L/1e3)*30:.1f} t")
# --- R1 safety: inventory = throughput x residence -> inherent. Planned vents: stop injection >= transit time of the stretch
for Lsec_km in (300,1000,2159):
    print(f"  purge time if injection stopped, {Lsec_km} km downstream of injection: {Lsec_km*1e3/v/3600:.0f} h")
# unplanned rupture of 30 km section, plume decay (Wikipedia/INERIS: half-life ~40 s to <1 min in air; slower with CO present)
m_sec = inv_t/(L/1e3)*30*1e3   # kg
IDLH_mg = 2*M_NiCO4/24.45      # mg/m3 at 2 ppm
print(f"IDLH 2 ppm = {IDLH_mg:.1f} mg/m3; 30-km section inventory {m_sec/1e3:.1f} t needs {m_sec*1e6/IDLH_mg:.2e} m3 air to reach IDLH (no decay)")
for t_half in (40,60,300):
    # release over typical blowdown ~ 1 h; with wind 3 m/s, fraction surviving at 1 km = 2^(-333/t_half)
    surv = 2**(-(1000/3)/t_half)
    print(f"  t1/2={t_half}s: fraction surviving 1 km downwind at 3 m/s = {surv:.3f}")
# LFL vs IDLH: mixture 0.04% carbonyl in gas; gas in air at which carbonyl = IDLH
print(f"gas-in-air fraction at which Ni(CO)4 = 2 ppm: {2e-6/x_Ni*100:.2f} % (LFL 4.4-5 %) -> toxic cloud reaches {5/(2e-6/x_Ni*100):.0f}x further dilution than flammable")
# --- equilibrium and CO dose (reviewer dH,dS)
dH,dS=161e3,410.0
def K(Tc): T=Tc+273.15; return math.exp(-(dH-T*dS)/(R*T))  # bar^3 = pCO^4/pNiCO4
Pline=98
pNi=x_Ni*Pline
for Tc in (40,50,60,80):
    pCO=(K(Tc)*pNi)**0.25
    print(f"  stable to {Tc} C needs CO >= {pCO/Pline*100:.3f} mol% at 98 bar")
# R2: cap compressor discharge at 50 C (aftercoolers) -> CO excess 0.05 mol% (2x margin over 50 C need)
for xCO in (0.0015,0.0005):
    t_CO = (4 + xCO/x_Ni)*M_CO/M_Ni
    print(f"CO consumed with excess {xCO*100:.2f}%: {t_CO:.2f} t CO / t Ni")
t_CO_min = 4*M_CO/M_Ni
t_CO_rep = (4+0.0005/0.0004)*M_CO/M_Ni
# polishing decomposer at 250 C on Ni bed, after letdown to 60 bar, CO 0.3%: residual carbonyl
for Tc in (180,200,250):
    pCO=0.0031*60
    pres=pCO**4/K(Tc)
    print(f"  residual Ni(CO)4 at {Tc} C, 60 bar, 0.31% CO: {pres/60*1e9:.4f} ppb (PEL 1 ppb)")
# Fe(CO)5 risk: keep CO partial pressure low -> 0.05% x 98 bar
print(f"pCO in line {0.0009*98:.3f} bar (0.04% bound is not free CO) vs reviewer 0.147 bar case")
# --- R3 economics per t Ni delivered (all $/t Ni)
CO_price=(60,300)  # $/t CO: low = by-product CO from electric-furnace off-gas at fuel value (~$3/GJ x 10.1 GJ/t x 2); high = merchant/ POX small plant (reviewer)
CO_credit_GJ=(2.0,7.0) # $/GJ: CO energy sold within the gas (domestic vs export gas price)
HV_CO=10.1 # GJ/t
displaced=(94,234)  # reviewer: line capacity used (sales gas displaced) $/t Ni
decomp=440          # reviewer/idea: recuperated decomposer at plant end
lo = t_CO_rep*CO_price[0] - t_CO_min*HV_CO*CO_credit_GJ[1] + displaced[0]
hi = t_CO_rep*CO_price[1] - t_CO_min*HV_CO*CO_credit_GJ[0] + displaced[1]
print(f"pipeline-specific cost (CO one-way + displaced gas - CO energy credit) = {lo:.0f} .. {hi:.0f} $/t Ni; + decomposer {decomp}")
# baselines ($/t Ni delivered to rail/port)
conc_trucking=1067   # reviewer: concentrate truck+rail
matte=150            # reviewer: 70% Ni matte
pellet = 100         # refined pellets ~ 1.0-1.1 t per t Ni, same haul as matte/0.7
print(f"baseline A ship concentrate {conc_trucking}; B ship matte {matte}; C carbonyl refinery at mine + ship pellets ~{pellet} (decomposer exists in both C and pipeline route -> cancels)")
print(f"vs C (decomposer cancels): pipeline {lo:.0f}..{hi:.0f} vs {pellet} -> ratio {pellet/max(lo,1):.2f}..{pellet/hi:.2f}")
print(f"vs A: pipeline+decomp {lo+decomp:.0f}..{hi+decomp:.0f} vs {conc_trucking}: ratio {conc_trucking/(lo+decomp):.2f}..{conc_trucking/(hi+decomp):.2f}")
print(f"Ni price ~16000 $/t: transport share matte {matte/16000*100:.1f}%")
