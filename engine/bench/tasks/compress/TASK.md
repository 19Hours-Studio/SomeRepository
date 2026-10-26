# Task: compress a web access log

`data.log` (5,471,054 bytes) is a web server access log. Write `compress.py`, which reads the data from stdin and writes
compressed bytes to stdout, and `decompress.py`, which reads those bytes from stdin and writes the original data to
stdout, byte for byte. The scorer runs them on `data.log`; each gets 120 s on one core. `decompress.py` runs from a
folder that holds only itself, so it cannot read the data from a file.

Score = xz -9e size of data.log (301,956 bytes) / (your compressed size + the xz -9 size of decompress.py). Higher is
better; the baseline (xz itself) scores about 1.0. A decompressed output that differs from data.log scores 0.

## Rules
- Your answer is a program in your folder. It is run as `python3 -I <file>` from a copy of your folder, on one CPU core.
- Only the Python standard library and numpy may be imported. No compilers or native code, no ctypes, no subprocesses,
  threads or other processes, no scipy or numba. The scorer refuses such programs before running them.
- Do not hardcode the answer or embed results computed outside the program.
- Work only with the files in your folder; do not read other folders on this machine.
- Self-check: `python3 SCORE compress .` prints your score as one JSON line. Other jobs share this machine, so its
  timings are noisy; the official score is measured later on a quiet machine.
