# Idea 1: residual droop guardband after adaptive clocking (POWER9 halves droop margin)
claimed_V=0.10; residual=0.05
dyn=lambda v:1-(1-v)**2
chipshare=0.6; power_terms=0.15+0.20   # ledger A electricity + facility
for v in (residual,0.20):
    s=dyn(v)*chipshare*power_terms; print("I1 V",v,"TCO saved",round(s,3),"ratio",round(1/(1-s),3))
print("I1 margin",residual/claimed_V)
# Idea 2: bits/weight
req=8/3; avail=3.0; print("I2 margin",round(req/avail,2))
nvfp4=4+8/16; w=nvfp4/3.0; f=0.5
print("I2 weight-traffic gain vs NVFP4",w,"Amdahl ratio",round(1/((1-f)+f/w),2))
# Idea 3: density
need_bits=2200*230e6*8; area=5*858
req_d=need_bits/area/1e6; cell=1/0.0249  # Mb/mm2 per layer (bitcell only)
print("I3 req Mb/mm2",round(req_d),"avail/layer",round(cell),"margin 1L",round(cell/req_d,3),"4L",round(4*cell/req_d,3))
# Idea 4: reconfig time budget
tok=10e-3; layers=61; reconf_per_layer=3; overhead=0.10
req_t=tok*overhead/(layers*reconf_per_layer)
print("I4 req us",round(req_t*1e6,1),"margin MEMS 10ms",req_t/10e-3,"Mordia 11.5us",round(req_t/11.5e-6,2))
print("I4 ratio if whole network share removed",round(1/(1-0.11),3))
