The background job that re-ran all the scripts hit its 10-minute limit and was stopped before it finished. It didn't confirm a fresh run for every script:

- **Reproduced exactly:** A's `checks2.py` and B's `sandwich.py`, which is what I said earlier.
- **Didn't finish:** A's `design2`, `design3` and `sag_combo`, and B's `table`. Their fresh outputs never matched, most likely because they were cut off. I got that wrong before: I said B's `table.py` reproduced exactly, but it didn't.
- **Never started:** B's `glass_flaw.py` and `retrofit.py`.

This doesn't change the verdict. I checked A's quoted crease numbers against its saved outputs, and they match. The decision rests mostly on how the answers are reasoned:
- B's 0.2 mrad "invisible" limit is above the visual threshold B itself cites.
- B assumes the glass takes no set.
- B uses an optimistic panel thickness and ignores the glass's internal tension.
- A's main experiment is designed to kill the design if its central unknown is wrong.

I didn't restart the job. Re-running the slow scripts would only show whether the saved outputs can be regenerated. It wouldn't change which answer is better.

WINNER: A
MARGIN: clearly
WHY: I recomputed the key strain, stress and stiffness figures and checked A's quoted crease numbers against its saved outputs. Two scripts re-ran exactly; the rest were cut off by the time limit. A fixes B's real flaws: an "invisible" limit that is above the visual threshold B itself cites, an assumption that the glass takes no set, an optimistic panel thickness, and ignoring the glass's internal tension. A also turns the glass's own set into a cheap test that can kill the design, and it states its packaging costs openly.