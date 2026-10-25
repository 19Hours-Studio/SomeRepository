from common import *
# Group full cost per t Ni-eq (order of magnitude). 2024 output from memory of Nornickel release: CHECK
out = dict(Ni=205.6e3, Cu=433e3, Pd=2767e3, Pt=664e3)   # t, t, oz, oz
for lab,p in (('base',P),('hi',P_hi)):
    rev = out['Ni']*p['Ni']+out['Cu']*p['Cu']+out['Pd']*p['Pd']+out['Pt']*p['Pt']
    nieq = rev/p['Ni']
    opex=5.1e9; capex=opex*0.37/0.63
    print(lab, f"Ni-eq {nieq/1e3:.0f} kt; gross {rev/1e9:.1f} bn$; full cost {(opex+capex)/nieq:,.0f} $/t Ni-eq; capex share 37% => {capex/1e9:.2f} bn$; PGM share of value {(out['Pd']*p['Pd']+out['Pt']*p['Pt'])/rev:.0%}")
print()
for k,o in ORES.items():
    for lab,p in (('base',P),('hi',P_hi)):
        v=value_per_t(o,p); tot=sum(v.values())
        print(f"{k:22s} {lab}: {tot:6.0f} $/t in situ; Ni-eq {o['Ni']*0+tot/p['Ni']*100:.2f}% ; PGM share {(v['Pd']+v['Pt'])/tot:.0%}; Ni share {v['Ni']/tot:.0%}")
