"""Repair calculations for the 6 energy-storage ideas. Run: python3 calc.py
All inputs carry a source tag; see NOTES at the end of LOG.md."""
import math
R, F, kB = 8.314, 96485.0, 1.380649e-23

def hdr(s): print("\n" + "=" * 8 + " " + s + " " + "=" * 8)

# ------------------------------------------------------------------ IDEA 1
hdr("IDEA 1 sugar-glass granules")
T = 443.0                     # 170 C melt
Tg = 323.0                    # glass with Tg ~50 C (task)
# WLF universal constants (Williams-Landel-Ferry 1955), eta(Tg)=1e12 Pa s
def wlf(Tc, Tg=Tg, C1=17.44, C2=51.6):
    return 10 ** (12 - C1 * (Tc - Tg) / (C2 + Tc - Tg))
for t in (140, 170, 200):
    print(f"WLF viscosity at {t} C: {wlf(t+273.15):.3g} Pa s")
eta = 0.5
# Stokes-Einstein diffusivities
D_small = kB * T / (6 * math.pi * eta * 0.35e-9)     # small ion r=0.35 nm
D_rad = kB * T / (6 * math.pi * eta * 0.5e-9)        # radical r=0.5 nm
D_olig = kB * T / (6 * math.pi * eta * 2.5e-9)       # oligomer r=2.5 nm
print(f"D small ion {D_small:.2e}, radical {D_rad:.2e}, oligomer {D_olig:.2e} m2/s")
# round 1: posolyte+negolyte in ONE melt -> diffusion-limited annihilation
kdiff = 8 * R * T / (3 * eta) * 1000      # L/mol/s (Smoluchowski)
print(f"R1 mixed melt: k_diff={kdiff:.2e} M^-1 s^-1 -> t1/2 at 0.5 M = {1/(kdiff*0.5):.1e} s  => FAIL, streams must be separate")
# heat balance per kWh
m_kWh = 25.0; cp = 1.6e3; dT = 145
Qth = m_kWh * cp * dT / 3.6e6
print(f"R1 heat to melt 25 kg: {Qth:.2f} kWh_th/kWh_e; with 90% recovery residual {0.1*Qth:.2f} kWh_th/kWh_e")
# energy density -> active-site concentration
V = 1.2; rho = 1500
mol_e_per_kg = 40 / (V * 26.8) / 2      # per side, half the mass each side
c_a = mol_e_per_kg * rho                 # mol/m3 of active e- per side
print(f"active e- per side {mol_e_per_kg:.2f} mol/kg -> {c_a:.0f} mol/m3")
# round 2: porous separator; crossover fraction x ohmic drop is geometry-invariant:
# f*eta = (RT/F) * c_a D_a / sum(c_i z^2 D_i)
def f_eta(c_a, D_a, carriers):
    return R * T / F * c_a * D_a / sum(c * D for c, D in carriers)
