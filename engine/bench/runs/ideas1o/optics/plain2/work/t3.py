from fin2 import build
from fast import trace
import numpy as np
d=build(0.5,0.5,300,0.0523,0.01)
g=trace(d['receiver'],d['mirrors'],NX=600,NA=7,ret=True)
for row in g: print(''.join('#' if v else '.' for v in row[300::3]))
