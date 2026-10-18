"""IDEA 4 - Shipyard-built floating mine plants frozen into a dug pond. Anchor: the plant floats in a pond dug at site,
so the talik its heat makes is irrelevant (no piles/thermosyphons).
Sources: F1 Moma (Kenmare): floating wet concentrator plants 3,000-3,500 t/h in dredge pond; WCP relocated (Hatch);
F2 Sevmorolovo used accommodation ship 'Petrodvorets' (goarctic.ru) - floating camp in the Arctic is precedent;
F3 K: Akademik Lomonosov floating NPP at Pevek (2019-20); Soviet 'Severnoye Siyanie' floating power plants in Siberia;
F4 AIME 1958: mill foundations 20-50% of structure cost (clay/permafrost); F5 K: White Sea-Baltic canal locks
135 x 14.3 m, ~4 m depth; freezing index Yakutia 5,500-6,500 C*day; Stefan ice 0.027 m/sqrt(C*d) snow-free;
F6 idea: capital charge 41-42% of delivered cost."""
import math
print("=== 4a. Pond ice & depth ===")
for FI in (4500, 6000, 7000):
    for a in (0.020, 0.027):
        print(f"FI {FI} C*d, coef {a}: max ice {a*math.sqrt(FI):.2f} m")
draft = 3.0
print(f"pond depth needed: draft {draft} + ice 2.2 + 0.8 keel margin = {draft+2.2+0.8:.1f} m (bottom always in liquid water -> talik)")
print("\n=== 4b. Keep a 2 m open moat round each hull with waste heat (avoid ice pressure/adfreeze) ===")
L, B, n = 130, 14, 5
perim = 2*(L+B)*n
for q in (300, 550):
    P = perim*2*q
    print(f"moat 2 m x {perim} m, {q} W/m2 -> {P/1e6:.2f} MW (power house 30 MWe rejects ~35-40 MW) ; with bubbler+cover ~1/4")
print("thermal ice pressure if frozen in: 150-300 kN/m (dam-design range, K) -> river ice-class hull side OK, moat optional")
print("\n=== 4c. Talik / bank retreat vs bedrock-founded mills ===")
for yrs in (5, 10, 20):
    talik = 0.9*math.sqrt(yrs*365)/10  # crude Stefan-type thaw bulb ~ 1.7 m after 1 yr scaling (K, lake taliks)
    print(f"{yrs:2d} yr: talik depth below pond ~{talik*5.6:.0f} m (ice-rich ground subsides; hull indifferent); "
          f"bank retreat at 0.5-2 m/yr -> {0.5*yrs:.0f}-{2*yrs:.0f} m -> mills need >= {2*yrs+10:.0f} m setback or bedrock edge")
print("\n=== 4d. Capex model, 2 Mtpa riverside/coastal concentrator (all $M) ===")
capex_conv = 500.0
split = dict(equipment=0.33, bulks=0.17, site_labour=0.30, foundations=0.10, indirects=0.10)
for k, v in split.items(): print(f"  {k:12s} {v*capex_conv:6.0f}")
def floating(f_float=0.6, yard_labour_ratio=0.4, hulls=5, hull_cost=10.0, tow=2.0, pond=3.0, link=8.0):
    eq = split['equipment']*capex_conv; bulks = split['bulks']*capex_conv
    lab = split['site_labour']*capex_conv; fnd = split['foundations']*capex_conv; ind = split['indirects']*capex_conv
    lab_new = lab*(1-f_float) + lab*f_float*yard_labour_ratio
    fnd_new = fnd*(1-f_float)
    extra = hulls*(hull_cost+tow) + pond + link
    return eq+bulks+lab_new+fnd_new+ind*0.9+extra
def modular(f_mod=0.6, yard_labour_ratio=0.45, module_set=0.03):
    eq = split['equipment']*capex_conv; bulks = split['bulks']*capex_conv
    lab = split['site_labour']*capex_conv; fnd = split['foundations']*capex_conv; ind = split['indirects']*capex_conv
    lab_new = lab*(1-f_mod) + lab*f_mod*yard_labour_ratio
    return eq+bulks+lab_new+fnd+ind*0.95+module_set*capex_conv
cf, cm = floating(), modular()
print(f"stick-built Far North {capex_conv:.0f}; modular-on-piles (best current) {cm:.0f}; floating-in-pond {cf:.0f}")
print(f"floating vs stick-built {100*(1-cf/capex_conv):.0f}% ; vs modular {100*(1-cf/cm):.0f}%")
print("\n=== 4e. Delivered cost per unit, incl. re-float and re-use (short-life deposits) ===")
cap_share = 0.415
for life, resid in ((15, 0.0), (7, 0.0), (7, 0.45)):
    def charge(capex, residual):
        r = 0.12; crf = r/(1-(1+r)**-life)
        return (capex - residual*capex/(1+r)**life)*crf
    base = charge(cm, 0.0)    # modular-on-piles: residual ~0
    flo = charge(cf, resid*0.6)  # 60% of capex is floating/re-usable
    # normalise: capital = 41.5% of delivered cost for the 15-yr modular case
    k = cap_share/(1-cap_share)
    ref = charge(cm, 0.0) if life == 15 else base
    opex = ref/k
    print(f"life {life:2d} yr, residual {resid:.2f}: delivered cost floating/modular = {(flo+opex)/(base+opex):.3f}")
print("\n=== 4f. Transport window check ===")
disp = 130*14*3.0*0.9
print(f"hull 130x14 m, draft 3.0 m: displacement {disp:.0f} t; lightship ~2,000 t -> payload ~{disp-2000:.0f} t; "
      f"5 hulls carry ~{5*(disp-2000)/1e3:.0f} kt topsides (flotation, thickeners, power, camp; mills on bedrock)")
