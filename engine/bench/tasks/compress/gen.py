"""Writes data.log: a synthetic web access log with structure a compressor can learn (deterministic, seed 2026)."""
import datetime, math, os, random

R = random.Random(2026); OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.log")
UAS = [f"Mozilla/5.0 ({os_}) AppleWebKit/537.36 (KHTML, like Gecko) {br}" for os_ in
       ("Windows NT 10.0; Win64; x64", "Macintosh; Intel Mac OS X 14_6", "X11; Linux x86_64", "iPhone; CPU iPhone OS 18_1 like Mac OS X",
        "Linux; Android 15; Pixel 9")
       for br in ("Chrome/130.0.6723.70 Safari/537.36", "Chrome/129.0.6668.100 Safari/537.36", "Firefox/131.0", "Safari/605.1.15",
                  "Edg/130.0.2849.56", "OPR/114.0.0.0")] + ["curl/8.10.1", "python-requests/2.32.3", "Googlebot/2.1 (+http://www.google.com/bot.html)"]
WORDS = "red blue green chair table lamp sofa desk shelf rug mirror clock vase pillow blanket curtain bed stool bench cabinet".split()
STATIC = [(f"/static/js/app.{R.getrandbits(32):08x}.js", R.randint(80000, 400000)) for _ in range(6)] + \
         [(f"/static/img/{w}.png", R.randint(3000, 90000)) for w in WORDS]
clients = []
for c in range(3000):
    ip = f"{R.choice([10, 172, 192, 203, 198, 81, 95, 185])}.{R.randint(0, 255)}.{R.randint(0, 255)}.{R.randint(1, 254)}"
    clients.append({"ip": ip, "ua": R.choice(UAS), "uid": R.randint(1000, 99999), "last": "-", "fav": [int(R.paretovariate(1.1) * 10) % 50000 for _ in range(5)]})
weights = [1 / (i + 1) ** 1.2 for i in range(len(clients))]
t = datetime.datetime(2026, 10, 1, tzinfo=datetime.timezone.utc); lines = []; cur = 0
for n in range(26000):
    t += datetime.timedelta(milliseconds=int(R.expovariate(1 / 250)) + 1)
    if R.random() > 0.45: cur = R.choices(range(len(clients)), weights)[0]
    cl = clients[cur]; k = R.random()
    if k < 0.40:
        i = R.choice(cl["fav"]) if R.random() < 0.6 else int(R.paretovariate(1.1) * 10) % 50000
        path, method = f"/api/v2/items/{i}", "GET"; size = (i * 7919) % 30000 + 1200; lat = R.lognormvariate(3.2, 0.5)
    elif k < 0.52:
        i = R.choice(cl["fav"]); pg = 1 + int(R.expovariate(0.7)); path, method = f"/api/v2/items/{i}/reviews?page={pg}", "GET"
        size = 2400 + 180 * ((i + pg) % 11); lat = R.lognormvariate(3.6, 0.6)
    elif k < 0.62:
        path = f"/api/v2/users/{cl['uid']}/cart"; method = R.choice(["GET", "GET", "POST", "DELETE"]); size = 300 + (cl["uid"] % 97) * 13; lat = R.lognormvariate(3.0, 0.4)
    elif k < 0.85:
        path, size = R.choice(STATIC); method = "GET"; lat = R.lognormvariate(1.2, 0.3)
    elif k < 0.95:
        q = "+".join(R.choice(WORDS) for _ in range(R.randint(1, 3))); path, method = f"/search?q={q}", "GET"; size = 800 + 37 * len(q) + R.randint(0, 9); lat = R.lognormvariate(4.0, 0.5)
    else:
        path, method, size, lat = R.choice([("/health", "GET", 2, R.lognormvariate(0.3, 0.2)), ("/login", "POST", 0, R.lognormvariate(4.5, 0.3)), ("/checkout", "POST", 512, R.lognormvariate(5.0, 0.4))])
    status = 200
    if path.startswith("/static") and R.random() < 0.5: status, size = 304, 0
    elif path == "/login": status = 302
    elif R.random() < 0.03: status, size = 404, 153
    elif R.random() < 0.005: status, size, lat = 500, 291, lat + R.uniform(1000, 3000)
    ts = t.strftime("%Y-%m-%dT%H:%M:%S.") + f"{t.microsecond // 1000:03d}Z"
    lines.append(f'{ts} {cl["ip"]} "{method} {path} HTTP/1.1" {status} {size} {max(1, int(lat))}ms "{cl["last"]}" "{cl["ua"]}"\n')
    cl["last"] = "https://shop.example.com" + path if R.random() < 0.7 else "-"
open(OUT, "w").write("".join(lines))
