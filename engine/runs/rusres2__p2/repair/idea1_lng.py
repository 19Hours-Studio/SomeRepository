# Idea 1 "Swing trains to hull-days" - repaired model. All $ real 2026.
import math
def crf(r,n): return r*(1+r)**n/((1+r)**n-1)
CRF=crf(0.12,25)                      # 12% real, 25 y -> 0.1275 (assumption; key rate 14% nominal, FACT 229)
MMBTU_T=52.0                          # MMBtu per t LNG
P_ASIA=10.0*MMBTU_T                   # $10/MMBtu Asia 2027 (assumption) -> $520/t
CARGO_LOAD=172600*0.45/1000           # kt per Arc7 cargo (172,600 m3, FACT 140; 0.45 t/m3)
CARGO_DEL=CARGO_LOAD*0.97             # ~3% boil-off/heel over a long voyage
LIQ_OPEX=1.2*MMBTU_T                  # feed gas + liquefaction opex $/t (assumption, ~$1.2/MMBtu)
# ---- hull costs
def hull_day(capex,opex_d): return capex*CRF/365+opex_d
ARC7_RU=hull_day(400e6,30e3)          # Zvezda Arc7: $400M (assumed, Yamal DSME ~$320M +25%)
CONV=90e3+30e3                        # conventional 174k m3 TC for Russia trade $90k/d + fuel $30k/d (assumption)
ICE_FEE=5.0                           # NSR/icebreaker fees $/t (assumption)
# ---- cycles (days) from facts
CYC_SHUTTLE_W=(14.0,16.4)             # Utrenneye-Ura/Kildin winter (FACT 364, 359)
CYC_SHUTTLE_S=9.0                     # summer, open Kara (calc: ~1,250 nm @14 kn x2 + 2 d port)
CYC_NSR_DES=2*20+2                    # Asian leg 19-21 d via NSR (FACT 308)
CYC_SUEZ_DES=2*35+2                   # 35 d via Suez (FACT 308)
CYC_CONV_ONWARD=2*30+2                # Kildin->China via Suez ~30 d one way
NSR_DAYS=150                          # Arc7 NSR east season Jul-late Nov (FACT 308)
WINTER=365-NSR_DAYS
print(f"CRF={CRF:.4f}  cargo={CARGO_LOAD:.1f} kt  Arc7(RU) ${ARC7_RU/1e3:.0f}k/d")

def per_hull_DES():
    c=NSR_DAYS/CYC_NSR_DES + WINTER/CYC_SUEZ_DES
    return c, c*CARGO_DEL/1000
c,mt=per_hull_DES()
print(f"Arc7 DES-only: {c:.1f} cargoes/hull-yr = {mt:.2f} Mt/hull-yr")
for cw in CYC_SHUTTLE_W:
    cs=WINTER/cw+NSR_DAYS/CYC_SHUTTLE_S
    print(f"Arc7 ice-leg shuttle (winter {cw} d): {cs:.1f} cargoes = {cs*CARGO_LOAD/1000:.2f} Mt/hull-yr  ratio vs DES {cs/c:.1f}x")

# ================= ARCTIC LNG 2 (US SDN) - compliant regime: Russian-built hulls DES only, no onward hull
print("\n== Arctic LNG 2, compliant (DES on Zvezda Arc7 only) ==")
CAPEX_AL2_BUILT=21e9*0.75             # T1+T2+2 GBS share of $21bn (FACT 48/209) - assumption 75%
disc=(0.30,0.40)                      # FACT 209
for N in (2,4,6,10,15,21):
    mt=N*per_hull_DES()[1]
    ship_t=ARC7_RU*365/(mt*1e6/N)
    suez=0.6e6*2*(WINTER/CYC_SUEZ_DES)*N/(mt*1e6)  # ~$0.6M per transit
    marg=LIQ_OPEX+ship_t+ICE_FEE+suez
    full=marg+CAPEX_AL2_BUILT*CRF/(mt*1e6)
    util=mt/13.2
    pr=[P_ASIA*(1-d) for d in disc]
    print(f"N={N:2d}: {mt:4.1f} Mt/y util T1-2 {util:4.0%}  ship ${ship_t:4.0f}/t marginal ${marg:4.0f}/t full ${full:5.0f}/t  realised ${pr[1]:.0f}-{pr[0]:.0f}/t")
# breakeven hulls on full cost at 35% discount
pr=P_ASIA*0.65
for N in range(1,80):
    mt=N*per_hull_DES()[1]; ship_t=ARC7_RU*365*N/(mt*1e6)
    full=LIQ_OPEX+ship_t+ICE_FEE+20+CAPEX_AL2_BUILT*CRF/(mt*1e6)
    if full<pr: print(f"full-cost breakeven DES-only: N={N} Zvezda Arc7 (= {mt:.1f} Mt/y)"); break
# train duty if only T1 runs: campaign factor
for N in (2,4,6):
    mt=N*per_hull_DES()[1]; print(f"  N={N}: T1 duty factor {mt/6.6:.0%} -> T2 and T3 hardware free as spares")
