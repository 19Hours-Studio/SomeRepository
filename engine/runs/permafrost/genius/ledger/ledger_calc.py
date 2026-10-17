"""Value-ledger arithmetic for five remote Siberian/Yakutian/Arctic resource archetypes (Oct 2026).

S = sourced anchor (see SOURCES in final answer); E = estimate / engineering assumption.
All money in 2026 USD unless stated. FX 84 RUB/USD (CBR early Oct 2026: 83.2-85.5) [S].
Categories: energy (fuel/power at commodity price), labour (wages+social+FIFO travel+camp),
inbound logistics (freight on fuel, reagents, spares, food), outbound logistics (product),
processing (mining+plant consumables, spares, maintenance, smelter/tolling charges),
capital (annuity on initial capex incl. remoteness premium + sustaining), other (royalty/MET, taxes, G&A).
"""

FX = 84.0          # RUB per USD [S]
G_OZ = 31.1035

def crf(r, n):
    """capital recovery factor (annuity)"""
    return r * (1 + r) ** n / ((1 + r) ** n - 1)

def report(name, items, unit, price=None):
    tot = sum(items.values())
    print(f"\n=== {name}: delivered cost {tot:,.0f} {unit}" + (f"  (price {price:,.0f})" if price else ""))
    for k, v in items.items():
        print(f"  {k:<10} {v:>10,.1f}  {100 * v / tot:5.1f}%")
    big = max(items, key=items.get)
    print(f"  LARGEST: {big} {100 * items[big] / tot:.1f}% -> 10x cut removes {90 * items[big] / tot:.1f}%")
    return tot

# ---------------- cross-cutting -----------------
diesel_exch_rub_l = 77177 * 0.84 / 1000        # exchange summer diesel 77,177 rub/t (15 Jun 2026) [S], density 0.84
diesel_site_rub_l = 125.0                     # remote site delivered (Yakutia retail avg 122.99 rub/l 12 Oct 2026 [S]; site 120-150 [E])
print(f"diesel exchange ~{diesel_exch_rub_l:.0f} rub/l; site {diesel_site_rub_l:.0f} rub/l = ${diesel_site_rub_l / FX:.2f}/l; "
      f"logistics+margin share {(1 - diesel_exch_rub_l / diesel_site_rub_l) * 100:.0f}%")
dg_rub_kwh = 0.27 * 130 + 6                   # 0.27 l/kWh genset [E] x 130 rub/l + O&M/capex 6 rub/kWh [E]
print(f"mine-scale diesel power ~{dg_rub_kwh:.0f} rub/kWh = ${dg_rub_kwh / FX:.2f}/kWh")
lorp = 10.1e9 / 1.257e6                        # LORP 2025 revenue / tonnes [S]
print(f"LORP average revenue {lorp:,.0f} rub/t = ${lorp / FX:.0f}/t")
fifo = 240e3 * 12 * 1.30 + 6 * 70e3 + 182 * 4500 + 1e5   # wage 240k/mo [S: Chukotka 261k, Magadan 214k May-2026], social ~30%, 6 flights, 182 camp days [E]
print(f"FIFO fully-loaded {fifo / 1e6:.1f} M rub = ${fifo / FX / 1e3:.0f}k per worker-year")
print(f"Baimskaya capital intensity: company ${8.5e9 / 300e3:,.0f}/t-yr; whole programme (1.1 trn rub) ${1.1e12 / FX / 300e3:,.0f}/t-yr; "
      f"global avg $22,359 (S&P Dec 2025)")
print(f"Gold MET at $4,150: 6% = ${0.06 * 4150:.0f}/oz + surcharge 10% x (4150-1900) = ${0.10 * 2250:.0f}/oz")

