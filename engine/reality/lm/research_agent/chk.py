import sys, os
sys.argv = ['x']; __file__ = os.path.abspath('harness.py')
exec(open('harness.py').read().split('if __name__')[0])
for p in sys.stdin.read().split():
    m = load_model(p); n = sum(q.numel() for q in m.parameters() if q.requires_grad)
    x = torch.randint(96, (2, 128)); assert m(x).shape == (2, 128, 96); causal_check(m, torch.Generator().manual_seed(0)); print(p, n, 'ok')
