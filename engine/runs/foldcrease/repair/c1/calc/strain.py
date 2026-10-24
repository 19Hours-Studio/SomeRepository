# Layer strain budget for a foldable stack.  Sources / assumptions in NOTES.md.
import numpy as np
# name, thickness um, E GPa, creeps?
stack = [
 ("PET protective film (hard-coated)", 60, 4.5, True),
 ("PSA (film adhesive)",               25, 0.00015, True),
 ("UTG (Fold7, FACT3)",                45, 70.0, False),
 ("OCA",                               25, 0.00015, True),
 ("POL-less CF + touch + TFE",         15, 5.0, True),
 ("OLED/TFT on CPI substrate",         20, 8.0, True),
 ("back film PET",                     38, 4.5, True),
]
def layer_strains(R_mm):
    out=[]
    for n,t,E,c in stack:
        out.append((n,t,(t*1e-3)/(2*R_mm)*100))   # decoupled: each layer about own mid-plane (soft OCA)
    return out
tot=sum(s[1] for s in stack)
if __name__=="__main__":
    print("total stack um",tot)
    for R in [1.5,2.0,3.0,5.0,7.0]:
        print(f"\nR={R} mm   fully-bonded outer strain t/2R={tot*1e-3/(2*R)*100:.2f}%")
        for n,t,e in layer_strains(R):
            print(f"  {n:36s} {t:4d}um  {e:5.2f}%")
    # UTG bending stress
    for R in [1.5,2,3,5]:
        s=70e9*45e-6/(2*R*1e-3)/(1-0.22**2)/1e6
        print(f"UTG 45um surface stress at R={R}: {s:.0f} MPa")
    # Kumoh no-set radius 5 mm -> no-set strain for assumed film thickness
    for tf in [25,50,80]:
        print(f"Kumoh CPI no-set strain if film {tf}um: {tf*1e-3/10*100:.2f}%")
    