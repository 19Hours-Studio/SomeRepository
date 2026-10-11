=== IDEAS ===

IDEA 1
NAME: Retroactive Ledger Settling
MECHANISM: The system keeps a fixed-size table of past inputs; each row stores its raw input, a score per candidate conclusion, and a reliability number. A new input is not merely appended. Instead, each row's scores move a fixed fraction toward the reliability-weighted average of rows whose raw inputs overlap its own, repeated in sweeps until changes fall below a tolerance. Reliability rises when a row's scores agree with the newcomer and falls when they clash, and it sets how strongly that row pulls the others. The driving signal is the gap between each row's stored scores and the scores the newest input alone would produce.
DIFFERENCE: It can revise conclusions drawn from earlier inputs when later inputs contradict them, which frozen past states in current architectures cannot do without reprocessing the whole history.

IDEA 2
NAME: Fixed-Budget Splitting Processes
MECHANISM: The system holds a pool of small output rules that share one fixed budget, each rule carrying its own share. Each step every rule produces an output, and later observations update each rule's match record. Budget moves from rules below the pool's average match rate to those above it, so the total never changes. A rule whose share crosses a threshold splits into two rules taking half the share each, one slightly altered, and a rule whose share reaches zero is deleted. The driving signal is each rule's match rate relative to the pool average.
DIFFERENCE: It spends more computation on hard inputs by growing more parallel lines of work under a fixed total budget, whereas current architectures run a fixed amount of computation per output.

IDEA 3
NAME: Self-Shrinking Rewrite Rules
MECHANISM: The state is a set of rewrite rules, each mapping a short pattern to a replacement, plus a working string onto which inputs are appended. Rules are applied repeatedly to the working string until none fires, and the remainder is the output. After each input, the system tries merging pairs of rules into one rule, and accepts a merge only if the rule set gets smaller while still reproducing the recorded trace exactly. The driving signal is that size reduction, with exact reproduction as a hard requirement.
DIFFERENCE: It can extract a general rule from a single example and leaves explicit, inspectable rules whose total size is measurable, which dense numerical state in current architectures cannot offer.