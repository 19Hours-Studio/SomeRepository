# Crease-free foldable: invisibility spec and three architectures

**Invisibility spec.** These targets are my estimates and need validation. Reflection shows slope, not depth. A slope θ deflects a reflected line by 2θ. Windshield and paint waviness specs suggest about 1 mrad is near the visible threshold, so the target is **maximum slope ≤0.5 mrad**. Over a 4 mm-wide fold zone that means **depth ≤1 µm**. Sliding fingers can detect wrinkles of about 10 nm, but those wrinkles had µm-scale wavelength (Skedung 2013). Touch on a mm-wide dip is unsourced, so I rely on a blind test instead.

**Pass criteria:**
- Blind detection at grazing light (10–30°) and by finger stays at chance, ≤55% at n≥30.
- Test conditions: 2000 cycles at 23 °C/50% RH and at 60 °C/90% RH, including 8 h and 72 h folded holds.
- Profile measured 10 s after opening, by white-light interferometry.

**Failure modes.**
- Creep in the OCA and polyimide (PI) sets the crease. Glass does not creep at room temperature.
- Adhesive cohesion failure at heat and humidity.
- UTG fatigue, which worsens as the glass gets thicker.
- Hinge wear, which shifts flatness tolerances.

**Trade-offs.** All three designs cost thickness or yield. Extra layers enter the module processing term, which is about 50% of the roughly $250 panel. Budget about $20, and only if yield holds.

**Comparison.** The Apple/SDC (laser-drilled plate) and Oppo N6 (liquid-printed fill) approaches publish only relative cuts. Both shape the support under a creeping polymer. Neither publishes slope figures or post-hold data.

**Cheapest experiment.** Profile a retail Fold 7 and an N6 with interferometry before and after a 72 h fold at 60 °C. Cost is about $5k. This tells us whether the residual is mostly recoverable creep, which recovers within minutes, or permanent set. That answer decides between the three ideas.

**Established vs speculative.**
- Established: glass elasticity, and the fact that polymer creep recovers.
- Speculative: the visibility thresholds, and every crease depth, since none has been rigorously measured.

=== IDEAS ===
IDEA 1
NAME: Glass-dominated elastic fold zone
MECHANISM: Two 30 µm UTG sheets enclose the OLED, joined by ≤10 µm low-modulus OCA across the fold zone only. More than 99% of the bending moment is then carried by glass that cannot creep, and the residual curvature scales with the polymer's moment share. The closest attempt is SDC Advanced Crease-less with a possible second UTG, which still leaves a thick PI/OCA stack bearing load. This design removes that load path. The deciding quantity is the polymer moment fraction times its unrecovered creep strain, which must give ≤0.5 mrad slope.
VALUE: An inward book-fold phone whose open-state flatness is set by elastic glass instead of creeping polymer.

IDEA 2
NAME: Hinge reverse-bend creep cancellation
MECHANISM: On opening, the hinge briefly over-extends 2–4° past flat, then settles at 180°. The reverse bend applies a counter-moment that, by Boltzmann superposition, cancels the stored viscoelastic creep from the folded hold. The dwell time adapts to the logged closed time and temperature. The closest attempt is neutral-plane balancing, which suits only one state, and this approach adds the missing second state. The deciding quantity is the reverse strain-time needed against a 72 h folded hold at 60 °C.
VALUE: Turns accumulated polymer creep from a permanent dent into a cancelled transient without adding layers.

IDEA 3
NAME: Tensioned membrane open state
MECHANISM: In the flat state, hinge cams pull the wing plates apart, putting the fold-zone stack in in-plane tension. The tension straightens residual curvature: deflection falls as tension rises relative to bending stiffness. The closest attempt is Oppo's tolerance-mapped hinge, which fills gaps but applies no restoring force. The deciding quantity is the tension needed for ≤1 µm depth against OCA shear-creep and UTG edge stress limits.
VALUE: Actively flattens whatever crease the materials leave, while reusing hinge parts that phones already have.