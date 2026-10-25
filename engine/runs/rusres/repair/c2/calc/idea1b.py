import numpy as np
exec(open('idea1.py').read().split('# ---- cost')[0].replace('print(','(lambda *a,**k:None)('))
# sensitivity of Norilsk 2050 margin to R and lateral gain
for Rv in (0.08,0.12,0.2):
  for ql in (5,15,30):
    T=np.array(sites['Norilsk'])+2.5
    e=(np.clip(Tg-dTstart-T,0,None)*days*86400/Rv).sum()/1e9
    L=(27+ql)*8760*3600/1e9
    print(f"R={Rv} q_lat={ql}W: Norilsk-2050 margin {e/L:.2f}; Salekhard-2050",
          round(((np.clip(Tg-dTstart-(np.array(sites['Salekhard'])+2.5),0,None)*days*86400/Rv).sum()/1e9)/L,2))
# program-level comparison, 165 monitored structures, 50 triaged (30%)
rub=85; per=102e6
prog={'A monitor + repair-on-failure (status quo)':None,
 'B blanket retrofit of all 165 structures':165*per,
 'C triaged retrofit of 50 structures (this idea)':50*per+165*2e6,  # +2M RUB/structure InSAR+thermistor triage
 'D underpinning the 50 triaged structures (1-2M RUB/pile x333)':(50*333*1.0e6,50*333*2.0e6)}
for k,v in prog.items():
  if v is None: print(k); continue
  if isinstance(v,tuple): print(f"{k}: ${v[0]/rub/1e6:.0f}-{v[1]/rub/1e6:.0f}M")
  else: print(f"{k}: ${v/rub/1e6:.0f}M")
