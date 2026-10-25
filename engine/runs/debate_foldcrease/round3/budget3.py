"""Round-3 full open-state slope budget (relative to the wings), same code for round-2 and round-3 hardware.
theta(x): D th'' - T th = D kres' + p*x   (clamped to wing slope at x=+-a), w = int th.
Terms: material-set crease; uniform pressure p (gravity q, thermal/barometric gas residual) with optional
sealed thin-gap gas cushion (p_gas = -(P0/h)*mean(w)); clamp-line kinks from seat repeatability, frame bow,
through-thickness thermal bow, lamination residual -> K*exp(-(a-|x|)/l). Worst-case linear sum, max over x."""
import numpy as np, math, sys
sys.dont_write_bytecode=True
from scipy.linalg import solve_banded
from design2 import shares
from design3 import solve
tp=30e-6; Dt,Dg,Dp,Da,zt=shares(tp); P0,T0=101.3e3,298.0
q=(2500*40e-6+1400*36e-6)*9.81
def th_solve(x,T,rhs):
    N=len(x); dx=x[1]-x[0]; n=N-2; ab=np.zeros((3,n))
    ab[0,1:]=Dt/dx**2; ab[1,:]=-2*Dt/dx**2-T; ab[2,:-1]=Dt/dx**2
    return np.concatenate([[0],solve_banded((1,1),ab,rhs[1:-1]),[0]])
def integ(th,dx): return np.concatenate([[0],np.cumsum((th[1:]+th[:-1])/2)*dx])
def budget(H,verbose=False):
    g=solve(H['R'],H['Lr1'],H['Lr2']); a=g['half']+H['margin']; T=H['T']
    x=np.linspace(-a,a,12001); dx=x[1]-x[0]; l=math.sqrt(Dt/T)
    eff=(Dp*H['ps']+Da*H['pa']+Dg*H['phig'])/Dt; kr=np.interp(x,g['s'],eff*g['k'],left=0,right=0)
    thc=th_solve(x,T,Dt*np.gradient(kr,dx)); wc=integ(thc,dx)
    thu=th_solve(x,T,1.0*x); wu=integ(thu,dx)          # response to +1 Pa uniform (sign arbitrary)
    m1=abs(wu.mean()); kgas=P0/H['h']
    # loads that act as a uniform pressure: gravity q, plus gas residual from session dT and altitude
    mode=H['mode']; dPeq=H['gas_coef']*H['dT']+H['dPbaro']
    if mode=='vented':  red=1.0; p_net=q+H['dPvent']
    elif mode=='sealed':   # passive: sag at the closing orientation is locked in (worst: closed and viewed face-up)
        red=1/(1+kgas*m1); p_net=q+red*(2*q+dPeq)
    else:                  # 'servo': piezo bridge holds mean gap (capacitive sense) -> net uniform load = residual
        red=1/(1+kgas*m1); p_net=H['servo_res']
    if mode!='vented':
        p_c=-wc.mean()/(m1+1/kgas)*np.sign(wu.mean()); thc=thc+p_c*thu
    thp=p_net*thu
    # clamp-line kink terms (mrad-level magnitudes, rad)
    sd=H['seat_sigma']*H['kfac']
    k_seat=(math.sqrt(2)*sd/H['Lt'])/2+math.sqrt(2)*sd/(2*a)
    k_bow=H['dF']*H['T']*0.15*H['e']/H['EI']*H['Lh']
    k_grad=H['alpha']/H['kth']*H['qflux']*H['Lh']
    K=k_seat+k_bow+k_grad+H['lam']
    # feature A: slope jump across each clamp line = K + |span slope 3l inside the clamp| (crease + pressure)
    j=np.argmin(np.abs(x-(a-3*l))); jj=np.argmin(np.abs(x+(a-3*l)))
    clamp=K+max(abs(thc[j])+abs(thp[j]),abs(thc[jj])+abs(thp[jj]))
    out=dict(a=a,zone=g['zone'],width=g['width'],Rn=g['Rn'],l=l,crease=np.abs(thc).max(),depth=wc.max()-wc.min(),
             press=np.abs(thp).max(),red=red,p_net=p_net,k_seat=k_seat,k_bow=k_bow,k_grad=k_grad,K=K,clamp=clamp,m1=m1,
             interior=(np.abs(thc)+np.abs(thp))[np.abs(x)<a-3*l].max())
    out['total']=max(out['clamp'],out['interior']); return out
