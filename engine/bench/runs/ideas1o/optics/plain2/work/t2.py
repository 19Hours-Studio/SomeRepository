from fin2 import build
from fast import score
for xmin in [0.01,0.03,0.06]:
    for N in [100,300]:
        print(xmin,N,*score(build(0.5,0.5,N,0.0523,xmin)),flush=True)
