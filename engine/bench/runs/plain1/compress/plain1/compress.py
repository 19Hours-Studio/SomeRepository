import sys, os
g = {'__name__': 'x'}
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'decompress.py')).read(), g)
c = g['C'](True)
g['run'](c, sys.stdin.buffer.read().decode('latin-1').split('\n'))
sys.stdout.buffer.write(c.fin())