base3=dict(R=5.5e-3,Lr1=25e-3,Lr2=9e-3,margin=6e-3,T=4000,ps=0.2,pa=0.1,phig=0.0,mode='servo',servo_res=0.05,h=5e-6,
           gas_coef=100.0,dT=10.0,dPbaro=360.0,dPvent=0.0,seat_sigma=0.1e-6,kfac=3.0,Lt=30e-3,
           dF=0.025,e=0.05e-3,EI=10.0,Lh=38e-3,alpha=8.0e-6,kth=180.0,qflux=100.0,lam=0.002e-3)
pess3=dict(base3,phig=1e-3,servo_res=0.6,h=8e-6,gas_coef=340.0,dPbaro=3600.0,seat_sigma=0.5e-6,dF=0.055,e=0.2e-3,EI=5.0,qflux=300.0)
# round-2 hardware: 15/15 ramps, T=3000, open vented cavity, ordinary detent stop (4 mm lever, 2 um), Al frame +-20%, e 1-2 mm
base2=dict(base3,Lr1=15e-3,Lr2=15e-3,margin=3e-3,T=3000,mode='vented',dPvent=1.0,seat_sigma=2e-6,kfac=1.0,Lt=4e-3,
           dF=0.20,e=1e-3,EI=40.0,alpha=23e-6,kth=160.0,lam=0.0)
pess2=dict(base2,phig=1e-3,dPvent=10.0,seat_sigma=5e-6,e=2e-3,EI=20.0,qflux=300.0)
if __name__=="__main__":
    print(f"q(gravity)={q:.3f} Pa")
    o=budget(base3); print(f"servo gearing: m1={o['m1']:.3e} m/Pa -> 1 nm of mean-gap error = {1e-9/o['m1']:.4f} Pa; gas stiffness/membrane = {P0/base3['h']*o['m1']:.0f}")
    for name,H in (("R2 hardware nominal",base2),("R2 hardware pessimistic",pess2),("R3 nominal",base3),("R3 pessimistic",pess3),
                   ("R3 nominal, phi_g 1e-3",dict(base3,phig=1e-3)),("R3 nominal, phi_g 3e-3",dict(base3,phig=3e-3)),
                   ("R3 nominal, vented cavity (1 Pa) instead of servo",dict(base3,mode='vented',dPvent=1.0)),
                   ("R3 nominal, passive sealed cushion (servo off)",dict(base3,mode='sealed')),
                   ("R3 nominal, feed-forward only (0.3 Pa residual)",dict(base3,servo_res=0.3)),
                   ("R3 nominal, T=3000",dict(base3,T=3000)),("R3 nominal, seat 0.25 um (QKC after wear-in)",dict(base3,seat_sigma=0.25e-6)),
                   ("R3 nominal, seat 0.25 um, tongue 50 mm",dict(base3,seat_sigma=0.25e-6,Lt=50e-3)),
                   ("R3 nominal, Ti housing (alpha/k 8.6/6.7)",dict(base3,alpha=8.6e-6,kth=6.7)),
                   ("R3 nominal, 15/15 ramps",dict(base3,Lr1=15e-3,Lr2=15e-3)),
                   ("R3 nominal, R=7 35/10",dict(base3,R=7e-3,Lr1=35e-3,Lr2=10e-3)),
                   ("R3 nominal, R=7 35/10, tongue 50 mm",dict(base3,R=7e-3,Lr1=35e-3,Lr2=10e-3,Lt=50e-3)),
                   ("R3 pessimistic except seat 0.25 um, e 0.05 mm",dict(pess3,seat_sigma=0.25e-6,e=0.05e-3))):
        o=budget(H)
        print(f"{name:48s}: zone {o['zone']*1e3:.0f} a {o['a']*1e3:.1f} width {o['width']*1e3:.1f} l {o['l']*1e3:.2f} mm | crease {o['crease']*1e3:.4f} (depth {o['depth']*1e6:.2f} um)"
              f" press {o['press']*1e3:.4f} (p_net {o['p_net']:.3f} Pa, gas factor {o['red']:.2e}) | kinks seat {o['k_seat']*1e3:.4f} bow {o['k_bow']*1e3:.4f} grad {o['k_grad']*1e3:.4f}"
              f" | interior {o['interior']*1e3:.4f} clamp-line {o['clamp']*1e3:.4f} -> worst {o['total']*1e3:.4f} mrad")
