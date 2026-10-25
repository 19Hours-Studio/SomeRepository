from common import *
import numpy as np
PAY=0.8; REC_NOF=dict(Ni=0.71,Cu=0.80,PGM=0.75)
def crf(r,n): return r/(1-(1+r)**-n)
# --- XRT option once NOF is full (N1 7 Mtpa + Maslovskoye 1.5 Mtpa) ---
nof_feed = {'Norilsk1_dissem(F2)':7.0,'Maslovskoye(F7)':1.5}
q_nof = sum(nieq_t(sum(value_per_t(ORES[o],P,REC_NOF).values()))*m*1e6*PAY for o,m in nof_feed.items())
print(f"NOF full-refill output {q_nof/1e3:.0f} kt Ni-eq/yr")
for up,metal in ((1.094,0.98),(1.156,0.98),(1.094,0.95),(1.156,0.95)):
    gain = up*metal-1                         # metal per NOF tonne
    dq = q_nof*gain
    rom_extra = 8.5*(1/(1/up*metal) - 1)       # extra ROM Mtpa to keep NOF full (mass pull = metal/up)
    rom_extra = 8.5*(up/metal-1) if False else 8.5*(1/(metal/up)-1)
    sorted_mt = 8.5+rom_extra
    for capex_t in (4.,8.):                   # USD per t annual sorting capacity (assumed; no source)
        cost = sorted_mt*1e6*(capex_t*crf(.12,15)+1.5) + rom_extra*1e6*35. + 1500*dq
        print(f" grade x{up} metal rec {metal:.0%}: +{dq/1e3:4.1f} kt/yr, extra ROM {rom_extra:.2f} Mtpa, capex {capex_t}$/t -> {cost/dq:6,.0f} $/t added Ni-eq")
# --- Pile adfreeze check NOF-type pile (approx. SP 25.13330 loam R_af table, MPa) ---
T_tab=np.array([-0.3,-0.5,-1,-1.5,-2,-2.5,-3]); R_tab=np.array([.05,.08,.13,.17,.20,.23,.26])
def cap(T,L_emb): return np.interp(T,T_tab,R_tab)*L_emb
print("\nPile capacity 2050 vs 2025 (12 m pile, active layer 1.0 m deepening 1 cm/yr F85; ground warming 0.02-0.16 K/yr F107)")
for T0 in (-1.0,-2.0,-3.0):
    for dT in (0.02,0.05,0.10,0.16):
        c0=cap(T0,12-1.0); c1=cap(min(T0+25*dT,-0.3),12-1.25)
        print(f" T0 {T0:+.1f}C warm {dT:.2f}K/yr: capacity ratio {c1/c0:.2f}  (active-layer share of loss {(1-11/ (12-1.25)**0 *0) if 0 else (1-(10.75/11)):.1%})")
