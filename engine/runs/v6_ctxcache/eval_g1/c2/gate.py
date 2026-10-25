# Whole-bill model from the ideas' cost ledger: bill = 0.45 fixed + 0.55 prefill; prefix-cache baseline = 1.0
# prefill fractions are relative to full compute; prefix caching prefill = 0.83 of full
F, P, PC, BL, PROBE, SHADOW = 0.45, 0.55, 0.83, 0.242, 0.031, 0.01
def idea1(m): return F + P*((1-m)*BL/PC + m*(PC+PROBE)/PC + SHADOW/PC)
def idea2(m): return F + P*((1-m)*BL + m*PC + SHADOW)/PC
print("check idea1 vs claimed 1.52/1.43/1.35/1.22:", [round(1/idea1(m),3) for m in (0.1,0.2,0.3,0.5)])
print("idea2 compute frac at m=.3:", round(0.7*BL+0.3*PC,3), "(claimed 0.42)")
for m in (0.1,0.2,0.3): print("idea2 whole-bill ratio m=%.1f"%m, round(1/idea2(m),3))
import scipy.optimize as o
print("m max for 1.5x idea1:", round(o.brentq(lambda m:1/idea1(m)-1.5,0,1),3), " idea2:", round(o.brentq(lambda m:1/idea2(m)-1.5,0,1),3))
print("ceiling m=0 idea1:", round(1/idea1(0),3), " absolute ceiling (prefill->0):", round(1/F,2))
# routed share m = s*recall + (1-s)*fpr for true multi-source share s
for s in (0.065,0.114,0.23,0.34):
    print("s=%.3f m(rec.9,fpr.05)=%.3f"%(s, s*0.9+(1-s)*0.05))
