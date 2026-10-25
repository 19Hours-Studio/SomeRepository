import math
# known-answer check: Llama-3.3-70B KV/token = 80 layers*8 kv heads*128 dim*2 (K,V) = 163840 values (=320 KB at BF16, known)
kv_vals=80*8*128*2; assert kv_vals*2==327680
kvB=kv_vals*4.5/8; W70=70.6e9*4.5/8
print("70B NVFP4 weights GB",W70/1e9,"KV/token KB",kvB/1e3)
# ---- Idea 1
cap=4*400*4*64e6/8*(1-0.045); print("I1 cap GB",cap/1e9,"BW/Gb req",44e12/(cap*8/1e9)/1e9)
W1T=1e12*4.5/8; kv1=61*8*128*2*4.5/8*8192  # GQA 1T assumption, 8K
for N in (24,72):
    u_c=(48e9*N-W1T)/kv1/N*1000; u_r=(22e9-W1T/N)/kv1*1000  # tok/s/pkg at 1 ms step
    print("I1 N",N,"tok/s/pkg cont",round(u_c),"rubin",round(u_r),"ratio",u_c/u_r)
def tco(pkg_frac,perf, power_frac):  # Rubin per-package TCO=1 with ledger A shares
    return (0.45*pkg_frac+0.20+0.12*power_frac+0.09*power_frac+0.03+0.11*(0.45*pkg_frac+0.2)/0.65)/perf
for perf in (1.7,2.85):
    print("I1 RATIO",1/tco(8/45,perf,1.2/2.3))
# ---- Idea 2
pkg=8*550+1500+2000; print("I2 pkg $",pkg)
for e in (1.0,1.2): print("I2 RATIO vs Nvidia",1/(0.45*pkg/45e3+0.46+0.09*e))
print("I2 pkg max for 1.5x",(1/1.5-0.46-0.09)/0.45*45e3)
print("I2 vs TPU (assume Ironwood pkg ~$12k at cost)",1/(0.38*pkg/12e3+0.62))
# ---- Idea 3
gross=lambda a:int(math.pi*150**2/a-math.pi*300/math.sqrt(2*a))
good=gross(100)*math.exp(-0.1); die=10e3/good
for tps,ovh in ((1198,7.5e3),(916,7.5e3),(1198,3e3)):
    hw=(544*die+17*ovh)*2; T=hw/0.60; tok=32*tps*0.6*4*3.156e7
    print("I3 die$",round(die),"tps",tps,"$/Mtok",T/(tok/1e6))
stage=1/(1198*17); print("I3 stage us",stage*1e6,"with 5us AR ->",1/(17*(37.7e-6+9.4*5e-6)))
# ---- Idea 4
dieBW=135*6.4e9; t=W70/dieBW; print("I4 per-user tok/s",1/t)
users=(112e9-W70)/(kvB*8192); sys=users/t; print("I4 users",users,"sys tok/s",sys)
hw4=(140*100+5*7.5e3)*2; c4=hw4/0.6/(sys*0.6*4*3.156e7/1e6)
gb=1.86*4*8766/(0.5*(8e12/(W70+users*kvB*8192))*96*0.6*4*3.156e7/1e6)
print("I4 $/Mtok",c4,"B200-class",gb,"RATIO",gb/c4)
