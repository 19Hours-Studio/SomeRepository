"""IDEA 3 - Barge augers for terrace placers. Anchor: auger-bore the frozen paystreak horizontally from a river barge,
leaving the frozen overburden in place as roof.
Sources: A1 auger mining: holes 1-2 m dia, 90-150 m (to 200 m), up to 60,000 t/month (Australian comparison, coal);
A2 Mae Tan: recovery 24-35% for webs 0.5-1.5 m, short safe lengths (coal); A3 RD 06-326-99 (Gosgortekhnadzor) underground
mining of permafrost placers by room-and-pillar - frozen-roof principle already standard; A4 Mining Journal 09/2016
cutter-combines selected for frozen gravel-pebble placers (mechanical cutting of frozen gravel exists);
K: frozen sandy gravel UCS ~5-8 MPa at -4 C, long-term ~1/3-1/4 (Tsytovich); frozen ground unit weight 20 kN/m3;
Russian placer grades 0.5-1 g/m3 open-pit, underground-mined 2-5 g/m3 (K); dozer stripping $1/m3 (calc_idea2)."""
import math
print("=== 3a. Geometric extraction & bedrock-contact capture ===")
for D, w in ((1.8, 0.5), (1.8, 0.8), (2.0, 0.6)):
    R = D/2
    seam_frac = math.pi*R*R/(D*(D+w))     # of a seam of height D
    for hc in (R, 0.5, 0.3):              # hole centre height above bedrock
        chord = 2*math.sqrt(max(R*R-hc*hc, 0))
        print(f"D {D} web {w}: seam extraction {seam_frac:.2f}; centre {hc:.2f} m above bedrock -> bedrock contact swept {chord/(D+w):.2f}, "
              f"bedrock dilution depth {max(R-hc,0):.2f} m")
print("\n=== 3b. Web pillar stress vs frozen gravel strength ===")
for H in (10, 20, 35):
    for D, w in ((1.8, 0.5), (1.8, 0.8)):
        s = 0.020*H*(D+w)/w
        print(f"cover {H} m, D {D} web {w}: pillar stress {s:.2f} MPa vs short-term UCS 5-8 / long-term 1.5-2 MPa (-4 C)")
print("\n=== 3c. Rate & cost per m3 pay and per g Au ===")
coal_m3_month = 60000/1.3
for fac, season_d, crew_yr in ((0.35, 130, 26), (0.5, 130, 26), (0.5, 280, 40)):
    vol = coal_m3_month*fac*season_d/30
    capex = 16e6; cap = capex*0.15
    om = 0.08*capex; crew = crew_yr*75e3; power = 1.5e3*24*season_d*0.6*0.27*1.2  # kW*h*load*l/kWh*$/l
    wear = 3.0*vol; heat = 0.4e6 if season_d > 200 else 0
    tot = cap+om+crew+power+wear+heat
    print(f"cut rate {fac:.2f} x coal, {season_d} d: {vol/1e3:5.0f} k m3/season, ${tot/1e6:4.1f}M -> ${tot/vol:5.1f}/m3 hole")
print("\n=== 3d. Best-practice baselines, $/m3 of pay sands and $/g recovered ===")
def per_g(cost_m3, grade, extraction, rec=0.85):
    return cost_m3/(grade*extraction*rec)
pay = 2.0
for H in (10, 15, 20, 30, 40):
    SR = H/pay
    op_thaw = SR*1.0 + 4.0        # natural thaw + dozer (only practical if thaw seasons allow) + sands mining/washing
    op_frozen = SR*3.5 + 4.0      # drill/blast + excavator-truck
    print(f"cover {H:2d} m (SR {SR:4.1f}): open pit thaw-doze ${op_thaw:5.1f}/m3, frozen D&B ${op_frozen:5.1f}/m3 pay; "
          f"thaw lead time ~{H/1.6:.0f} seasons for natural layer thaw")
for grade in (1.0, 3.0):
    print(f"-- grade {grade} g/m3 --")
    for name, c, ex in (("open pit H=15 thaw-doze", 15*0.5+4, 0.95), ("open pit H=30 frozen D&B", 15*3.5+4, 0.95),
                        ("underground drift (D&B, rooms) K est.", 60.0, 0.80),
                        ("auger barge open-water only", 90.0, 0.60), ("auger barge year-round frozen-in", 55.0, 0.60)):
        print(f"   {name:38s} ${c:5.1f}/m3 -> ${per_g(c, grade, ex):6.1f}/g Au")
