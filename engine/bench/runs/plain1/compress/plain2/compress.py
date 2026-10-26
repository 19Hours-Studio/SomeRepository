import sys, os
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'decompress.py')).read()
g = {'__name__': 'codec'}
exec(compile(src, 'decompress.py', 'exec'), g)
g['ENC'] = True
g['C'] = g['Coder']()
lines = sys.stdin.buffer.read().decode('latin-1').split('\n')
g['run'](lines)
sys.stdout.buffer.write(g['C'].finish())
if os.environ.get('COSTS'):
    for k, v in sorted(g['COST'].items(), key=lambda x: -x[1]):
        sys.stderr.write('%-10s %9.0f\n' % (k, v / 8))
