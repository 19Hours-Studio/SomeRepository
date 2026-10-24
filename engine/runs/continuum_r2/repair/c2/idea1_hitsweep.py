exec(open('idea1_round2.py').read().split('L=131072')[0])
L=131072
print("hit  Vera/GPU  Cont/die  Cont/stack  Vera/stack  stack-ratio")
for hit in [0.0,0.3,0.4,0.5,0.6,0.7,0.87,0.95]:
    v,bv=run(L,100,8,hit,0.6e12,0.6,750e9); c,bc=run(L,100,4,hit,0.7e12,0.5,512e9)
    print(f"{hit:4.2f} {v:7.1f}({bv}) {c:7.1f}({bc}) {c/4:7.1f} {v/8:7.1f} {c/4/(v/8):6.2f}")
