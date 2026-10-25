#!/usr/bin/env python3
"""Sensitivity of the Continuum conclusions to its weakest assumptions."""
import copy, roofline as R
m, L = R.MODELS["DSv3-671B"], 32768
def run(label, sysname, target, **over):
    s = copy.deepcopy(R.SYS[sysname]); s.update(over)
    r = R.best_at(sysname, s, m, L, target)
    print(f"{label:46s} >= {target:4d} t/s/u: " + ("infeasible" if r is None else
          f"B={r['B']:5d} tok/s/u={r['tps_user']:6.0f} tok/J={r['tpj']:5.2f} tok/s/kW={r['tps_kw']:6.0f}"))
for t in (200, 1000):
    run("Continuum baseline (6us/layer, 0.3pJ/b)", "Continuum x64", t)
    run("Continuum floor 12us/layer", "Continuum x64", t, floor_us=12)
    run("Continuum floor 20us/layer", "Continuum x64", t, floor_us=20)
    run("Continuum SRAM 0.6 pJ/b", "Continuum x64", t, e_w=0.6)
    run("Continuum half compute (15/7.5 PF)", "Continuum x64", t, fp4=15e15, fp8=7.5e15)
    run("Rubin opt SW floor 10us/layer", "Rubin NVL72 (opt. SW)", t, floor_us=10)
    run("Rubin HBM 13 TB/s (low report)", "Rubin NVL72 (opt. SW)", t, hbm_bw=13e12)
    run("Groq3 at 400 W/chip", "Groq3 LPU", t, watt=400)
R.HBM_PJ = 3.0
for t in (200,):
    run("HBM 3.0 pJ/b: Continuum", "Continuum x64", t)
    run("HBM 3.0 pJ/b: Rubin opt SW", "Rubin NVL72 (opt. SW)", t)
