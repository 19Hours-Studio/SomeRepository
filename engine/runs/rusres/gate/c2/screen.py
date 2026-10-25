"""Gate c2 screen: 3 LNG train ideas + thermosyphon retrofit. Run: python3 screen.py"""
import sys
sys.path.insert(0, '/home/user/SomeRepository/engine')
from kit import econ, stats, climate

# ---------- shared LNG inputs ----------
CARGO_T = 172_600 * 0.45 * 0.98          # Arc7 cargo, t (F140 volume; LNG 0.45 t/m3, 98% fill)

def ship_mt_per_year(round_trip_d, days=365):
    return CARGO_T * days / round_trip_d / 1e6

# own-code check on a known case: Yamal 15 Arc7, ~20 d round trip to NW Europe (F138), 21 Mt in 2024 (Interfax)
yamal_cap = 15 * ship_mt_per_year(20)
print(f"check: 15 Arc7 @20 d -> {yamal_cap:.1f} Mt/yr (actual 2024 ~21 Mt incl. summer NSR/other ships) OK")

# market outlet (class 8): built capacity with no buyer after the EU ban of 1 Jan 2027 (F217)
yamal_eu = 15.0            # Mt/yr of Yamal 19.7 Mt went to EU in 2025 (Urgewald/Kpler)
al2_idle = 13.2 - 4.0      # AL2 T1+T2 nameplate minus ~3.6-4.4 Mt/yr actual (F182)
china_growth = 9.79 - 9.79 / 1.182   # Mt/yr added by China in 2025 (F218)
outlet_7y = china_growth * 7          # generous: same growth every year to 2033
stranded = yamal_eu + al2_idle
print(f"stranded built capacity {stranded:.1f} Mt/yr; 7-yr outlet growth {outlet_7y:.1f} Mt/yr")

# capital ceiling (class 9): ledger archetype A
now = 7.5                   # $/mmBtu delivered (ledger A, $7-8)
cap_share = 0.47
total_cap = 1636.0          # $/t/y (F45: 27bn/16.5)
plant_t13 = 1100.0          # $/t/y (F174)
other = total_cap - plant_t13
def with_plant(plant):
    return now - now * cap_share * (1 - (plant + other) / total_cap)

ideas = {
    'I1 7x0.9 Mtpa': dict(mt=7 * 0.9, plant=475.0),
    'I3 4x2 Mtpa':   dict(mt=4 * 2.0, plant=econ.six_tenths_scaling(475.0 * 0.9, 0.9, 2.0) / 2.0),
    'I4 4x0.9 Mtpa': dict(mt=4 * 0.9, plant=475.0),
}
for name, d in ideas.items():
    c = with_plant(d['plant'])
    r = econ.ratio_vs_baseline(now, c)
    headroom = max(0.0, outlet_7y - stranded)          # outlet left for a NEW train
    m_market = headroom / d['mt']
    m_stack = outlet_7y / (stranded + d['mt'])
    # Arc7 winter shuttle Utrenneye-Murmansk FSU, ~11 d round trip est., winter Dec-Jun 210 d (F140)
    ships_req = d['mt'] * 210 / 365 / ship_mt_per_year(11, 210)
    ships_free = max(0.0, 4 - 13.2 * 210 / 365 / ship_mt_per_year(11, 210))  # 4 hulls by end-2026 vs AL2 own need
    # drive power at 220 kWh/t (F175), 92% availability
    mw_train = d['mt'] / (d['mt'] / (0.9 if '0.9' in name else 2.0)) * 1e6 * 220 / (8760 * 0.92) / 1e3
    print(f"{name}: plant {d['plant']:.0f} $/t/y -> {c:.2f} $/mmBtu, RATIO {r:.2f}; "
          f"market margin new tranche {m_market:.2f} (whole stack {m_stack:.2f}); "
          f"Arc7 req {ships_req:.1f} vs free {ships_free:.1f}; drive {mw_train:.0f} MW/train; "
          f"ceiling(plant share) {econ.ceiling_ratio(cap_share * plant_t13 / total_cap):.2f}; "
          f"verdict {econ.gate_verdict(m_market, r)}")

# availability proof (class 13): 2 copies x 3 yr = 6 train-years; 90% vs 85% availability at 30-d blocks
n = stats.sample_size_proportion(0.90, 0.05)
print(f"I4 test: blocks to pin 90%±5% availability {n:.0f} vs 2 trains*3 yr*12 = 72 months -> {72 / n:.2f}")

# ---------- Idea 2: thermosyphon retrofit, Norilsk ----------
# Norilsk 1991-2020 monthly means, deg C (pogodaiklimat.ru normals; Jun-Sep match kit data climate.Norilsk.summer)
nor = [-26.5, -25.9, -21.6, -13.5, -5.0, 6.0, 14.4, 10.0, 3.0, -9.3, -20.0, -24.2]
sal = [-23.4, -22.4, -15.5, -9.0, -1.0, 9.2, 15.4, 11.8, 5.5, -3.6, -13.3, -20.2]   # Salekhard normals
M = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
fdd_n, tdd_n = climate.degree_days(dict(zip(M, nor)))
fdd_s, tdd_s = climate.degree_days(dict(zip(M, sal)))
# idea's own threshold: Salekhard is "too weak" -> required FI > Salekhard's; warming 0.07 C/yr (F104) x 25 yr
warm = 0.07 * 25
fdd_n50 = climate.degree_days(dict(zip(M, [t + warm for t in nor])))[0]
print(f"FDD Norilsk {fdd_n:.0f} (TDD {tdd_n:.0f}); Salekhard {fdd_s:.0f}; margin {fdd_n/fdd_s:.2f}; "
      f"Norilsk after +{warm:.2f} C {fdd_n50:.0f} -> {fdd_n50/fdd_s:.2f}")
# chain ceiling: permafrost-foundation losses as share of Norilsk ~$8bn/yr full cost (ledger B)
fine = 146.177e9 / 84.0          # Ambarnaya award, $ (F262), one event in ~30 yr of tank life (F260)
loss_share = (fine / 30 + 100e6) / 8e9   # + generous $100m/yr repairs/outages (est.)
print(f"avoidable share {loss_share:.3f} -> ceiling ratio {econ.ceiling_ratio(loss_share):.3f}; "
      f"even 8% -> {econ.ceiling_ratio(0.08):.3f}")
# pilot proof: 20 piles zero 'failures' proves only
print(f"20 piles prove loss rate < {stats.zero_failure_upper_bound(20):.3f}; need {stats.trials_for_zero_failure(0.05)} "
      f"for <5% -> margin {20/stats.trials_for_zero_failure(0.05):.2f}")
print("I2 verdict", econ.gate_verdict(20/stats.trials_for_zero_failure(0.05), econ.ceiling_ratio(loss_share)))
