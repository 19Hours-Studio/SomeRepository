# Check of answer.md (Continuum-9)

Reproduced: `all9.py` re-run gives output byte-identical to `all9.txt`.

## Finding: the gain depends on how Rubin's slot power is split (`overhead.py`, `overhead2.py`)
The model gives Rubin a 1,870 W chip inside a 3,056 W slot, so ~1.04 kW per slot stays fixed when voltage scales.
Continuum gets chip x 0.146 + 110 W (~400 W). Both are undervolted to 0.55 V, so the split decides the result.

Decode tok/s/W ratio, 128K, p = 0.8, tiers >=200 / 500 / 1000 / 1500 / 2000 tok/s/user:

| Variant | C9 / Rubin | C9 / Ultra 4-die |
|---|---|---|
| As in answer | 1.22 1.35 1.63 1.81 2.67 | 1.11 1.11 1.23 1.27 1.34 |
| Rubin at analyst Max-P (2.3 kW GPU, 230 kW rack) | 1.08 1.19 1.44 1.60 2.35 | -- |
| Rubin at analyst Max-Q (1.8 kW GPU, 190 kW rack) | 0.94 1.04 1.25 1.39 2.04 | -- |
| Rubin chip 2.3 kW in 3,056 W slot (Ultra scaled the same way) | 0.97 1.07 1.29 1.44 2.11 | 0.86 0.86 0.95 0.98 1.03 |
| Continuum +150 / +300 W fixed per slot | 1.53 / 1.44 at >=1000 | 1.16 / 1.09 at >=1000 |
