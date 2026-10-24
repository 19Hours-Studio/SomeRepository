# Crease-free foldable: strain budget per layer and three architectures

**Deciding number.** A crease is permanent set in any layer that leaves its recoverable regime during a folded dwell. Bending strain is ε = y/R, where y is the distance from the bending axis.

- **Bonded stack:** with a 150 µm stack and the neutral plane at the OLED, the cover sits at y ≈ 60 µm. At R = 1.5 mm that gives ε ≈ 4%, beyond the yield of PI (≈2–3%).
- **Decoupled layers:** each layer bends about its own midplane, so ε = t/2R. Slip between layers then follows Δ = d·θ, which does not depend on R. With d = 50 µm and θ = π, Δ ≈ 157 µm. Across a 25 µm OCA that is about 600% shear, and this is where creep sets in.

| Layer | ε at R = 1.5 mm, decoupled | Recoverable after 8 h at 60 °C? |
|---|---|---|
| UTG 30 µm | 1.0% | Yes. Glass does not creep at room temperature, and it is fatigue-rated (NEG, Samsung) |
| PI 10 µm | 0.33% | Unmeasured. I estimate the limit at about 0.3–0.5% |
| OCA | ~600% shear | **No. This layer sets the limit** (3M: hours to recover) |
| Polarizer replaced by colour-filter-on-encapsulation | — | Removes about 50 µm of d |
| Support plate | Elastic only if strain < ~0.2% | Laser-perforated plate |

**Invisibility targets** (perception thresholds are my speculation):
- Residual depth below 3 µm.
- Peak slope below 0.05°, so reflected lines deviate by less than 0.1° at 60° off-axis, viewed under a striped light box.
- In a double-blind finger swipe, detection at chance level (n ≥ 30).

**Persistence test.** Run 2000 cycles at 60 °C and 90% RH, including 8 h folded dwells and −10 °C cycles. Measure with white-light interferometry at 1 min and 1 h after opening. The main failure modes are:
- OCA creep and delamination
- PI viscoelastic set
- glass fatigue at the edges
- plate yield
- debris in the hinge

**Established versus speculative.**
- Established: the strain formulas, the fact that glass does not creep, and OCA's slow recovery.
- Speculative: the PI creep limits, the gel's long-term stability, and the perception thresholds.
- No public µm baseline exists for any phone.

**Cheapest experiment (about $5k).** Fold coupons of each stack around mandrels at 60 °C for 8 h, then profile them.

**Comparison with shipped approaches.**
- The reported Apple/Samsung perforated plate makes the support smoother. It still keeps an OCA-bonded stack at about 1.5 mm, so the shear-creep source remains.
- Oppo's liquid printing evens out hinge height to about 50 µm. It does not address stack set.

**Cost.** The retail cost ceiling is about 2.3x, so I claim no cost gain. Expect about $10–30 extra per module, with yield as the risk. The trade-offs are 1–2 mm more folded thickness, about 5–10 g more mass, a firmer touch feel over the gel band, and a brightness gain of about 1.5x from dropping the polarizer.

=== IDEAS ===
IDEA 1
NAME: Gel-slip decoupled glass stack
MECHANISM: In the fold band, the OCA is replaced by an index-matched, sealed silicone gel or fluid that carries the 157 µm interlayer slip as flow with no shape memory. Each solid layer then bends about its own midplane at ε = t/2R ≤ 1%. This differs from creep-recovery OCAs, which still store shear; the deciding quantity is the gel's residual shear set after 8 h folded at 60 °C. The polarizer is replaced by colour-filter-on-encapsulation, which cuts layer separation by about 50 µm.
VALUE: It removes the layer that dominates crease formation, so a crease cannot form under worst-case dwell.

IDEA 2
NAME: OLED directly on UTG
MECHANISM: The TFT and OLED are built on a 30 µm strengthened glass substrate instead of PI, and the panel is sealed with a second UTG. Only glass carries strain, at 0.75% for R = 2 mm. Glass shows no creep at room temperature, so there is no material that can take a permanent set. This differs from earlier thick-UTG covers, which still sat on PI and OCA that creep. The deciding quantity is the 2000-cycle fatigue survival of glass at 0.75% strain with TFT films on it.
VALUE: Every load-bearing layer stays fully elastic, which makes crease persistence a non-issue.

IDEA 3
NAME: Large-radius tensioning teardrop hinge
MECHANISM: A teardrop hinge with R ≥ 3 mm keeps every bonded layer below 0.3% strain. On opening, sliding wing plates put the panel under about 0.1% in-plane tension, pulling any residual curvature flat against a continuous, interlocking plate. This differs from current teardrop hinges, which leave the panel slack and depend on hinge tolerance. The deciding quantity is the residual depth under tension after dwell, versus the tension the edge bonds can hold.
VALUE: It actively flattens the panel each time it opens, using shipped materials, at a cost of about 1.5 mm more folded thickness.