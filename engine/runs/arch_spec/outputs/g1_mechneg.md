**1. Mechanical confession** (objects | flow | rule | signal)
1. Pixel arrays, weight stacks | image → weighted sums → category | weights nudged down the error slope | disagreement with human tags
2. Hand-coded generator, weights | generator output → network | same | disagreement with the generator's answer
3. Unlabelled streams | parts hidden, then predicted | same | reconstruction mismatch
4. Large prior weights, few examples | a small subset adjusted | same | tag disagreement
5. Solver with tunable fields | input → solver → prediction | slope passed back through the solver | gap to measurement
6. Fast copy of a solver | search over inputs | slope over inputs | distance to target output
7. Sensor sequences, carried state | past → state → next value | slope over time | forecast miss
8. Two opposed mappers | A → B → A | slope | round-trip mismatch
9. Proposer plus scorer | candidates expanded, then pruned | keep the best | scalar score
10. Vector library | query → nearest stored items | pull pairs together, push others apart | pair similarity
11. Actor in a simulator | act → outcome | make rewarded acts more likely | scalar reward
12. Noise-to-sample mapper | stepwise cleanup | slope | cleanup error

**2. Paradigm:** All twelve keep one store of continuous parameters. They change it offline and globally, using the slope or ranking of a single scalar that compares output against a stored target. **Forbidden:** any adjustment driven by a scalar objective. That includes fitness selection, relaxing toward a scalar energy, contrastive scores and learned surrogates.

**3–5.** None of the ideas below uses the twelve rows or the banned list. I fixed the mechanics first and named each idea last. The three driving signals are physical persistence, co-occurrence with a sound, and phase lag.

=== IDEAS ===
IDEA 1
NAME: Weathered Contact Ledger
MECHANISM: Task: dry-stone walling, choosing the next stone from an irregular pile. AI is absent here because a wall's stability only shows over seasons, and no dataset or reliable simulator exists. Phone depth video of each placed stone is fused on the GPU into contact patches, and a fixed, untrained curvature hash turns each patch into a 64-bit code. A ledger in RAM stores integer counts for pairs of codes, and 32 GB holds tens of millions of them. Each weekly rescan adds one count to every contact pair whose stones have not moved and deletes pairs that shifted, so there is no target and no error, only survival. To place a stone, the system ranks the scanned pile by the summed survival counts of each stone's possible contacts against the gap, a hash sweep that takes seconds.
VALUE: It learns stability from real walls surviving frost and time, which no same-budget simulator or labelled set can supply.

IDEA 2
NAME: Crackle-Gated Grain Map
MECHANISM: Task: choosing hand-plane direction and depth on figured wood (curly or interlocked grain) without tear-out. AI is absent because the work is tactile, every board is different, and tear-out only appears after the cut. Phone macro video of the board is cut into tiles, and a fixed random projection turns each tile into 2048 sparse binary cells. A contact microphone on the plane sorts each stroke, with a fixed spectral threshold, into a smooth hiss or a crackle. A 2048×16 cell-to-direction link table is updated locally: links active during a smooth stroke are strengthened and those active during a crackle are inhibited, and no output is ever scored. Recall is one sparse product per tile, so a full map of safe directions for the board renders live.
VALUE: It gives a safe-planing map for a board it has never seen, learned from the sound of the user's own strokes.

IDEA 3
NAME: Breath-Locked Drone Swarm
MECHANISM: Task: live accompaniment of unmetered, ornamented solo singing such as sean-nós or Persian āvāz, where beat- and score-based systems fail because there is no meter. A GPU bank of 8192 phase oscillators with periods from 0.2 to 20 s is driven by the singer's breath and syllable onsets, picked up by a phone microphone. Each oscillator shifts its frequency by the sign of its phase lag to the input, splits when it locks onto two alternating periods, and dies after a long time unlocked. Drone swells and harp strikes fire when large locked groups pass phase zero together, and a ring buffer of past phrase phases lets recurring phrases lock in again at once. Nothing is trained offline, and it runs in milliseconds within a few hundred MB.
VALUE: It accompanies free-rhythm singing by following the singer's breathing, which tempo trackers and sequence models cannot do on any budget.