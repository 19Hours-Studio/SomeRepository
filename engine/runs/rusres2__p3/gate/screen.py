import sys; sys.path.insert(0,'/home/user/SomeRepository/engine')
from kit import econ, stats, data
fx=data.get('price.fx_rub_usd'); ni=data.get('price.nickel_lme'); cu=data.get('price.copper_conc_delivered_cost')
pd_g=1096/31.1035   # Kitco 17 Oct 2026; used for all 6PGM (conservative for Pt)
def val(ni_pct,cu_pct,pgm): return ni_pct*10*ni/1000+cu_pct*10*cu/1000+pgm*pd_g
v_n1=val(0.25,0.33,4.56); v_mas=val(0.3,0.5,7.0)
print('in-situ $/t Norilsk-1',round(v_n1),' Maslovskoye',round(v_mas))
# IDEA 1 capacity: NOF actual 7.6 Mt (AR2020), nominal 9.3 (AR2018); baseline Norilsk-1 to 730 m at 7 Mtpa to 2048 (AR2024)
mas_rate=206.8/25   # GKZ reserves / ~25 yr life (2012 figure)
print('I1 total margin', 7.6/(7.0+mas_rate), 9.3/(7.0+mas_rate), ' Maslovskoye room', (7.6-7.0)/mas_rate, (9.3-7.0)/mas_rate)
print('I1 ceiling if all concentrator capital (~half of 37%) removed', econ.ceiling_ratio(0.185), ' all capital', econ.ceiling_ratio(0.37))
# IDEA 2 XRT: reject 15.2% mass; processing cost $8-15/t (assumption); payable at 75% recovery
for pc in (8,15):
    be=econ.breakeven_loss_fraction(0.152*pc, v_n1*0.75)
    print('I2 proc',pc,'breakeven loss',round(be,4),'margin vs 2% Selebi loss',round(be/0.02,2))
for g in (1.094,1.156):
    s=(0.22+0.185)*(1-1/(g*0.98)); print('I2 grade',g,'cost cut',round(s,3),'ratio',round(econ.ceiling_ratio(s),3))
# IDEA 3 availability: fixed share f of cost; pts needed for ratio 1.5 at A0=0.93
f=0.8; A0=0.93
x=f/(1/1.5-(1-f))-1; print('I3 output gain needed',round(x,3),'pts',round(x*A0*100,1),'headroom pts',round((0.98-A0)*100,1),'margin',round((0.98-A0)/(x*A0),3))
for dp in (2,5):
    r=1/((1-f)+f/(1+dp/93)); print('I3 +%d pts ratio'%dp, round(r,3))
print('I3 pts to replace +8 Mtpa stage at 10 Mtpa', 80, 'margin', round(5/80,3))
# IDEA 4
full=(5.1+3.0)*1e9   # cash opex 2024 + capex ~2023 (F61,F62)
amb=146.177e9/fx
for yrs in (10,20):
    s=amb/yrs/full+0.02; print('I4 interval',yrs,'share removed',round(s,4),'ratio',round(econ.ceiling_ratio(s),3))
lo,hi=stats.poisson_ci(2); print('I4 poisson 2 events CI',lo,hi)
print('I4 events needed to show halving (two arms, cv=1/sqrt(n))')
# test known: kit example
print(round(econ.breakeven_loss_fraction(74.6,2500),3), econ.ceiling_ratio(0.05))
