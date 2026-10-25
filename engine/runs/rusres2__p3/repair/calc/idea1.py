from common import *
import itertools
# ---- Recoveries (Nornickel AR2020 via search: NOF Ni 71.9/71.3/70.6% 2018-20, TOF 83.2->87.9%) ----
# Cu/PGM recoveries ASSUMED (no source found): NOF Cu 80, PGM 75 ; TOF Cu 92, PGM 85
REC_NOF = dict(Ni=0.71, Cu=0.80, PGM=0.75)
REC_TOF = dict(Ni=0.85, Cu=0.92, PGM=0.85)
PAY = 0.80   # payable/smelter-refinery recovery on concentrate value (assumed)
r = 0.12     # real discount (key rate 14%, F229)

def nieq_rec(ore, rec, mt, p=P):
    return nieq_t(sum(value_per_t(ORES[ore],p,rec).values()))*mt*1e6*PAY   # t Ni-eq/yr

def run(capex_tof3_bn, uplift_frac, nof_cap, life_ext_bn, newconc_bn, defer_yrs, p=P, verbose=False):
    # TOF-3 adds 7.8 Mtpa (10.2->18, smart-lab/TOF plan). NOF currently treats Talnakh cuprous+dissem (moved) + Norilsk-1.
    moved = min(5.0, nof_cap-1.5)    # Mtpa of Talnakh ore moved NOF->TOF (assumed; NOF also has ~1.5-3 Mtpa Norilsk-1 now)
    new_talnakh = 7.8 - moved        # extra Talnakh mine output TOF-3 absorbs
    # recovery uplift on moved ore: only part of the TOF-NOF gap is plant-related (rest is ore type, F362)
    rec_moved_tof = {k: REC_NOF[k]+uplift_frac*(REC_TOF[k]-REC_NOF[k]) for k in REC_NOF}
    d_uplift = nieq_rec('Talnakh_proven(F1)', rec_moved_tof, moved,p) - nieq_rec('Talnakh_proven(F1)', REC_NOF, moved,p)
    d_newtal = nieq_rec('Talnakh_proven(F1)', rec_moved_tof, new_talnakh,p)
    # refill freed NOF: Norilsk-1 up to 7 Mtpa total (F360: +4 Mtpa vs ~3 now), rest Maslovskoye
    n1 = min(moved, 4.0); masl = moved-n1
    d_n1 = nieq_rec('Norilsk1_dissem(F2)', REC_NOF, n1,p)
    d_ma = nieq_rec('Maslovskoye(F7)', REC_NOF, masl,p)
    # capex: TOF-3 + NOF life extension ; credit = PV of deferring new 18 Mtpa dissem. concentrator by defer_yrs
    defer_credit = newconc_bn*(1-1/(1+r)**defer_yrs)
    alone = d_uplift + d_newtal
    pair  = alone + d_n1 + d_ma
    capex_alone = capex_tof3_bn
    capex_pair  = capex_tof3_bn + life_ext_bn - defer_credit
    if verbose:
        print(f" moved {moved:.1f} Mtpa, new Talnakh {new_talnakh:.1f}, N1 refill {n1:.1f}, Masl {masl:.1f}")
        print(f" dNi-eq kt/yr: uplift {d_uplift/1e3:.1f}, new Talnakh {d_newtal/1e3:.1f}, N1 {d_n1/1e3:.1f}, Masl {d_ma/1e3:.1f}")
        print(f" alone {alone/1e3:.1f} kt/yr for {capex_alone:.0f} bnRUB -> {capex_alone*1e9/alone/1e3:.0f}k RUB per annual t Ni-eq")
        print(f" pair  {pair/1e3:.1f} kt/yr for {capex_pair:.0f} bnRUB (defer credit {defer_credit:.0f}) -> {capex_pair*1e9/pair/1e3:.0f}k RUB per annual t Ni-eq")
    return capex_alone*1e9/alone, capex_pair*1e9/pair, alone, pair

print("BASE CASE")
a,pp,_,_ = run(capex_tof3_bn=100, uplift_frac=0.5, nof_cap=8.5, life_ext_bn=25, newconc_bn=150, defer_yrs=8, verbose=True)
# The fair comparison: pair vs Nornickel plan (TOF-3 + new 18 Mtpa dissem concentrator, NOF retired).
# Nornickel plan delivers same ore flows but pays new conc now; pair pays life-ext and defers.
print()
print("SENSITIVITY: ratio (pair capex/t) vs (TOF-3 + new concentrator now)/t, same ore output")
res=[]
for cap,uf,nof,le,nc,dy in itertools.product([70,100,130],[0.25,0.5,0.75],[7.5,8.5,10],[15,25,40],[110,150,190],[5,8,12]):
    a,pp,alone,pair = run(cap,uf,nof,le,nc,dy)
    plan = (cap+nc)*1e9/pair          # Nornickel plan: same output, builds new conc now (NOF retired)
    res.append((pp/plan, a/pp, cap,uf,nof,le,nc,dy))
import statistics as st
rs=[x[0] for x in res]; ra=[x[1] for x in res]
print(f" pair/plan capex per t Ni-eq: min {min(rs):.2f} median {st.median(rs):.2f} max {max(rs):.2f}")
print(f" alone/pair capex per t Ni-eq: min {min(ra):.2f} median {st.median(ra):.2f} max {max(ra):.2f}")
# full-cost effect: per t Ni-eq of group (~789 kt, $10.26k/t, capex 37%)
_,_,alone,pair = run(100,0.5,8.5,25,150,8)
print(f" pair adds {pair/789e3:.1%} to group Ni-eq")
