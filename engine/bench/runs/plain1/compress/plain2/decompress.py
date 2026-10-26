import sys, re, time, calendar
from math import log2, log, exp, erf

ENC = False
COST = {}
TAG = ['?']
C = None
TOT = 1 << 24


class Coder:
    def __init__(self, data=None):
        self.rng = (1 << 48) - 1
        if data is None:
            self.low = 0; self.cache = 0; self.csize = 1; self.out = bytearray()
        else:
            self.d = data; self.p = 7
            self.code = int.from_bytes(data[1:7], 'big')

    def shift(self):
        low = self.low
        if low < 0xFF << 40 or low >= 1 << 48:
            c = low >> 48
            t = self.cache
            while True:
                self.out.append((t + c) & 255)
                t = 255
                self.csize -= 1
                if not self.csize:
                    break
            self.cache = (low >> 40) & 255
        self.csize += 1
        self.low = (low & 0xFFFFFFFFFF) << 8

    def enc(self, cum, f, tot):
        COST[TAG[0]] = COST.get(TAG[0], 0) + log2(tot / f)
        r = self.rng // tot
        self.low += r * cum
        self.rng = r * f
        while self.rng < 1 << 40:
            self.rng <<= 8
            self.shift()

    def finish(self):
        for _ in range(7):
            self.shift()
        return bytes(self.out)

    def getf(self, tot):
        self.r = r = self.rng // tot
        v = self.code // r
        return v if v < tot else tot - 1

    def upd(self, cum, f):
        self.code -= cum * self.r
        self.rng = self.r * f
        while self.rng < 1 << 40:
            self.rng <<= 8
            self.code = (self.code << 8) | (self.d[self.p] if self.p < len(self.d) else 0)
            self.p += 1


def codef(freqs, i):
    # code index i given integer frequency list
    t = sum(freqs)
    if ENC:
        C.enc(sum(freqs[:i]), freqs[i], t)
        return i
    v = C.getf(t)
    cum = 0; i = 0
    while cum + freqs[i] <= v:
        cum += freqs[i]; i += 1
    C.upd(cum, freqs[i])
    return i


def raw(v, nbits):
    while nbits > 0:
        k = min(nbits, 16)
        nbits -= k
        if ENC:
            C.enc((v >> nbits) & ((1 << k) - 1), 1, 1 << k)
        else:
            x = C.getf(1 << k)
            C.upd(x, 1)
            v = (v or 0) | (x << nbits)
    return v


class Bit:
    __slots__ = ('a', 'b')

    def __init__(self):
        self.a = self.b = 0.4

    def code(self, b):
        p = int(4096 * self.b / (self.a + self.b))
        p = 1 if p < 1 else 4095 if p > 4095 else p
        if ENC:
            if b:
                C.enc(0, p, 4096)
            else:
                C.enc(p, 4096 - p, 4096)
        else:
            b = C.getf(4096) < p
            if b:
                C.upd(0, p)
            else:
                C.upd(p, 4096 - p)
        if b:
            self.b += 1
        else:
            self.a += 1
        if self.a + self.b > 4096:
            self.a *= 0.5; self.b *= 0.5
        return b


ESC = object()


class Freq:
    def __init__(self, inc=8, esc=1):
        self.s = [ESC]; self.c = [esc]; self.ix = {}
        self.t = esc; self.inc = inc

    def code(self, sym):
        c = self.c
        if ENC:
            i = self.ix.get(sym, 0)
            C.enc(sum(c[:i]), c[i], self.t)
        else:
            v = C.getf(self.t)
            cum = 0; i = 0
            while cum + c[i] <= v:
                cum += c[i]; i += 1
            C.upd(cum, c[i])
        if i == 0:
            return ESC
        c[i] += self.inc; self.t += self.inc
        if self.t > 1 << 16:
            self.rescale()
        return self.s[i]

    def add(self, sym):
        self.ix[sym] = len(self.s)
        self.s.append(sym); self.c.append(self.inc)
        self.c[0] += 1
        self.t += self.inc + 1

    def rescale(self):
        c = self.c
        for i in range(len(c)):
            c[i] = (c[i] + 1) >> 1
        self.t = sum(c)


