"""Idea 4 - snow-buoyed under-ice ore pods. Binding quantity: the buoyancy budget of a sealed snow pod over the
41-68 d transit vs the +3..+9 kg trim window (shell melt, snow creep under hydrostatic load, air compressibility),
then the friction/drag balance of the repaired (rolling, robustly buoyant) pod vs measured under-ice velocity.
Sources: snow viscosity Vionnet et al. 2012 (GMD, Crocus): eta = eta0*(rho/250)*exp(0.1*(Tf-T)+0.023*rho),
eta0 = 7.62e6 Pa s; under-ice velocity Lena delta Apr 2019: main channel 0.12-0.18, Bykovskaya 0.20-0.25,
Olenekskaya 0.05-0.11 m/s (Fedorova et al. 2020, E3S conf 163:05003); Krasnoyarsk tailwater still +2 C off winter
equilibrium 40 km below dam (Tech. Phys. 2025)."""
import math
rw, ri = 1000.0, 917.0
def eta(rho, T=0.0):
    return 7.62237e6*(rho/250)*math.exp(0.1*(0-T)+0.023*rho)

# ---------------- original pod: 10 t ore, 5.0 x 2.2 x 1.2 m, shell 8-10 cm, trim +3..+9 kg --------------
Lp, Wp, Hp, sh = 5.0, 2.2, 1.2, 0.09
A_shell = 2*(Lp*Wp + Lp*Hp + Wp*Hp)
print(f"shell area {A_shell:.1f} m2, shell ice {A_shell*sh:.2f} m3")
melt = 0.06
dB_melt = -A_shell*melt*(rw-ri)
print(f"(1) shell melt 6 cm over transit (the idea's own number) -> buoyancy change {dB_melt:.0f} kg vs trim window +3..+9 kg")
# snow volume in a 10 t rock-ore pod: 0.74 m3/t -> 7.4 m3 at ~150-300 kg/m3
V_snow = 7.4
for rho in (250, 350, 450, 550):
    for dp in (20e3, 5e3):
        rate = dp/eta(rho)            # 1/s volumetric strain (uniaxial approx)
        dV = V_snow*rate*86400        # m3/day
        print(f"(2) snow {rho} kg/m3, pressure excess {dp/1e3:4.0f} kPa: creep {rate*86400*100:7.3f} %/d -> buoyancy loss {dV*1000:8.1f} kg/day")
# air compressibility if the shell/snow are not rigid
V_air = V_snow*(1-250/917)
dBdz = V_air*rw/10.33
print(f"(3) compressible air {V_air:.1f} m3 -> buoyancy changes {dBdz:.0f} kg per metre depth (Cartesian-diver unstable vs 3-9 kg trim)")
# warm tailwater below dams: shell melt rate at +0.5..+2 C, h~600 W/m2K
for dT in (0.05, 0.5, 2.0):
    m = 600*dT/(ri*334e3)*86400*100
    print(f"(4) water {dT:+.2f} C above freezing: shell melts {m:.1f} cm/day -> 9 cm shell lasts {9/m:.1f} d")
# friction of near-neutral pod vs drag (the idea's own numbers): mu 0.5
for B in (3, 9, 50, 200):
    for v in (0.12, 0.16, 0.25):
        Fd = 0.5*rw*1.1*(Lp*Hp)*v**2
        print(f"   net buoyancy {B:3d} kg, v_rel {v:.2f}: sliding friction {0.5*B*9.81:6.0f} N vs drag {Fd:5.0f} N -> {'moves' if Fd > 0.5*B*9.81 else 'STALLS'}")

# ---------------- repair: cold-sealed, dense-snow ROLLING log pod ----------------
print("\n--- repair: cylinder 'log' pod, snow pre-compacted to 550 kg/m3 and sealed at -35 C ---")
T_seal = -35.0
p_int = 101.3e3*(273.15)/(273.15+T_seal) - 101.3e3   # gauge pressure after warming to 0 C (air fraction)
print(f" sealing cold air at {T_seal} C gives +{p_int/1e3:.1f} kPa at 0 C = hydrostatic head {p_int/9810:.2f} m")
depth_axis = 1.6 + 0.8       # ice draft 1.6 m + radius
for draft_var in (0.0, 0.5, 1.0):
    dp = abs(9810*(depth_axis+draft_var) - p_int)
    r = dp/eta(550)*86400*45*100
    print(f"  ice draft +{draft_var} m: residual dp {dp/1e3:.1f} kPa -> 45-d snow creep {r:.2f} %")
