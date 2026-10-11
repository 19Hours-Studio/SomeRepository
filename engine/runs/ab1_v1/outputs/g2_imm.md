**1. Goals (from the center)**
- G1: Keep learning after deployment without breaking anything that relies on older knowledge.
- G2: Reason through many steps without errors piling up.
- G3: Know how reliable a newly learned piece of knowledge is before much evidence exists for it.

**2. Paradigm negation**
Mainstream approaches share one paradigm: a single network fitted by gradient descent, which produces each step in one forward pass and accepts it at face value. That is forbidden here as the mechanism.

**3. Forbidden families**
I avoided all of the listed families, including the geodetic network adjustment that V18 already covers.

**4. Mechanisms from the periphery**
- G1 → zoological nomenclature (ICZN). Each name is tied to one physical type specimen. If a taxon is split, the name stays with the half that holds the type. If two names are merged, the older one wins (the priority rule).
- G2 → kinetic proofreading in biochemistry (Hopfield, 1974). Delayed intermediate steps that cost energy give each wrong candidate several independent chances to fall away. The error rate then drops from ε to roughly ε^k.
- G3 → animal breeding, specifically BLUP (best linear unbiased prediction) with a pedigree relationship matrix. An animal with few records of its own borrows strength from its relatives through the inverse relationship matrix A⁻¹, which can be built sparsely with Henderson's rules.

**5. Honesty check**
- Idea 1: the closest work is prototype networks and ontology versioning. Neither has a rule for which part keeps the identity when a concept is split or merged, so this is kept.
- Idea 2: the closest work is verifier cascades and rejection sampling. Those run one-shot filters. They have no off-rates that depend on margin and no reset to the start, so the error doesn't compound down exponentially. Kept.
- Idea 3: the closest work is hierarchical Bayesian models and COMPMAP. Neither uses a lineage (derivation) kinship matrix, so this is kept, though it is the nearest of the three to existing work.

=== IDEAS ===
IDEA 1
NAME: Type-Specimen Concept Nomenclature
MECHANISM: Every learned concept gets an identifier tied to a frozen type specimen: one stored input plus the internal state it produced. Concept regions may drift, split or merge as new data arrives. On a split, the identifier follows the part that contains the type specimen, and the other part gets a new identifier. On a merge, the older identifier wins. Downstream skills cite identifiers, not weights, so they re-resolve through the types and keep working after revisions.
VALUE: It allows open-ended concept revision without silently breaking the skills and inferences built on older concepts.

IDEA 2
NAME: Kinetic Proofreading Decoder
MECHANISM: A candidate step does not commit right away. It passes through k timed holding stages, and each stage re-scores it under a freshly perturbed context. A candidate drops out at each stage with an off-rate that grows exponentially as its support margin falls; a candidate that drops out restarts from scratch rather than going back one stage. The value of k and the compute spent per stage are set according to how much is at stake in the step.
VALUE: Error per step falls exponentially with the compute spent, so long chains of reasoning stay reliable instead of degrading.

IDEA 3
NAME: Pedigree-BLUP Knowledge Reliability
MECHANISM: Each acquired fact, rule or skill is logged with its parents, meaning the items it was derived or distilled from. This builds a sparse relationship matrix. Reliability is solved as a breeding value with Henderson's mixed-model equations, so an item with almost no direct checks borrows strength from its relatives. A single new check updates the whole family through A⁻¹.
VALUE: Reliability estimates for brand-new knowledge become usable after one or a few observations, because they draw on where that knowledge came from.