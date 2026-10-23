# Idea 4: barge = boilerhouse + coal store, frozen in at the settlement for the winter.
# Kill test: bubbler on 0.01-0.2 C water (FACT 7) has ~2 days of stored heat. Repair: heat the moat with the boiler's own low-grade heat, covered moat.
L=80; B=16; perim=2*(L+B)
for width,cover in ((0.5,False),(0.5,True),(1.0,True)):
    A=perim*width
    if cover:   # floating insulated lid (30 mm XPS + tarp), U~1.0 W/m2K incl. edges (assumption)
        q=1.0*40
    else:       # open water at -40 C calm: turbulent ~250 W/m2 (calm polynya case, Antarctic aircraft obs) + net longwave ~120
        q=250+120
    P=A*q
    print(f"moat {width} m, cover={cover}: area {A:.0f} m2, flux {q} W/m2 -> {P/1e3:.0f} kW")
boiler=3e6; eff=0.75; flue_loss=0.12
print(f"3 MW boiler flue loss ~{boiler/eff*flue_loss/1e3:.0f} kW; covered 1 m moat needs {perim*1.0*40/1e3:.0f} kW ({perim*1.0*40/boiler:.1%} of output)")
# Hull side losses alone: boiler room +10 C, steel side, water-side conv h~50 W/m2K at 0.1 C water, air side h~8 -> U~6.9 W/m2K over submerged wetted side 2 m deep
U=1/(1/8+1/50); A_side=perim*2.0
print(f"uninsulated wetted side heat to river: {U*A_side*10/1e3:.0f} kW (this alone keeps a thin melt film on the hull)")
# Coal: 3 MW peak, ~ 9,000 Gcal/yr? Village heat: 2,500 t/yr hard coal (5,200 kcal, eff 0.7) => Gcal
coal=2500; gcal=coal*5.2*0.7
print(f"{coal} t coal -> {gcal:.0f} Gcal useful heat; hold 2-3 kt covers one season")
# Economics per t of coal burned (rub): what the barge deletes at a barge-reachable riverbank settlement
unload=600; stock_loss=0.05*15000; yard_haul=400   # unloading/crane, 5% stockpile loss (weathering, spillage, theft) of 15k rub/t coal, truck to boilerhouse
deleted=unload+stock_loss+yard_haul
# Boilerhouse capex avoided vs new modular coal boilerhouse 3 MW: 90-150 M rub (assumption, Yakutian modular coal boilerhouses ~30-50 M rub/MW)
for bh in (90e6,150e6):
    conv=12e6+45e6+15e6   # old barge (scrap-value) + containerised 3 MW coal boiler + flexible heat link/berth/moat
    dcap=(bh-conv)*0.11   # 20 yr at ~10%
    extra_ops=2.0e6       # RRR class/survey, berth watch, ice/moat ops, tow to/from refill each year (assumption)
    tow=0.4e6*6           # 6 pusher-days per season round trip to the coal source extra vs normal delivery (assumption)
    net=deleted + (dcap-extra_ops-tow)/coal
    print(f"boilerhouse {bh/1e6:.0f} M: deleted handling {deleted:.0f} rub/t + capex delta {dcap/coal:.0f} - ops {(extra_ops+tow)/coal:.0f} = net {net:.0f} rub/t of ~15000-23000 delivered -> cost ratio {15000/(15000-net):.2f}-{23000/(23000-net):.2f}")
