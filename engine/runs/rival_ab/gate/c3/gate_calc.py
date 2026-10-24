# Idea 2: tiled-GEMM arithmetic intensity (FP8 operands, 1 B/elem, output tile resident on chip)
def gemm(M,N,K,tile=8192):
    # output M x N tiled into <=tile x tile blocks; each block streams (m+n)*K bytes
    import math
    fl=2*M*N*K; by=0
    for i in range(math.ceil(M/tile)):
        m=min(tile,M-i*tile)
        for j in range(math.ceil(N/tile)):
            n=min(tile,N-j*tile); by+=(m+n)*K
    return fl,by
# known-answer check: square 8192 GEMM -> 2*8192^2/(2*8192)=8192 FLOP/B
f,b=gemm(8192,8192,8192); print("check square intensity",f/b)
d,fexp=7168,2048  # DeepSeek-V3 hidden, expert intermediate
for t in (2048,8192,32768):
    F=B=0
    for (din,dout) in ((d,fexp),(d,fexp),(fexp,d)):  # gate, up, down
        for (M,N,K) in ((t,dout,din),(t,din,dout),(din,dout,t)):  # fwd, dgrad, wgrad
            a,c=gemm(M,N,K); F+=a; B+=c
    print(f"tokens/expert/die {t}: expert-FFN step intensity {F/B:.0f} FLOP/B")
bw_ch=38.4e9; bw=32*bw_ch; print("LPDDR6 32ch BW TB/s",bw/1e12,"required FLOP/B at 5PF",5e15/bw)
# Idea 4: tokens per kW
gb300=12534*72/135; cont=1e5/32; print("GB300 tok/s/kW",gb300,"idea4",cont,"ratio",cont/gb300,"margin vs 3x",cont/(3*gb300))
kv8k=656*61*8192; print("MLA KV per step @8K MB",kv8k/1e6,"tile LPDDR BW needed for 1e5 tok/s TB/s",1e5*kv8k/80/1e12)
# Idea 3: LPDDR efficiency required
print("idea3 required LPDDR eff",150*4.1e9/1e12, "HBM need TB/s",150*52e9/1e12)
