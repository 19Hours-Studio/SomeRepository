# Combine client levers with an operator-side read price set from op_cost.py (read real cost ~2-3% of
# recompute when KV is parked in DRAM/NVMe during the inter-turn gap -> price reads at 0.03x instead of 0.1x,
# keeping the same margin multiple as base input). Also: fractional batching from a real SWE-agent demo
# trajectory (11 actions -> 6 requests when independent/ordered-safe actions are issued together; k~1.8).
import levers, statistics as st
def run(R, **kw):
    levers.R=R
    r=[levers.session(s,**kw) for s in range(200)]
    return st.mean(x[0] for x in r)+st.mean(x[1] for x in r), st.mean(x[0] for x in r)
base_tot, base_in = run(0.10)
print(f"baseline (in-place, k=1, R=0.10): input {base_in:,.0f}, input+output {base_tot:,.0f}")
for R in (0.10, 0.05, 0.03):
    for name,kw in (("in-place, k=1",{}),("errata, k=1",dict(policy="erratum")),
                    ("errata, k=1.5",dict(policy="erratum",ks=(1,2))),("errata, k=2",dict(policy="erratum",k=2)),("errata(full), k=1.5",dict(policy="erratum",ks=(1,2),e_tok=2300))):
        tot,inp=run(R,**kw)
        print(f"R={R:.2f} {name:20} input {inp:9,.0f} ({inp/base_in-1:+.1%})  input+output {tot:9,.0f} ({tot/base_tot-1:+.1%})")
