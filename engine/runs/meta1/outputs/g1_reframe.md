These three ideas each change what the pipeline does, not just how it filters. The first reshapes the question, the second explores what happens after an idea is adopted, and the third builds up mechanisms before any question exists.

=== IDEAS ===
IDEA 1
NAME: Sibling-Question Expansion
MECHANISM: Before attractor mapping, a "question mutator" agent applies named operators to the input question to produce 6-10 sibling questions: invert the goal, change the scale by 1000x, swap who benefits, remove the main resource, or ask what would make the question moot. Each sibling question runs through the normal generate-and-judge stages. A "porter" agent then translates each sibling's best answers back into the original question, and the judges score the ported answers against the original question. Each operator's record of producing ported answers classified NEW is stored across runs, and the operators are re-weighted so the mutator learns which reframings pay off for which kinds of question.
VALUE: The pipeline delivers a map of neighbouring questions that are worth asking, each with its own answers, alongside answers to the question it was given.

IDEA 2
NAME: Adopted-World Diary Simulation
MECHANISM: After stage 3, each survivor is assumed to be fully adopted. Three inhabitant agents (an operator, a competitor and a bystander affected by it) each write a dated diary of the first year in that world. A "consequence miner" pulls out the second-order problems and opportunities from the diaries. Those become new seed prompts, which the portfolio answers in a follow-up generation pass. The resulting parent idea, consequence and child idea chains are stored and scored as one unit.
VALUE: The pipeline can discover ideas that only make sense once another idea exists, so it produces linked sequences of ideas instead of standalone answers.

IDEA 3
NAME: Orphan Mechanism Inventory
MECHANISM: In every run, a separate "inventor" agent is given no question at all. It is only given random constraint tuples (one material, one actor, one timing rule, one quantity), and it builds fully specified mechanisms from them. These "orphan" mechanisms are stored in a persistent cross-run inventory. A "matchmaker" agent searches that inventory for orphans that answer the current question, and the judges score each match. An orphan's match history raises or lowers the chance that its constraint tuple is sampled again.
VALUE: Over many runs the pipeline builds up a stock of concrete mechanisms made before any question existed, so it can answer future questions it has never seen using mechanisms that no question-driven search would have produced.