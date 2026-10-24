# Idea 1 round 3: index-matched photo-spacer pillars + sealed fluid at sub-ambient pressure dp
import numpy as np; pi=np.pi
Dg=1.70e-4; dp=3e3; rho=1050; g=9.81; H=0.15; h=10e-6
print(f"hydrostatic head over 150 mm: {rho*g*H:.0f} Pa  (< dp={dp:.0f} Pa -> UTG never lifts by gravity)")
for a in [6e-3,9.4e-3,15e-3,20e-3]:
    w=dp*a**4/(384*Dg); print(f"  UTG sag into sub-stack dip of width {a*1e3:4.1f} mm at dp: {w*1e6:.2f} um, slope ~{3.2*w/a*1e3:.2f} mrad")
for pitch in [1e-3,0.3e-3]:
    F=2.0; ap=pitch/2; w=F*ap**2/(16*pi*Dg)
    pill_p=dp*pitch**2/(pi*(10e-6)**2)
    print(f"  pitch {pitch*1e3:.1f} mm: stylus 2N local deflection between pillars {w*1e6:.1f} um (gap {h*1e6:.0f}); pillar contact stress {pill_p/1e6:.1f} MPa; area fraction {pi*(10e-6)**2/pitch**2*100:.2f}%")
for mu_f in [0.02,0.05]:
    N=mu_f*dp*0.07; Nc=(Dg*dp**2)**(1/3)
    print(f"  pillar friction mu={mu_f}: compressive line force {N:.1f} N/m vs heavy-sheet lift-off scale (D p^2)^(1/3)={Nc:.1f} N/m (prefactor >=1 assumed)")
# wear: Archard
k=1e-15; pitch=0.3e-3; Fp=dp*pitch**2; s=2*134e-6*200e3; A=pi*(10e-6)**2
print(f"  pillar wear over 200k cycles (k=1e-6 mm3/Nm assumed): {k*Fp*s/A*1e6:.3f} um")
Vf=0.021*h; print(f"  fluid volume {Vf*1e6:.2f} mL; 60 K expansion {9.6e-4*60*Vf*1e9:.1f} mm3 -> bellows {9.6e-4*60*Vf/0.58*1e6:.3f} mm2 per m of perimeter")
# protective polymer on UTG would print through:
Ec,tc,z=4e9,5e-6,17.5e-6; r=Ec*tc*z**2/Dg; set=0.3; R=3e-3; kap=r*set/R; a=pi*R
print(f"  5um bonded hardcoat on UTG: moment ratio {r*100:.1f}%, at 30% set -> crease {kap*a**2/32*1e6:.1f} um  => no polymer film on UTG")
