"""Reproduce round 6 (tau 10, vendor profiles only) through model7, then show each profile's slot power and FLOP/W."""
import model7 as q
R = q.gpu_env([p for p in q.RUBIN_PROF() if p[0] in ("0.75V", "MaxQ")], tau_scale=False)
C = q.pipe_env([p for p in q.cont_prof(q.C6, q.C6_PARTS) if p[0] in ("0.75V", "MaxQ")], tau_scale=False)
print("round-6 reproduction C6/Rubin 128K:", q.ratio(C, R)); print(" Rubin", q.vals(R)); print(" C6   ", q.vals(C))
for name, profs in (("Rubin", q.RUBIN_PROF()), ("C6", q.cont_prof(q.C6, q.C6_PARTS)), ("C7", q.cont_prof(q.C7, q.C7_PARTS)),
                    ("Ultra600", q.profiles(q.ultra(600e3/144), 4*860, 4*75, 0, rack_share=0.83)),):
    for lab, s, f in profs:
        print(f"{name:<9}{lab:<9} f {f:.3f} slot {s['P']:7.0f} W  dense FP4 {s['F4']/1e15:5.1f} PF  {s['F4']/s['P']/1e12:5.2f} PF/kW  tau {q.tau_f(f)*1e6:.1f} us")
