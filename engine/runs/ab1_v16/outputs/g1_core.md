**1. Goals**
- G1: Keep learning from deployment experience without forgetting old knowledge.
- G2: Know when an answer is wrong, in a way that comes from inside the system's own structure.
- G3: Handle truly new problems by changing how the problem is represented, so known solutions apply.

**2. Paradigm negation**
Mainstream systems share one paradigm: a single differentiable network, trained by gradient descent on a prediction loss, that emits answers in one forward stream conditioned on context. That is forbidden as the mechanism here (gradient training of a monolithic network, forward-pass answering).

**3. Known families**
All 13 listed families are excluded as mechanisms.

**4. Mechanisms from the periphery**
- G1 comes from numerical weather prediction. The ensemble Kalman filter takes in a stream of observations without retraining. It uses covariance localization so that one observation only corrects nearby state, and inflation so the ensemble does not collapse.
- G2 comes from radio interferometry. "Closure phases" are sums around triangles of antennas, in which each antenna's own error cancels exactly. Solving across many triangles ("self-calibration") recovers each antenna's bias with no ground truth.
- G3 comes from compiler optimization. Equality saturation keeps an e-graph that stores every equivalent form of an expression at once. It applies rewrite rules until nothing new appears, then extracts the cheapest form.

**5. Honesty check**
- Idea 1: the closest work is ensemble Kalman inversion for neural networks (Kovachki & Stuart, 2019) and variational continual learning. Those train offline over the whole parameter space. The new part here is localization in representation space plus inflation, used as the anti-forgetting mechanism during deployment. Kept.
- Idea 2: the closest work is self-consistency voting and cycle-consistency. Neither solves for per-component bias from closure invariants; they only vote or penalize. Kept.
- Idea 3: the closest work is neural-guided equality saturation for program superoptimization. Here the e-graph is the general reasoning state, holding problem descriptions, with rewrite rules learned from solved episodes. That is an extension, not a copy. Kept, as the most incremental of the three.

=== IDEAS ===
IDEA 1
NAME: Localized Ensemble Kalman Learning
MECHANISM: The system keeps an ensemble of perturbed copies of a set of adapter parameters. Each new observation is assimilated by a Kalman-gain update computed from the ensemble's covariance between parameters and predictions; no gradients are used. The gain is tapered by distance in representation space, so an update only shifts parameters that covary with nearby inputs. Inflation keeps the ensemble's spread from collapsing.
VALUE: The system can learn continuously from single examples while deployed, with interference limited by construction rather than by replay.

IDEA 2
NAME: Closure-Invariant Self-Calibration
MECHANISM: Each query is answered through many short loops of different modules or routes (A→B, B→C, A→C, and inverse maps). For each loop the system computes the closure residual, in which each module's systematic error cancels. A least-squares solve over thousands of these triangles estimates and stores a bias term for each module. Those terms correct later outputs, and a large residual that remains after correction flags an unreliable answer.
VALUE: Error detection and correction become intrinsic and need no labels, because errors are attributed to specific components.

IDEA 3
NAME: Saturating Equivalence-Graph Reasoning
MECHANISM: The reasoning state is an e-graph that holds all known equivalent descriptions of the problem at once, with no destructive rewriting. Rewrite rules mined from solved episodes are applied until saturation or until a budget runs out. The system then extracts the representation with the lowest cost under a learned "solvability" cost. New rules are added when an extracted form leads to success.
VALUE: Unfamiliar problems become solvable when some equivalent re-description reaches already-mastered territory, and rules combine across domains.