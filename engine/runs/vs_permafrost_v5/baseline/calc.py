rho_w,rho_i,L=1000,917,334e3
# solid slab
for h in (2,3,4): print("slab h",h,"m payload t/m2",round((rho_w-rho_i)*h/1000*0.75,3))
# hollow ice-pykrete hull 60x25x4.5 m, walls/bottom 1.5 m, freeboard 1.0 m
Lb,B,H,t=60,25,4.5,1.5
ice=Lb*B*t+2*(Lb+B)*(H-t)*t
disp=Lb*B*(H-1.0)
pay=disp-ice*rho_i/1000
print("hull ice m3",ice,"displ t",disp,"payload t",pay,"pay/ice",round(pay/(ice*0.917),2))
# thermal: time for 1.5 m wall to warm through (alpha ice 1.1e-6)
print("wall diffusion days",round(1.5**2/1.1e-6/86400,1))
# melt in 0.5 K water, h=500 W/m2K
q=500*0.5; print("melt m/day @0.5K",round(q/(rho_i*L)*86400,3))
# drift time Yakutsk->delta 1500 km at 1.0-2.5 m/s
for v in (1.0,1.5,2.5): print("drift days v",v,round(1.5e6/v/86400,1))
# freezing rate by flooding: surface flux 25 W/m2K * 30 K
q=25*30; print("flood-freeze m/day",round(q/(rho_i*L)*86400,3))
# cost per tonne: crew 12 x $150/day x 20 days per hull + fuel $15k + tug share $20k
c=12*150*20+15000+20000; print("cost/hull $",c,"per t",round(c/pay,1))
# benchmark LORP 2010: 2.3e9 RUB / 1e6 t, ~30 RUB/$
print("LORP avg $/t",round(2.3e9/1e6/30))
# kite sled: 32 t pull, mu 0.05-0.1
for mu in (0.05,0.08,0.1): print("kite train gross t mu",mu,round(32/mu))