fe2 = f_eta(c_a, D_rad, [(c_a, D_rad), (c_a, D_small)])
print(f"R2 radicals + same-size counterions: f*eta = {fe2*1000:.1f} mV -> crossover at 50 mV separator drop = {fe2/0.05:.0%}  => FAIL")
# round 3: bulky oligomeric actives + small decoupled carrier (proton/Li+, decoupling x10 vs SE)
D_carrier = 10 * D_small
fe3 = f_eta(c_a, D_olig, [(c_a, D_olig), (c_a, D_carrier)])
print(f"R3 oligomer actives + decoupled small carrier: f*eta = {fe3*1000:.2f} mV -> crossover at 50 mV = {fe3/0.05:.1%}")
sigma3 = F**2 / (R*T) * (c_a*D_olig + c_a*D_carrier)
print(f"   melt conductivity with decoupled carrier: {sigma3:.3f} S/m")
# electrode access with oligomers: electron self-exchange hopping between redox sites
# (Dahms-Ruff) D_app = D_phys + k_ex*delta^2*c/6 ; k_ex ~1e7 M^-1s^-1 (TEMPO/viologen), delta ~1.2 nm
k_ex = 1e7 / 1000; delta = 1.2e-9
D_hop = k_ex * delta**2 * c_a / 6
D_app = D_olig + D_hop
print(f"   Dahms-Ruff hopping D_app = {D_app:.2e} m2/s (physical {D_olig:.1e})")
# channel: half-height h per side; full conversion in residence t_res = h^2/(2 D_app)
for h in (5e-6, 10e-6, 15e-6):
    t_res = h**2 / (2*D_app)
    i = F * c_a * h / t_res * 0.8            # 80% utilisation single pass
    i = min(i, 15.0)                          # cap by ohmic budget below
    # ohmic across both half-channels + 10 um separator (eps/tau=0.3)
    eta_ohm = i * (h / sigma3 + 10e-6 / (0.3 * sigma3))
    # pressure drop slit flow length 2 cm
    vs = i / (F * c_a * 0.8)                   # m3/m2/s of melt per side
    L = 0.02
    dP = 12 * eta * L**2 * vs / h**3
    print(f"   h={h*1e6:.0f} um: t_res={t_res:.0f} s, i={i:.1f} A/m2, ohmic={eta_ohm*1000:.0f} mV, dP(2cm)={dP/1e5:.1f} bar")
# chosen h=10 um, i=10 A/m2, V 1.2 -> W/m2 ; area per kWh vs duration; cell cost $25/m2
i_op = 10.0; Pm2 = i_op * (V - 0.1)
for hrs in (100, 300, 1000):
    a = 1000 / (Pm2 * hrs)
    print(f"   duration {hrs} h: {a:.3f} m2/kWh -> cell {a*25:.1f} $/kWh at $25/m2")
# medium cost: sugar fraction + actives
for p_act in (1, 3, 10):
    act_kg = 2 * mol_e_per_kg * 0.25 * 25 / 1   # 0.25 kg per mol e- oligomer, fraction of 25 kg
    print(f"   actives {act_kg:.1f} kg/kWh at ${p_act}/kg -> ${act_kg*p_act:.0f}/kWh (+ sugar {25-act_kg:.1f} kg x $0.45 = ${(25-act_kg)*0.45:.1f})")

# ------------------------------------------------------------------ IDEA 2
hdr("IDEA 2 locked rubber")
rho_r = 1.15e3
# R1: lightly crosslinked NR (shape-memory NR, Katzenberg 2011): G~0.25 MPa, lambda up to 10
def neo(G, lam): return G/2*(lam**2 + 2/lam - 3)
W = neo(0.25e6, 5) / rho_r / 3600; W10 = neo(0.25e6, 10) / rho_r / 3600
print(f"R1 light-NR neo-Hookean: lam5 {W:.2f} Wh/kg, lam10 {W10:.2f} Wh/kg")
for price in (1.7, 0.3, 0.02):
    print(f"   medium at ${price}/kg, 3 Wh/kg x 0.7 recoverable -> ${price/(3*0.7)*1000:.0f}/kWh")
# R3: carbon-black-filled NR truck tread, M300 11-17 MPa, TS 18-22 MPa (US5132357) -> lambda=4 (300%)
eps = [0, 1, 2, 3]; sig = [0, 3e6, 8e6, 14e6]
Win = sum((sig[k]+sig[k+1])/2*(eps[k+1]-eps[k]) for k in range(3))
print(f"R3 tread strip to 300%: input {Win/1e6:.1f} MJ/m3 = {Win/rho_r/3600:.2f} Wh/kg; recoverable 55% -> {0.55*Win/rho_r/3600:.2f} Wh/kg")
Wr = 0.55*Win/rho_r/3600
print(f"   rubber per kWh {1000/Wr:.0f} kg; bales 600 kg/m3 -> {1000/Wr/600:.2f} m3/kWh -> yard ${1000/Wr/600*10:.1f}/kWh")
# heat needed: warm 20->45 C (cp 1.9 kJ/kgK) plus latent of ~15% crystallinity x 61 J/g
q = 1.9e3*25 + 0.15*61e3
print(f"   heat to trigger per kg {q/1e3:.0f} kJ vs work {Wr*3.6:.1f} kJ -> heat/work = {q/(Wr*3600):.0f}")
# cold-climate lock: stretched tread rubber must be held below crystal melting; winter mean -5 C
# winch: 500 kg/stroke at ~3 Wh/kg; L0 2 m -> 8 m stroke
stroke_E = 1.5e3*3600; F_avg = stroke_E/6.0
print(f"   1.5 kWh stroke over 6 m -> mean force {F_avg/1e3:.0f} kN (hydraulic-press class)")
# resource: scrap truck tyres, ~6 kg cord-free tread+undertread each
for n in (35e6,):
    print(f"   {n/1e6:.0f}M truck tyres/yr x 6 kg -> {n*6/(1000/Wr)/1e6:.2f} GWh/yr of store")

