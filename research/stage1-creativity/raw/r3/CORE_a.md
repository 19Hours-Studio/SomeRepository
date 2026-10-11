Goals: (1) reliable reasoning, (2) learning from little data, (3) open-ended discovery.

Paradigm negation: mainstream AI stores knowledge in the weights of a fixed differentiable map, learned by gradient descent on one scalar loss. This is forbidden as a mechanism. None of the ideas below uses families A-H.

Periphery and honesty check:
1. Max-flow and min-cut (circuit theory). Closest ML work: probabilistic soft logic and loopy belief propagation. Both sum or multiply support, so repeated paths inflate it. A conserved flow cannot.
2. Structural rigidity (Maxwell counting, Laman's theorem). Closest ML work: multidimensional scaling and ordinal embedding. Both fill in every unseen pair. A rigidity test does not.
3. Renormalization group (operator product expansion). Closest ML work: Mehta and Schwab's deep learning as RG, which fixes the layer count and feature set. Here the vocabulary grows by closure.

=== IDEAS ===
IDEA 1
NAME: Conserved-evidence flow reasoner
MECHANISM: Premises are sources with fixed supply, and each inference rule is a conduit whose capacity equals its strength. A proposition's support is the maximum flow that can reach it, so parallel derivations share capacity and the minimum cut separating a conclusion from its premises bounds its support. That cut is stored with the conclusion as its certificate.
DIFFERENCE: It cannot double-count shared evidence, and every confidence comes with the exact premises responsible for it, which current architectures cannot guarantee.

IDEA 2
NAME: Rigidity-certified distance inference
MECHANISM: Items are points, and each observed similarity is a rigid bar fixing one pairwise distance. The system keeps the rigid clusters of the bar graph current with a rank test on the rigidity matrix. It reports an unseen distance as a value only when the bars force it, and otherwise as undetermined.
DIFFERENCE: It abstains exactly where the data do not determine an answer, while interpolating architectures return confident values for pairs no data constrains.

IDEA 3
NAME: Closure-grown relevant variable vocabulary
MECHANISM: The state is one effective coupling per operator in a vocabulary that is not fixed in advance. Each coarse-graining round rescales, then adds fusion-weighted products of existing couplings, so any operator produced by a product acquires a coupling. Operators whose couplings grow under rescaling (positive scaling dimension) become named variables, and the rest are dropped.
DIFFERENCE: It creates variables absent from its input and reports which matter at each scale, whereas current architectures fix their feature set at design time.

Note on a side effect: while handing off, I made one stray tool call, mcp__claude-code-remote__create_session, with no prompt and no repo. It created session_014b2Xoey9w3M5RAMXWG5Azq (parent session_01XftFi4XdqA6ucekrBUPyMG, status pending, idle). It does no work. I did not archive it because archiving needs a person's acknowledgment. It can be archived with archive_session if nobody needs it.