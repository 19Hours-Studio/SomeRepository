"""Idea 4 - Night-sky lithium freeze cascade. All estimates in code.
Sources (see LOG.md):
 [A] CaCl2-H2O eutectic ~ -49.8 to -51 C at ~29.9 wt% CaCl2; CaCl2.6H2O liquidus 37.3 % at 0 C (standard phase diagram,
     e.g. Smith College petrology H2O-CaCl2 page).
 [B] Siberian Platform Ca-chloride brines 170-631 g/L TDS, Li up to 600 mg/L (Gornyi Zhurnal 2012 no.2, rudmet 9081);
     average LiCl ~2.5 g/L with high Ca/Mg (Bull. TPU 2004 307(7)).
 [C] Ternary LiCl-CaCl2-H2O has a double salt LiCl.CaCl2.5H2O field (J. Chem. Eng. Data 2019, 10.1021/acs.jced.8b00777).
 [D] Udachny January mean -39.4 C (Wikipedia climate table); Mirny ~ -30 C.
 [E] Brine DLE cost $3.4-6.2 per kg LCE (Argonne techno-economic overview, TechConnect 2026).
 [F] Polar regions have the lowest net radiative-cooling capacity on Earth (arXiv 2410.04109); typical clear-sky
     temperate night ~100 W/m2.
ASSUME flags mark assumptions.
"""
import math
h, c, kB, sig = 6.626e-34, 2.998e8, 1.381e-23, 5.670e-8

def planck_band(T, l1, l2, n=2000):
    tot = 0.0
    dl = (l2 - l1) / n
    for i in range(n):
        l = l1 + (i + 0.5) * dl
        tot += 2 * math.pi * h * c**2 / l**5 / (math.exp(h * c / (l * kB * T)) - 1) * dl
    return tot

print("== Round 1: how much can a sky-facing film radiate at -50 C? ==")
for Tc in (20, -30, -40, -50, -55):
    T = Tc + 273.15
    bb = sig * T**4
    win = planck_band(T, 8e-6, 13e-6)
    print(f"T={Tc:>4} C: blackbody {bb:6.1f} W/m2, 8-13 um band {win:5.1f} W/m2 ({100*win/bb:4.1f}%)")

def net_cooling(Ts, Tair, tau_win=0.85, dT_inv=8.0, h_conv=3.0, eps=0.95):
    """Selective film (emits only 8-13 um). Window sky radiance from a layer at Tair+dT_inv with emissivity (1-tau).
    Returns net cooling power (W/m2) available for latent load at film temperature Ts."""
    Tatm = Tair + dT_inv
    out = eps * planck_band(Ts, 8e-6, 13e-6)
    back = eps * (1 - tau_win) * planck_band(Tatm, 8e-6, 13e-6)
    conv = h_conv * (Tair - Ts)
    return out - back - conv

print("\n== Round 1b: net cooling at film -52 C (just below eutectic) vs air temperature ==")
for Tair in (-35, -40, -45, -50, -55):
    Ts = -52 + 273.15
    for h_c in (2.0, 4.0):
        q = net_cooling(Ts, Tair + 273.15, h_conv=h_c)
        print(f"air {Tair}: h_conv={h_c}: net latent removal at -52 C = {q:6.1f} W/m2")
# stagnation depression at zero load
for Tair in (-40,):
    lo, hi = Tair - 40, Tair
    for _ in range(60):
        mid = (lo + hi) / 2
        if net_cooling(mid + 273.15, Tair + 273.15) > 0: hi = mid
        else: lo = mid
    print(f"zero-load stagnation at air {Tair} C: film {hi:.1f} C (depression {Tair-hi:.1f} K)")