# ------------------------------------------------------------------ IDEA 3
hdr("IDEA 3 crystallizing twin ditch")
c = 20.0; D = 5e-10
# R1 original: flow-by on ditch floor, boundary layer 100 um
i_lim_floor = F * c * D / 100e-6
print(f"R1 floor flow-by i_lim ~ {i_lim_floor:.1f} A/m2 (so 10 A/m2 is mass-transfer bound); converter $30/m2 /10 W/m2 = $3/W")
# crossover through 2.5 mm divider eps/tau 0.4
xo = 0.4 * D * c / 2.5e-3 * F
print(f"   crossover current {xo:.2f} A/m2 = {xo/10:.1%} of 10 A/m2")
# R2: electrodes as vertical flow-through felts on both faces of the divider, ditch = feed channel
k_a = 0.05      # 1/s volumetric mass transfer in felt at low percolation (order from felt RFB lit.)
for Le in (3e-3, 5e-3):
    il = F * c * k_a * Le
    print(f"R2 flow-through felt {Le*1e3:.0f} mm: i_lim {il:.0f} A/m2")
i2 = 50.0
sig = 10.0     # S/m, ~1 M KCl supporting salt
eta2 = i2 * 2.5e-3 / (0.4*sig) + i2 * 2e-3 / (0.6*sig)
print(f"   at {i2} A/m2: ohmic {eta2*1000:.0f} mV, crossover {xo/i2:.2%}")
felt = 2*18 + 8   # two felts $18/m2 each + divider $8/m2
for hrs in (200, 500):
    print(f"   converter ${felt}/m2 at {i2*0.9:.0f} W/m2 -> ${felt/(i2*0.9):.2f}/W -> ${felt/(i2*0.9)*1000/hrs:.1f}/kWh at {hrs} h")
# flow needed: 1 mM supersaturation budget, per m2 felt
flux = i2 / F
print(f"   feed per m2 electrode {flux/2*1e3:.3f} L/s for 2 mM conversion per pass")
# molecule
for MW, n, Vc in ((200, 2, 1.0), (300, 2, 0.9)):
    kg = 2 * 1000 / (Vc * n * 26.8) * MW / 1000
    print(f"   powder: MW {MW}, {n} e-, {Vc} V -> {kg:.1f} kg/kWh both sides; at $1.5/kg ${kg*1.5:.0f}/kWh")
# delayed crystallization requirement: residence in ditch vs induction time
L_ditch, v = 50.0, 0.05
print(f"   ditch residence {L_ditch/v/60:.0f} min -> need induction time >> that at S~1.1-1.3, but seconds-minutes on seeds")

# ------------------------------------------------------------------ IDEA 4
hdr("IDEA 4 vapour-swing clay")
M = 0.018
def psat(TC): return 610.94 * math.exp(17.625*TC/(TC+243.04))   # Magnus
for TC in (25, 35, 50):
    for RH in (0.15, 0.37):
        p = psat(TC)*RH
        w = R*(TC+273.15)/M*math.log(1/RH)     # J/kg vapour (isothermal ideal)
        rho_v = p*M/(R*(TC+273.15))
        vol = 1000/(w*rho_v)                   # m3/s per kW
        print(f"T={TC} C RH={RH}: work {w/1e3:.0f} kJ/kg, {vol:.2f} m3/s per kW, ratio {1/RH:.1f}")
