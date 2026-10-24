# Idea 2 round 2: detached attention stacks (SPHBM4-style organic mount) vs best practice, Llama-3.1-70B-class @128K
hrs=4*8766; elec=0.08; pue=1.25; sysov=0.35; fac_W=10.0; fac_hrs=10*8766
def cph(capex,W,sys=sysov): return capex*(1+sys)/hrs + W*pue/1000*elec + W*pue*fac_W/fac_hrs
kv_u={'FP8':21.5e9,'FP4':12.1e9}; Wt=39e9; fl_tok=140e9
def rubin_only(kv,cost):
    users=int((288e9*0.9-Wt)/kv_u[kv]); step=(Wt+users*kv_u[kv])/(22e12*0.85)
    return users, step, cph(cost,2000)/(users/step*3600)*1e6
def h200_lamina(kv,cost_h200,cost_rubin):     # attention on H200 pool, FFN on Rubin
    u=int(141e9*0.9/kv_u[kv]); step=u*kv_u[kv]/(4.8e12*0.85)
    B=int(step*17.5e15*0.6/fl_tok); n_h=B/u      # Rubin batch sized to step
    capex=cost_rubin+n_h*cost_h200; W=2000+n_h*700
    return u, step, cph(capex,W)/(B/step*3600)*1e6
def stacks(kv,cost_stack,cost_rubin,BW=2.5e12,fill=0.9):
    cap=48e9*fill; u=cap/kv_u[kv]; step=cap/(BW*0.85)
    B=int(step*17.5e15*0.6/fl_tok); n_s=B/u
    capex=cost_rubin+n_s*cost_stack; W=2000+n_s*72
    return u, step, cph(capex,W)/(B/step*3600)*1e6, n_s
die=60; stack_cogs=48*16+die+80+250
print(f"attention-stack node COGS ${stack_cogs}")
for view,(rub,h2,st) in {"COGS":(8311,3800,stack_cogs),"price":(55000,30000,stack_cogs/0.4)}.items():
    for kv in ('FP8','FP4'):
        a=rubin_only(kv,rub); c=h200_lamina(kv,h2,rub); s=stacks(kv,st,rub)
        print(f"[{view} {kv}] Rubin-only: {a[0]} users, {1/a[1]:.0f} tok/s/u, ${a[2]:.3f}/Mtok | "
              f"Lamina(H200 attn): {1/c[1]:.0f} tok/s/u ${c[2]:.3f}/Mtok | "
              f"AttnStacks: {1/s[1]:.0f} tok/s/u, {s[3]:.0f} stacks/Rubin, ${s[2]:.3f}/Mtok | best-baseline/stacks = {min(a[2],c[2])/s[2]:.2f}x")
# energy per decode token, KV part only (FP8, 128K)
for lab,pj in (("GPU-attached",5.34),("in-base-die",3.58)):
    print(f"KV energy/token/user {lab}: {kv_u['FP8']*8*pj*1e-12:.2f} J")
# sensitivity: HBM4 at $32/GB (Samsung ask) and short context 16K
st32=48*32+die+80+250
print("HBM4 $32/GB COGS: stacks", round(stacks('FP8',st32,8311)[2],3), "vs Rubin-only(HBM $32)", round(rubin_only('FP8',8311+288*16)[2],3))
kv_u['FP8_16K']=21.5e9/8
a=rubin_only('FP8_16K',8311); s=stacks('FP8_16K',stack_cogs,8311)
print(f"16K ctx: Rubin-only {a[0]} users ${a[2]:.4f}/Mtok vs stacks ${s[2]:.4f}/Mtok -> {a[2]/s[2]:.2f}x")
# thermal 1-D: 16-high, per-interface R; heat through interface i = base + DRAM below
A=110e-6; t=10e-6
for k in (1.5,3.0):
    R=t/(k*A); P_d=51/16
    for base in (5,17):
        dT=sum((base+P_d*i)*R for i in range(16))
        print(f"k_int {k} W/mK, base {base} W: base-die rise over top {dT:.1f} K")
