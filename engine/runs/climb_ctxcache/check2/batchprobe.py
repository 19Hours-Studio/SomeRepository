# check2: decode weight-read cost when batch size is limited by KV memory (8xH100, 640 GB, 141 GB BF16
# weights, ~450 GB for KV): shorter contexts -> bigger batch -> fewer weight reads per output token.
# billing2/decode_dilute charge every policy the same decode weight cost; this varies it with mean context.
import re, sys
rows = {}
for l in open(sys.argv[1]):
    m = re.match(r"\s+(\S+)\s+[\d.]+\s+\S+\s+[\d.]+\s+\S+\s+([\d.]+)\s+\S+\s+([\d.]+)x", l)
    if m: rows[m.group(1)] = (float(m.group(2)), float(m.group(3)))
NOUT, KVB, MEANCTX_APP = 2_707_390, 327_680, 29_912
step_s = 141e9 / (8 * 3.35e12 * 0.7)          # one decode step reads all weights across 8 GPUs
for kvmem in (450e9, 250e9):
    print(f"KV memory {kvmem/1e9:.0f} GB")
    base = None
    for k, (gh, res) in rows.items():
        B = kvmem / (res * MEANCTX_APP * KVB)        # sequences that fit
        dec = NOUT / B * step_s * 8 / 3600           # GPU-h of weight reads
        tot = gh + dec; base = base or tot
        print(f"  {k:24s} batch {B:5.1f}  decode-weights {dec:5.2f} GPU-h  total {tot:5.2f}  vs append {tot/base-1:+.1%}")
