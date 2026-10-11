Seed use: idea 1 draws on "uaccess" (device grants that exist only while a session is active) and "manager". Idea 2 uses "updating", "silence" and "commas", with "anibal" as a principal identifier. Idea 3 uses "hashable", "causing" and "fixation", with "tiscali" as an external anchor. Two seeds are proper names, so their roles are loose.

=== IDEAS ===

IDEA 1
NAME: Lease-Gated Problem Memory Repository
MECHANISM: The model keeps a repository of learned solution slots partitioned by problem domain, and attention can read or write a partition only while a manager network holds a time-bounded lease on it for the current problem. Leases are granted at minimal scope as a problem opens, mirroring uaccess ACLs that exist only while a session is active, and are revoked when it closes. Training teaches the manager to issue the narrowest lease that still solves each problem.
DIFFERENCE: It can revoke or audit one learned item instantly and enforce per-task isolation at access time, which transformers cannot because their knowledge is spread across shared weights with no per-item access control.

IDEA 2
NAME: Clause-Gated Per-Speaker Fast Weights
MECHANISM: Each named principal (the "anibal" seed) owns a low-rank fast-weight adapter stored outside the frozen base model, and the base model reads it as conditioning on every forward pass. Incoming text is buffered and committed to the adapter only at comma boundaries, where a clause closes and the sentence is still open, so partial thoughts are never written. During silence, with no input from that principal, the adapter decays toward zero, so unused knowledge fades without explicit erasure.
DIFFERENCE: It keeps a persistent, isolated, self-decaying parameter-level memory for each person it works with, changing during deployment without retraining, which frozen transformers can only imitate by stuffing context.

IDEA 3
NAME: Fixation-Breaking Causal Hash Chain
MECHANISM: Each inferred cause-to-effect transition is stored as an immutable record keyed by a hash of its cause, which is safe as a lookup key only because it never changes, and each record links to its predecessor's hash. An external provider (the "tiscali" seed) signs the chain head periodically, so every causal claim can be checked against records the model cannot rewrite. A fixation detector counts how often one reasoning episode returns to the same record and, past a learned threshold, suppresses that record and forces retrieval of an alternative cause.
DIFFERENCE: It can justify each causal belief against an unrewritable history and break its own repetitive reasoning loops structurally, which transformers cannot, since their beliefs have no verifiable provenance and nothing watches for repetition.