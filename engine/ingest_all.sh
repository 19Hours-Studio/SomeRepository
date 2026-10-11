#!/bin/sh
# Ингест всех завершённых агентов прогона по таблице runs/<RUN>/agents.tsv (label, agentId, arm, gen).
# Использование: sh engine/ingest_all.sh RUN TASKS_DIR [label-префикс]
RUN=$1; T=$2; P=${3:-}
D=$(dirname "$0")
while IFS="$(printf '\t')" read -r label id arm gen; do
  case "$label" in "$P"*) ;; *) continue;; esac
  [ -f "$T/$id.output" ] && python3 "$D/ce.py" ingest "$RUN" "$label" --arm "$arm" --gen "$gen" --transcript "$T/$id.output"
done < "$D/runs/$RUN/agents.tsv"
