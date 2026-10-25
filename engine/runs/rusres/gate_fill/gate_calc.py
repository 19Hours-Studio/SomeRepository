import sys; sys.path.insert(0, '/home/user/SomeRepository/engine')
from kit import econ, geotech, stats, data
P = print
# sanity checks of kit on known answers
P('check ceiling 0.05 ->', round(econ.ceiling_ratio(0.05),3), '| breakeven(74.6,2500) ->', round(econ.breakeven_loss_fraction(74.6,2500),3))

P('\n=== IDEA 1: XRT pre-concentration, Norilsk disseminated ore ===')
# Class 10 recovery: allowed loss vs 3% claim. Value per t ore (disseminated Norilsk-1, F2): 0.25% Ni, 0.33% Cu, 4.56 g/t PGM
ni, cu, pgm = data.get('price.nickel_lme'), 12000, 1300/31.1035  # $/t, $/t, $/g (PGM basket ~ $1,300/oz est.)
val = 0.0025*ni + 0.0033*cu + 4.56*pgm*0.8
P('in-situ value $/t disseminated ore ~', round(val))
# saving per t ore from rejecting fraction f of mass (processing cost avoided ~ $15/t est.; sorter cost ~ $1.5/t)
proc, sortc = 15.0, 1.5
# Selebi XRT (2025, NexMetals): 15.2% mass rejected at ~2% metal loss -> use as best measured Ni-sulphide analogue
f, loss = 0.152, 0.02
save = f*proc - sortc
P('net processing saving $/t ore', round(save,2), 'metal lost $/t', round(loss*val,2))
P('margin (saving / lost value) =', round(save/(loss*val),2))
# Concentrator capacity value: Talnakh concentrator expanding 10 -> 18 Mtpa anyway (Nornickel/techinsider) -> idea only defers that capex.
# Disseminated share of Norilsk reserves: Norilsk-1 disseminated 32 Mt of 1,203 Mt (F1,F2)
sh = 32/1203; P('disseminated share of reserves', round(sh,3))
# Chain: processing share 11% (ledger B). Upper bound: remove f of processing on disseminated ore, plus capital deferral
r1 = econ.ceiling_ratio(0.11*f*1.0)   # even if applied to ALL ore
P('chain ratio upper bound (all ore, 15% of processing share removed) =', round(r1,3))
P('gate', econ.gate_verdict(save/(loss*val), r1))

P('\n=== IDEA 2: re-levelling jack foundations ===')
# Class 4/12 thaw settlement over life vs jack stroke; ground allowed to thaw.
# Yamal tabular ice 10-20 m near surface (F97); thaw strain 0.2 (kit default, ice-rich 0.1-0.4)
# Thaw under heated/unventilated footing: allow 3 m extra thaw over design life (conservative)
for dz, eps in [(1.0,0.2),(3.0,0.2),(3.0,0.4)]:
    s = geotech.thaw_settlement(dz, eps); P(f'thaw {dz} m strain {eps}: settlement {s:.2f} m, stroke margin {0.3/s:.2f}')
# seasonal movement 60-180 mm (F101) vs 300 mm stroke
P('seasonal stroke margin', round(0.3/0.18,2))
# Chain: foundations/upkeep. Hjort 2022: Russian road upkeep loss $7bn over 2020-50 (F270) -> per year
P('road upkeep loss per year $bn', round(7/30,2))
# Infrastructure foundation repair ~ <=2% of Norilsk full cost ($8bn/yr ledger B) est.; baseline already adjustable foundations (Alaska/Nunavut guidance)
r2 = econ.ceiling_ratio(0.02); P('chain ratio ceiling (remove 2% share fully)', round(r2,3))
P('gate', econ.gate_verdict(0.3/0.6, r2))

P('\n=== IDEA 3: powered-first Baimskaya 5-8 Mtpa on Lomonosov ===')
# Available: Lomonosov 76 MW to shore, 44 MW in max-heat mode (Rosatom via korabel/goarctic);
# node consumption 377 GWh in 2022 (Chukotka scheme 2023-27); Lomonosov covers 84% after Bilibino shut Dec 2025 (m-atom)
node_avg = 377e6/8760/1e3
on_fnpp = 0.84*node_avg
P('node avg MW', round(node_avg,1), 'on FNPP MW', round(on_fnpp,1))
spare_summer, spare_winter = 76-on_fnpp, 44-on_fnpp
P('spare summer', round(spare_summer,1), 'spare winter (heat mode)', round(spare_winter,1))
# Required: idea 30 MW; check: 8 Mtpa * 25 kWh/t / 8760 h
req_idea = 8e6*25/8760/1e3
# realistic porphyry site 35-40 kWh/t (est. from KAZ 60-70 Mtpa served by 3 x 106 MW working FNPP units (Rosatom) -> 318 MW*8760*0.9/70Mt)
kwh_t = 3*106e3*8760*0.9/70e6
req_real = 8e6*kwh_t/8760/1e3*1.0
P('kWh/t implied by Baimskaya power plan', round(kwh_t,1), 'req idea MW', round(req_idea,1), 'req at implied', round(req_real,1))
P('MARGIN winter vs idea 30 MW', round(spare_winter/30,2), '| summer', round(spare_summer/30,2), '| winter vs implied', round(spare_winter/req_real,2))
# Chain cost per t Cu: full project ledger D ~ $6,500/t (capital $2,900 + opex 3,600)
capex_full, mt_full = 8e9, 60
mt = 6.5
capex_ph1 = econ.six_tenths_scaling(capex_full, mt_full, mt) if True else None
P('phase-1 capex $bn (six-tenths)', round(capex_ph1/1e9,2))
cu_t = mt*1e6*0.0043*0.88
cap_per_t = capex_ph1*data.get('price.capital_charge_ledger')/cu_t
opex_per_t = 3600*(mt_full/mt)**0.2   # mild diseconomy of opex, est.
new = cap_per_t+opex_per_t
P('Cu t/yr', round(cu_t), 'capital $/t', round(cap_per_t), 'total $/t', round(new))
r3 = econ.ratio_vs_baseline(6500, new); P('RATIO', round(r3,2))
# even with no opex penalty
P('RATIO no opex penalty', round(econ.ratio_vs_baseline(6500, cap_per_t+3600),2))
P('gate', econ.gate_verdict(spare_winter/30, r3))

P('\n=== IDEA 4: crusher-conveyor underground haulage, Talnakh ===')
# Idea's own claim: full cost -3..-6% -> ratio
P('ratio at claimed 3-6%:', round(1/(1-0.03),3), round(1/(1-0.06),3))
# Ceiling: underground haulage share of Norilsk full cost. Energy share 6% (ledger B); haulage ~30% of mine diesel est. -> energy part
# plus labour 27% * haulage crews ~10% est.
share = 0.06*0.3 + 0.27*0.10 + 0.11*0.10
P('haulage share est.', round(share,3), 'ceiling', round(econ.ceiling_ratio(share),3))
# Pilot provability (class 13): to show belt availability >=90% failure per shift <10% with zero failures
P('trials for zero failure at 5%', stats.trials_for_zero_failure(0.05))
P('gate', econ.gate_verdict(1.0, econ.ceiling_ratio(share)))
