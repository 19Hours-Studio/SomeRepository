# Передача: доделать проверку римского додекаэдра на ПК с полным интернетом

Ветка: `claude/awesome-clarke-5b1tou`. Всё состояние прогона лежит в `engine/runs/dodeca/`. Разбор и итог:
`research/stage1-creativity/14-dodecahedron.md` и `14a-dodecahedron-answer.md`. Скилл движка:
`.claude/skills/creativity-engine/SKILL.md`, раздел v3.6.

## Где остановились
- Лучшая гипотеза: `final#1` — бронзовый жребий на 12 исходов. Вторая: насадка на древко (`g2_evo#7`, `final#2`).
- Обзор следов (`tests/wear/RESULT.md`): микроскопного сравнения кончиков шишечек нет нигде. «Износа нет» —
  оценка на глаз (Нортон-Дисни, Хитченс). КТ, химии остатков и записей о чистке не опубликовано.
- Сводка отверстий (`tests/holes/`: `data.py`, `analyse.py`, `results.txt`; агент остановлен до итогового текста,
  источники чисел в `data.py` не перепроверены). Выдержки поиска дали таблицы для 3 предметов:
  - Жюблен — классы есть;
  - Тонгерен — сплошной ряд;
  - Ромфорд — неясно;
  - у Тонгерена противоположные отверстия почти равны, p = 0.0005.
- Не сделано, потому что облаку закрыты sketchfab.com, zenodo.org, arxiv.org и cambridge.org:
  - каталог 3D-моделей (`tests/models3d/TASK.md`);
  - измерительный инструмент по 3D-моделям (`tests/mesh/TASK.md`).

## Что сделать (по порядку)
1. По `tests/models3d/TASK.md` найти и скачать опубликованные 3D-модели додекаэдров (Sketchfab, музеи, университеты),
   положить в `tests/models3d/files/`.
2. По `tests/mesh/TASK.md` написать и проверить на синтетике инструмент `measure.py` + `analyse.py`. Затем измерить
   реальные модели: 12 диаметров, противоположные пары, кривизна 20 шишечек.
3. Дополнить `tests/holes/data.py` полными таблицами (Guggenberger 2013; Nouwen 1993; Sparavigna 2012, arXiv 1204.6497;
   музейные каталоги) и перезапустить `python3 engine/runs/dodeca/tests/holes/analyse.py`.
4. Свести результаты как данные и сделать финальную починку и слепой аудит:
   ```
   python3 engine/ce.py repairtask dodeca --ids "final#1,final#2,g2_evo#7,g1_mech#2" --dir engine/runs/dodeca/repair_v2 \
     --tpl repair_explain --audits engine/runs/dodeca/audit_5,engine/runs/dodeca/audit_3,engine/runs/dodeca/audit_4 \
     --notes "<итоги шагов 1-3: таблицы отверстий, кривизна шишечек, что найдено про износ>"
   ```
   Агенту дать `engine/runs/dodeca/repair_final/TASK.md`-подобный промпт: «Read the task file and follow it».
   Затем `ingest`, затем `redteamtask dodeca --ids <итоги + 2 лидера> --dir engine/runs/dodeca/audit_6 --blind
   --tpl redteam_explain`, затем `python3 engine/runs/dodeca/audit_stats.py --only=audit_6 audit_6=<транскрипт>`.
5. Записать итог в `research/stage1-creativity/14-dodecahedron.md` и `14a-dodecahedron-answer.md`, закоммитить и
   запушить в эту же ветку.

## Готовый промпт для Claude Code на ПК
> В репозитории на ветке `claude/awesome-clarke-5b1tou` прочитай `engine/runs/dodeca/HANDOFF.md` и выполни шаги 1–5.
> Правила: не выдумывать числа и наблюдения, у каждого числа источник. Инструмент сначала проверить на синтетике.
> Итоговую гипотезу выбирает слепой аудит, а не ты. Отчёт — по-русски, коротко: лучшая гипотеза, что подтвердили
> или опровергли 3D-измерения, и решающая проверка.
