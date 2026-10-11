1. GOALS: long-horizon credit assignment; continual learning without overwriting; extrapolation beyond seen magnitudes.

2. PARADIGM: Mainstream AI stores knowledge in fixed numeric parameters, all moved down the gradient of one averaged error. This is forbidden as a mechanism.

3. All of families A–H are avoided.

4. PERIPHERY:
(1) Hydrology, end-member mixing: conservative tracers in a stream are unmixed to find each source's share of the flow.
(2) Frost's bone mechanostat: bone tissue is added above one strain set point, removed below another, and left alone between them.
(3) Buckingham π with data collapse: exponents are chosen so that data from all scales fall on one curve, which is then tabulated (Moody diagram).

5. HONESTY:
(1) Closest is eligibility traces. This differs because provenance is conserved and solved exactly, with no decay horizon.
(2) Closest is coupled learning in flow networks (Stern et al.). This differs by having no clamped/free contrast and an untouched dead band.
(3) Closest is dimensionless learning (BuckiNet). That needs the units given; here the units are discovered. This is nearest the line, but kept.

=== IDEAS ===
IDEA 1
NAME: Tracer-Unmixing Credit Flow
MECHANISM: Signals are a conserved quantity routed between units. Each unit holds the flow-weighted mix of its inflows, and each decision injects a unique tracer vector that mixes along conservatively. When an outcome arrives, the local tracer composition is unmixed by solving a small mass-balance system, giving each past decision's exact share. Each link then scales its routing fraction by (1 + rate × outcome × credited tracer it carried), and nodes renormalize.
DIFFERENCE: Exact credit across arbitrarily long delays in one forward pass, with no backward sweep or decaying trace.

IDEA 2
NAME: Lazy-Zone Remodeling Network
MECHANISM: Knowledge is the link capacities in a graph. During learning, inputs supply flux, required outputs demand it, and flow settles by conservation at nodes; in use, outputs are left open and the flux they receive is the answer. Each link tracks a slow average strain (flux ÷ capacity): above an upper set point its capacity grows with the excess, below a lower one it slowly shrinks, and inside the band nothing changes.
DIFFERENCE: New learning reshapes only links that are overloaded locally, so practiced skills are not worn down by a global error that touches everything.

IDEA 3
NAME: Scaling-Collapse Similarity Tables
MECHANISM: Each raw input gets a small integer exponent vector over k hidden base dimensions. The exponents are chosen by discrete search (smallest k first) for the assignment under which data from all scales collapse onto one surface in dimensionless products. That surface is stored as a sparse table, filled in and interpolated from experience; only quantities with identical exponent vectors may be added or compared.
DIFFERENCE: Predictions stay valid at magnitudes never seen, because the relation is built to be unchanged when any discovered dimension is rescaled.