All three ideas below use only objects, flows, rules and signals. Each one changes either what the generators are given to start from or how a kept answer is measured, so none of them re-skins the forbidden families.

=== IDEAS ===
IDEA 1
NAME: Stall-Point Seeding
MECHANISM: Before generation, a walker agent takes each plain answer and plays it out step by step on one specific, concrete instance of the question. It records the first step where the walk stalls: what was missing, what contradicted what, or what cost exploded. Generators receive only these stall records, never the plain answers, and must produce an answer that gets past a named stall. The same walker then replays that instance to confirm the answer passes the step. A stall table is kept between runs, holding each stall, how often it was hit and how many answers got past it. Stalls nobody has passed get more sampling weight in the next run, and stalls that have been passed are retired.
VALUE: Originality is pointed at the exact places where obvious answers break, so new ideas start from real failure points and are less likely to lose on value to the plain answers.

IDEA 2
NAME: Hint-Gap Selection
MECHANISM: For each surviving idea, an author agent writes a hint of at most 15 words. N fresh agents each get the question plus the hint and try to rebuild the full mechanism, and N other fresh agents get only the question. A comparer agent scores each rebuild against the original, field by field. Selection keeps ideas where rebuild success with the hint minus rebuild success without it is large. A high with-hint score means the idea is crisp enough to be compressed. A low without-hint score means it does not follow from the question alone. Ideas that score low with the hint are sent back for rewriting instead of being dropped. Hints that score well, and their ideas, are stored so later runs can tell whether a "new" idea rebuilds from an old hint.
VALUE: One signal that comes from repeated sampling rewards ideas that are both unexpected and concretely specified, without depending on what the judges happen to know.

IDEA 3
NAME: Outcome-First Reverse Build
MECHANISM: A first agent writes a dated, specific success record: who used it, the measured before and after numbers, and what changed. A judge accepts the record only if it would surprise someone holding the plain answers. A second agent sees only the record, not the forbidden families, and works out the smallest mechanism that could produce it. A third agent walks forward from that mechanism to see whether it really yields the record's numbers, and keeps only matching pairs. Records with no workable mechanism are stored as open targets and seeded into the next run. Mechanisms that worked are stored as templates that the next run must not repeat.
VALUE: Concreteness and value are built in from the start, because every idea is derived backward from a specific measured payoff instead of having details added after the idea exists.