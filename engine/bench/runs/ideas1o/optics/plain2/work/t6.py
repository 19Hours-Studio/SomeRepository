import fan, numpy as np
d=fan.build()
M=d['mirrors'][:len(d['mirrors'])//2]
for k in range(30,len(M)):
    m=np.array(M[k]); print(k, np.round(m[0],3), np.round(m[-1],3))
