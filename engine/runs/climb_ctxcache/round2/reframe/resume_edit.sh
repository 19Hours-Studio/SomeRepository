#!/bin/sh
# Resume shards one at a time (low-memory fallback for run_edit.sh); finished traces are skipped.
cd "$(dirname "$0")"
for s in 0 1 2 3; do python3 -I exp_edit.py data/traces.jsonl $s 4 out/edit_$s.jsonl >> out/edit_$s.log 2>&1; done
