# Sensitivity of the headline ratios to the chars/token estimate (answer assumes 3.5).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import traces as T, probe_lib as P
W, R = T.PRICES["anthropic"]
Tr = T.load(sys.argv[1])
for ch in (2.8, 3.5, 4.2):
    T.CH = ch; tot = {}
    for tr in Tr:
        ntok = [T.tok(s) for s in tr["text"]]
        for k, s in (("append", T.policy_seq(tr, ntok, "append", W, R)), ("sliding", T.policy_seq(tr, ntok, "sliding", W, R)),
                     ("batch5k", T.policy_seq(tr, ntok, "batch", W, R, 5000)), ("horizon", P.horizon_seq(tr, ntok)),
                     ("polling10", P.polling_seq(tr, ntok, 10))):
            tot[k] = tot.get(k, 0) + T.bill(s, W, R)[0]
    print(f"chars/token={ch}: " + "  ".join(f"{k} vs sliding {tot[k]/tot['sliding']-1:+.1%} / vs append {tot[k]/tot['append']-1:+.1%}" for k in ("batch5k", "horizon", "polling10")))
