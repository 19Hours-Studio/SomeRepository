#!/bin/sh
# Bailian production traces (Git LFS objects of github.com/alibaba-edu/qwen-bailian-usagetraces-anon)
# and recorded SWE-agent billing stats. data/traces.jsonl is copied from round1/fix/data.
set -e; cd "$(dirname "$0")/.."; mkdir -p data
for f in qwen_traceA_blksz_16 qwen_traceB_blksz_16 qwen_thinking_blksz_16 qwen_coder_blksz_16; do
  [ -s data/$f.jsonl ] || curl -sS -o data/$f.jsonl https://media.githubusercontent.com/media/alibaba-edu/qwen-bailian-usagetraces-anon/main/$f.jsonl
done
[ -s data/traces.jsonl ] || cp ../../round1/fix/data/traces.jsonl data/
[ -s data/swe_stats.jsonl ] || python3 -I scripts/fetch_stats.py data/traces.jsonl data/swe_stats.jsonl
sha256sum -c data/SHA256SUMS
