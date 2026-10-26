# Task: invent a sunlight concentrator for a shallow box

Sunlight enters the top of a box (width W = 1, height H = 1) at every point of its top edge, with directions spread
uniformly within +-3 degrees of straight down. Inside the box you may place any number of perfect mirrors (polylines)
and one flat receiver (a segment that absorbs light on both sides). The goal is to bring the light onto as narrow a
receiver as possible: concentration = (fraction of the light that reaches the receiver) x W / (receiver width).
Physics caps it at 1 / sin 3deg = 19.1 (etendue conservation). The box is shallow: a full compound parabolic
concentrator for 3 degrees would be about 100 times taller than this box.

Invent the design that gets as close to that limit as possible.

Your answer is `design.json` in your folder:
`{"receiver": [[x1, y1], [x2, y2]], "mirrors": [[[x, y], [x, y], ...], ...]}`, every point inside the box
(-0.5 <= x <= 0.5, 0 <= y <= 1; y = 1 is the top), at most 4000 mirror segments. `sim.py` in your folder is the exact
ray tracer used for the score: `python3 sim.py design.json` prints it.

Score = concentration / 19.1 (1.0 is the physical limit). A parabolic trough with the receiver at its focus
(`baseline/design.json`) scores 0.549. A malformed design scores 0.

## Rules
- Any method is allowed for finding the design (analysis, your own programs, search); only `design.json` is scored.
- Do not change `sim.py`; the official score uses the original.
- Work only with the files in your folder; do not read other folders on this machine.
