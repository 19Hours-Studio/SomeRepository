# Long single prompt (128K) TTFT: Continuum-P 8-stage pipeline with chunking vs 8x Rubin context/tensor parallel
fl128=399e9; T=131072; util=0.6
for PF,N in ((20e15,8),):
    best=None
    for chunks in range(1,9):
        Tc=T/chunks; tc=Tc*fl128/N/(PF*util); tw=(376e9/N)/(1.37e12*0.8)
        st=max(tc,tw); ttft=(chunks+N-1)*st
        best=min(best or 1e9,ttft); print(f"chunks {chunks}: stage {st*1e3:.0f} ms TTFT {ttft:.2f} s")
    print("Continuum-P best TTFT", round(best,2), "s ; ideal 8-die", round(T*fl128/(N*PF*util),2))
print("8x Rubin ideal (35 PF dense, 0.6, 85% CP efficiency):", round(T*fl128/(8*35e15*util*0.85),2),"s")
