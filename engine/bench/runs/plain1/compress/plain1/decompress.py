import sys, re, math, datetime as D

M = (1 << 64) - 1
TOP = 1 << 56


class C:
    def __init__(s, enc, data=b''):
        s.enc = enc
        s.lo = 0
        s.rg = M
        s.out = bytearray()
        s.cache = 0
        s.cs = 1
        s.T = {}
        s.B = {}
        if not enc:
            s.d = data
            s.p = 9
            s.code = int.from_bytes(data[1:9], 'big')

    def shl(s):
        if s.lo < 0xFF << 56 or s.lo > M:
            c = s.lo >> 64
            s.out.append((s.cache + c) & 255)
            s.out += bytes([(255 + c) & 255]) * (s.cs - 1)
            s.cs = 0
            s.cache = (s.lo >> 56) & 255
        s.cs += 1
        s.lo = (s.lo << 8) & M

    def fin(s):
        for _ in range(9):
            s.shl()
        return bytes(s.out)

    # code one symbol from (cum, freq) lists given total; get(target)->(cum,freq,x)
    def go(s, tot, cf, get):
        r = s.rg // tot
        if s.enc:
            c, f = cf
            s.lo += r * c
            x = None
        else:
            c, f, x = get(min(s.code // r, tot - 1))
            s.code -= r * c
        s.rg = r * f
        while s.rg < TOP:
            s.rg <<= 8
            if s.enc:
                s.shl()
            else:
                s.code = ((s.code << 8) | (s.d[s.p] if s.p < len(s.d) else 0)) & M
                s.p += 1
        return x

    def uni(s, n, x):
        r = s.go(n, (x, 1), lambda t: (t, 1, t))
        return x if s.enc else r

    def bit(s, k, b):
        p = s.B.get(k, 2048)
        r = s.go(4096, (0, p) if b == 0 else (p, 4096 - p), lambda t: (0, p, 0) if t < p else (p, 4096 - p, 1))
        if not s.enc:
            b = r
        s.B[k] = p + ((4096 - p) >> 4) if b == 0 else p - (p >> 4)
        return b

    def pc(s, F, v, cap, k):
        A = (1 << 40) - cap - 1
        cum = lambda j: int(F(j) * A) + j
        tot = 1 << 40
        def get(t):
            lo, hi = 0, cap
            while lo < hi:
                m = (lo + hi + 1) >> 1
                if cum(m) <= t:
                    lo = m
                else:
                    hi = m - 1
            a = cum(lo)
            return a, (tot if lo == cap else cum(lo + 1)) - a, lo
        if s.enc:
            a = cum(min(v, cap))
            r = s.go(tot, (a, (tot if v >= cap else cum(v + 1)) - a), None)
            r = v
        else:
            r = s.go(tot, None, get)
        if r >= cap:
            r = s.num(k, None if v is None else v - cap) + cap
        return r

    def plog(s, k, v):
        n, a, b = s.T.get(('pl', k), (1, 3.0, 10.0))
        mu = a / n
        sg = math.sqrt(max(b / n - mu * mu, 0.01))
        F = lambda x: 0.5 * (1 + math.erf((math.log(x) - mu) / sg / 1.4142135623730951)) if x > 0 else 0.0
        v = s.pc(F, v, 4096, ('ple', k))
        x = math.log(v + 0.5)
        if v < 4096:
            s.T[('pl', k)] = (n + 1, a + x, b + x * x)
        return v

    def pexp(s, k, v):
        n, a = s.T.get(('pe', k), (1, 100.0))
        m = a / n
        v = s.pc(lambda x: 1 - math.exp(-x / m), v, 1 << 16, ('pee', k))
        if v < 1 << 16:
            s.T[('pe', k)] = (n + 1, a + v)
        return v

    def num(s, k, n):
        nb = s.ppm([(k, 'nb')], None if n is None else n.bit_length(), lambda x: s.uni(64, x))
        if nb <= 1:
            return nb
        v = 1
        for i in range(nb - 2, -1, -1):
            b = s.bit((k, nb, i, v if nb - i < 5 else 0), None if n is None else (n >> i) & 1)
            v = v * 2 + b
        return v

    def ppm(s, ctxs, x, fb, inc=2):
        T = s.T
        exc = set()
        res = x
        found = False
        for key in ctxs:
            t = T.get(key)
            if not t:
                continue
            items = [(a, n) for a, n in t.items() if a not in exc]
            if not items:
                continue
            esc = len(items)
            tot = sum(n for _, n in items) + esc
            if s.enc:
                c = 0
                f = 0
                for a, n in items:
                    if a == x:
                        f = n
                        break
                    c += n
                if f:
                    s.go(tot, (c, f), None)
                    found = True
                    break
                s.go(tot, (tot - esc, esc), None)
            else:
                def get(tg):
                    c = 0
                    for a, n in items:
                        if tg < c + n:
                            return c, n, a
                        c += n
                    return c, esc, exc
                r = s.go(tot, None, get)
                if r is not exc:
                    res = r
                    found = True
                    break
            exc.update(a for a, _ in items)
        if not found:
            res = fb(x)
            if s.enc:
                res = x
        for key in ctxs:
            t = T.get(key)
            if t is None:
                t = T[key] = {}
            t[res] = t.get(res, 0) + inc
            if t[res] > 4000:
                for a in t:
                    t[a] = (t[a] + 1) // 2
        return res

    def lit(s, k, x):
        # string coded by order-2 char ppm, -1 terminates
        out = []
        a = b = ''
        i = 0
        while True:
            ch = None
            if s.enc:
                ch = x[i] if i < len(x) else -1
                i += 1
            ch = s.ppm([('L', k, a, b), ('L', k, b), ('L', k)], ch, s.ulit)
            if ch == -1:
                return ''.join(out)
            out.append(ch)
            a, b = b, ch

    def ulit(s, c):
        if s.enc:
            s.uni(257, 256 if c == -1 else ord(c))
            return c
        v = s.uni(257, 0)
        return -1 if v == 256 else chr(v)

    def sym(s, ctxs, x, k):
        return s.ppm(ctxs, x, lambda v: s.lit(k, v))


PAT = re.compile(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d\.\d{3}Z) (\S+) "(\S+) (\S+) (\S+)" (\d+) (\d+) (\d+)ms "([^"]*)" "([^"]*)"\Z')
EP = D.datetime(2000, 1, 1)
HOST = 'https://shop.example.com'


def fmt(t):
    d = EP + D.timedelta(milliseconds=t)
    return d.strftime('%Y-%m-%dT%H:%M:%S.') + '%03dZ' % (t % 1000)


def pts(x):
    d = D.datetime.strptime(x[:19], '%Y-%m-%dT%H:%M:%S')
    return (d - EP).days * 86400000 + (d - EP).seconds * 1000 + int(x[20:23])


def cat(u):
    return re.sub(r'\d+', '#', u.split('?')[0])


def ipcode(c, ip):
    p = None if ip is None else ip.split('.')
    if p is not None and (len(p) != 4 or any(not q.isdigit() or str(int(q)) != q or int(q) > 255 for q in p)):
        c.ppm([('ipf',)], 1, lambda v: c.uni(2, v))
        c.lit('ipl', ip)
        return ip
    f = c.ppm([('ipf',)], 0 if c.enc else None, lambda v: c.uni(2, v))
    if f:
        return c.lit('ipl', ip)
    o = []
    for i in range(4):
        v = None if p is None else int(p[i])
        o.append(c.ppm([('o',)], v, lambda v: c.uni(256, v)) if i == 0 else c.uni(256, v))
    return '.'.join(map(str, o))


def zq(c, status, size, o):
    v = None if size is None else size - o
    v = c.ppm([('zq', status)], v, lambda v: (lambda z: z >> 1 if z % 2 == 0 else -(z + 1) // 2)(c.num(('zqn',), None if v is None else v * 2 if v >= 0 else -2 * v - 1)))
    return v + o


def rebuild(tpl, nums, q):
    it = iter(nums)
    return re.sub(r'[#*]', lambda m: q if m.group() == '*' else str(next(it)), tpl)


def ucode(c, st, ip, meth, url):
    mt = q = nums = None
    if c.enc:
        m = re.search(r'q=([^&]*)', url)
        u2 = url
        if m:
            q = m.group(1)
            u2 = url[:m.start(1)] + '*' + url[m.end(1):]
        nums = [int(x) for x in re.findall(r'\d+', u2)]
        mt = meth + ' ' + re.sub(r'\d+', '#', u2)
        try:
            if rebuild(mt.split(' ', 1)[1], nums, q) != url:
                mt = '!'
        except Exception:
            mt = '!'
    mt = c.sym([('t',)], mt, 'tpl')
    if mt == '!':
        meth = c.sym([('m',)], meth, 'm')
        url = c.lit('url', url)
        return meth, url, mt, None
    meth, tpl = mt.split(' ', 1)
    o = []
    for j in range(tpl.count('#')):
        p = tuple(o)
        o.append(c.ppm([('n', tpl, j, p, ip), ('n', tpl, j, p)], None if nums is None else nums[j], lambda v: c.num(('nn', tpl, j), v)))
    if '*' in tpl:
        w = None if q is None else q.split('+') + [-1]
        r = []
        a = -2
        while True:
            x = wcode(c, a, None if w is None else w[len(r)])
            if x == -1:
                break
            r.append(x)
            a = x
        q = '+'.join(r)
    return meth, rebuild(tpl, o, q), mt, q


def wcode(c, a, x):
    def fb(v):
        e = c.ppm([('we',)], None if v is None else int(v == -1), lambda b: c.uni(2, b))
        return -1 if e else c.lit('wl', v)
    return c.ppm([('w', a), ('w',)], x, fb)


class IPM:
    def __init__(s):
        s.n = 1 << 12
        s.f = [0] * (s.n + 1)
        s.ips = []
        s.ix = {}
        s.cnt = []
        s.prev = None

    def add(s, i, d):
        i += 1
        while i <= s.n:
            s.f[i] += d
            i += i & -i

    def pre(s, i):
        r = 0
        while i > 0:
            r += s.f[i]
            i -= i & -i
        return r

    def find(s, t):
        # largest i with pre(i) <= t -> symbol index i
        i = 0
        b = s.n
        while b:
            if i + b <= s.n and s.f[i + b] <= t:
                i += b
                t -= s.f[i]
            b >>= 1
        return i

    def code(s, c, ip):
        p = s.prev
        same = c.ppm([('sm',)], None if ip is None else int(ip == p), lambda v: c.uni(2, v))
        if same:
            return p
        k = s.ix.get(ip, -1) if c.enc else None
        new = c.ppm([('nw',)], None if k is None else int(k < 0), lambda v: c.uni(2, v)) if s.ips else 1
        if new:
            ip = ipcode(c, ip)
            k = len(s.ips)
            s.ips.append(ip)
            s.ix[ip] = k
            s.cnt.append(0)
            if k >= s.n:
                s.n *= 2
                s.f = [0] * (s.n + 1)
                for j, v in enumerate(s.cnt):
                    s.add(j, v)
        else:
            pk = s.ix[p]
            pc = s.cnt[pk]
            s.add(pk, -pc)
            tot = s.pre(s.n)
            if c.enc:
                cf = (s.pre(k), s.cnt[k])
            def get(t):
                j = s.find(t)
                return s.pre(j), s.cnt[j], j
            r = c.go(tot, cf if c.enc else None, get)
            if not c.enc:
                k = r
            s.add(pk, pc)
            ip = s.ips[k]
        s.cnt[k] += 1
        s.add(k, 1)
        return ip


def run(c, lines=None):
    out = []
    S = {}
    F = IPM()
    lt = 0
    i = 0
    while True:
        L = None
        if c.enc:
            if i == len(lines):
                ty = 2
            else:
                L = lines[i]
                m = PAT.match(L)
                ty = 1
                if m:
                    g = list(m.groups())
                    ok = fmt(pts(g[0])) == g[0] and pts(g[0]) >= lt and all(str(int(g[j])) == g[j] for j in (5, 6, 7))
                    ty = 0 if ok else 1
            i += 1
        ty = c.ppm([('ty',)], ty if c.enc else None, lambda v: c.uni(3, v))
        if ty == 2:
            return '\n'.join(out)
        if ty == 1:
            out.append(c.lit('raw', L))
            continue
        if not c.enc:
            g = [None] * 10
        ip = F.code(c, g[1])
        rk = 0 if ip == F.prev else 1
        F.prev = ip
        st = S.get(ip)
        new = st is None
        if new:
            st = S[ip] = {'c': '', 'c2': '', 'ua': None, 'id': None, 't': lt, 'ru': ''}
        # time
        t = None if not c.enc else pts(g[0])
        dt = c.pexp('dt', None if t is None else t - lt)
        t = lt + dt
        lt = t
        # request
        meth, url, cu, q = ucode(c, st, ip, g[2], g[3])
        proto = c.sym([('p',)], g[4], 'p')
        co = cu.rsplit('/', 1)[0]
        if co.count('/') < 2:
            co = cu
        status = int(c.sym([('s', co), ('s',)], g[5], 's'))
        size = None if g[6] is None else int(g[6])
        if q is None:
            size = c.ppm([('z', url, status), ('z', cu, status), ('z', status)], size, lambda v: c.num(('zn', cu), v))
        else:
            o = 37 * len(q)
            size = zq(c, status, size, o)
        lat = c.plog((co, status), None if g[7] is None else int(g[7]))
        ref = g[8]
        rv = None
        pu = HOST + st['ru']
        if c.enc:
            rv = 0 if ref == '-' else 1 if (ref == pu and not new) else 2
        rv = c.ppm([('r', new, st['c'], cu), ('r', new, cu), ('r', new)], rv, lambda v: c.uni(3, v))
        ref = '-' if rv == 0 else pu if rv == 1 else c.lit('ref', ref)
        ua = g[9]
        if st['ua'] is not None:
            f = c.ppm([('uaf',)], None if ua is None else int(ua != st['ua']), lambda v: c.uni(2, v))
            if not f:
                ua = st['ua']
            else:
                ua = c.sym([('ua',)], ua, 'ua')
        else:
            ua = c.sym([('ua',)], ua, 'ua')
        st['ua'] = ua
        st['c2'] = st['c']
        st['c'] = cu
        st['ru'] = url
        st['t'] = t
        if not c.enc:
            out.append('%s %s "%s %s %s" %d %d %dms "%s" "%s"' % (fmt(t), ip, meth, url, proto, status, size, lat, ref, ua))


if __name__ == '__main__':
    d = sys.stdin.buffer.read()
    c = C(False, d)
    sys.stdout.buffer.write(run(c).encode('latin-1'))
