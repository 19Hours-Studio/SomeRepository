`solution.py` prints the correct count, **434536**, and the self-check gave a **score of about 155** (0.36 s against the baseline's roughly 56 s). That machine is shared and noisy, so the official run may differ.

**Approach (meet in the middle, using numpy):**
- **Two halves:** I list every valid placement for rows 0–6 and, separately, for rows 7–14 (going upward). That's about 0.8 million and 2.4 million partial placements, each built row by row with vectorized masks.
- **Compact state:** each partial placement is stored as one 64-bit number: which columns it uses, plus both diagonal directions as they cross row 7. This is enough information: any diagonal that has queens from both halves has to pass through row 7.
- **Pairing:** a top and a bottom placement fit together when their columns exactly fill all 15 and none of their diagonals overlap. I sort both halves by column set (6435 groups) and count the compatible pairs in each group with one numpy array operation. That is about 290 million pair checks, which takes around 0.25 s.

The answer is computed from scratch every run; nothing is hardcoded.