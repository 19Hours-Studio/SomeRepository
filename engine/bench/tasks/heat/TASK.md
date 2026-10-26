# Task: invent how to cool a plate that heats everywhere

A square plate (101 x 101 cells) produces heat uniformly in every cell. The heat can leave only through a small sink:
the 5 middle cells of the bottom edge, held at T = 0. All other edges are insulated. The plate is made of a base
material (conductivity 1); you may replace at most 10% of the cells with a highly conductive material (conductivity
200). Where you put it decides how hot the plate gets.

Invent the layout that keeps the hottest point of the plate as cool as possible.

Your answer is `design.txt` in your folder: 101 lines of 101 characters, '1' = conductive material, '0' = base
material; the first line is the bottom row (the sink side). `sim.py` in your folder is the exact physics used for the
score: `python3 sim.py design.txt` prints it.

Score = hottest point of the bare plate / hottest point with your design (higher is better). A single straight strip
up the middle (`baseline/design.txt`) scores 8.9. More than 10% material, or a malformed file, scores 0.

## Rules
- Any method is allowed for finding the design (analysis, your own programs, search); only `design.txt` is scored.
- Do not change `sim.py`; the official score uses the original.
- Work only with the files in your folder; do not read other folders on this machine.
