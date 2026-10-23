# Idea 3: pre-loaded barge winters in a backwater and leaves on the flood crest.
# Round 1 (kill test): Kolyma main stem, crest helps only the first trip -> barge leg -17%. Reproduce:
trips=6; full=2200; part=0.5*full
base=trips*part; crest=full+(trips-1)*part
print(f"Kolyma main stem: t/season per barge {base:.0f} -> {crest:.0f}; barge-leg cost/t x{base/crest:.2f}")
# Round 2: move the anchor to a river where the flood is the ONLY window: small tributary navigable only on spring high water.
# Model: depth at limiting riffle h(t) = h_low + (h_crest-h_low)*exp(-t/tau) after the crest (t days after ice clears).
import math
h_low=0.6; h_crest=3.0; tau=12.0   # m, m, days (assumption: typical small-river snowmelt recession, Yakutia)
draft_full=2.2; draft_empty=0.6     # 2,000 t class river barge (assumption ~ project 942/R-56 type)
def load_frac(h):  # linear draft-load
    return max(0.0,min(1.0,(h-0.2-draft_empty)/(draft_full-draft_empty)))
for delay in (0,5,10,15,20):  # days between tributary ice-out and arrival of convoy from the main-river base
    # convoy must pass the riffle on the way IN (loaded) at t=delay+transit_in
    transit=3
    h=h_low+(h_crest-h_low)*math.exp(-(delay+transit)/tau)
    print(f" arrival delay {delay:2d} d: riffle depth {h:.2f} m, load {load_frac(h):.0%}")
# Pre-loaded wintering at the tributary mouth: delay=0 -> full. Current practice: barges from base wait for main-river ice-out
# + loading + transit (main-river ice-out at the base is often 5-15 d later than tributary ice-out in the south-to-north Lena system;
# assumption, the deciding hydrograph data are below in NOTES).
# Cost per tonne delivered on the tributary leg (rub): one trip/season either way
tow=0.4e6*8   # pusher days per tributary round trip (assumption 0.4 M rub/day)
barge_ann=3e6 # old 2000 t barge ownership + upkeep per year (scrap-value hull ~300 t steel)
for f_now in (0.25,0.4,0.6):
    now=(tow+barge_ann)/(full*f_now)
    pre=(tow+barge_ann+0.6e6)/(full*1.0)   # +0.6 M rub wintering watch / ice cutting / insurance for loaded hull
    print(f" current load {f_now:.0%}: {now:.0f} rub/t vs pre-loaded {pre:.0f} rub/t -> x{now/pre:.1f}")
# Baseline: winter road to the same village: 20-40 rub/t-km over 150-400 km + winter-road upkeep
for km,r in ((150,25),(400,35)):
    print(f" winter road {km} km at {r} rub/tkm = {km*r:.0f} rub/t")
# Consistency: loaded hull frozen in. Backwater depth needed >= loaded draft + 0.3 m keel clearance at autumn low water
print(f"backwater depth required at freeze-up >= {draft_full+0.3:.1f} m; ice 1.5-2.0 m grows around hull (hull must be rated for it, same as any wintering barge)")
