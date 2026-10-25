# Llama-3-70B class: 80 layers, 8 KV heads, d_head 128, hidden 8192
L=80; P=70e9; kvv=L*2*8*128           # KV values per token
w_nv=P*4.5/8/1e9                       # GB weights NVFP4
kv_user=kvv*4.5/8*8192/1e9             # GB per user at 8K NVFP4
print("check (idea4 known answer 62.8 GB):", round(w_nv+31*kv_user,1), "GB; weights",round(w_nv,1),"kv/user",round(kv_user,3))
flop_tok=2*P + 2*2*L*8192*8192        # matmul + attention ~ (QK,PV over 8K ctx, 64 q heads*128)
print("FLOP/token GF", flop_tok/1e9, "-> 31k tok/s needs PF", round(31e3*flop_tok/1e15,2), "(idea says 5.0)")
# Idea 4: layer-serial bound. dies holding layer l only; per-user time = L * (F/L)/(Ptot/L) = L*F/Ptot
Ptot=6.8e15
u4=Ptot/(L*flop_tok); print("IDEA4 per-user upper bound tok/s", round(u4), "margin", round(u4/1000,2), "aggregate tok/s", round(31*u4))
# Idea 1: BW per stored bit
need_per_gbit=1000*1/8                 # GB/s per Gbit if every bit read once/token at 1000 tok/s
print("IDEA1 BW/bit need", need_per_gbit, "avail 135 -> margin", round(135/need_per_gbit,2))
need=1000*(w_nv+kv_user); print("IDEA1 need TB/s 1 user", round(need/1e3,2))
dens_hb=0.064                          # Gb/mm2 ISSCC2022 HB logic-DRAM
print("IDEA1 single-layer area for 312Gb at 0.064:", 312/dens_hb, "mm2 vs 3200/pkg -> pkgs", round(312/dens_hb/3200,2))
print("IDEA1 per-user BW with 2 pipeline stages", 42/2, "TB/s margin", round(21e3/need,2))
# Ideas 2/3 density
print("IDEA2 density need", 80*8/(2*400*4), "Gb/mm2 -> margin vs 0.064:", round(0.064/(80*8/(2*400*4)),2))
print("IDEA2 current/stack @0.75V", 1000/0.75/2, "A (idea says 340)")
print("IDEA3 density need", 80*8/(4*400*4), "-> margin", 0.064/0.10)
print("HBM3E 24Gb die <=121mm2 (11x11 pkg) -> >=", round(24/121,3), "Gb/mm2")
print("IDEA3 DRAM W", 64e12*8*0.88e-12)
rubin=22/2.3; i3=64/2.04; i2=32/1.0
print("BW/kW TB/s: Rubin",round(rubin,1),"I3",round(i3,1),"I2",i2,"raw ratio",round(i3/rubin,2),round(i2/rubin,2))
cap=4*400*4*0.064; bw=135*cap/1e3; pw=2.04-0.45+0.45*bw/64
print("IDEA3 at measured density: Gb",cap,"BW TB/s",round(bw,1),"BW/kW ratio factor",round((bw/pw)/i3,2),"-> tok/kW ~",round(2.13*(bw/pw)/i3,2))
