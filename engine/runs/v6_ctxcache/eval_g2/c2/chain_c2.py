# Archetype C GPU cost: prefill 55 at baseline (hash-canonical APC), rest 45 fixed. Prefill ∝ uncached tokens.
rows={(1.05,'inf'):(0.201,0.448,0.890),(1.05,'1k'):(0.100,0.337,0.646),(1.2,'inf'):(0.295,0.598,0.933),
(1.2,'1k'):(0.153,0.477,0.793),(1.5,'inf'):(0.607,0.818,0.980),(1.5,'1k'):(0.354,0.696,0.930)}
D,Q,probe,rec=4.0,0.2,1/32,0.15
for k,(rh,rp,hc) in rows.items():
    base=D*(1-rh)+Q; unit=55/base
    blend=D*((1-hc)+hc*rec)+Q+D*probe
    exact=D*(1-rp)+Q+D*probe
    f=lambda m:100/(45+unit*((1-m)*blend+m*exact))
    mm=next((m/100 for m in range(100,-1,-1) if f(m/100)>=1.5),None)
    print(k,f"m=0.25 ratio={f(0.25):.2f} m=0 {f(0):.2f} m=1 {f(1):.2f} max m for 1.5x={mm} prefill-only m=.25 {base/((0.75)*blend+0.25*exact):.2f}")