# storage check: GBS tank (assume 2x114.5k m3 per GBS) vs 6.6 Mt/y production
prod_m3_d=6.6e6/365/0.45; tank=229e3
print(f"  T1 fills 229k m3 in {tank/prod_m3_d:.1f} d -> must ramp down when no hull within ~{tank/prod_m3_d:.0f} d")

# ================= YAMAL LNG after 1 Jan 2027 (EU ban, no Zeebrugge) - anchor applied
print("\n== Yamal LNG post-2027 ==")
PROD=19.7; CAPEX_Y=27e9; ARC7_Y=hull_day(320e6,30e3)   # existing DSME Arc7 (built capacity)
prod_w=PROD*WINTER/365; prod_s=PROD-prod_w
car_w=prod_w*1e3/CARGO_LOAD; car_s=prod_s*1e3/CARGO_LOAD
print(f"winter {prod_w:.1f} Mt = {car_w:.0f} cargoes; summer {prod_s:.1f} Mt = {car_s:.0f} cargoes")
# Y0: DES only with 15 Arc7
cap_w=15*WINTER/CYC_SUEZ_DES; cap_s=15*NSR_DAYS/CYC_NSR_DES
del_Y0=(min(cap_w,car_w)+min(cap_s,car_s))*CARGO_DEL/1000
print(f"Y0 Arc7 DES-only: winter cap {cap_w:.0f} car, summer cap {cap_s:.0f} car -> {del_Y0:.1f} Mt/y ({del_Y0/PROD:.0%})")
# Y1: anchor - winter Kildin STS shuttle, summer: Arc7 NSR DES east + shuttle remainder
for cw in CYC_SHUTTLE_W:
    hulls_w=car_w*cw/WINTER
    hulls_left=15-hulls_w
    # summer: Arc7 DES east first; remainder shuttled (9 d)
    des_s=min(car_s,15*NSR_DAYS/CYC_NSR_DES)
    rem=car_s-des_s
    hulls_s=des_s*CYC_NSR_DES/NSR_DAYS+rem*CYC_SHUTTLE_S/NSR_DAYS
    onward=(car_w+rem)*CYC_CONV_ONWARD/365
    print(f"Y1 winter cyc {cw}: Arc7 needed winter {hulls_w:.1f}/15 (spare {hulls_left:.1f}); summer {hulls_s:.1f}; onward conventional ~{onward:.0f} hull-equiv yr-round")
    # cost per t delivered
    sh_w=ARC7_Y*cw/(CARGO_LOAD*1e3); on=CONV*CYC_CONV_ONWARD/(CARGO_DEL*1e3)+1.2e6/(CARGO_DEL*1e3)
    sts=3.0
    win=sh_w+sts+on+ICE_FEE
    des=ARC7_Y*CYC_SUEZ_DES/(CARGO_DEL*1e3)+1.2e6/(CARGO_DEL*1e3)+ICE_FEE
    print(f"   winter logistics $/t: shuttle+STS+onward {win:.0f}  vs Arc7 DES via Suez {des:.0f}")
cap_charge=CAPEX_Y*CRF
for d_mt,lab in ((PROD,"Y1 full"),(del_Y0,"Y0 DES-only"),(prod_s,"summer-only")):
    print(f"   {lab}: plant capital ${cap_charge/(d_mt*1e6):.0f}/t over {d_mt:.1f} Mt")
for dsc in (0.05,0.15):
    print(f"   realised at {dsc:.0%} discount ${P_ASIA*(1-dsc):.0f}/t")

# ---- summer fleet allocation for Yamal (fix): x NSR-DES + y shuttle, 15 hulls x 150 d
x=(15*NSR_DAYS-104*CYC_SHUTTLE_S)/(CYC_NSR_DES-CYC_SHUTTLE_S)
print(f"\nYamal summer: max {x:.0f} NSR-DES cargoes east + {104-x:.0f} shuttled; fits 15 hulls")
# open-water option at berth: non-ice hulls at Sabetta ~90 d (Aug-Oct; Ob fast ice to ~July FACT 117)
print(f"non-ice hulls at berth in 90 d window could take {90*PROD/365:.1f} Mt directly (frees Arc7 for DES east)")
# sensitivity: conventional onward rate $60-130k/d
for tc in (60e3,90e3,130e3):
    on=(tc+30e3)*CYC_CONV_ONWARD/(CARGO_DEL*1e3)+1.2e6/(CARGO_DEL*1e3)
    print(f"onward TC ${tc/1e3:.0f}k/d -> onward ${on:.0f}/t; chain winter ${on+ARC7_Y*15/(CARGO_LOAD*1e3)+3+ICE_FEE:.0f}/t")
# full cost Yamal Y1 vs price
full_Y1=LIQ_OPEX+cap_charge/(PROD*1e6)+150
print(f"Yamal Y1 full cost ~${full_Y1:.0f}/t vs realised $442-494/t")
full_Y0=LIQ_OPEX+cap_charge/(del_Y0*1e6)+130
print(f"Yamal Y0 (DES only, trains turned down) full ~${full_Y0:.0f}/t on {del_Y0:.1f} Mt")
