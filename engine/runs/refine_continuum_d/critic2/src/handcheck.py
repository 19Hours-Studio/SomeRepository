import model9 as e9
q, e8, m = e9.q, e9.e8, e9.m
M = e9.M
g=13; D=e9.D(g); print("D(13)=%.3f"%D, "EP bytes/hid per pos per pkg x1.07 = %.3f"%(1.07*(1+3*D*(g-1)/g)/g), "TP =",(  (g-1)/g+2))
f=q.fr(0.55); print("f(0.55)=%.4f tau=%.2f us"%(f, q.tau_f(f)*1e6))
pos=2; b=713; n=b*pos
print("link CSA us", 1.07*n/g*7168*(1+3*D*(g-1)/g)/(1.8e12*0.85)*1e6)
for HO in (4,8,16): print(" HO",HO,"link us", 1.07*n/g*7168*(HO+3*D*(g-1)/g)/(1.53e12)*1e6)
T=max(2*11.07e-6, 11.07e-6+q.tau_f(f)); print("T us",T*1e6, "spd", 1.8/(62*T), "eff", 0.85*2*713*1.8/T/(710*2257))
print("HBM per CSA pkg GB", 88412*(32768*(e8.m.ENTRY)+128*e8.m.ENTRY)/13/1e9, "cap(90%)", 0.9*3*48, "physical", 144)
# failure cost with author's own prefill energy
pr = e9.design_profiles(3, 0.7, 64, ("0.55V wt",))["0.55V wt"][0]
Jc = m.comp_time(M, dict(pr, imb=1.07), 1, 61, q.C128//2) * 2257 / m.DERATE
users_lost = 88412/13; tok = users_lost*q.C128
E = tok*Jc; print("prefill J/tok %.4f; lost users %.0f; re-prefill tokens %.2e; energy %.2e J = %.1f s of the 1.60 MW pod"%(Jc, users_lost, tok, E, E/1.6025e6))
fails = 0.1729*710; print("fails/yr %.0f, annual loss %.4f%% of capacity (answer: 2.7%%, 1.9 h each)"%(fails, fails*E/1.6025e6/(365*86400)*100))
print("mirror 10 W/slot cost: %.2f%%"%(10/2257*100))
print("break-even fraction for 1.63x: 1/1.63 = %.3f -> parity, not 1.63x"%(1/1.63))
# KV-mirror bandwidth per CSA pkg
tps = 2*713*1.8/T/13; print("tok/s per CSA pkg %.2e; compressed KV+idx %.2f GB/s; incl. window entries %.2f GB/s"%(tps, tps*(m.ENTRY+m.IDX_B)/4/1e9, tps*((m.ENTRY+m.IDX_B)/4+m.ENTRY)/1e9))