# ---------------- A. placer gold (Magadan/Yakutia/Chukotka), RUB per gram -----------------
# anchors: Susumanzoloto RAS 2025 revenue 59.3 bn, cost of sales 34.6 bn, S&A ~2.5 bn [S]; output ~6.0 t [E from revenue/price]
susu_2025 = (34.573e9 + 2.5e9) / 6.0e6
print(f"\nSusumanzoloto 2025 cost ~{susu_2025:,.0f} rub/g = ${susu_2025 * G_OZ / 81:,.0f}/oz at 81 rub/$")
price_g = 4150 * FX / G_OZ
met = 0.06 * price_g + 0.10 * (4150 - 1900) * FX / G_OZ
L_PER_G = 11.0                                   # diesel litres per gram (stripping ratio ~4-5, sands ~0.5 g/m3) [E]
A = {
    "energy":   L_PER_G * diesel_exch_rub_l,
    "labour":   1400,          # ~8,000 placer workers in Magadan for ~16 t [S], ~2.7 M rub per seasonal worker [E]
    "inbound":  L_PER_G * (diesel_site_rub_l - diesel_exch_rub_l) + 150,
    "outbound": 15,            # gold escort/insurance to refinery [E]
    "process":  1400,          # fleet spares, tyres, repairs, contractors, washing plants, refining [E]
    "capital":  1000,          # fleet & plant replacement, camp, exploration, licence auctions [E]
    "other":    met + 255,     # MET 6% + 10% of price above $1,900/oz [S], property/land/eco/reclamation fund [E]
}
tA = report("A placer gold (rub/g)", A, "rub/g", price_g)
print(f"  = ${tA * G_OZ / FX:,.0f}/oz vs price $4,150/oz; MET {met:,.0f} rub/g")

# ---------------- B. Baimskaya-type Cu-Au concentrate, USD per year -> per t Cu -----------------
cu_t = 300e3                                     # first-10-yr Cu [S BFS]; Au 490 koz [S]
ore, moved = 70e6, 70e6 * 1.8                    # 70 Mt/yr ore [S], strip 0.8 [S]
conc_t = 1.4e6                                   # concentrate t/yr [S]
diesel_l = moved * 0.45                          # l/t moved [E]
power_kwh = 251e3 * 8760 * 0.92                  # 251 MW demand [S]
fnpp = 6.45 * 1.51 / FX                          # 6.45 rub/kWh 2020 prices [S] x CPI 2020-26 ~1.51 [E]
B = {
    "energy":   power_kwh * fnpp + diesel_l * diesel_exch_rub_l / FX,
    "labour":   4500 * fifo / FX,                # ~4,500 FIFO on payroll (3-6k jobs quoted) [S/E]
    "inbound":  diesel_l * (130 - diesel_exch_rub_l) / FX + 150e3 * 250,   # fuel freight + 150 kt reagents/spares at ~$250/t (NSR+428 km road) [E]
    "outbound": conc_t * (428 * 0.07 + 8 + 45),  # road $0.07/t-km, port $8, NSR to China $45/t [E]
    "process":  moved * 1.0 + ore * 3.2 + conc_t * 20,  # mining maint/tyres/explosives, plant consumables+maint, TC/RC ~$0 benchmark [S] + $20/t Russian discount [E]
    "capital":  8.5e9 * crf(0.10, 25) + 120e6,   # BFS capex $8.5bn [S], 10% real, 25 yr, sustaining $120m [E]
    "other":    0.06 * cu_t * 13980 * 0.965 + 60e6 + 60e6,  # Cu MET ~6% avg (8% less TOR/Arctic relief) [E], property tax, G&A [E]
}
B = {k: v / cu_t for k, v in B.items()}
tB = report("B Cu concentrate CIF China (USD/t Cu, gross of Au)", B, "$/t Cu", 13980)
au_credit = 490e3 * 4150 * (1 - 0.114) / cu_t
print(f"  gold credit net of Au MET ${au_credit:,.0f}/t Cu -> net cost ${tB - au_credit:,.0f}/t Cu")
print(f"  site opex per t ore ${(tB - B['capital'] - B['other'] + 120e6 / cu_t) * cu_t / ore:.1f}")

# ---------------- C. coal -----------------
# C1 export: Elga/Neryungri washed coal, RZD ~2,000 km -> Vanino/Vostochny, USD per t FOB
C1 = {
    "energy":   4.5,      # fuel ~20-35% of open-pit coal cost [S], commodity part [E]
    "labour":   8.0,      # [E]
    "inbound":  3.5,      # fuel & spares freight [E]
    "outbound": 46.0,     # RZD tariff+wagons ~2,000 km ~$35 + port ~$11 [E]; RZD = 61% of FOB on Kuzbass hauls [S]
    "process":  9.0,      # spares, tyres, explosives, wash plant [E]
    "capital":  9.0,      # mine + wash plant annuity [E]
    "other":    3.0,      # coal MET small, export duty zero since 1 Jan 2025 [S]
}
tC1 = report("C1 Yakutian export coal FOB (USD/t)", C1, "$/t", 106)
priv = 100e9 * crf(0.10, 25) / FX / 30e6 + 8.0   # Elga private railway+port 100 bn rub for 30 Mt/yr [S] + O&M $8/t [E]
print(f"  own 531-km railway+port: ~${priv:.0f}/t vs RZD route ~$46/t")
# C2 settlement coal: pit-head share 12/79 of delivered (Momsky district: coal 79% of heat cost, purchase price 12%) [S]
pit = 3500.0                                     # rub/t pit-head 2026 [E]
deliv = pit * 79 / 12
print(f"\nC2 settlement coal: pit-head {pit:,.0f} rub/t -> delivered {deliv:,.0f} rub/t = ${deliv / FX:,.0f}/t; "
      f"logistics share {100 * (1 - 12 / 79):.0f}%")
