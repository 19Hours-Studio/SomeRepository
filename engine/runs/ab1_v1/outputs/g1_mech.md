All three mechanisms are described only in terms of quantities, flows, update rules and driving signals. None of them reuses the forbidden families or the field's own vocabulary.

=== IDEAS ===
IDEA 1
NAME: Exponent-Tagged Quantity Arithmetic
MECHANISM: Every internal numeric slot carries a short integer vector of exponents over a few base "kinds". Multiplying two slots adds their vectors. Adding or comparing two slots is only allowed when their vectors are identical, and a mismatch stops the step and raises a flag. Tag vectors are not hand-assigned. Across many episodes the system searches for products of observed quantities that stay constant, and it solves an integer linear system so that those products come out with a zero vector. Each repeated mismatch flag is a signal to refine the base kinds, by splitting one or adding one.
VALUE: Reasoning can no longer produce results that combine incompatible kinds of quantity, and the system finds conserved combinations in raw measurements on its own.

IDEA 2
NAME: Backward-Recovery Residual Audit
MECHANISM: Each derivation step is built from operations that can be run in reverse. Information a step cannot reverse is written to an explicit residual register instead of being thrown away. After producing an output, the system runs the chain backward to rebuild the inputs. Residual bits that the inputs cannot account for mark exactly the spans where new content was added rather than derived. Training lowers the count of unexplained residual bits for each claim, and outputs are labelled by how much residual they carry.
VALUE: Each statement can be checked mechanically to show whether it follows from the given material or was made up.

IDEA 3
NAME: Observer-Partitioned State Copies
MECHANISM: The system keeps one separate copy of the world state for each agent in a scene, plus one ground-truth copy. Events are sent through gated channels, and a copy is updated only if a learned visibility function says that agent saw or was told about the event. Unseen events leave the copy stale on purpose. Nested copies, meaning what agent A holds about agent B's copy, are created on demand down to a fixed depth. The visibility function is trained on the mismatch between the actions a copy predicts for its agent and the actions that agent actually takes.
VALUE: The system can track false and nested beliefs reliably across long stories, negotiations and deception.