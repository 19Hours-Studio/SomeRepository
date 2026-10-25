import sys; sys.path.insert(0,'/home/user/SomeRepository/engine')
from kit import econ
crf=econ.crf(0.10,20); print('crf',round(crf,4))
# --- measured winter shuttle (Bellona Jan-Apr 2026: 1.0 Mt total; DM shuttling from late Dec 2025, Kosygin first load 28 Jan)
cargo=0.0775  # Mt per 172.6k m3 cargo
n=1.0/cargo; hulldays=120+(30-28+28+31+30)  # DM Jan-Apr + Kosygin 28 Jan-30 Apr
cyc=hulldays/n; print('cargoes',round(n,1),'hull-days',hulldays,'cycle d',round(cyc,1),'margin vs 14 d',round(14/cyc,2))
# Idea 1 claim with 4 hulls: Jan-Jul shuttle + Aug-Oct open water at design + Nov-Dec shuttle
def shuttle(h,days): return h*days/cyc*cargo
for h in (2,3,4):
    ice=shuttle(h,212+61); ow=13.2*92/365
    print('hulls',h,'shuttle Mt',round(ice,2),'open-water at design Mt',round(ow,2),'total',round(ice+ow,2))
# hull availability winter 2027: Kosygin + de Margerie delivered; Stolypin 'preparing for handover' Sep 2026
print('hull margin (3 available/4 needed)',0.75)
# chain: capital 21bn annuitised; non-capital = 970-620 = 350 $/t (ledger B)
cap=21e9*crf; other=350
def cost(mt): return cap/(mt*1e6)+other
base=cost(5.7)   # Kpler 2026 forecast with the shuttle already in use
print('baseline 2026 $/t',round(base),'idea1 same hulls ~5.7-6 Mt',round(cost(6.0)), 'ratio',round(econ.ratio_vs_baseline(base,cost(6.0)),2))
# Idea 3: Train 3 deferral; Novatek already postponed T3 (Reuters Jun 2026) -> baseline already defers
t3=7e9*crf; print('T3 annuity $bn/yr',round(t3/1e9,2),'per t at 5.7Mt',round(t3/5.7e6))
print('idea3 ratio if baseline did NOT defer (upper bound)',round(econ.ratio_vs_baseline(base,base-t3/5.7e6),2),'; vs actual practice (already deferred) 1.00')
print('Zvezda rate: required 2/yr; available ~1/yr (1 hull Dec 2025, Stolypin not handed over by Sep 2026) margin',0.5)
# Idea 2: southbound spare capacity and refinery absorption
spare=25-14.8; surplus=30-3*2.1
print('Vankor-Purpe spare Mt/y',spare,'surplus to move',round(surplus,1),'pipe margin',round(spare/surplus,2))
print('refinery absorption: runs -13.5% y/y, crude forced to export -> spare domestic crude demand ~0 Mt/y, margin ~0')
for m,r in ((0.0,1.0),(0.0,1.0),(0.5,1.0),(0.0,1.0)): print(econ.gate_verdict(m,r))
