import math
D=1.763e-3; t=68e-6; rho=2400; g=9.81; L=38.8e-3
q=rho*g*t  # Pa, self weight (approx all-glass density)
print(f"self-weight q={q:.2f} Pa")
print(f"sag, clamped-clamped beam, no tension: {q*L**4/(384*D)*1e6:.1f} um")
for T in (500,1000):
    print(f"sag membrane T={T}: {q*L**2/(8*T)*1e6:.2f} um")
# 1 N fingertip, r=5 mm, clamped plate of span L, tension T: deflection lower bound (beam strip of width w=10mm)
F=1.0
for T in (0,1000):
    # line-load approx over width b=10mm -> beam center load
    b=10e-3; P=F/b
    dbend=P*L**3/(192*D); dmem=P*L/(4*T) if T else float('inf')
    d=1/(1/dbend+ (1/dmem if T else 0))
    print(f"1 N finger over 10 mm strip, T={T}: deflection ~{d*1e6:.0f} um (vs 10-20 um backstop gap)")
# visibility of untensioned case: reflected-ray deviation
for sl in (0.29,1.22,0.04,0.16,0.43):
    print(f"slope {sl} mrad -> reflected deviation {2*sl*3.438:.1f} arcmin")
# loss of preload: spring set; tension sensitivity table from answer: 0->3-13um
