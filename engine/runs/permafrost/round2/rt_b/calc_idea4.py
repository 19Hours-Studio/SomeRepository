"""Idea 4 repair: under-ice drifting ore pods. Trim window, shell melt, compressibility, route, economics. [S]/[A]/[R]"""
import numpy as np
rw=1000; ri=917; Lf=334e3; Cd=1.2; Afront=5.0*2.2; Asurf=39.3
def drag(U): return 0.5*rw*Cd*Afront*U**2
print("Stall limit B_max = drag/mu (kg):")
for U in (0.16,0.2,0.3):
    print(f" U={U}: drag {drag(U):.0f} N; mu 0.5 (ice-ice, R) -> {drag(U)/0.5/9.81:.0f} kg; mu 0.15 (HDPE skid on wet ice, A) -> {drag(U)/0.15/9.81:.0f} kg")
def buoy_loss_per_day(dT,h=400):  # kg/day lost by shell melt (ice->water)
    m_ice=h*dT*86400/Lf*Asurf; return m_ice/ri*(rw-ri)
for dT in (0.01,0.03,0.05):
    bl=buoy_loss_per_day(dT); mm=400*dT*86400/Lf/ri*1000
    for U in (0.2,0.3):
        Bmax=drag(U)/0.15/9.81; Tmax=0.9*Bmax/bl
        print(f" water +{dT} K: shell melt {mm:.1f} mm/d, buoyancy loss {bl:.1f} kg/d; U={U}: usable trip {Tmax:.0f} d = {Tmax*86400*U/1000:.0f} km; shell needed {mm*Tmax/10+2:.0f} cm")
# compressibility check (why the shell must be rigid): air in 7.4 m3 snow (rock-ore pod) at 100 kg/m3 -> 6.6 m3 air
Vair=7.4*(1-100/ri)
for dz in (0.7,):
    dV=Vair*(dz*rw*9.81)/(101325+1.5*rw*9.81)
    print(f"\nFlexible bag: draft change {dz} m changes air volume {dV:.2f} m3 = {dV*rw:.0f} kg buoyancy -> unstable; rigid ice shell essential")
# cold content (soak defect): ore loaded in autumn at -2..-5 C instead of -20..-30
for Tc in (-25,-4):
    Q=10000*800*(-Tc)+7400*0.1*2100*(-Tc)
    print(f"contents at {Tc} C: cold reserve {Q/1e6:.0f} MJ freezes {Q/Lf:.0f} kg ice -> +{Q/Lf/ri*(rw-ri):.0f} kg buoyancy")
# coal bookkeeping (defect 7): 8 t coal solids at 1350 kg/m3 with flooded voids
coal=8000; Vs=coal/1350; deficit=coal-Vs*rw
shell=Asurf*0.15*ri; shell_b=Asurf*0.15*(rw-ri)
snow=(deficit-shell_b)/(rw-100)
print(f"\nCoal pod: 8 t solids {Vs:.2f} m3, flooded deficit {deficit:.0f} kg, 15 cm shell gives +{shell_b:.0f} kg, snow pocket {snow:.2f} m3; bulk coal at 0.62 packing {coal/1350/0.62:.1f} m3 + snow {snow:.1f} = {coal/1350/0.62+snow:.1f} m3 (inner 13.2 OK)")
# route: Kolyma Zyryanka -> Srednekolymsk; winter Q ~ 330 m3/s (Nov-Apr low flow +130..268 m3/s, +43..454 % post-dam at Srednekolymsk [S Majhi et al. 2007])
Q0=268/4.54; Qw=Q0+268
print(f"\nKolyma late-winter Q pre-dam {Q0:.0f}, post-dam {Qw:.0f} m3/s")
for W,D in ((400,2.5),(600,3.0)):
    print(f" under-ice section {W} m x {D} m -> U = {Qw/(W*D):.2f} m/s; pod (1.2 m) + ice draft 1.1-1.8 needs {1.2+1.1:.1f}-{1.2+1.8:.1f} m water depth")
# polynya below Kolyma HPP: reach starts ~1,400 km downstream (Zyryanka) -> frazil source far upstream [S distance: Srednekolymsk 1720 km from dam, Majhi 2007]
# economics per delivered tonne (winter delivery to a winter consumer; baseline = summer barge + 1-yr stockpile, or winter road)
dist=330  # km Zyryanka-Srednekolymsk by river [A]
road=0.118*dist  # $/t at reviewer's winter-road rate $0.118/t.km [R]
for barge in (12,37):
    pod_lo,pod_hi=10,20  # $/t: 15 cm shell freezing (5.4 t ice/pod), molds, crane, launch+catch slots, pingers, loss [A, orig $7.3 + soak/slot/shell]
    print(f" barge leg ${barge}/t [R] vs pod ${pod_lo}-{pod_hi}/t -> ratio {barge/pod_hi:.1f}-{barge/pod_lo:.1f}x; winter road {dist} km ${road:.0f}/t -> {road/pod_hi:.1f}-{road/pod_lo:.1f}x")
# loss measurement with tags: rule of three
print(" zero losses in n tagged pods bounds loss <3/n at 95%: n for <1% =",300,"; for <0.5% =",600)
