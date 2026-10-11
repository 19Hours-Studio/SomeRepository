**1. Adaptive concept mesh (from finite-element analysis)**
- **Goal and symptom:** Too coarse in the places that matter. Two inputs that differ in a small but decisive way get the same confident answer.
- **Paradigm negated:** One fixed-resolution representation trained end to end. No loss, perplexity or calibration measures allowed.
- **Pair ported:** The Zienkiewicz-Zhu a posteriori error estimator plus adaptive mesh refinement.
  - State: a partition of the latent space into cells, each with a local linear map.
  - Measurement: η = ‖local Jacobian − patch-recovered (neighbour-averaged) Jacobian‖. It needs no labels.
  - Update: split a cell into children with their own maps when η > 2·mean(η). Merge siblings when η < 0.2·mean(η).
- **Honesty:** The closest work is mixture-of-experts, growing neural gas and adaptive trees. Those are driven by loss. This one is driven by smoothness that the neighbouring cells don't support, so it is kept.

**2. Taxonomy regrafting (from phylogenetics)**
- **Goal and symptom:** Inheritance doesn't hold. Properties inferred down the concept hierarchy turn out wrong, such as "whale breathes through gills".
- **Paradigm negated:** Flat associative similarity. No accuracy or embedding-distance measures allowed.
- **Pair ported:** The parsimony consistency index plus subtree prune-and-regraft (SPR).
  - State: a rooted concept tree with property characters at the leaves.
  - Measurement: CI = (minimum possible changes) / (changes the tree forces). Homoplasy is a property that has to arise independently in several branches.
  - Update: when the mean CI of a subtree falls below 0.6, prune it. Regraft it at the position with the best tree-length score.
- **Honesty:** The closest work is ontology learning and hierarchical clustering. Neither uses a homoplasy-driven rewiring rule. This differs from CAUSGR because it is a heritability tree, not a prediction-error causal graph.

**3. Premise status estimation (from power-grid state estimation)**
- **Goal and symptom:** One wrong premise spreads into everything. A single bad source quietly bends the whole answer.
- **Paradigm negated:** Weighting each source by its own confidence or by attention. No confidence or entropy scores allowed.
- **Pair ported:** The largest normalized residual test plus topology-error processing.
  - State: premises as typed meters (evidence or suspect) and rule links with a status (applies or doesn't apply), all fitting one weighted least-squares situation estimate.
  - Measurement: rᴺᵢ = rᵢ / √Ωᵢᵢ. This is the residual of each premise against the redundancy from all the others.
  - Update: when max rᴺ > 3, re-type that premise as suspect or flip a link's status, then re-estimate and repeat.
- **Honesty:** The closest work is RANSAC and robust estimation. Neither re-types the structure. This differs from TMS because there is no justification ledger, and conflicts are found from statistical redundancy.

The three use different fields and different structural changes: create/delete, rewire and re-type.

=== IDEAS ===
IDEA 1
NAME: Error-Estimated Adaptive Concept Mesh
MECHANISM: The latent space is divided into cells, each holding its own local linear map. For each cell, a Zienkiewicz-Zhu-style estimator compares the cell's Jacobian with the Jacobian recovered from its neighbours. Cells whose discrepancy is above 2x the mean are split into children with new maps, and calm siblings are merged. Resolution grows only where distinctions actually change.
VALUE: It can tell apart near-identical cases with different outcomes, without uniform scaling or labelled error.

IDEA 2
NAME: Homoplasy-Driven Taxonomy Regrafting
MECHANISM: Concepts sit in a rooted tree with property characters at the leaves. The system computes the parsimony consistency index of each subtree. When convergent properties push the index below 0.6, it prunes that subtree and regrafts it where the total tree length is smallest. Inheritance inference only runs over the repaired tree.
VALUE: Properties inferred down the hierarchy stay valid, and the system restructures its own categories when inheritance fails.

IDEA 3
NAME: Normalized-Residual Premise Re-typing
MECHANISM: Premises and rule links are treated as redundant meters that fit one weighted least-squares situation estimate. For each premise, the system computes a residual against the others, normalized by its residual covariance. If the largest is above 3, that premise is re-typed as suspect, or a rule link's applies/doesn't-apply status is flipped, and the estimate is recomputed until every residual passes.
VALUE: A single corrupt input can no longer quietly distort the whole conclusion, because redundancy finds it and isolates it.