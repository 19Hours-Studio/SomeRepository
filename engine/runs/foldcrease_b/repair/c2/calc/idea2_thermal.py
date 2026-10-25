# passive CTE-scheduled tension: glass stretch s(theta) linear, set by Al link in Ti frame via lever
Eg,t,W=72e9,50e-6,0.14
def stretch(T): return T/(Eg*t)*W
# requirements from idea2.py (10 um residual dent, FWHM 8 mm): -20C bonded 12406? use 15mm-FWHM row: -20C 3482, 25C 592, 60C decoupled 90
req={-20:3482,25:592,60:90}
s_m20,s_60=stretch(req[-20]),stretch(req[60])*1.5
c=(s_m20-s_60)/80; s25=s_m20-45*c
print(f"needed stretch -20C {s_m20*1e6:.0f}um, 60C {s_60*1e6:.1f}um -> slope {c*1e6:.2f} um/K, 25C stretch {s25*1e6:.0f}um = T {s25/W*Eg*t:.0f} N/m (need {req[25]})")
da=23e-6-8.6e-6
for lever in [1,2,3]:
    print(f"Al link in Ti frame, lever {lever}:1 -> link length {c/(da*lever)*1e3:.0f} mm")
F=req[-20]*0.15; print(f"peak hinge/frame force at -20C {F:.0f} N, glass stress {req[-20]/t/1e6:.0f} MPa (CS>=700MPa surface; Corning US9321679)")
# cost per delivered glossy crease-free display (estimates, flagged)
disp=122  # Fold5 inner display subsystem, TechInsights via International Finance
for n,dc in [("idea1 wrung laminate: +back UTG 8-15, fluid 0.1, epilame barrier 0.3, stop calibration 1-2, -PET&3xOCA 3-5",(8+0.1+0.3+1-5,15+0.1+0.3+2-3)),
             ("idea2 tension add-on: toggle+links+edge clamps 2-5, glass edge finish 1-2",(3,7))]:
    print(f"{n}: +${dc[0]:.0f}..{dc[1]:.0f} per phone = {dc[0]/disp*100:.0f}-{dc[1]/disp*100:.0f}% of display subsystem")
print("Apple Duo: matte layer replacement $19 each (AppleCare) + optical penalty; crease 48->167um (HTX) = not invisible")
