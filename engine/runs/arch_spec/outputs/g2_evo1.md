OFFSPRING 1 (Pair 1: decay clock × difference-map editing)
Task: telling search-and-rescue teams how many separate parties walked a muddy trail, when, and in what order. AI is absent because nobody has labelled multi-party trails, and single-print aging ignores the fact that later prints overprint earlier ones. A phone walk-video of 50 m of trail gives per-print relief profiles. The working hypothesis is a ledger of passes (party size, direction, time), with each print assigned to a pass. The weather-integrated decay function renders the expected relief of every print, including truncation where a younger print cuts an older one. Observed minus predicted gives a residual. A cluster that is too fresh splits a pass, and an inconsistent pair merges two passes. Each edit is kept only if R-free on 5% held-out prints improves. The coupling runs both ways: the decay clock decides which edits survive, and cut relations the ledger accepts become hard ordering constraints that fine-tune the clock on real trails.
Closest work: shoeprint/fingerprint aging (Rajs et al.) and forensic trackway counting. Neither infers a time-ordered set of passes.

OFFSPRING 2 (Pair 2: seasonal bathymetry × branching genealogies)
Task: finding sieves and undercuts, where water flows under rock and drowns paddlers. Foam patches and boils are tracked as genealogies: an eruption, splits into child boils, and terminations. They are scored with a multitype branching process whose offspring mean and delay are spatial fields predicted from a bed hypothesis. Foam that dies without spreading marks downwelling. The coupling: the bed grid sets the branching parameters, and the branching likelihood trains the bed on the many high-water clips that have no low-water pair.
Closest work: LSPIV/PIV depth retrieval (Legleiter) and kolk-boil geomorphology. Neither infers the bed from event genealogies.

OFFSPRING 3 (Pair 3: neighbour-predicted taps × impedance compartments)
Task: finding unrecorded burial vaults and voids under church floor slabs before floors collapse. Tap rings are predicted from neighbouring taps, and a compartment posterior groups slabs that share an air cavity. The coupling: compartment membership decides which neighbours a tap is compared against, and neighbour residuals in the 50–400 Hz cavity band are the impedance input that sizes each compartment.
Closest work: GPR crypt surveys and Shi et al. pole tap tests. Neither infers cavity volume and connectivity from residuals.

=== IDEAS ===
IDEA 1
NAME: Trail Pass Ledger
MECHANISM: Per-print relief profiles from a phone trail video are explained by a ledger of passes, each with a time and direction. A learned weather-integrated decay function (~2M weights, trained on staked time-lapse prints) renders expected relief, including overprint truncation. Residual clusters drive pass insert, split and merge edits, each accepted only if R-free on 5% held-out prints improves. Accepted cut relations become ordering losses that fine-tune the decay function. Prints are a few thousand numbers each, so the whole edit loop runs in RAM and the decay function trains on the 3060.
VALUE: It gives a count, order and time window for each party on a trail, which single-print aging or tracker intuition cannot.

IDEA 2
NAME: Boil Genealogy Riverbed Reader
MECHANISM: Foam and boil events tracked in a 10-second clip form trees of eruption, split and termination. A ~5M-weight network maps the surface-speed field and a bed hypothesis to per-cell branching parameters, and exact tree likelihood scores them. Low-water exposed beds supervise depth where a seasonal pair exists. Elsewhere the tree likelihood alone trains the bed, so unpaired high-water clips also become training data. Tree likelihoods take seconds on the CPU and the model fits in 12 GB.
VALUE: It flags sieves and undercuts from a phone clip by reading how surface events are born and die, which bathymetry-from-velocity methods ignore.

IDEA 3
NAME: Slab-Coupled Vault Mapper
MECHANISM: About 400 hammer taps on floor slabs are reduced to 64-band spectra. A <1M-weight network predicts each tap from neighbours that a <20M-parameter transformer assigns to the same air compartment. The transformer reads the cavity-band residual field and outputs a posterior over compartment count, volume and connectivity, and its assignments re-gate the neighbour predictor until both settle. It is pretrained on millions of lumped plate-over-cavity simulations, fine-tuned on churches with recorded vault plans, and trains overnight.
VALUE: It gives a sized, uncertainty-bounded vault map from a hammer and phone, where the same budget otherwise buys only guesswork or a hired GPR crew.