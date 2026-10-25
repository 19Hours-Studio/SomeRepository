import math
# sanity check on a known case: Groq LPU 230MB on 725mm2 (14nm) -> Mb/mm2
print("Groq v1 density Mb/mm2", 230*8/725)
print("V-cache N7 density Mb/mm2", 512/36)
# ---- Idea 1: N6 SRAM chiplets
wafer=10000  # $ N7/N6-class wafer (CSET ~$9.3k N7; ~+10% 2025)
d=100; dpw=math.floor(math.pi*150**2/d - math.pi*300/math.sqrt(2*d)); yld=0.9
die_cost=wafer/(dpw*yld); mb_die=112e3/512
print("dies/wafer",dpw,"die $",round(die_cost,1),"MB/die",mb_die,"$/MB",round(die_cost/mb_die,3),
      "implied Mb/mm2",mb_die*8/d)
# bottom-up per package (32 dies) all-in: silicon, substrate+assembly+test, board/VRM/cooling, host/net/rack share
pkg=32*die_cost+1500+2500+3500
sys=16*pkg; print("system $",round(sys),"$/GB",round(sys/112))
# with vendor margin 50% gross
print("with 2x vendor markup $/GB",round(2*sys/112))
# KV/concurrency: Llama-3 70B KV FP8 = 80L*8kv*128*2*1B
kv=80*8*128*2; users=(112-70)*1e9/(kv*8192)
tok_s=users*1000; capex_hr=1.5e3*112/(4*8760); hr=capex_hr/0.85
print("users@8K",round(users,1),"tok/s",round(tok_s),"$ /Mtok at $1.5k/GB",round(hr/(tok_s*3600/1e6),3))
# Cerebras: 4 CS-3 (~$2.5M) for 70B, assume 30 users @2200 tok/s
c_hr=4*2.5e6/(4*8760)/0.85; c_tok=30*2200
print("Cerebras owner $/Mtok",round(c_hr/(c_tok*3600/1e6),2), "$/GB SRAM", 2.5e6/44)
# ---- Idea 3: bits & quality
print("QTIP 2b 70B ppl gap %", round((3.78/3.12-1)*100,1))
w_share=0.36; r=4.5/2.1
print("HBM decode speedup vs NVFP4 at weight share 36%:",round(1/(1-w_share+w_share/r),2))
print("SRAM-silicon cost ratio (share .6):",round(1/(0.4+0.6/r),2))
# ---- Idea 4: SRAM capacity
for dens in (14.2,30):
    gb=2*800*dens*0.75/8/1000
    print("density",dens,"GB/pkg",round(gb,2),"pkgs for 545GB",math.ceil(545/gb),"margin in 144",round(144*gb/545,2))
# ---- Idea 2 thermal margin (rise above 35C coolant)
print("thermal margin",round((95-35)/(141.7-35),2))