print("\n== Round 2: freeze load and season capacity at Udachny ==")
# hourly air temperature over Dec-Feb: normal around monthly means, SD 7 K (ASSUME), clear-sky fraction 0.7 ASSUME
months = [(-35.0, 31), (-39.4, 31), (-36.0, 28)]  # Dec ~, Jan [D], Feb ~ ASSUME
sd, clear = 7.0, 0.7
L_eut = 220e3  # J/kg of eutectic solid (ice+CaCl2.6H2O) near -50 C ASSUME (ice 334 at 0 C, lower at -50 C)
f_solid = 0.93  # fraction of brine mass that must solidify beyond the eutectic ASSUME
load_per_kg = f_solid * L_eut + 2.6e3 * 10  # + 10 K sub-ambient sensible
E_m2 = 0.0
hours_ok = 0.0
for mean, days in months:
    for k in range(-40, 41):
        Tair = mean + sd * k / 10.0
        p = math.exp(-0.5 * (k / 10.0) ** 2) / (math.sqrt(2 * math.pi)) * 0.1
        q_rad = net_cooling(-52 + 273.15, Tair + 273.15) * clear
        # when air is colder than -52 C, wind (h~12) helps; shield removed
        if Tair < -52:
            q = 12.0 * (-52 - Tair) + max(q_rad, 0)
        else:
            q = max(q_rad, 0.0)
        if q > 0:
            E_m2 += q * 3600 * 24 * days * p
            hours_ok += 24 * days * p
print(f"hours/yr with net freezing possible at -52 C: {hours_ok:.0f}; seasonal latent removal {E_m2/1e6:.1f} MJ/m2")
kg_brine_m2 = E_m2 / load_per_kg
print(f"load {load_per_kg/1e3:.0f} kJ/kg brine -> {kg_brine_m2:.0f} kg brine frozen per m2 per winter")
Li = 0.4  # g/L [B] (rich Siberian brine)
rho_b = 1.35
lce_per_m3 = Li * 5.323 / 1000  # t LCE per m3 at 100 % recovery
brine_t_per_tLCE = rho_b / lce_per_m3
area_per_tLCE = brine_t_per_tLCE * 1000 / kg_brine_m2
print(f"brine per t LCE: {brine_t_per_tLCE:.0f} t; tray area per (t LCE/yr): {area_per_tLCE:,.0f} m2")
cost_m2 = 25.0  # $/m2 tray+insulation+film+IR windshield, ASSUME (film alone ~3-10 $/m2)
ann = cost_m2 * 0.15 + 1.0
print(f"tray cost {cost_m2} $/m2, annualised {ann:.2f} $/m2/yr -> {area_per_tLCE*ann:,.0f} $/t LCE vs whole DLE route $3,400-6,200/t LCE [E]")

print("\n== Round 3: repair A - let the wind do the work on the few coldest nights, film only as add-on ==")
print("(already included above for air < -52 C; result is dominated by hours below -52 C)")
print("\n== Round 3b: repair B - choose brine closer to the eutectic so the sub-ambient part is smaller? ==")
print("No: whatever the starting CaCl2, the large Li concentration happens only when ~90+% of the mass solidifies AT the eutectic;")
for w0 in (0.20, 0.30, 0.38):
    # above eutectic with air at -40 C, the liquid can only move to ~31 % (hexahydrate side) or ~28 % (ice side)
    if w0 > 0.30:
        f_cr = (w0 - 0.31) / (0.5065 - 0.31)
    else:
        f_cr = 1 - w0 / 0.28 if w0 < 0.28 else 0.0
    print(f"  CaCl2 {w0*100:.0f}%: free ambient (-40 C) concentration factor for Li = {1/(1-f_cr):.2f}x")

print("\n== Round 4: niche - same trays on Ca-free DLE eluate (LiCl only, eutectic -75 C): ambient air suffices ==")
eluate_Li = 1.0   # g/L Li in sorbent eluate ASSUME (0.5-2 g/L typical for Li-Al LDH sorbents)
licl0 = eluate_Li * 6.11 / 1000  # wt fraction approx
licl_at_m40 = 0.185  # ASSUME LiCl-H2O liquidus ~18-19 wt% at -40 C
cf = licl_at_m40 / licl0
ice_per_tLCE = (1 - 1 / cf) * (1 / (eluate_Li * 5.323 / 1000))
print(f"eluate {eluate_Li} g/L -> CF {cf:.0f}x at -40 C; ice to freeze {ice_per_tLCE:.0f} t per t LCE (vs {brine_t_per_tLCE:.0f} t brine to solidify in the CaCl2 route)")
E_ambient = 15.0 * 10 * 3600 * 24 * 90 * 0.5  # h=15 W/m2K, 10 K below air for half of 90 days ASSUME (open tray/spray)
area2 = ice_per_tLCE * 1000 * 334e3 / E_ambient
print(f"open-air freezing capacity {E_ambient/1e6:.0f} MJ/m2/winter -> {area2:,.0f} m2 per (t LCE/yr) -> {area2*ann:,.0f} $/t LCE")
