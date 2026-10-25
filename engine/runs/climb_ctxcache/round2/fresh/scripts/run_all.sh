#!/bin/sh
# Re-runs every result in out/ (about 35-40 min serially, ~6 GB RAM peak). Standard library only.
set -e; cd "$(dirname "$0")/.."; S="python3 -I scripts"; A=data/qwen_traceA_blksz_16.jsonl; Bt=data/qwen_traceB_blksz_16.jsonl
C=data/qwen_coder_blksz_16.jsonl; T=data/qwen_thinking_blksz_16.jsonl
$S/probe.py $C $T $A $Bt            > out/probe.txt
$S/reuse.py $A $Bt $C $T            > out/reuse.txt
$S/sessions.py $A $Bt $C $T         > out/sessions.txt
$S/compose.py $A $Bt $C $T          > out/compose.txt
$S/ttl.py $A $Bt $C $T              > out/ttl.txt
$S/taxonomy.py $A $Bt               > out/taxonomy.txt
$S/retain.py $A $C $T               > out/retain_fixed.txt
$S/policy.py $A $C $T               > out/policy.txt
$S/exact_ceiling.py $A $C $T        > out/exact_ceiling.txt
W=1.0 ROWS=openai $S/exact_ceiling.py $A $C $T $Bt > out/openai_retention.txt
$S/keep_cost.py $A $C               > out/keep_cost.txt
$S/controller.py $A $C $T           > out/controller.txt
$S/calibrate.py data/traces.jsonl data/swe_stats.jsonl  > out/calibrate.txt
$S/carry_swe.py data/traces.jsonl   > out/carry_swe.txt
$S/swe_crossreuse.py data/traces.jsonl > out/swe_crossreuse.txt
for k in 4 8 16; do $S/copyspec.py data/traces.jsonl $k; done > out/copyspec.txt
$S/agent_gpu.py data/traces.jsonl data/swe_stats.jsonl > out/agent_gpu.txt
for a in "1.82 0.89" "1.99 1.39" "2.10 2.34"; do echo "tau rho = $a"; $S/agent_gpu_spec.py data/traces.jsonl data/swe_stats.jsonl $a; done > out/agent_gpu_spec.txt
