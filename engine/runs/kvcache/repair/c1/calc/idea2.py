# Idea 2: probe-gated per-layer FP8 KV. Configs from public model cards (config.json values quoted in NOTES).
import math
models={ # name: layers, kv_heads, head_dim, sliding layers(count, window), weights GB
 "R1-Distill-Qwen-7B":(28,4,128,(0,0),15.2),
 "Qwen2.5-7B-Instruct":(28,4,128,(0,0),15.2),
 "Gemma-3-1B-IT":(26,1,256,(22,512),2.0),
 "Llama-3.1-8B":(32,8,128,(0,0),16.1),
}
def kv_bytes(m,ctx,bf16_layers=set(),skip_sliding=True):
    Lr,H,D,(ns,win),_=models[m]; tot=0
    for l in range(Lr):
        sliding = ns>0 and (l%6!=5)           # Gemma3 5 local : 1 global
        toks=min(ctx,win) if sliding else ctx
        bpe=2 if (l in bf16_layers or (sliding and skip_sliding)) else 1
        tot+=2*H*D*toks*bpe
    return tot
def bf16(m,ctx):
    Lr,H,D,(ns,win),_=models[m]
    return sum(2*H*D*(min(ctx,win) if ns and l%6!=5 else ctx)*2 for l in range(Lr))
HBM=80e9*0.9-4e9
for m,ctx,gate in [("R1-Distill-Qwen-7B",32768,{27}),("R1-Distill-Qwen-7B",32768,{0,27}),("R1-Distill-Qwen-7B",32768,set(range(0,28,2))),
                   ("Gemma-3-1B-IT",32768,set()),("Gemma-3-1B-IT",32768,{5}),("Gemma-3-1B-IT",32768,{5,11,17,23}),("Llama-3.1-8B",32768,set())]:
    b=bf16(m,ctx); g=kv_bytes(m,ctx,gate); W=models[m][4]*1e9
    Bb=int((HBM-W)//b); Bg=int((HBM-W)//g)
    # decode tokens/s, memory bound: step=(W+B*kv)/BW ; compute check at 989 TFLOPs dense
    BW=3.35e12*0.8
    def tps(B,kvb): return B/((W+B*kvb)/BW)
    print(f"{m:20s} ctx {ctx} gated {len(gate):2d} layers: KV/req BF16 {b/1e9:.3f} GB gated {g/1e9:.3f} GB "
          f"ratio {b/g:.2f}x  maxB {Bb}->{Bg}  decode tok/s ratio {tps(Bg,g)/tps(Bb,b):.2f}x  FP8-all ratio {b/kv_bytes(m,ctx,set()):.2f}x")
# Probe cost: 100 prompts x 32K x 2 arms (+1 fake-quant arm), prefill + 512 teacher-forced tokens
P=100; ctx=32768; params=7.6e9; L=28; dm=3584
fl=(2*params*(ctx+512)+2*L*dm*(ctx+512)**2)*P*3
print(f"probe FLOPs {fl:.2e} -> {fl/400e12/60:.1f} GPU-min at 400 TFLOP/s; ${fl/400e12/3600*2.5:.2f} at $2.5/h")
# Falsification sample size: paired McNemar, detect delta accuracy d with discordance p_d
from statistics import NormalDist
z=NormalDist().inv_cdf
for d,pd in [(0.03,0.10),(0.05,0.15),(0.10,0.25)]:
    n=((z(0.975)*math.sqrt(pd)+z(0.8)*math.sqrt(pd-d*d))/d)**2
    print(f"detect RULER gap {d:.0%} (discordance {pd:.0%}): n = {math.ceil(n)} paired items per arm")
# Rank stability of per-layer probe: with N prompts, SE of per-layer mean KL ~ sd/sqrt(N); need sep > 3 SE
for N in [20,50,100]: print(f"N={N}: outlier layer detectable if its KL exceeds the median by >{3/math.sqrt(N):.2f} x per-prompt sd")
