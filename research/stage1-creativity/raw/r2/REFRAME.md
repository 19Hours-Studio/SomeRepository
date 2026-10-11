=== IDEAS ===
IDEA 1
NAME: Co-Entraining Oscillator Mesh
MECHANISM: Units are coupled oscillators whose phase and natural frequency carry the state, not activation vectors alone. Each unit stores a learned intrinsic frequency and adjusts it by phase-locking to incoming rhythms and to peer units, so information lives in the pattern of synchrony. Coupling strengths learn from locking error through a local Kuramoto-style rule, with no backpropagation through time.
DIFFERENCE: It can settle into a shared tempo with another system over time, developing a mutual rhythm that neither party was instructed to adopt.

IDEA 2
NAME: Self-Grown Aesthetic Preference Field
MECHANISM: The system maintains a taste field, a learned scoring function over its own outputs, built only from its past choices and their downstream trajectories. Before answering, it generates candidate outputs and ranks them by this field as well as by requester approval. Each choice updates the field, so preferences accumulate, drift, and persist across unrelated tasks.
DIFFERENCE: It can hold and openly act on aesthetic commitments of its own, preferring an output it finds more beautiful even when a requester would find it less useful.

IDEA 3
NAME: Place-Dwelling Trace Agent
MECHANISM: The agent lives in a persistent world graph and leaves a trace on each node it visits, with trace strength set by surprise at that node. A small policy reads the local trace landscape to choose where to go next and updates its weights online whenever it returns to a place. Its internal state is a geography of visited places rather than a set of stored facts.
DIFFERENCE: It can return to a place out of its own interest, with no task or query requiring it, and develop a favourite place it revisits by choice.