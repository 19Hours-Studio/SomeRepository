"""Round 8e: checks. (1) GB300 InferenceX calibration under GPU tau 140 us; (2) extreme Rubin Ultra (600 kW at 100 PF
plus undervolt law) under GPU tau 10/40/140; (3) Rubin+LPX with LP30 at 625 / 400 W.  Usage: python3 run8e.py > run8e.txt"""
import model8 as e, model5 as m, model7 as q
GB = dict(m.SYS["GB300"], imb=q.IMB_G, s=1.0)
ISL, OSL = 8192, 1024
pre_t = m.comp_time(m.V4, GB, 1, 61, ISL // 2)
for tau in (10e-6, 140e-6):
    ev = m.envelope(lambda k: m.gpu_points(GB, tau, ISL + OSL // 2, k, 0.8), (50,), ks=range(4))
    dec = ev[50][0] * GB["P"] / m.DERATE; out = 1 / (1 / dec + (ISL / OSL) * pre_t)
    print(f"(1) GB300 tau {tau*1e6:.0f} us: model {out*(1+ISL/OSL):,.0f} total tok/s/GPU at >=50 tok/s/user -> measured 12k = {12e3/(out*(1+ISL/OSL)):.2f} of model")
C7P = q.cont_prof(q.C7T, q.C7T_PARTS)
A = e.pipe_env_tau(C7P, e.tau_sym)
UX = q.profiles(dict(q.ultra(600e3 / 144), P_maxq=600e3 / 144), comp_w=3440 * 4167 / 5690, leak_w=300 * 4167 / 5690,
                other_w=0, rack_share=1, vendor_maxq=False)
for t0 in (10, 40, 140):
    U = e.gpu_env_tau(UX, e.tau_gpu(t0))
    print(f"(2) 128K C7 / Ultra(600 kW @100 PF + undervolt), GPU tau {t0:3d}: {q.ratio(A, U)}   Ultra max {U['max']:.0f}")
for P in (625, 400):
    old = m.LP30["P"]; m.LP30["P"] = P
    L = q.afd_env()
    m.LP30["P"] = old
    print(f"(3) 128K C7 / Rubin+LPX (LP30 {P} W, FP8 weights, AFD tau 8 us): {q.ratio(A, L)}   LPX-combo max {L['max']:.0f}")
