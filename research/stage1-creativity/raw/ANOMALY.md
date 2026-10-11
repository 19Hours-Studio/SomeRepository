Untested proposals:

**1. Grokking: two-speed memory with delayed compression.** Memorizing is fast; generalizing means finding a shorter description of the same data, which gradient descent reaches slowly and only under weight-decay pressure. So split the system into a fast episodic store and a slow compressor that keeps searching for a program explaining the store, even after training loss is zero.

**2. Partly wrong CoT still helps: causal, repairable scratchpad.** If wrong steps don't ruin the answer, the trace works as computation and structure rather than a faithful proof. So make reasoning a graph of typed intermediate results that can be checked and recomputed locally, and learn which nodes matter by intervening on them.

**3. In-context learning without weight updates: transient weight compilation.** The forward pass can be read as a learning step, with the context held as activations. Make that explicit: the context is compiled into a small temporary parameter set, which answers queries and can then be stored, merged, or discarded.

=== IDEAS ===
IDEA 1
NAME: Two-Speed Memory with Consolidation
MECHANISM: A fast episodic store records each training example verbatim on first exposure. A slow compressor runs offline, including after training loss reaches zero, searching for the shortest program that reproduces the store. Predictions come from that program once its description length beats the stored table.
DIFFERENCE: It can detect when it has found a compact rule and switch from memory to rule explicitly, rather than relying on weight decay to slowly drive one parameter set toward generalization.

IDEA 2
NAME: Causal Typed Scratchpad with Repair
MECHANISM: Reasoning is a directed graph of typed intermediate results, each computed by an explicit operation over its inputs. A verifier flags nodes that fail local checks, and only those nodes and their dependents are recomputed. Training intervenes on each node and measures the change in answer, so the model learns which steps are causally load-bearing.
DIFFERENCE: It can localize and repair one wrong step without regenerating the whole trace, which a flat token stream cannot do because its steps have no separable causal identity.

IDEA 3
NAME: Transient Weight Compilation
MECHANISM: An encoder reads the context examples once and emits a low-rank parameter delta for a small task module, held in a transient weight buffer separate from the main weights. Queries run through the compiled module at a cost that does not grow with context length. The buffer can then be saved, merged with others, or erased.
DIFFERENCE: It makes a task a storable, composable, and removable object, whereas in-context learning leaves no reusable state and must re-attend over all examples on every query.