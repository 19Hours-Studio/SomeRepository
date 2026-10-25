"""Fallback check with the critic's coupled model: single 70um UTG / soft OCA / panel, Ti foil NOT bonded in fold zone
(t2 -> ~0). Reports residual depth and the panel's folded axial strain (TFT limit ~1%)."""
import critic_oca_coupled2 as C
for G,phi in ((1e4,0.05),(1e5,0.05),(1e4,0.10),(1e6,0.0)):
    for T in (0,1000):
        r=C.solve(G=G,phi=phi,T=T,E2=1e3,t2=1e-9,n=500)
        ep=r['sTi']*1e6/1e3  # sTi = N/EA2*E2 -> strain*E2; recover strain
        print(f"G={G:.0e} phi={phi:.2f} T={T:4d}: depth {r['depth']*1e6:6.2f} um slope {r['slope']*1e3:5.2f} mrad | OCA shear {r['gam']:.1f} | panel extra axial strain {ep*100:.2f}%")