# clay isotherm: GAB fit typical of Ca-montmorillonite (Keren & Shainberg 1975 shape): Wm=0.09, C=15, K=0.75
def gab(a, Wm=0.09, C=15, K=0.75): return Wm*C*K*a/((1-K*a)*(1-K*a+C*K*a))
def work_per_kg(a_lo, a_hi, TC=25, Wm=0.09, C=15, K=0.75, n=400):
    tot = 0
    for k in range(n):
        a1 = a_lo + (a_hi-a_lo)*k/n; a2 = a_lo + (a_hi-a_lo)*(k+1)/n
        dm = gab(a2,Wm,C,K)-gab(a1,Wm,C,K); am = (a1+a2)/2
        tot += dm*R*(TC+273.15)/M*math.log(1/am)
    return tot
for lo in (0.05, 0.15, 0.37):
    w = work_per_kg(lo, 0.9)
    print(f"R1 clay swing RH {lo}-0.9: uptake {gab(0.9)-gab(lo):.3f} g/g, work {w/3600:.2f} Wh/kg -> {3.6e6/w:.0f} kg/kWh")
# R2: salt-in-clay (CaCl2 ~30 wt% in bentonite): step uptake ~0.3 g/g between RH 0.3 and 0.6 (CaCl2 hydrates/deliquescence)
w_salt = 0.30 * R*298/M*math.log(1/0.45)
print(f"R2 CaCl2-in-clay: 0.30 g/g at mean RH 0.45 -> {w_salt/3600:.1f} Wh/kg -> {3.6e6/w_salt:.0f} kg/kWh; cost at $90/t {3.6e6/w_salt*0.09:.1f} $/kWh")
# heat flux: adsorption heat ~2.8 MJ/kg water, work per kg water ~ w_salt/0.3
qr = 2.8e6/(w_salt/0.3)
print(f"   heat/work ratio {qr:.0f}; 3 K penalty -> lnp shift {0.0595*3:.2f} vs ln(1/RH)={math.log(1/0.45):.2f}")
for dT in (0.5, 1.0, 3.0):
    print(f"   dT={dT} K each way: round-trip work loss ~{2*0.0595*dT/math.log(1/0.45):.0%}")
# bed thickness for heat removal at 1000 h discharge; k=0.5 W/mK; dT 0.5K
mass = 3.6e6/w_salt; vol = mass/1100
Qdot = qr*1000/1000      # W per kWh capacity at 1000 h discharge
b = math.sqrt(2*2*0.5*0.5*vol/Qdot)   # two faces, k dT/(b/2)
print(f"   at 1000 h: heat {Qdot:.0f} W per kWh; bed thickness {b*100:.0f} cm, wall area {2*vol/b:.2f} m2/kWh")
# machine: at 35 C, RH ~0.45 sorbent side, ratio 2.2 (single radial stage)
TC = 35; RH = 0.45
p = psat(TC)*RH; w = R*308/M*math.log(1/RH); rho_v = p*M/(R*308)
vol_kw = 1000/(w*rho_v)
print(f"R3 35 C, RH 0.45: {vol_kw:.2f} m3/s per kW, pressure ratio {1/RH:.1f}")
for cost_per_m3s in (3000, 6000):
    ckw = cost_per_m3s*vol_kw/0.75     # 75% isentropic-ish
    print(f"   machine ${cost_per_m3s}/(m3/s) -> ${ckw:.0f}/kW -> ${ckw/500:.1f}/kWh at 500 h, ${ckw/1500:.1f}/kWh at 1500 h")

