import sys, os, re, time, calendar

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import decompress as g

LRE = re.compile(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)\.(\d{3})Z (\d+)\.(\d+)\.(\d+)\.(\d+) "(\S+) (\S+) (\S+)" '
                 r'(\d+) (\d+) (\d+)ms "([^"]*)" "([^"]*)"$')
N = r'([1-9]\d{0,8})'
PATS = [
    ('i', re.compile(r'/api/v2/items/%s$' % N)),
    ('r', re.compile(r'/api/v2/items/%s/reviews\?page=%s$' % (N, N))),
    ('c', re.compile(r'/api/v2/users/%s/cart$' % N)),
    ('g', re.compile(r'/static/img/([^/+]+)\.png$')),
    ('j', re.compile(r'/static/js/app\.([^/+]+)\.js$')),
    ('s', re.compile(r'/search\?q=([^+]+(?:\+[^+]+)*)$')),
]


def parse(line):
    # split a log line into the record tuple used by the codec, or None if it doesn't round-trip
    m = LRE.match(line)
    if not m:
        return None
    x = m.groups()
    try:
        ms = calendar.timegm(time.strptime(x[0], '%Y-%m-%dT%H:%M:%S')) * 1000 + int(x[1])
    except Exception:
        return None
    ip = tuple(int(v) for v in x[2:6])
    if max(ip) > 255:
        return None
    path = x[7]
    for cls, rx in PATS:
        mm = rx.match(path)
        if mm:
            params = mm.groups()
            if cls == 's':
                params = params[0].split('+')
            break
    else:
        cls = '=' + path; params = ()
    if x[6] == '' or x[8] == '' or '"' in x[12] + x[13]:
        return None
    r = (ms, ip, (x[6], cls), params, x[8], x[9], int(x[10]), int(x[11]), x[12], x[13])
    try:
        return r if g.fm(r) == line else None
    except Exception:
        return None


g.parse = parse
g.E = 1
g.C = g.K()
g.run(sys.stdin.buffer.read().decode('latin-1').split('\n'))
sys.stdout.buffer.write(g.C.fin())
