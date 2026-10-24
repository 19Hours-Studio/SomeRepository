# Gate arithmetic for 4 Continuum ideas. Inputs sourced in gate notes.
import math
print("== IDEA 1: LPDDR prefill die ==")
PF=10e15; BW=1e12; ridge=PF/BW
# check on known case: dense model, FP8, 8K chunk -> 2*8192/1 = 16384 FLOP/B (idea's claim)
print("dense FP8 8K intensity",2*8192/1,"ridge",ridge)
# DeepSeek-V3: 256 routed experts, top-8 (public config)
tok_per_exp=8192*8/256
for b,name in [(1,'FP8'),(0.5,'FP4')]:
    I=2*tok_per_exp/b; print(f"MoE {name} expert intensity {I:.0f} FLOP/B margin {I/ridge:.3f}")
# batch tokens needed for compute>=weight time, FP4 377GB, 37B active
print("tokens needed for overlap:",377e9/BW*PF/(2*37e9))
lp=256*10   # $10/GB LPDDR 2026 (SemiAnalysis via wccftech)
print("LPDDR alone $",lp,"vs idea BOM 2500")
bom=lp+1000+300   # die ~$1k + substrate/test ~$300 (est)
print("Continuum-P $/PF",bom/10," B200 $/PF",6400/9)
print("TCO ratio vs B200 if accel BOM (8% share) falls by", (6400/9)/(bom/10), "->", 1/(1-0.08*(1-1/((6400/9)/(bom/10)))))
print("== IDEA 2: FP4 training ==")
E,A,B,al,be=1.69,406.4,410.7,0.34,0.28   # Chinchilla fit (Hoffmann 2022)
N,D=12e9,10e12
L=E+A/N**al+B/D**be; dL=0.015*L
k=((B/D**be+dL)/(B/D**be))**(1/be)
print(f"L={L:.3f}, 1.5% gap -> FP4 equals FP8 at D/{k:.2f}: tokens-to-target x{k:.2f}")
# idea: 16% layers kept high precision (paper), final 18% tokens promoted, FP4=2x FP8 GEMM
g=0.82*(0.84*0.5+0.16)+0.18
step=0.3+0.7*g
cost=33+(44+13+4+6)*step
print(f"GEMM time {g:.3f}, step speedup {1/step:.2f}, cost ratio {100/cost:.2f}")
print("== IDEA 3: stacked SRAM ==")
dens=64/36  # MB/mm2 V-Cache
cap=64*4*800*dens/1000
need_ds=671e9*4.5/8/1e9; need_k2=1.04e12*4.5/8/1e9
print(f"rack SRAM {cap:.0f} GB; DSV3 NVFP4 {need_ds:.0f} GB margin {cap/need_ds:.2f}; K2 {need_k2:.0f} GB margin {cap/need_k2:.2f}")
print("SRAM cost at $170/GB for DSV3:",170*need_ds)
for w in (0.23,0.30,0.36):
    d=1/(1-w); sys=1/(0.3+0.7/d)
    print(f"weight share {w}: decode x{d:.2f}, system (70% decode) x{sys:.2f}")
print("== IDEA 4: LPDDR MoE decoder ==")
vera_pj=35/(1.2e12*8)*1e12
print(f"Vera LPDDR5X {vera_pj:.2f} pJ/bit vs HBM3E 3.44")
lp_perTBs=512*10/1.2; hbm_perTBs=2900/8
print(f"$/TB/s LPDDR {lp_perTBs:.0f} HBM {hbm_perTBs:.0f} margin {hbm_perTBs/lp_perTBs:.3f}")
tco=1.86*35000  # per-GPU 4-yr TCO proxy from rental
new=tco-2900+lp_perTBs*8 - 0.2*tco*0.3  # air cooling credit: 30% of facility share
print(f"TCO/GPU-equiv now {tco:.0f}, with idea {new:.0f}, ratio {tco/new:.2f}")
# all-to-all vs DRAM time (idea's own deciding quantity)
a2a=1000*58*7168*3*8/160; print("per-chip a2a bytes/step",a2a/1e6,"MB ->",a2a/400e9*1e3,"ms at 400GB/s vs 10 ms step")
