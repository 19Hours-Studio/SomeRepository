import sys
sys.path.insert(0, "/home/user/SomeRepository/engine/runs/refine_continuum_d/round3")
import sens10 as S
from multiprocessing import Pool
q = S.q
jobs = [("PAIR eta+leak", S.merge(S.SINGLES["eta 0.5 (Continuum only)"], S.SINGLES["leakage x2"]), q.C128),
        ("eta 0.5 1M", S.SINGLES["eta 0.5 (Continuum only)"], q.C1M)]
if __name__ == "__main__":
    with Pool(2) as p:
        for n, ctx, r, v in p.imap(S.run, jobs): print(ctx // 1024, n, r, v, flush=True)
