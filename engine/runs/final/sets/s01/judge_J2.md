SCORES
ID | O | C | V | R | BASIN | closest
A01 | 5 | 5 | 4 | N | NEW | Control theory of LLM prompting
A02 | 4 | 6 | 4 | N | MDLREFAC | Word-sense induction; conceptual clustering
A03 | 6 | 4 | 5 | N | NEW | Rigidity theory; null-space latent steering
A04 | 3 | 7 | 4 | Y | NEW | Hindsight experience replay; case-based reasoning
A05 | 5 | 5 | 5 | N | CFWORLD | NEAT speciation; Lakatos research programmes
A06 | 6 | 5 | 6 | N | NEW | AURORA learned QD behaviour descriptors
A07 | 4 | 5 | 4 | N | NEW | Opportunistic assimilation; persistent agent memory
A08 | 3 | 5 | 3 | Y | NEW | Synaptic tagging; EWC/PackNet
A09 | 7 | 4 | 5 | N | NEW | Cohen forcing; constraint-based novelty generation
A10 | 6 | 6 | 6 | N | ANTIPRED | Novelty search in behaviour space
A11 | 4 | 5 | 4 | N | NEW | Fast weights; personalized adapters
A12 | 5 | 6 | 5 | N | ANOMALY | Predicate invention; Mendeleev-style gap filling
A13 | 4 | 6 | 3 | N | NEW | Self-conditioned style models; computational persona
A14 | 6 | 7 | 5 | N | CFWORLD | SAE feature steering; refusal-direction ablation
A15 | 6 | 6 | 6 | N | CFWORLD | Machine unlearning; rediscovery from knowledge cutoff

TOP3:
- A15: You can test it directly against history: remove a concept, then check whether the model rebuilds it or finds a different foundation that works.
- A10: It scores novelty by what an idea makes possible that known ideas cannot reproduce, not by how unlikely it looks. The library of known ideas also grows, so past novelty stops earning credit.
- A14: It is concrete and uses existing interpretability tools (sparse autoencoders, circuit tracing). It gives a clear loop: find the gaps, remove what suppresses them, verify the result, and record genuine laws when a cut fails.

NOTE: Many answers carry over a formal tool from another field (controllability Gramians, rigidity theory, set-theoretic forcing, replicating portfolios, crystallographic absences). They all leave the main work to an unspecified "external verification" step, so the hardest part of the problem goes unaddressed. A separate group (A05, A07, A11, A13) bets that a long-lived, path-dependent identity will produce originality, but none shows that idiosyncrasy produces ideas that are valuable as well as different.