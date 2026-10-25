# own4.py omits decode weight reads (shared by a batch of B, but not free) and zeroes the swap reload.
# Uses own4.out totals and the trace totals (19,514 requests, 373 output tokens/request, mean prompt 21,219).
tot = dict(new_prefill=2.69, att=1.03, decode_kv=9.22, pin=4.42, swap=0.88, recompute=91.86)
out_tok = 19514 * 373; GPU_S = 2 / 3600
for B in (16, 32, 64):
    w = out_tok * 140e9 / B / 3.35e12 * GPU_S
    T = tot["new_prefill"] + tot["att"] + tot["decode_kv"] + tot["pin"] + w
    print(f"batch {B}: weight reads ${w:.2f}; operator total ${T:.2f} (answer $17.37); decode-KV share {tot['decode_kv']/T:.1%};"
          f" FP8 KV {-tot['decode_kv']/2/T:+.1%}; swap-over-gaps {-(tot['pin']-tot['swap'])/T:+.1%}")
reload = 19073 * 21219 * 327680 / 50e9 * GPU_S
print(f"swap reload if NOT hidden: ${reload:.2f} -> hit marginal cost {(tot['att']+tot['swap']+reload)/tot['recompute']:.1%} of recompute"
      f" (answer 2.1%); swap still beats pin: {tot['swap']+reload:.2f} vs {tot['pin']:.2f}")
