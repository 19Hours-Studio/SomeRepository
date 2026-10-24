# incremental cost per DELIVERED phone meeting the invisibility spec (depth<=5um, slope<=1mrad).
# Hinge cost reference: Kuo est. $70-80 (AppleInsider/9to5mac Oct 2025). Adders below are my estimates (no source) -> flagged.
hinge=(70,80)
idea1_adders={"Ti edge rails+flexure springs+cam latch":(3,6),"silicone gel lamination (vs OCA)":(1,3),"edge-bond of UTG to rails":(1,2)}
idea2_adders={"CPI back film instead of PET":(1,3),"silicone OCA instead of acrylic":(1,2),"hard-coated UTG, no PET protector":(0,2)}
for name,ad,yld in [("idea1",idea1_adders,(0.85,0.95)),("idea2",idea2_adders,(0.9,0.97))]:
    lo=sum(a for a,b in ad.values()); hi=sum(b for a,b in ad.values())
    # cost per delivered good unit: adders / yield; extra scrap of a ~$150-250 inner panel module (assumed) at (1-yield)
    per_lo=lo/yld[1]+(1-yld[1])*150; per_hi=hi/yld[0]+(1-yld[0])*250
    print(f"{name}: BOM adder ${lo}-{hi}; per delivered spec-passing unit ${per_lo:.0f}-{per_hi:.0f}; vs hinge ${hinge[0]}-{hinge[1]} -> {per_lo/hinge[1]*100:.0f}-{per_hi/hinge[0]*100:.0f}% of hinge cost")
print("Baselines (Fold7 teardrop, Apple/SDC drilled plate, Oppo N6 printed hinge+thick glass): reported creases 0.15-0.7 mm-class or 'still visible' -> spec yield ~0 -> cost per spec-passing unit undefined (no unit delivered).")
