The retrofit re-run (Idea 3) has finished and matches the author's numbers, so I've now checked every script except the slow round-0 rows of `table.py`. The "failed" status came from `diff`, not the model: it exits with code 1 whenever the files differ at all. Every row matches `retrofit.out`:
- **Untensioned:** 3.9–8.5 µm.
- **At 1000 N/m:** 0.5–1.1 µm.
- **Extra axial strain in the panel:** 0.46–0.93%, rising to 1.21% if the adhesive stiffens in the cold.

The only difference is that the author's stored file is missing the last row (G = 10⁶ Pa, no set, T = 1000 N/m: 0 µm, 1.21% strain). That row repeats the untensioned one and changes nothing. I've added this to `review.md`.

The verdict is unchanged. Idea 3's numbers hold, and its 1.2% cold-opening strain is still above the roughly 1% limit for the panel's transistors, so it stays second choice. Idea 1 still decides the result. The round-0 rows of `table.py` remain the only part I didn't re-run myself; they are the same function's output already stored in `critic0/oca_coupled2.out`.

HONEST GAIN: modelled residual of about 0.1–0.9 µm and 0.04–0.30 mrad at 1000 N/m (realistic set, 22–30 µm panel), about 50–800× below the aged Duo's 167 µm (unverified until the strip test). It is not shown to be invisible: slopes above about 0.024 mrad fail the answer's own vernier criterion.