C2 = {"energy": 0.03, "labour": 0.04, "inbound": 0.015, "outbound": 1 - 12 / 79,
      "process": 0.03, "capital": 0.022, "other": 0.015}
C2 = {k: v * deliv / FX for k, v in C2.items()}
report("C2 Arctic settlement coal at boiler (USD/t)", C2, "$/t")

# ---------------- D. lithium: Kolmozerskoye-type spodumene -> LiOH/Li2CO3, USD/t LCE -----------------
lce = 45e3                                       # t/yr [S]; ore 1.96 Mt/yr [S]
ore_d, moved_d = 1.96e6, 1.96e6 * 7              # strip 6 [E]
dsl = moved_d * 0.5                              # l diesel [E]
D = {
    "energy":   (dsl * diesel_exch_rub_l / FX + ore_d * 25 * 0.08) / lce + 715,   # mining diesel, mill power, calcination+evaporation ~45 GJ + 2.5 MWh/t [E]
    "labour":   1300 * 50e3 / lce,               # [E]
    "inbound":  (dsl * (130 - diesel_exch_rub_l) / FX) / lce + 325,  # reagents ~5.5 t/t LCE by rail/road [E]
    "outbound": 150,                             # LCE to China/Russian gigafactory [E]
    "process":  (moved_d * 1.0 + ore_d * 5.0) / lce + 970 + 300,      # mining & mill consumables, acid/soda/lime, plant maint [E]
    "capital":  (91e9 + 40e9) / FX * crf(0.10, 20) / lce + 200,      # capex 91 bn rub + 40 bn rub road [S], sustaining [E]
    "other":    790 + 400,                       # MET ~4% of product value, property tax, G&A [E]
}
report("D spodumene LCE (USD/t LCE)", D, "$/t LCE", 19750)
tolling = 17000 / 7.1
print(f"  China tolling benchmark CNY 17,000/t = ${tolling:,.0f}/t [S]; Kokorin brine 17,000 m3/d x 0.276 kg Li/m3 = "
      f"{17000 * 0.276 * 365 * 5.323 / 1000:,.0f} t LCE/yr at 100% recovery")

# ---------------- E. stranded oil: 0.2 Mt/yr East-Siberian field, 300 km trucking to ESPO, FOB Kozmino, USD/bbl -----------------
bbl_t = 7.3
espo_tariff = 3373 * 1.058 * 1.051 / FX / bbl_t   # 2024 ESPO network tariff [S] x 2025/2026 indexation [S]
truck = 300 * 20 / FX / bbl_t                     # 20 rub/t-km winter road [S]
prod_bbl = 0.2e6 * bbl_t
capex_rub = 8e9                                   # wells, EPF, tank farm, camp [E]
E = {
    "energy":   1.0,
    "labour":   120 * fifo / FX / prod_bbl,
    "inbound":  1.5,
    "outbound": truck + espo_tariff + 0.5,
    "process":  4.0,
    "capital":  capex_rub / FX * crf(0.12, 12) / prod_bbl,
}
pre_tax = sum(E.values())
met_ndd = 25.0 + 0.5 * (100 - (pre_tax - E["capital"]) - 25.0 - E["capital"])   # MET under NDD ~$25 [E] + NDD 50% [E]
E["other"] = met_ndd
report("E stranded oil FOB Kozmino (USD/bbl)", E, "$/bbl", 100)
print(f"  trucking ${truck:.1f}/bbl, ESPO tariff ${espo_tariff:.1f}/bbl; full MET Sep-2026 38,312 rub/t = "
      f"${38312 / FX / bbl_t:.0f}/bbl [S]")
