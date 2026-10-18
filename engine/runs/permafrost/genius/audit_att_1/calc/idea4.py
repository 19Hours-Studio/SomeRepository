import math
print("100 d * 24 h * 60 t/h =",100*24*60/1e3,"kt; utilisation implied for 80 kt:",80e3/(100*24*60))
# hole
t_per_m=190/80
for rho in [1.3,1.35]:
    A=t_per_m/rho
    D=math.sqrt(4*A/math.pi)
    print(f"rho {rho}: {t_per_m:.3f} t/m -> section {A:.2f} m2 -> single auger D {D:.2f} m")
holes=80e3/190
print("holes per year",holes,"per day over 100 d",holes/100)
for sp in [2.14,2.42]:
    print("bluff per year km at spacing",sp,":",holes*sp/1e3)
D=1.5
print("spacing for 62% if seam = D:",D/0.62,"web",D/0.62-D)
print("spacing implied by 0.9 km:",900/holes)
# cycle
for cut in [60,100,140]:
  t_cut=190/cut
  for flight_len,t_flight in [(6.1,0.1),(6.1,0.15)]:
    n=80/flight_len
    t_handle=2*n*t_flight   # add on way in, remove on way out
    for t_move in [1.0,2.0]:
        cyc=t_cut+t_handle+t_move
        print(f"cut rate {cut} t/h: cut {t_cut:.1f} h, flights {n:.0f}x2 at {t_flight*60:.0f} min -> {t_handle:.1f} h, move/rebolt {t_move} h => cycle {cyc:.1f} h, avg {190/cyc:.0f} t/h")
# web stress
for H in [20,30]:
    sv=2.0*9.81*H/1e3  # MPa approx (density 2.0)
    print(f"cover {H} m: sv {sv:.2f} MPa, web stress at 62% recovery {sv/(1-0.62):.2f} MPa")
# village demand
for vill in [1000,3000,5000]:
    print(f"80 kt/yr supplies {80e3/vill:.0f} villages at {vill} t/yr")
# cost at 20kt vs 80kt
# fixed vs variable estimate from two points: c(20)=4100, c(80)=1800 => F/q + v
q1,c1,q2,c2=20e3,4100,80e3,1800
F=(c1-c2)/(1/q1-1/q2); v=c1-F/q1
print(f"fixed {F/1e6:.1f} M rub/yr, variable {v:.0f} rub/t")
for q in [10e3,20e3,30e3,40e3,60e3]:
    print(f"sales {q/1e3:.0f} kt/yr -> {F/q+v:.0f} rub/t")
# breakeven vs pit 2800-3700
for pit in [2800,3700]:
    print("breakeven sales vs pit",pit,":",F/(pit-v)/1e3,"kt")
