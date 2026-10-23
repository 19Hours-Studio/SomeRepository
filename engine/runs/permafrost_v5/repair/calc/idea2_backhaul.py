# Idea 2: pairing opposite flows on the Kolyma in the same hulls.
# Flows (sources in NOTES): coal down from Zyryanka 160-175 kt/yr (2019-20 actual, nedradv/uk42);
# upstream to Zyryanka/Srednekolymsk: fuel ~17 kt (13 kt = 3/4 of plan, 2025, portnews/marine.org.ru), dry goods: small (Yakutopttorg 'Freyer' >50 t/season; big dry-cargo ships can't enter since 2019)
coal=165e3; fuel_up=17e3; dry_up=3e3   # dry_up = assumption (order of magnitude, few kt)
print(f"Original direction (coal down on empty upbound dry-cargo returns): max share of coal = {dry_up/coal:.1%}")
# Repaired direction: fuel UP in ISO tank containers on the empty upbound leg of the coal fleet
cap_barge=1000     # t per coal barge trip at shoal-limited load (<50% of ~2000-2200 t, kill tests)
coal_trips=coal/cap_barge
print(f"coal barge trips/season ~{coal_trips:.0f}; upbound empty capacity ~{coal_trips*cap_barge/1e3:.0f} kt vs fuel {fuel_up/1e3:.0f} kt -> fits in {fuel_up/cap_barge:.0f} upbound legs ({fuel_up/coal:.0%} of legs)")
# Tank containers: 24 m3 T11 ~ 20 t diesel; ~$15-20k each new; round-trip Chersky-Zyryanka ~ 2.5-3 weeks -> 4 cycles/season (May 23-Oct 10 ~ 140 d)
usd=80; tc_cost=18e3*usd; tc_t=20; cycles=4
n_tc=fuel_up/tc_t/cycles
capex=n_tc*tc_cost; ann=capex*0.15   # 10 yr, 8% + upkeep
lift=2*400   # rub/t: lift on at Chersky (from sea tanker via hose to tank container on barge, or crane) and off/decant at destination (assumption)
marg_tow=0.10   # extra tow fuel for loaded vs empty upbound leg: fraction of the leg's tow cost
print(f"tank containers needed {n_tc:.0f}, capex {capex/1e6:.0f} M rub, annual {ann/1e6:.0f} M rub -> {ann/fuel_up:.0f} rub/t; handling {lift} rub/t")
# Baseline A: dedicated river tanker (current). Cost of tanker leg per t: ship-day cost x days / payload.
# Old tanker (38-54 yr, FACT 2) day cost (crew 10, fuel, upkeep): ~0.6-1.0 M rub/day (assumption); round trip 18 d; payload limited by shoals ~600-1000 t
for day,payload in ((0.6e6,1000),(1.0e6,600)):
    tank=day*18/payload
    # backhaul: pay marginal tow on coal convoy (pusher day ~0.5 M rub, 8 days upbound, marginal 10%) spread over upbound load
    marg=0.5e6*8*marg_tow/cap_barge
    alt=ann/fuel_up+lift+marg
    print(f" tanker {day/1e6} M/day, {payload} t: {tank:.0f} rub/t vs backhaul {alt:.0f} rub/t -> ratio {tank/alt:.1f}")
# Baseline B (cheapest real alternative): replace old tankers with new shallow tanker -> capital ~ (FACT 6 barge $3M/5000 t) x3 for tanker+self-propulsion
new_tanker=3*3e6*usd*(1000/5000)*1.0   # 1000 t tanker
print(f" new 1000 t shallow tanker approx {new_tanker/1e6:.0f} M rub -> annual {new_tanker*0.13/1e6:.0f} M rub -> {new_tanker*0.13/(1000*7):.0f} rub/t capital alone at 7 trips/season")

print("\n--- Round 3: bladders (pillow tanks) in the coal hold, hold = secondary containment; revised tanker day-cost ---")
bl_m3=50; bl_t=42; bl_cost=8e3*usd; life=3
n_bl=fuel_up/bl_t/cycles; ann_bl=n_bl*bl_cost*(1/life+0.05)
pump=400; marg=0.5e6*5*marg_tow/(fuel_up/ (fuel_up/cap_barge))   # 5 upbound days, marginal 10% of pusher day cost per loaded leg
alt=ann_bl/fuel_up+pump+marg
print(f"bladders {n_bl:.0f}, annual {ann_bl/1e6:.1f} M rub -> {ann_bl/fuel_up:.0f} rub/t; pump {pump}; marginal tow {marg:.0f}; total {alt:.0f} rub/t")
# Revised dedicated-tanker baseline: crew 10x200k/month=67k/d, fuel 3 t/d x 100k rub/t = 300k/d, upkeep/insurance ~50-200k/d -> 0.3-0.6 M rub/d; RT Chersky-Zyryanka ~ 870 km each way, 9-12 d incl. ops
for day,rt,payload in ((0.3e6,9,1000),(0.45e6,10,800),(0.6e6,12,600)):
    tank=day*rt/payload
    print(f" tanker {day/1e6} M/d x {rt} d / {payload} t = {tank:.0f} rub/t  -> ratio vs bladder backhaul {tank/alt:.1f}")
# Consistency: bladder fuel mass vs barge shoal-limited load (1000 t): one leg can take ~ 1000/42 = 23 bladders
print(f"bladders per barge at shoal-limited 1000 t: {1000/bl_t:.0f}; legs needed {fuel_up/1000:.0f} of ~{coal_trips:.0f} upbound legs")
