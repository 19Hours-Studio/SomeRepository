# Idea 3: 70B GQA L=80 Hq=64 Hkv=8 d=128
kv_tok=2*80*8*128*2  # bytes/token
print("kv/token KiB",kv_tok/1024)
L=100_000;n=2000
kv=kv_tok*L; print("KV GB",kv/1e9)
# per-GPU on 8-way TP, 50GB/s NIC each
print("fetch s (8 NICs x50GB/s)",kv/8/50e9)
fl=2*70e9*n + 4*80*64*128*n*L  # linear + attention flops
print("prefill GFLOP",fl/1e12,"TFLOP; s on 8 GPU @400TFLOPs eff",fl/8/400e12)
print("transfer/compute",(kv/8/50e9)/(fl/8/400e12))
# attention-offload traffic: q+o per layer
qo=2*n*64*128*2*80; print("q/o bytes GB",qo/1e9,"ratio kv/qo",kv/qo)
# Idea 8
for tok in (2048,4096):
    b=tok*128*1024; print(tok,"GB/step",b/1e9,"GB/s @30ms",b/0.030/1e9)
for bw in(31.5,55): 
  for B in (1,8,32): print("bw",bw,"B",B,"margin",bw/(0.537/0.030*B))
# Idea 9
print("idea9",100e3*1.25/(50*5e3*1.25))
