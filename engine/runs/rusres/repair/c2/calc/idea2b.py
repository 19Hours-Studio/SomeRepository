import numpy as np
exec(open('idea2.py').read().split('print(f"avoided')[0])
# NPV check of hoist-bound acceleration with finite reserve (lost tail metal counted)
def npv_ratio(r,L,T=30,i=0.14):
    rr=r*f_sort; LL=L*f_sort
    rate=(1-LL)/(1-rr); Ts=T*(1-rr)
    t=np.arange(0,T,0.01); disc=np.exp(-np.log(1+i)*t)
    base=np.sum(disc)*0.01
    sort=np.sum(disc[t<Ts])*0.01*rate
    return sort/base, rate
for k,(r,L) in tests.items():
    nr,rate=npv_ratio(r,L)
    print(f"{k:26s} metal rate x{rate:.3f}, metal NPV x{nr:.3f} (30-yr reserve, 14%)")
# mine-level cost per t Ni-eq (hoist-bound deep rich-ore mine, 2 Mtpa hoisted)
H=2.0e6; c_mine=60; down=0.25
for o in ('massive rich (ASSUMED 3Ni 4Cu 12g)','cuprous/stringer (ASSUMED 1Ni 3Cu 8g)','Talnakh probable (F1)'):
  Vo=ores[o]
  for k,(r,L) in list(tests.items())[:2]:
    rr=r*f_sort; LL=L*f_sort
    cost_t=c_mine+3+12+2+Vo*pay*down   # $/t hoisted: mine+hoist+conc+tailings+downstream
    capex_t=40                          # sustaining+expansion capex per t (ASSUMED)
    base_cost=H*(cost_t+capex_t); base_ni=H*Vo*pay/15500
    rom=H/(1-rr)
    s_cost=rom*(c_mine+0)+H*(3+12+2)+H*Vo*pay*(1-LL)/(1-rr)*down+rom*f_sort*s_sort-rom*rr*6+H*capex_t+25e6*0.1455  # +$25M chamber+2 sorters annualised
    s_ni=H*Vo*pay*(1-LL)/(1-rr)/15500
    print(f"{o[:22]:22s} {k[:16]:16s} $/t Ni-eq base {base_cost/base_ni:6.0f} -> sorted {s_cost/s_ni:6.0f}  ratio {base_cost/base_ni/(s_cost/s_ni):.3f}; Ni-eq +{100*(s_ni/base_ni-1):.1f}%")
# consistency: backfill void balance - rejects per t ROM must be <= fill tonnes per t ROM
for rho in (3.0,3.5,4.5):
    print(f"ore density {rho}: fill capacity {2.0/rho:.2f} t/t ROM vs max rejects {0.63*f_sort:.2f}")
# sorter count: 2 Mtpa hoisted, ROM up to /(1-rr)
for k,(r,L) in tests.items():
    rr=r*f_sort; feed=H/(1-rr)*f_sort/6500
    print(f"{k:26s} sorter feed {feed:5.0f} t/h -> {int(np.ceil(feed/150))} x 150 t/h XRT units")
