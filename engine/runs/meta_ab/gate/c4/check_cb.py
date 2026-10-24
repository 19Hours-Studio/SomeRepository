import numpy as np, importlib.util
spec=importlib.util.spec_from_file_location("m","measure.py")
src=open("measure.py").read().split("# synthetic LLM-like")[0]; exec(src)
rng=np.random.default_rng(1)
O,I=256,1024
for name,W in [("gauss",rng.standard_normal((O,I))),("t5*lognorm ch",rng.standard_t(5,(O,I))*np.exp(0.6*rng.standard_normal(I))[None])]:
    def int4g(w,G=128):
        r=w.reshape(-1,G); s=np.abs(r).max(1,keepdims=True)/7; return (np.clip(np.round(r/s),-7,7)*s).reshape(w.shape)
    def cbg(w,G,it):
        r=w.reshape(-1,G); return np.stack([kmeans1d(x,16,it) for x in r]).reshape(w.shape)
    print(name, "NVFP4",round(sqnr(W,nvfp4(W)),2),"INT4/g128",round(sqnr(W,int4g(W)),2),
          "CB16/g128 it25",round(sqnr(W,cbg(W,128,25)),2),"it100",round(sqnr(W,cbg(W,128,100)),2),"CB16/g16",round(sqnr(W,cbg(W,16,25)),2))
W=rng.standard_t(5,(O,I))*np.exp(0.6*rng.standard_normal(I))[None]
Wt=W.T.copy()  # groups of 128 output rows within a single input channel
print("t5*lognorm, CB16 grouped within input channel:",round(sqnr(Wt,cbg(Wt,128,25)),2),"CB8:",round(sqnr(Wt,np.stack([kmeans1d(x,8,25) for x in Wt.reshape(-1,128)]).reshape(Wt.shape)),2),
      "NVFP4 same:",round(sqnr(W,nvfp4(W)),2),"FP8:",round(sqnr(W,fp8_tensor(W)),2))