# ------------------------------------------------------------------ IDEA 5
hdr("IDEA 5 earthen bipolar pile")
def pile(cap_mmol_g, L_fe, V=0.6, days=14, char_sig=2.0, sig_w=8.0, phi=0.45):
    rho_d = 1.3e3
    q = cap_mmol_g*1e-3*1e3*rho_d*L_fe*F/3600   # Ah/m2
    E = q*V/1000                                  # kWh/m2
    i = q/(days*24)
    sig_ion = sig_w*phi**2                        # Archie m=2
    sig_liner = 8.0*0.4**2.5
    # ion path: ~L/2 in Fe layer (uniform reaction), 5 mm liner, ~1/2 of thin MnO2 layer
    L_mn = 0.01
    eta_ion = i*(L_fe/2/sig_ion + 5e-3/sig_liner + L_mn/2/sig_ion)
    eta_e = i*(L_fe/2/char_sig)                   # electron path to foil through char network
    return q, E, i, eta_ion, eta_e
for cap, L in ((1.0, 0.03), (0.4, 0.03), (0.4, 0.06), (1.5, 0.04)):
    q, E, i, ei, ee = pile(cap, L)
    print(f"cap {cap} mmol/g L {L*100:.0f} cm: {E:.2f} kWh/m2, i {i:.2f} A/m2, ionic {ei*1000:.0f} mV, electronic {ee*1000:.0f} mV, foil $/kWh {6/E:.1f}")
# char percolation: 10 vol% random char near threshold; GEM sigma = s_c*((f-fc)/(1-fc))^2
for f in (0.10, 0.15, 0.20, 0.25):
    s = 200*max(0, (f-0.12)/(1-0.12))**2   # compacted high-T char ~200 S/m (lit. range 10-1000)
    print(f"   char {f:.0%} vol -> composite sigma_e {s:.2f} S/m")
# mediator self-discharge across 5 mm compacted bentonite
for cm in (10, 50):
    Jx = 3e-11*cm/5e-3*F
    print(f"   mediator {cm} mM, De 3e-11 -> shuttle {Jx*1000:.2f} mA/m2 -> {Jx*24*14/ (pile(1.0,0.04)[0]):.1%} per 2 weeks")
# mediator reach: 2 mm to carbon within 2-week discharge
Dp = 2e-10
print(f"   2 mm mediator diffusion time {(2e-3)**2/Dp/3600:.1f} h; volumetric supply {Dp*20*F/(2e-3)**2:.0f} A/m3 vs need {pile(1.0,0.04)[2]/0.04:.0f} A/m3")
# cost
q, E, i, ei, ee = pile(1.5, 0.04)
earth = (0.04*1.3e3*0.05 + 0.012*2e3*0.25 + 0.005*1.6e3*0.06 + 0.04*0.2*400*0.25)  # $: Fe-clay $50/t, Mn ore $250/t, bentonite $60/t, char 20vol% 400 kg/m3 $250/t
print(f"   chosen 1.5 mmol/g, 4 cm: {E:.2f} kWh/m2; materials ${earth:.1f}/m2 + foil $6/m2 + placing $4/m2 -> ${(earth+10)/E:.1f}/kWh")

# ------------------------------------------------------------------ IDEA 6
hdr("IDEA 6 floating solar gravity cell")
V6 = 1.75
E = 1.9  # kWh/m2
Ah = E*1000/V6; mol_e = Ah*3600/F
print(f"Zn-Br: {Ah:.0f} Ah/m2, Br2 {mol_e/2:.1f} mol/m2, in 6 cm coke bed eps 0.4 = {mol_e/2/24:.2f} M Br2 in pores")
ZnBr2 = mol_e/2*1.3*0.225   # kg/m2 with 30% excess
print(f"   ZnBr2 {ZnBr2:.1f} kg/m2 -> {ZnBr2/E:.1f} kg/kWh; at $3/kg ${ZnBr2/E*3:.1f}/kWh")
# self-discharge: free aqueous Br2 c_f with quaternary-ammonium complexer ~10 mM; gap 3 cm
for cf, lab in ((10, "diffusive gap"),):
    J = 1e-9*cf/0.03*2*F
    print(f"R1 diffusive: {J*1000:.0f} mA/m2 -> {J*240/Ah:.1%} per 10 days")
