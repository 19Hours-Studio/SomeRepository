# Idea 2: shaft-bottom XRT sorting, rejects to backfill. Value per t ROM and per t Ni-eq.
P=dict(Ni=15500,Cu=9500,pgm_g=1100/31.1)   # $/t, $/t, $/g (6PGM basket ASSUMED ~$1100/oz)
def V(ni,cu,g): return ni/100*P['Ni']+cu/100*P['Cu']+g*P['pgm_g']
ores={'Norilsk-1 dissem (F2)':V(0.25,0.33,4.56),
      'Talnakh probable (F1)':V(0.94,1.64,5.17),
      'Maslovskoye (F7)':V(0.3,0.5,7.0),
      'cuprous/stringer (ASSUMED 1Ni 3Cu 8g)':V(1.0,3.0,8.0),
      'massive rich (ASSUMED 3Ni 4Cu 12g)':V(3.0,4.0,12.0)}
pay=0.75    # payable/recovered fraction of in-situ value through plant+smelter (ASSUMED)
# measured (rejection r of ROM, metal loss L) - vendor/company data
tests={'Selebi bulk XRT (F350)':(0.152,0.02),
       'Carlingup RAV1 stringer':(0.44,0.04),
       'Carlingup RAV8 stringer':(0.63,0.06),
       'Carlingup RAV4W dissem':(0.23,0.16)}
f_sort=0.65   # share of ROM in sortable +15 mm size (ASSUMED 0.6-0.7)
# r above is of sorter feed -> ROM rejection = r*f_sort (fines bypass, carry their full metal)
s_sort=3.0    # $/t sorted underground (surface ~1.5; x2 for chamber, ventilation, maintenance; ASSUMED)
# Case 1 BROWNFIELD, concentrator not binding (kill-test case): avoided cost per rejected t
C_av_brown=dict(hoist=3,surface_rail=1.5,conc_opex=12,tailings=2,backfill_aggregate=6)
Cb=sum(C_av_brown.values())
print(f"avoided cost per rejected t, unconstrained = ${Cb}")
print("ore values $/t in situ:",{k:round(v) for k,v in ores.items()})
def net_unconstrained(Vo,r,L):
    rr=r*f_sort; LL=L*f_sort    # metal loss only in sorted fraction
    return rr*Cb - LL*Vo*pay - f_sort*s_sort
# Case 2 HOIST-BOUND deep mine (Skalisty-type, 2.1 km shafts): hoist capacity fixed;
# sorting lets mine send H/(1-rr) ROM, metal hoisted up by (1-LL)/(1-rr)
c_mine=60   # $/t extra ROM mined underground (stoping+development, backfill partly from rejects) ASSUMED
down=0.25   # downstream variable cost as share of payable value (smelt/refine/logistics) ASSUMED
def net_hoistbound(Vo,r,L):
    rr=r*f_sort; LL=L*f_sort
    extra_metal=(1-LL)/(1-rr)-1
    rev=Vo*pay*extra_metal*(1-down)
    cost=rr/(1-rr)*c_mine + f_sort/(1-rr)*s_sort - rr/(1-rr)*C_av_brown['backfill_aggregate']
    return rev-cost
print("\n$/t hoisted ore | unconstrained (net per t ROM) ; hoist-bound (net per t hoisted)")
for o,Vo in ores.items():
  for t,(r,L) in tests.items():
    print(f"{o:38s} {t:26s} {net_unconstrained(Vo,r,L):8.1f} ; {net_hoistbound(Vo,r,L):8.1f}")
# break-even loss for Selebi-like rejection in unconstrained case
print()
for o,Vo in ores.items():
    r=0.152; Lbe=(r*f_sort*Cb - f_sort*s_sort)/(f_sort*Vo*pay)
    print(f"{o:38s} break-even metal loss at 15% rejection, unconstrained: {100*Lbe:5.2f}%")
