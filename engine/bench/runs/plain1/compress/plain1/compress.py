import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decompress as d

c = d.C(1)
d.run(c, sys.stdin.buffer.read().decode('latin-1').split('\n'))
sys.stdout.buffer.write(c.fin())
