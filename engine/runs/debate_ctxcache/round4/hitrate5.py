# Token hit rate (cached input tokens / all input tokens) for the round-4 layouts. Usage: python3 -I hitrate5.py <trajs_dir>
import sys, os, io, contextlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
with contextlib.redirect_stdout(io.StringIO()):
    import trace5 as T5, rag5 as G
R0, W0 = T5.R, T5.W
def hits(fn):
    """re-run fn with prices read=1, write=0 to count hit tokens, then read=0, write=1 to count missed tokens"""
    T5.R, T5.W, T5.O = 1, 0, 0; h = fn(); T5.R, T5.W = 0, 1; m = fn(); T5.R, T5.W, T5.O = R0, W0, 5.0
    return h / (h + m)
for n, p, mode in ((None, 1, "prefix"), (5, 1, "prefix"), (5, 20, "prefix"), (5, 1, "span")):
    print(f"real traces LastN n={n} p={p} {mode}: token hit rate {hits(lambda: sum(T5.run(t, n, p, mode)[0] for t, _ in T5.TR)):.1%}")
for lay in ("sysctx", "tail", "tail_span"):
    G.Rd, G.W, G.O = 1, 0, 0; h = G.rag(lay, drift=0.3)[0]; G.Rd, G.W = 0, 1; m = G.rag(lay, drift=0.3)[0]
    print(f"RAG drift 0.3 {lay}: token hit rate {h/(h+m):.1%}")