MODELS = {}


def M(key, factory=Freq):
    m = MODELS.get(key)
    if m is None:
        m = MODELS[key] = factory()
    return m


def num(ctx, v):
    m = M(('nb', ctx))
    nb = v.bit_length() if ENC else None
    r = m.code(nb)
    if r is ESC:
        nb = raw(nb, 7)
        m.add(nb)
    else:
        nb = r
    if nb <= 1:
        return nb
    val = 1
    k = nb - 1
    top = min(k, 3)
    for j in range(top):
        b = M(('nbit', ctx, nb, val), Bit).code(((v >> (k - 1 - j)) & 1) if ENC else None)
        val = (val << 1) | b
    k -= top
    if k:
        val = (val << k) | raw(v & ((1 << k) - 1) if ENC else None, k)
    return val


def cdfnum(ctx, v, F, hi):
    # code int v in [0, hi] with continuous cdf F on cells [v-.5, v+.5]; escape above
    S = TOT - hi - 2
    cum = lambda x: int(F(x - 0.5) * S) + x
    top = cum(hi + 1)
    if ENC:
        if v > hi:
            C.enc(top, TOT - top, TOT)
            return num(ctx, v - hi - 1) + hi + 1
        a = cum(v)
        C.enc(a, cum(v + 1) - a, TOT)
        return v
    t = C.getf(TOT)
    if t >= top:
        C.upd(top, TOT - top)
        return num(ctx, None) + hi + 1
    lo, h = 0, hi
    while lo < h:
        mid = (lo + h + 1) >> 1
        if cum(mid) <= t:
            lo = mid
        else:
            h = mid - 1
    a = cum(lo)
    C.upd(a, cum(lo + 1) - a)
    return lo


class LogN:
    def __init__(self):
        self.n = 2.0; self.s = 6.0; self.q = 20.0

    def code(self, ctx, v):
        n = self.n
        mu = self.s / n
        sd = max((self.q / n - mu * mu) ** 0.5, 0.03) * 1.414213562
        F = lambda x: 0.0 if x <= 0 else 0.5 * (1 + erf((log(x) - mu) / sd))
        v = cdfnum(ctx, v, F, 8191)
        lv = log(max(v, 0.5))
        self.n += 1; self.s += lv; self.q += lv * lv
        return v


def sym(key, v, lit=None, **kw):
    m = M(key, lambda: Freq(**kw))
    r = m.code(v)
    if r is ESC:
        v = (lit or string)(v)
        m.add(v)
        return v
    return r


def string(s):
    n = num('slen', len(s) if ENC else None)
    out = ''
    for i in range(n):
        ch = s[i] if ENC else None
        ch = sym(('c2', out[-2:]), ch, lambda x: sym(('c0',), x, lambda y: chr(raw(ord(y) if ENC else None, 8))), inc=4)
        out += ch
    return out


def words(s):
    n = num('wn', s.count(' ') + 1 if ENC else None)
    p = ''; o = []
    for x in s.split(' ') if ENC else [None] * n:
        p = sym(('w1', p), x, lambda y: sym(('w0',), y), inc=4)
        o.append(p)
    return ' '.join(o)


def flag(key, b):
    return M(key, Bit).code(b)