# convection in open water layer cooled from top at night: Ra
g, beta, nu, al = 9.81, 2.5e-4, 1e-6, 1.4e-7
H, dT = 0.03, 2.0
Ra = g*beta*dT*H**3/(nu*al)
print(f"   open gap Ra = {Ra:.0f} (>1708 -> convects); convective BL ~1 mm -> {1e-9*10/1e-3*2*F*240/Ah:.0%} per 10 days => FAIL")
k_perm = 1e-10
Ram = g*beta*dT*k_perm*H/(nu*al)
print(f"R2 gap filled with nonwoven (k=1e-10 m2): Darcy-Ra = {Ram:.3f} (<4pi^2=39.5 stable) -> back to diffusive")
# DC coupling: per battery cell, 4 c-Si cells (0.55 V MPP) -> 2.2 V; charging 1.95 V; dark leakage at night
Jsc, Voc, Vt = 0.040, 0.70, 0.0257*1.0
for Vb in (1.75,):
    Vc = Vb/4
    Jd = Jsc*math.exp((Vc-Voc)/Vt)
    A_pv = 4*0.033
    print(f"   4 PV cells at {Vc:.2f} V each in dark: {Jd*1e4*A_pv*1e3:.2f} mA leakage (A/cm2 {Jd:.1e})")
# PV cell IV at 1.95/4=0.49 V vs MPP 0.55 V: single-diode
def Ipv(v): return Jsc - Jsc*math.exp((v-Voc)/(1.3*Vt))
Pm = max(v*Ipv(v) for v in [k/1000 for k in range(0, 700)])
print(f"   power at 0.49 V/cell vs MPP: {0.49*Ipv(0.49)/Pm:.0%}")
# capacity sizing: mat/PV area ratio
pv = 0.2*1000*4.5/1000  # kWh/m2/day of PV at 4.5 sun-h
print(f"   PV {pv:.2f} kWh/m2/day; mat 5x PV -> refill 1.9 kWh/m2 of mat in {1.9*5/pv/0.85:.0f} sunny days (charge eff 0.85)")
coke = 0.06*1000*0.5/E*0.0   # placeholder
cost = {"coke 6cm @$200/t": 0.06*0.6*1000*0.2/E, "ZnBr2": ZnBr2/E*3, "complexer": 0.4*ZnBr2/E*4,
        "felt floor+mat $25/m2": 25/E, "liner+nonwoven $6/m2": 6/E}
print("   cost $/kWh:", {k: round(v, 1) for k, v in cost.items()}, "total", round(sum(cost.values()), 1))

# ---------------------------------------------------------------- extra rounds
hdr("IDEA 4 round 4: sorbent RH window trade-off (35 C)")
for RHm in (0.05, 0.1, 0.2, 0.3, 0.45):
    w = R*308/M*math.log(1/RHm); rho_v = psat(35)*RHm*M/(R*308)
    print(f"mean RH {RHm}: heat/work {2.6e6/w:.1f}, loss at 0.5 K each way {2*0.0595*0.5/math.log(1/RHm):.0%}, {1000/(w*rho_v):.2f} m3/s/kW")
hdr("IDEA 5 round 3: concentrated brine, 25 vol% char, 4-week discharge")
for cap, L, days, sw in ((1.5, 0.03, 14, 15.0), (1.5, 0.04, 28, 15.0), (1.0, 0.04, 28, 15.0)):
    q, E, i, ei, ee = pile(cap, L, days=days, char_sig=4.4, sig_w=sw)
    print(f"cap {cap} L {L*100:.0f} cm {days} d brine {sw} S/m: {E:.2f} kWh/m2, i {i:.2f}, ionic {ei*1000:.0f} mV, electronic {ee*1000:.0f} mV, total {(ei+ee)*1000:.0f} mV of 600")
hdr("IDEA 1 round 4: cost closure vs cell voltage")
for Vc in (0.6, 1.0, 1.4):
    for gpe in (100, 250):
        kg = 2*1000/(Vc*26.8)*gpe/1000
        print(f"V {Vc}, {gpe} g per mol e-: actives {kg:.0f} kg/kWh -> max price for $10/kWh actives: ${10/kg:.2f}/kg")
