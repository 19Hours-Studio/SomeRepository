# SIEVE («Решето»)

Маленькая модель, которая решает гипотезы о машинной арифметике (это язык АЛУ и процессоров)
и учится **только на проверенном**. Дизайн и обоснование: `research/stage2-architecture/02-sieve.md`.

| Файл | Что внутри |
|---|---|
| `bitworld.py` | мир: w-битные выражения, правила (истинные и «почти верные»), семейства гипотез с ослаблениями, точный верификатор, контрпримеры |
| `lattice.py` | решётка импликаций: распространение меток по конусу, невязка, выбор проверки по ожидаемому снятию энтропии |
| `model.py` | древесный трансформер с типизированными головами VERDICT (калиброванная p(true)) и WITNESS (биты контрпримера); конфиги tiny / small / base |
| `train.py` | цикл: семейства → прогноз → выбор проверок → верификатор → распространение → обучение; R-free-валидация по семействам |
| `learner_np.py`, `experiment_ablation.py` | CPU-абляция ядра на простой голове (numpy) |
| `test_sieve.py` | дымовые тесты |

```
python3 test_sieve.py                                                  # тесты (torch-часть пропускается без torch)
python3 train.py --config tiny --rounds 20 --device cpu                # проверка цикла на CPU
python3 train.py --config small --rounds 3000 --device cuda --amp      # RTX 3060, ~25M параметров
python3 train.py --config small --rounds 3000 --device cuda --amp --acq random --no-prop --out runs/baseline   # контроль
python3 experiment_ablation.py --seeds 3                               # абляция на CPU (~10 мин)
```

Метрики в `<out>/log.jsonl` считаются только на отложенных семействах (R-free):
`val_logloss`, `val_acc`, `val_ece`, `witness_hit` (доля ложных гипотез, где первый же
предложенный контрпример верен) против `random_point_hit` (вероятность попасть случайной точкой).