LRE = re.compile(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)\.(\d{3})Z (\d+)\.(\d+)\.(\d+)\.(\d+) "(\S+) (\S+) (\S+)" (\d+) (\d+) (\d+)ms "([^"]*)" "([^"]*)"$')
N = r'([1-9]\d{0,8})'
PATS = {
    'item': (re.compile(r'/api/v2/items/%s$' % N), '/api/v2/items/%s'),
    'rev': (re.compile(r'/api/v2/items/%s/reviews\?page=%s$' % (N, N)), '/api/v2/items/%s/reviews?page=%s'),
    'cart': (re.compile(r'/api/v2/users/%s/cart$' % N), '/api/v2/users/%s/cart'),
    'img': (re.compile(r'/static/img/([^/+]+)\.png$'), '/static/img/%s.png'),
    'js': (re.compile(r'/static/js/app\.([^/+]+)\.js$'), '/static/js/app.%s.js'),
    'search': (re.compile(r'/search\?q=([^+]+(?:\+[^+]+)*)$'), '/search?q=%s'),
}
HOST = 'https://shop.example.com'


def fmt_ts(ms):
    t = time.gmtime(ms // 1000)
    return '%04d-%02d-%02dT%02d:%02d:%02d.%03dZ' % (t[0], t[1], t[2], t[3], t[4], t[5], ms % 1000)


def parse(line):
    m = LRE.match(line)
    if not m:
        return None
    g = m.groups()
    try:
        ms = calendar.timegm(time.strptime(g[0], '%Y-%m-%dT%H:%M:%S')) * 1000 + int(g[1])
    except Exception:
        return None
    ip = tuple(int(x) for x in g[2:6])
    if max(ip) > 255:
        return None
    path = g[7]
    for cls, (rx, tpl) in PATS.items():
        mm = rx.match(path)
        if mm:
            params = mm.groups()
            if cls == 'search':
                params = params[0].split('+')
            break
    else:
        cls = '=' + path; params = ()
    f = dict(ms=ms, ip=ip, mc=(g[6], cls), params=params, proto=g[8], st=g[9], size=int(g[10]),
             lat=int(g[11]), ref=g[12], ua=g[13])
    return f if fmt_line(f) == line else None


def mkpath(mc, params):
    cls = mc[1]
    if cls[0] == '=':
        return cls[1:]
    if cls == 'search':
        params = ('+'.join(params),)
    return PATS[cls][1] % tuple(params)


def fmt_line(f):
    return '%s %d.%d.%d.%d "%s %s %s" %s %d %dms "%s" "%s"' % (
        fmt_ts(f['ms']), *f['ip'], f['mc'][0], mkpath(f['mc'], f['params']), f['proto'], f['st'], f['size'],
        f['lat'], f['ref'], f['ua'])


class IPState:
    def __init__(self):
        self.ua = None; self.path = None; self.user = None; self.items = {}


class State:
    def __init__(self):
        self.ips = {}
        self.lastms = 0
        self.nl = 0
        self.pip = None
        self.sizes = {}
        self.gid = []; self.gcnt = {}; self.gtot = 0


ALPHA = 16.0


def ritem(S, h, v):
    # item id: per-ip counts smoothed toward global counts
    TAG[0] = 'item'
    ids = S.gid; g = S.gcnt
    E = 1 + len(ids)
    k = ALPHA / (S.gtot + E)
    w = [E * k] + [h.get(j, 0) + g[j] * k for j in ids]
    sc = (TOT - len(w)) / sum(w)
    fr = [int(x * sc) + 1 for x in w]
    if ENC:
        v = int(v)
        i = ids.index(v) + 1 if v in g else 0
    i = codef(fr, i if ENC else None)
    if i:
        v = ids[i - 1]
    else:
        v = num('gidn', v)
        ids.append(v); g[v] = 0
    g[v] += 1; S.gtot += 1
    h[v] = h.get(v, 0) + 1
    return str(v)


def code_line(S, f):
    TAG[0] = 'time'
    d = f['ms'] - S.lastms if ENC else None
    neg = flag(('tneg',), d < 0 if ENC else None)
    dm = (S.lastms - S.t0) / (S.nl - 1) if S.nl > 10 else 250.0
    F = lambda x: 0.0 if x <= 0 else 1 - exp(-x / dm)
    a = cdfnum('dt', (-d if neg else d) if ENC else None, F, 1 << 14)
    d = -a if neg else a
    ms = S.lastms = S.lastms + d
    if S.nl == 0:
        S.t0 = ms
    S.nl += 1
    TAG[0] = 'ip'
    pip = S.pip
    if ENC:
        ip = f['ip']
    z = flag(('r0',), ip == pip if ENC else None) if pip else False
    if z:
        ip = pip
    else:
        ip = sym(('ipf',), ip if ENC else None, newip, inc=1)
    st = S.ips.get(ip)
    new = st is None
    if new:
        st = S.ips[ip] = IPState()
    S.pip = ip
    TAG[0] = 'ua'
    same = flag(('uasame',), f['ua'] == st.ua if ENC else None) if not new else False
    ua = st.ua = st.ua if same else sym(('ua',), f['ua'] if ENC else None, words)
    TAG[0] = 'mc'
    mc = sym(('mc',), f['mc'] if ENC else None, lambda x: (string(x[0] if ENC else None), string(x[1] if ENC else None)))
    cls = mc[1]
    TAG[0] = cls
    P = f['params'] if ENC else None
    if cls == 'item':
        params = (ritem(S, st.items, P[0] if ENC else None),)
    elif cls == 'rev':
        it = ritem(S, st.items, P[0] if ENC else None)
        TAG[0] = 'page'
        params = (it, str(num(('page',), int(P[1]) if ENC else None)))
    elif cls == 'cart':
        u = int(P[0]) if ENC else None
        same = flag(('usame', st.user is None), u == st.user if ENC else None)
        u = st.user = st.user if same else num('user', u)
        params = (str(u),)
    elif cls == 'search':
        n = sym(('sn',), len(P) if ENC else None, lambda x: num('snn', x))
        params = [sym(('sw',), P[j] if ENC else None) for j in range(n)]
    elif cls in ('img', 'js'):
        params = (sym(('nm', cls), P[0] if ENC else None),)
    else:
        params = ()
    TAG[0] = 'proto'
    proto = sym(('proto',), f['proto'] if ENC else None)
    TAG[0] = 'st'
    stt = sym(('st', mc), f['st'] if ENC else None)
    path = mkpath(mc, params)
    TAG[0] = 'size'
    key = ('cart', params[0], stt) if cls == 'cart' else (path, stt)
    pred = S.sizes.get(key)
    if pred is None and stt != '200':
        pred = S.sizes.get(stt)
    size = f['size'] if ENC else None
    hit = False
    if cls == 'search' and stt == '200':
        base = 800 + 37 * (len(path) - 10)
        if flag(('srch',), 0 <= size - base < 16 if ENC else None):
            size = base + sym(('srd',), size - base if ENC else None, lambda x: raw(x, 4))
            hit = True
    if not hit and pred is not None:
        hit = flag(('shit', cls, stt), size == pred if ENC else None)
        if hit:
            size = pred
    if not hit:
        size = num(('size', cls), size)
    S.sizes[key] = size
    if stt != '200':
        S.sizes[stt] = size
    TAG[0] = 'lat'
    lc = '500' if stt == '500' else 'st' if cls in ('img', 'js') else cls
    lat = M(('lat', lc), LogN).code(('lat', lc), f['lat'] if ENC else None)
    TAG[0] = 'ref'
    pref = HOST + st.path if st.path else None
    if ENC:
        ref = f['ref']
        rs = 0 if ref == '-' else 1 if ref == pref else 2
    rs = sym(('ref', new), rs if ENC else None, lambda x: num('rsn', x))
    ref = '-' if rs == 0 else pref if rs == 1 else sym(('refo',), ref if ENC else None)
    st.path = path
    return dict(ms=ms, ip=ip, mc=mc, params=params, proto=proto, st=stt, ua=ua, size=size, lat=lat, ref=ref)


def newip(ip):
    TAG[0] = 'newip'
    o = [sym(('oct1',), ip[0] if ENC else None, lambda x: raw(x, 8))]
    for j in range(1, 4):
        o.append(raw(ip[j] if ENC else None, 8))
    return tuple(o)


def run(lines=None):
    S = State()
    TAG[0] = 'hdr'
    n = num('nlines', len(lines) if ENC else None)
    out = []
    for i in range(n):
        f = parse(lines[i]) if ENC else None
        TAG[0] = 'parse'
        if flag(('ok',), f is not None if ENC else None):
            out.append(fmt_line(code_line(S, f)))
        else:
            TAG[0] = 'rawline'
            out.append(string(lines[i] if ENC else None))
    return out


if __name__ == '__main__':
    data = sys.stdin.buffer.read()
    C = Coder(data)
    sys.stdout.buffer.write('\n'.join(run()).encode('latin-1'))
