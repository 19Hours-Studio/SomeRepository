# idea1: 50-turn agent 20k base +2k/turn; one idle expiry at turn t
for t in (10,25,40):
    ctx=20000+2000*t
    w=20000+2000*50; f=ctx/(w+ctx); print("I1 expiry at turn",t,"f=%.2f"%f)
# I3: 70B, 100k ctx, 2k suffix, 8 GPU TP
kv=320*1024*100000; per=kv/8; print("I3 KV GB/GPU",per/1e9,"fetch ms @50GB/s",per/50e9*1e3)
lin=2*70e9*2000; att=4*100000*2000*8192*80
for mfu in (400e12,):
    c=(lin+att)/8/mfu*1e3; print("compute ms",c,"unoverlapped transfer share",82/(82+c))
# I8
for tok in (2000,4000):
    b=tok*131072
    for ms in (30,):print("I8 GB",b/1e9,"GB/s need",b/(ms/1e3)/1e9)
for bw in (7,26,31.5,50):
    print("bw",bw,[round(bw/(t*131072/0.03/1e9),2) for t in (2000,4000)])
# I9: miss rate for 10% of write term
m=0.1*5000/0.9/100000; print("I9 miss rate/turn",m,"1 per",1/m)
# I7
print("I7",0.26*0.761)
# I4
print("I4 recovered",(0.2611-0.2111)/(0.3833-0.2111),"rel loss",1-0.2611/0.3833)
