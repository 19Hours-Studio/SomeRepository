import sys, math
sys.argv=['x','131072','1']
import model2 as m
s=m.CONT
for tau in (5e-6,):
  for b in (64,128,200,256,300,350,400):
    lay_b=m.N_EXP*m.B_EXP+m.B_DENSE_LAYER; g=2
    kvl=b*m.kv_store(m.CTX)
    sram=(m.touched(b*m.POS)*m.B_EXP+m.B_DENSE_LAYER)/(g*s['srambw'])
    kv=b*m.kv_read(m.CTX)/m.LAYERS/(g*s['hbmbw'])
    comp=b*m.POS*(m.LIN_FLOPS/s['F4']+m.attn_flops(m.CTX)/s['F8'])/m.LAYERS/g/m.ETA
    print(b, f"KV/pkg {kvl/2/1e9:.0f}GB sram {sram*1e6:.1f} kv {kv*1e6:.1f} comp {comp*1e6:.1f} us")
r=m.SYS['Rubin NVL72']
for tier,p in zip(m.TIERS, m.best(m.gpu_points(r,15e-6))): print('Rubin15',tier,p)
for tier,p in zip(m.TIERS, m.best(m.pipe_points(s,5e-6))): print('Cont5',tier,p)
