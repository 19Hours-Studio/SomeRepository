# Shared prices and ore definitions. Sources in LOG.md / notes.
OZ = 31.1035
FX = 85.0          # RUB/USD assumption (2026), sensitivity below
# Base prices (USD): conservative vs Legor May-2026 snapshot (Pt 58.85 EUR/g, Pd 42 EUR/g, Ni 18.28 EUR/kg, Cu 14.02 EUR/kg)
P = dict(Ni=16000., Cu=10500., Pd=1300., Pt=1800.)
P_hi = dict(Ni=21000., Cu=16000., Pd=1550., Pt=2150.)   # Legor snapshot at ~1.15 USD/EUR (includes fabricator premium)

def value_per_t(ore, p=P, rec=None):
    """gross USD per tonne ore; rec = dict of recoveries (default 1)."""
    rec = rec or {}
    v = {}
    v['Ni'] = ore['Ni']/100*p['Ni']*rec.get('Ni',1)
    v['Cu'] = ore['Cu']/100*p['Cu']*rec.get('Cu',1)
    v['Pd'] = ore['Pd']/OZ*p['Pd']*rec.get('PGM',1)
    v['Pt'] = ore['Pt']/OZ*p['Pt']*rec.get('PGM',1)
    return v

def nieq_t(usd, p=P):   # tonnes Ni-eq
    return usd/p['Ni']

# Ores (F1, F2, F7). 6PGM split Pd:Pt assumed ~0.72:0.28 of Pd+Pt (Pd+Pt ~ 92% of 6PGM) for Norilsk ores
def split(pgm6, pd_share=0.67, pt_share=0.25):
    return pgm6*pd_share, pgm6*pt_share
ORES = {
 'Talnakh_proven(F1)':   dict(Ni=0.67, Cu=1.33, Pd=split(4.25)[0], Pt=split(4.25)[1]),
 'Norilsk1_dissem(F2)':  dict(Ni=0.25, Cu=0.33, Pd=split(4.56,0.62,0.30)[0], Pt=split(4.56,0.62,0.30)[1]),
 'Maslovskoye(F7)':      dict(Ni=0.30, Cu=0.50, Pd=5.0, Pt=2.0),
}
