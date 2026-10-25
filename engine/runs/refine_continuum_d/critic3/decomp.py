"""Where does the 1.64 come from? Positions per output token, compute energy per FLOP and compute share of slot power, both systems at their chosen points."""
f=((0.55-0.3)/0.45)**1.3*0.75/0.55; e=(0.55/0.75)**2
def tok(k,p=0.8): return sum(p**i for i in range(k+1))
rows={"Rubin >=200":(1,1720,35,1562),"C10 >=200":(0,2640,64,2486),
      "Rubin >=1000":(4,1720,35,1562),"C10 >=1000":(1,2640,64,2303),
      "Rubin >=2000":(6,1720,35,1562),"C10 >=2000":(2,2640,64,2215)}
for n,(k,cw,pf,P) in rows.items():
    ppt=(1+k)/tok(k); wpf=cw/pf; share=cw*f*e*1.146/P
    print(f"{n:<14} k={k} positions/token {ppt:.2f}  compute W/PF(V0) {wpf:.1f}  compute share of slot {share:.2f}")
for t,(r,c_) in {"200":("Rubin >=200","C10 >=200"),"1000":("Rubin >=1000","C10 >=1000"),"2000":("Rubin >=2000","C10 >=2000")}.items():
    kr,kc=rows[r][0],rows[c_][0]
    spec=((1+kr)/tok(kr))/((1+kc)/tok(kc)); node=(1720/35)/(2640/64)
    sh=(2640*f*e*1.146/rows[c_][3])/(1720*f*e*1.146/rows[r][3])
    print(f">={t}: speculative-waste factor {spec:.2f} x node factor {node:.2f} / compute-share factor {sh:.2f} = {spec*node/sh:.2f}")
