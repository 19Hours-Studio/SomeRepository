# Empirical entropy of exponent fields: BF16 (check vs DFloat11 ~0.70) and FP8 E4M3 with per-block scaling
import torch, numpy as np
torch.manual_seed(0)
def H(x):
    _,c=np.unique(x,return_counts=True); p=c/c.sum(); return -(p*np.log2(p)).sum()
for name,w in [("gauss",torch.randn(4096,4096)*0.02),
               ("student-t3 (heavy tail)",torch.distributions.StudentT(3.).sample((4096,4096))*0.01)]:
    b=w.to(torch.bfloat16).view(torch.int16).numpy().astype(np.int32)&0xFFFF
    eb=(b>>7)&0xFF
    r_bf16=(16-8+H(eb))/16
    # FP8 E4M3 with 128x128 block scaling (DeepSeek-V3 style): scale block amax -> 448
    W=w.reshape(32,128,32,128)
    s=W.abs().amax(dim=(1,3),keepdim=True)/448
    q=(W/s).to(torch.float8_e4m3fn).view(torch.uint8).numpy().astype(np.int32).ravel()
    e8=(q>>3)&0xF
    r_fp8_exp=(8-4+H(e8))/8
    r_fp8_byte=H(q)/8
    print(f"{name}: BF16 exp-coded ratio {r_bf16:.3f} | FP8 exp-only {r_fp8_exp:.3f} | FP8 whole-byte entropy {r_fp8_byte:.3f}")
