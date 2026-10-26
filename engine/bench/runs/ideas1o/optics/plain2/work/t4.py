from fin2 import build
from fast import trace
import numpy as np
for w in [0.0523,0.07,0.1,0.3]:
    d=build(0.5,0.5,300,w,0.01)
    g=trace(d['receiver'],d['mirrors'],NX=600,NA=7,ret=True)
    print(w, g.mean(axis=1))