cargo = {"coal": (1350,), "rock ore": (2700,), "sulphide ore": (4200,)}
for name, (rho_o,) in cargo.items():
    M = 10000.0
    Vo = M/rho_o; W_sub = M - Vo*rw
    margin = 500.0               # kg positive buoyancy after melt allowance
    melt_allow = 250.0
    need = W_sub + margin + melt_allow
    # snow 550 kg/m3: net 450 kg/m3 ; shell 12 cm ice net 83 kg/m3 (counted as bonus, ignored)
    Vs = need/(rw-550)
    Vt = Vo + Vs
    D = 1.6; Lc = Vt/(math.pi*D*D/4)
    print(f" {name:12s}: snow {Vs/10:.2f} m3/t (vs 0.28-0.86 dry snow), pod volume {Vt:.1f} m3 -> D {D} m x L {Lc:.1f} m")
# rolling: resistance coefficient on wet ice underside unknown: 0.02-0.08 (ice adhesion/sintering at 0 C)
print(" rolling balance (net buoyancy 750 kg incl. melt allowance, D 1.6 m, L ~9 m):")
B = 750.0
for crr in (0.02, 0.05, 0.08):
    F_roll = crr*B*9.81
    D, Lc = 1.6, 9.0
    v_need = math.sqrt(F_roll/(0.5*rw*1.0*D*Lc))
    print(f"  Crr {crr}: resistance {F_roll:.0f} N -> needs relative velocity {v_need:.2f} m/s at the ice; near-ice flow ~0.7x mean -> mean >= {v_need/0.7:.2f} m/s")
print(" measured under-ice: Lena delta main channel 0.12-0.18 m/s, Bykovskaya 0.20-0.25, Olenekskaya 0.05-0.11 (Apr 2019)")
# under-ice ripples/ridges: a cylinder climbs a step of height s if drag*... (step ratio s/R)
for s in (0.05, 0.10, 0.20, 0.40):
    R = 0.8
    # buoyant cylinder pressed up against an inverted step: to pass it must be pushed DOWN by s; needs Fd > B*g*tan(theta)
    th = math.acos(1 - s/R)
    F = B*9.81*math.tan(th)
    vneed = math.sqrt(F/(0.5*rw*1.0*1.6*9.0))
    print(f"  inverted step (ice keel) {s*100:.0f} cm: needs drag {F:.0f} N -> v {vneed:.2f} m/s")

# cost per tonne delivered vs best practice
print("\ncost per t delivered, 700 km:")
truck = (2*700/30*55 + 2*700*0.4*0.95)/25    # $55/h truck+driver, 0.4 L/km diesel, 25 t payload, empty return
print(f" winter-road truck (cost model, 30 km/h, empty back-haul): ${truck:.0f}/t  (= ${truck/700:.3f}/t-km)")
barge = 700*0.03 + 6     # $0.03/t-km summer barge + transshipment; + winter stockpile carry $3-6/t
print(f" summer barge + winter stockpile: ~${barge:.0f}-{barge+6:.0f}/t  (assumed 0.03 $/t-km; NOTES)")
for name, snow in (("coal", 0.43), ("rock ore", 1.1)):
    make = snow*1.5 + 1.0           # snow compaction/handling $1.5/m3, wrap+spray-freeze shell $1/t
    slot = 2.0                      # launch + receive slots, cranes, guide boom, per t at 144 kt/season
    loss = 0.05*(60 if name == "coal" else 150)/0.95
    print(f" pods ({name}): make ${make:.1f} + slots ${slot:.1f} + 5% loss ${loss:.1f} = ${make+slot+loss:.1f}/t  (only IF velocity >= 0.3-0.5 m/s all the way)")
