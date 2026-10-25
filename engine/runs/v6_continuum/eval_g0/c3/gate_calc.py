# check: KV bytes/token formula on Llama-3-70B (80L, 8 KV heads, hd128, bf16) known = 320 KiB = 327,680 B
kv=lambda L,h,d,b: 2*L*h*d*b
assert kv(80,8,128,2)==327680
# IDEA 1: MiniMax-M2 (62L, 8 KV heads, hd 128), 230B total
kv_fp8=kv(62,8,128,1); kv_nv4=kv_fp8*4.5/8
print("KV/token FP8 B",kv_fp8,"NVFP4",kv_nv4)
ctx=9000  # 8k in /1k out benchmark the GB300 $0.06 anchor uses
# GB300 anchor: $0.06/Mtok at $1.86/chip-hr -> tok/s per chip
tps_gpu=1.86/0.06e-6/3600; print("GB300 tok/s/chip",round(tps_gpu))
# Continuum: 3 wafers; CS-3 ~$3M each; owner TCO/hr per wafer ~ capex/4yr / 0.45 package share
wafer_hr=3.0e6/(4*8760)/0.45; sys_hr=3*wafer_hr; print("sys $/hr",round(sys_hr))
need_tps=sys_hr/0.06e-6/3600; users=need_tps/500; print("needed tok/s",round(need_tps),"users @500",round(users))
for wbits,kvB,lab in [(8,kv_fp8,"FP8 w + FP8 KV"),(4.5,kv_nv4,"FP4 w + NVFP4 KV")]:
    free=300e9-230e9*wbits/8; avail=free/(kvB*ctx); need=users
    tps=avail*500; cost=sys_hr/(tps*3600)*1e6
    print(lab,"free GB",free/1e9,"users fit",round(avail),"margin",round(avail/need,3),"$/Mtok",round(cost,2))
# IDEA 2: decode power floor at Rubin-class 22 TB/s
bw=22e12*8
for pj in (3.44,5.74):
    print("HBM W @",pj,"pJ/b:",round(bw*pj*1e-12))
nvl=3.6e12*8*5e-12; onchip=bw*1e-12  # ~5 pJ/b serdes, ~1 pJ/b on-die SRAM/NoC
print("nvlink W",round(nvl),"on-die W",round(onchip))
rubin_decode_W=0.8*2300  # assume decode draws ~80% of 2.3 kW TDP
req=rubin_decode_W/2
for pj in (3.44,5.74):
    floor=bw*pj*1e-12+nvl+onchip+100  # +100 W compute/leak
    print("required W",round(req),"floor W",round(floor),"margin",round(req/floor,2))
# chain: 2x tok/kW halves energy (9%) + facility (12%, power-provisioned) per token; package gain generous 30%
s=0.09/2+0.12/2; print("ratio energy-only",round(1/(1-s),2))
print("ratio + 30% package cut",round(1/(1-s-0.45*0.3),2))
