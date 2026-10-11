**My 12 first answers:**
1. A cross-run ledger of forbidden families.
2. A forecaster that predicts families before generation.
3. Literature-backed problem cards placed up front.
4. Pre-registered kill tests run by a verifier.
5. Asymmetric graft crossover.
6. Judges from different providers or personas.
7. Pairwise Elo or tournament scoring.
8. A MAP-Elites archive.
9. A Pareto front with a value floor.
10. A critique-and-revise stage.
11. Retrieved cross-domain analogies.
12. Human expert raters in the loop.

**The paradigm they share:** they all keep "generate answers, then judge them" as the core loop and add better filtering, scoring or memory around it.

**What I forbid:** everything above and anything near it. That means no new selection rule, no new judge set-up, no archive of families, no evidence stage moved to the front, no falsification stage, no crossover variant, no polishing stage and no analogy seeding.

**Where I look instead:** the idea is not the only place originality can live. It can sit in the question that gets asked, in the gaps inside obvious plans, or in the structure an idea has to fit.

=== IDEAS ===
IDEA 1
NAME: Odd Question, Plain Answer
MECHANISM: A new first stage rewrites the original question into many changed versions, each made by one rewrite operator: change the scale, the actor, the time horizon, the unit of analysis, or who pays. The forbidden-family check is applied to these rewritten questions instead of to the answers. Each kept question is answered by the ordinary plain-answer stage, and an agent then maps that answer back onto the original question. The pipeline stores which rewrite operators produced answers that kept their value after mapping back, and samples those operators more often in later runs.
VALUE: Plain answers are already the most valuable and concrete outputs, so moving originality into the question gives answers that are both original and dependable.

IDEA 2
NAME: Hand-Wave Mining
MECHANISM: Implementer agents take each plain answer and expand it into a detailed step-by-step build plan. They must mark every step where they cannot say exactly what is done ("then calibrate appropriately"). These gaps are collected across all the plain answers and grouped together, and generation then targets only the gaps that recur. A finished idea is a specific way to fill one gap, inserted into the plain plan it came from. The pipeline keeps a list of gaps that are still unfilled and checks whether each fill actually removes the gap when the plan is expanded again.
VALUE: Originality goes into the step everyone skips, inside a plan that is already valuable, so the new ideas arrive concrete and buildable.

IDEA 3
NAME: Structural Signature Sampling
MECHANISM: Before writing any content, a generator is assigned a structural signature: who acts, what is stored, when it fires, and what is measured. Signatures are drawn from a grid of combinations, weighted toward combinations that past runs rarely produced. The generator must write an idea that fits that signature exactly. Judges classify ideas by signature rather than by meaning, which gives a fixed set of categories and stops new attractor families from appearing at every layer. How often each signature turns out valuable is stored, so later sampling moves toward rare combinations that are still valuable.
VALUE: Novelty becomes a controlled, repeatable input rather than a lucky output, which cuts run-to-run variance and makes it clear which structures produce value.