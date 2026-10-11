"""Принудительная текстовая диффузия (masked discrete diffusion, исполняемая СНАРУЖИ модели).
Холст из N шумовых слов; на каждом шаге скрипт выбирает K позиций, модель возвращает ровно K слов,
скрипт вставляет их. Переписать зафиксированные слова модель физически не может.
  init T     — создать траекторию T     show T — промпт текущего шага     apply T 'k: w' ... — применить ответ"""
import sys, json, re, secrets
N, K, STEPS = 32, 8, 4
p = lambda t: f"diffusion/{t}.json"
cmd, t = sys.argv[1], sys.argv[2]
if cmd == "init":
    rng = secrets.SystemRandom(); pool = open("wordpool.txt").read().split()
    order = list(range(N)); rng.shuffle(order)
    st = {"canvas": [rng.choice(pool) for _ in range(N)], "noise": None, "schedule": [order[i*K:(i+1)*K] for i in range(STEPS)], "step": 0, "history": []}
    st["noise"] = list(st["canvas"]); json.dump(st, open(p(t), "w"), indent=1); print("ok")
    sys.exit()
st = json.load(open(p(t)))
if cmd == "show":
    pos = st["schedule"][st["step"]]; view = []
    for i, w in enumerate(st["canvas"]):
        view.append(f"[{pos.index(i)+1}]" if i in pos else w)
    print(f"STEP {st['step']+1}/{STEPS}. CANVAS:\n" + " ".join(view))
elif cmd == "apply":
    pos = st["schedule"][st["step"]]
    fills = dict((int(a), b) for a, b in re.findall(r"^\s*\[?(\d+)\]?\s*[:.)-]\s*([A-Za-z][A-Za-z'-]*)\s*$", sys.argv[3], re.M))
    assert sorted(fills) == list(range(1, K+1)), f"need exactly {K} single-word fills, got {sorted(fills)}"
    for j, i in enumerate(pos): st["canvas"][i] = fills[j+1]
    st["history"].append(" ".join(st["canvas"])); st["step"] += 1
    json.dump(st, open(p(t), "w"), indent=1); print(f"applied step {st['step']}:", " ".join(st["canvas"]))
