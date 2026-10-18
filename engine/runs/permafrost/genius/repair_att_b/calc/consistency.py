import math
print("=== I1: casing through ice: talik water +2 C up the casing melts ice around it ===")
A=math.pi*0.4*1.8; h=500; dT=2
P=A*h*dT; melt=P/(334e3*917)*86400
print(f" bare casing: {P/1e3:.1f} kW -> {melt:.2f} m3/day ice melted (annulus ~{melt/(math.pi*0.4*1.8):.2f} m/day) over 1-2 day hole life -> insulated sleeve (k 0.03, 50 mm) cuts to {A*0.03/0.05*dT/1e3*1e3:.1f} W -> OK")
print("=== I2: portal exchange flow (doorway formula Q=Cd/3*W*sqrt(g*H^3*dT/T)) ===")
W=3; H=1.8; Cd=0.6; T=288
for dT in (10,15):
    Q=Cd/3*W*math.sqrt(9.81*H**3*dT/T)
    P=Q*1.2*1005*dT
    print(f" open portal dT={dT} K: exchange {Q:.2f} m3/s -> {P/1e3:.0f} kW into 80 m adit ({P/(80*8):.0f} W/m2 roof+walls) ; with curtain (5% leakage) {P*0.05/(80*8):.1f} W/m2")
print("=== I3: Kovin check (66,056 h -> 4,400,863 t commercial coal) ===")
r=4400863/66056
print(f" Kovin average {r:.0f} t/h commercial lignite; model 150 kW cutter UCS 5-7 MPa 46-65 m3/h x 1.25 t/m3 x 0.8 rec = {46*1.25*0.8:.0f}-{65*1.25*0.8:.0f} t/h -> consistent")
print(" Arctic Yakutia coal demand: 88 kt (Dzhebariki-Khaya, 2016) + ~115 kt other -> ~200 kt/yr total market (Tkach et al.)")
