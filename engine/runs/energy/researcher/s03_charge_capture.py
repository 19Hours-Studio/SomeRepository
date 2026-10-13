# K16: how big must the CHARGE converter be to capture enough surplus, given RTE?
# Uses the same German daily system as s02 (daily resolution: intraday shaping by batteries assumed).
import importlib.util, sys, io, contextlib
spec=importlib.util.spec_from_file_location("s02","s02_deficit_shape.py")
with contextlib.redirect_stdout(io.StringIO()):
    s02=importlib.util.module_from_spec(spec); spec.loader.exec_module(s02)
ny=len(s02.R)/365.25
for OVER in (1.3,1.5,1.8):
    R=s02.run(OVER,quiet=True)
    sur=[max(0,x)/24 for x in R]   # GW daily mean
    deff=sum(max(0,-x) for x in R)/ny  # GWh/yr
    print(f"OVER {OVER}: deficit {deff/1000:.0f} TWh/yr, surplus {sum(sur)*24/ny/1000:.0f} TWh/yr, peak surplus {max(sur):.0f} GW")
    for rte in (0.6,0.4,0.25,0.18):
        need=deff/rte
        # find charge converter P such that captured = need
        lo,hi=0,500
        for _ in range(50):
            P=(lo+hi)/2
            cap=sum(min(s,P) for s in sur)*24/ny
            if cap<need: lo=P
            else: hi=P
        cap=sum(min(s,hi) for s in sur)*24/ny
        ok = cap>=need*0.999
        cf = need/(hi*8766) if ok else float('nan')
        print(f"   RTE {rte:.2f}: need {need/1000:5.0f} TWh in -> charge conv {hi:6.1f} GW, cap factor {cf:5.2f}" + ("" if ok else "  IMPOSSIBLE"))
