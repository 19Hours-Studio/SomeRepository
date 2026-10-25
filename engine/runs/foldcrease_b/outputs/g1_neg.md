# Crease-free foldable: three architectures (concept-level, unvalidated)

**The usual paradigm.** The first eight answers most experts would give are thicker or more flexible UTG, a recoverable OCA, a perforated plate, neutral-plane tuning, a teardrop radius, a fill under the hinge, self-healing layers and better glass. All of them share one idea: let the stack bend, then hope it springs back flat. The three answers below take a different approach. They either remove the stack's reason to set, or they force flatness using external stiffness or tension.

**"Invisible" targets** (my thresholds, not measured):
- **Depth:** residual depth ≤2 µm over a 10 mm window, by white-light interferometry.
- **Slope:** peak slope ≤0.5 mrad (0.03°).
- **Reflection:** a reflected line grid at 0°, 30° and 60° distorts by ≤1 arcmin.
- **Touch:** a blind fingertip two-choice test stays at chance (<55%, n≥20).

**2000-cycle test protocol:**
- Profile every 250 cycles.
- Run each arm at 25 °C/50% RH, at 60 °C/90% RH with 72 h held folded, and with opening at −20 °C.
- The worst arm decides the result.

**Cost.** No answer claims "several times cheaper". The phone-level cost ceiling is about 2.3×. Each answer adds roughly $5–20 at module level, so yield impact dominates the cost.

**Established vs. speculative.**
- Established: polymer creep sets the crease (3M data), and glass resists bending but does not creep.
- Speculative: every magnitude below.

**Cheapest experiment.** Build 20 UTG/OCA/PI coupons. Cycle them 2000× on a 1.5 mm mandrel, with and without each answer's mechanism, and profile them. Estimated cost is about $5k in fixtures and interferometer time.

**Comparison with reported approaches.**
- Apple/Samsung (perforated plate) and Oppo (3D-printed fill) both reduce the crease statically, by about 4–5×. Neither has an absolute µm figure or a persistence result.
- The answers below either act after creep has occurred (B, C) or remove the drive toward creep (A).

**Trade-offs and failure modes:**
- **Mass and thickness:** about 0.2–0.4 mm and 3–8 g added.
- **Hinge:** load on the hinge rises, which affects wear and yield.
- **Optics:** no extra optical layers are added above the OLED, so brightness is unchanged.
- **Main failure modes:** OCA delamination under shear, static fatigue of the glass, and actuator drift.

=== IDEAS ===
IDEA 1
NAME: Fold-native polymer lamination
MECHANISM: The OCA and polyimide layers are laminated while the panel is held at its fold radius. Their stress-free shape is therefore the folded state, so the long hours folded in a pocket cause no creep. When the phone is open, the polymers try to re-curl, but the stress-free flat glass and the plate are much stiffer and hold the panel flat. The closest earlier attempt is neutral-plane balancing, which is tuned for one state and still creeps; here the creep-prone layers spend their long holds at zero stress. The deciding quantity is the polymer's relaxing moment compared with the bending stiffness of the glass plus plate, which must be at least 50× larger to keep depth under 2 µm.
VALUE: It removes the cause of the crease instead of repairing its effect, at near-zero material cost.

IDEA 2
NAME: Drumhead tension hinge
MECHANISM: A cam in the hinge slides both panel ends outward on opening and applies about 600 N/m of in-plane tension. This pulls any set curvature down onto a flat lapped support plate. With UTG bending stiffness of about 1.6×10⁻⁴ N·m, flattening decays over √(D/T) ≈ 0.5 mm, while the glass strain stays at about 0.03%. The closest earlier attempt is Oppo's tolerance fill, which is static and cannot follow creep; tension adapts automatically as the set grows. The deciding quantity is roughly 90 N of sustained hinge force without causing OCA shear delamination.
VALUE: Flatness is restored on every opening, whatever creep has accumulated.

IDEA 3
NAME: Closed-loop active fold support
MECHANISM: A row of about 30 piezo or wedge actuators under the fold zone has about 60 µm of stroke and 1 µm resolution. Strain gauges printed on the polyimide estimate the crease profile at each opening, and a stored map drives the actuators to cancel it. The map is updated as creep grows. The closest earlier attempt is Oppo's laser-mapped liquid printing, a one-time static fill that cannot track drift. The deciding quantity is whether the panel's bending stiffness lets discrete supports cancel slope below 0.5 mrad between actuators.
VALUE: Flatness is held under 2 µm across temperature, humidity and wear by measuring and correcting it, not by hoping the materials recover.