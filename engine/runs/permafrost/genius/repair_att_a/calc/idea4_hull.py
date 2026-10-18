import math
# relay timing
for season in (100,120,150):
    print(f"season {season} d: relays per spare at 12/17/22-d round trip = {season//12}/{season//17}/{season//22}")
# draft limit: B1500 barge 75x17.2 m, draft 1.8 m, 1500 t [S: Nibulon V1500]; light draft ~0.45 m [E]
L,B = 75,17.2
for depth in (1.2,1.5,1.8):
    cap = min(1500,(depth-0.15-0.45)*L*B*1.0*0.85)
    print(f"guaranteed depth {depth} m -> usable load {cap:.0f} t")
# hold thermal: deck 1290 m2 U=0.5 W/m2K insulated hatch, coal +2C, air -40C; freeboard sides ~ coal-insulated
q_deck = L*B*0.5*42/1e3; q_moat = 2*(L+B)*0.3*1.0   # kW; 0.3 m heated slot around hull at ~1 kW/m2 [E]
boiler_avg = 2500*20e9/(240*86400)/1e6   # MW average for 2,500 t/yr over 240-d season, 20 GJ/t [E]
print(f"hold heat {q_deck:.0f} kW + moat slot {q_moat:.0f} kW vs boiler avg {boiler_avg:.1f} MW -> {100*(q_deck+q_moat)/1e3/boiler_avg:.1f}% (flue-gas waste heat suffices)")
# buoyancy change frozen-in: 1,500 t unload -> line load on ice; semi-infinite plate edge moment 0.3224 P/beta
E,h,nu = 5e9,1.5,0.33; D = E*h**3/(12*(1-nu**2)); l = (D/9810)**0.25; beta = 1/(math.sqrt(2)*l)
P = 1500e3*9.81/(2*(L+B)); M = 0.3224*P/beta; Mcap = 0.6e6*h*h/6
print(f"frozen-in uplift line load {P/1e3:.0f} kN/m -> ice moment {M/1e3:.0f} vs capacity {Mcap/1e3:.0f} kNm/m -> ice ring cracks: keep heated moat slot (above)")
# flue gas as inert: coal boiler excess air -> O2 6-9% [E] vs SOLAS inert gas <=5% delivered/<=8% in tank [E]
# sealed hold: air ingress only = withdrawn volume
V_in = 1500/0.85; O2 = V_in*0.21*1.43; heat = O2*13e6   # 13 MJ/kg O2 coal oxidation [E]
print(f"sealed hold: ingress air {V_in:.0f} m3 -> O2 {O2:.0f} kg -> oxidation heat {heat/1e9:.1f} GJ/winter = {heat/(240*86400):.1f} W avg -> self-heating negligible if hold sealed")
# flue-gas moisture: ~8 vol% H2O, dew ~40C; must be cooled/dried to ~0C (0.6 vol%) before blanketing or it frosts the coal [E]
# --- per-tonne economics
delivered = (7100, 11600)    # rub/t from idea3 baseline range (central mine + river)
savings_lo = 300+150+300+0.05*delivered[0]; savings_hi = 600+300+800+0.15*delivered[1]
print(f"avoided: transshipment 300-600, stockpile rehandle 150-300, trucking 300-800, losses 5-15% -> {savings_lo:,.0f}-{savings_hi:,.0f} rub/t")
Q = 2500  # t/yr per village
for label, hull_cost, occupy_frac in (("R1 N+1 relay, used hull, year-round occupancy", 25e6, 1.0),
                                      ("R1 N+1 relay, new B1500-class hull", 200e6, 1.0),
                                      ("R2 winter-idle hull (last voyage winters at village)", 25e6, 0.15)):
    hulls = math.ceil(Q/1300)   # draft-limited ~1,300 t per hull
    ann_hull = hulls*hull_cost*0.15*occupy_frac + hulls*1.5e6
    site = (12e6 + 10e6 + 10e6)*0.12   # sheltered basin dredging, dolphins, 150 m screw/conveyor gallery to bank boiler [E]
    print(f"{label:55s}: {hulls} hull(s) -> {(ann_hull+site)/Q:,.0f} rub/t vs savings {savings_lo:,.0f}-{savings_hi:,.0f}")
# heat main instead of bank boiler next to berth: 0.5-1 km at 40 M rub/km [E]
print(f"if boiler not at bank: heat main adds {0.75*40e6*0.12/Q:,.0f} rub/t")
