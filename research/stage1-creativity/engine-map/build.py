import html
W, BW, BH = 1160, 196, 56
X = [40, 260, 480, 700, 920]
def esc(s): return html.escape(s, quote=True)
parts = []
def box(c, y, lines, st="built", badge=None):
    x = X[c]
    parts.append(f'<rect x="{x}" y="{y}" width="{BW}" height="{BH}" rx="6" class="b-{st}"/>')
    ys = [y + 33] if len(lines) == 1 else [y + 24, y + 41]
    for ln, yy in zip(lines, ys):
        cls = "t-code" if ln.startswith(("ce.py", "runner", "plan ")) else "t"
        parts.append(f'<text x="{x + BW/2}" y="{yy}" text-anchor="middle" class="{cls}">{esc(ln)}</text>')
    if badge:
        bx = x + BW
        parts.append(f'<circle cx="{bx}" cy="{y}" r="10" class="badge"/>'
                     f'<text x="{bx}" y="{y + 4}" text-anchor="middle" class="badge-t">{esc(str(badge))}</text>')
def label(y, title, sub=None):
    parts.append(f'<text x="40" y="{y}" class="sec">{esc(title)}</text>')
    if sub: parts.append(f'<text x="270" y="{y}" class="sec-sub">{esc(sub)}</text>')
def arrow(x1, y1, x2, y2, text=None, tx=None, ty=None, cls="ln", marker="arr"):
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" class="{cls}" marker-end="url(#{marker})"/>')
    if text: parts.append(f'<text x="{tx}" y="{ty}" class="al">{esc(text)}</text>')
def path(d, cls="ln", marker="arr"):
    parts.append(f'<path d="{d}" class="{cls}" fill="none" marker-end="url(#{marker})"/>')

# Input
label(22, "Вход")
box(0, 32, ["Вопрос"])
box(1, 32, ["Тип вопроса:", "изобрести · объяснить"])
box(2, 32, ["Подсказки человека", "(необязательно)"])
box(3, 32, ["Бюджет токенов"])
arrow(248, 88, 248, 126, "вопрос", 256, 110)
arrow(578, 88, 578, 126, "как данные, с проверкой", 586, 110)
# Step 0: brief
label(120, "0 · Постановка", "агент собирает бриф, ответов не предлагает")
box(0, 130, ["Агент постановки:", "бриф задачи"])
box(1, 130, ["тип, точный вопрос,", "критерий успеха"])
box(2, 130, ["ограничения, контекст,", "где искать данные"])
box(3, 130, ["скрытые допущения,", "что неясно"])
arrow(248, 186, 248, 228, "бриф", 256, 210)
# Raw material
label(222, "1 · Сырьё", "что известно до генерации")
box(0, 232, ["Карта аттракторов", "(типовые ответы модели)"])
box(1, 232, ["Ядро вопроса", "и намерение"])
box(2, 232, ["Бухгалтерия затрат", "или реестр фактов"])
box(3, 232, ["Прежние попытки", "или прежние объяснения"])
box(4, 232, ["Набор расчётов:", "13 классов убийц"])
box(0, 302, ["Потолки «в разы»", "до генерации"], "part", 11)
box(1, 302, ["Охота за сырыми", "данными"], "prop", 2)
box(2, 302, ["Срезы фактов", "для каждого шага"], "prop", 3)
arrow(248, 358, 248, 410, "сырьё", 256, 384)
# Generation
label(404, "2 · Генерация", "без инструментов, ~13 тыс. токенов на шаг")
box(0, 414, ["Портфель техник", "против бассейнов"])
box(1, 414, ["Слои A → B → C", "новизна, гениальность, ценность"])
box(2, 414, ["Подвопросы", "по отдельности"], "prop", 5)
box(3, 414, ["Память аттракторов", "(запрет найденного)"])
box(4, 414, ["Эволюция: потомки", "из дефектов"])
arrow(248, 470, 248, 524, "идеи", 256, 492)
path("M600 528 L600 496 L1018 496 L1018 474")
parts.append('<text x="800" y="490" text-anchor="middle" class="al">дефекты аудита → потомки</text>')
# Truth
label(518, "3 · Отбор правдой", "поиск, Python, расчёты")
box(0, 528, ["Тест на смерть", "+ набор расчётов"])
box(1, 528, ["Починка с поиском", "(−72% FATAL)"])
box(2, 528, ["Слепой аудит:", "FATAL, MAJOR, FIT"])
box(3, 528, ["Сборщик цепочек"])
box(4, 528, ["Измерь или смоделируй", "(3D, физика)"], "part", 2)
box(0, 598, ["Матрица предсказаний", "→ решающий опыт"], "prop", 1)
box(1, 598, ["Защита", "проигравшего"], "prop", 7)
box(2, 598, ["Проверка", "согласованности"], "part", 5)
box(3, 598, ["Судьи: только", "оригинальность"])
box(4, 598, ["Проверка", "по литературе"])
path("M480 556 L470 556 L470 260 L478 260", cls="ln-prop", marker="arr-prop")
parts.append('<text x="478" y="389" class="al-prop">↑ новые факты</text>')
parts.append(f'<circle cx="470" cy="492" r="10" class="badge"/><text x="470" y="496" text-anchor="middle" class="badge-t">6</text>')
arrow(248, 654, 248, 706, "лучшие", 256, 684)
# Output
label(700, "4 · Выход")
box(0, 710, ["Победитель +", "таблица уверенности"])
box(1, 710, ["Решающая проверка"])
box(2, 710, ["Калибровка:", "исход → оценка Брайера"], "prop", 8)
box(3, 710, ["Отчёт пользователю"])
# Orchestration
parts.append('<rect x="24" y="792" width="1112" height="138" rx="8" class="band"/>')
label(816, "Оркестрация", "каждый шаг выше вызывает модель через runner")
box(0, 828, ["ce.py", "состояние, промпты, отбор"])
box(1, 828, ["runner", "claude -p, модель, инструменты"])
box(2, 828, ["plan · run · usage", "токены по шагам"])
box(3, 828, ["Адаптивный конвейер", "(ценность информации)"], "prop", 4)
box(4, 828, ["Память между прогонами", "· полигон"], "prop", "9")
parts.append(f'<circle cx="{X[4] + BW - 26}" cy="828" r="10" class="badge"/><text x="{X[4] + BW - 26}" y="832" text-anchor="middle" class="badge-t">10</text>')

svg = (f'<svg viewBox="0 0 {W} 950" role="img" aria-label="Схема движка: вход, постановка задачи агентом (бриф), сырьё, генерация без инструментов, '
       'отбор правдой с инструментами, выход; петли эволюции и новых фактов; оркестрация через ce.py и runner; '
       'пунктиром отмечены предложения 1-11">'
       '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
       '<path d="M0 0 L10 5 L0 10 z" class="mk"/></marker>'
       '<marker id="arr-prop" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
       '<path d="M0 0 L10 5 L0 10 z" class="mk-prop"/></marker></defs>' + "".join(parts) + "</svg>")
page = open("template.html").read().replace("%%SVG%%", svg)
open("engine-map.html", "w").write(page)
print("ok", len(page))
