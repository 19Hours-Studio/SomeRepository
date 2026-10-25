#!/bin/sh
# Runs the real-model edit experiment in 4 single-threaded shards (multi-threading is contended here).
cd "$(dirname "$0")"
for s in 0 1 2 3; do nohup python3 -I exp_edit.py data/traces.jsonl $s 4 out/edit_$s.jsonl > out/edit_$s.log 2>&1 & done
