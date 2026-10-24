**Core claim (physics, established):** creases come from polymer layers (PI, OCA, films) held past their viscoelastic recovery strain. The strain is roughly ε ≈ t/2R, where t is the bonded thickness and R the bend radius. Glass survives fine. Zero crease requires every polymer in the bend zone to stay elastic, or the residual to be flattened.

**"Invisible" targets** (my thresholds, not sourced):
- Residual depth ≤2 µm, measured by white-light interferometry 10 s after opening.
- Maximum slope ≤0.5 mrad (0.03°).
- No line seen by 20 observers viewing a reflected straight-edge grid at 0–70° off-axis.
- Finger-slide detection at chance in a 2AFC test. Humans can feel ~10 nm wrinkles (Skedung 2013), so touch is the hardest target.

**2000-cycle test:**
- 2000 cycles at 25 °C.
- 2000 cycles at 45 °C / 90% RH.
- 72 h held folded at 60 °C.
- Opening at −20 °C.
- Profilometry at cycles 0, 100, 500, 2000.
- Main breakers: hot folded holds and cold opening, where OCA recovery slows sharply.

**Failure modes:** PI plastic set, OCA creep and delamination, UTG fatigue (low risk at only 2000 cycles), hinge wear shifting the support surface.

**Cost:** each idea adds roughly $10–30 per module, or about 1–2% of retail. Yield risk matters more than material cost. None of these ideas claims a cheaper phone; the ledger caps that at about 2.3x anyway.

**Comparison with shipped approaches:** Samsung/Apple's perforated plate (reported about 25% of Fold 7 depth, unverified) and Oppo's pre-use mapping (variance cut from 0.2 to 0.05 mm, still visible in some light) both reduce the crease. Neither removes polymer creep.

**Cheapest experiment:** fold strips of a production stack on mandrels at R = 1–6 mm. Hold them 12 h at 45 °C, then profile residual depth against computed ε. This costs a few $k and sets the zero-residual strain threshold that all three ideas rely on.

**Established vs speculative:** the ε ≈ t/2R relation and polymer creep are established. All thresholds, gel/fluid behaviour and saturation behaviour are untested.

=== IDEAS ===
IDEA 1
NAME: Liquid-coupled slip stack
MECHANISM: In a 10 mm bend strip, the bonded OCA is replaced by a sealed, index-matched fluid film. This lets the UTG, the touch/polarizer layer and the OLED-on-PI each bend about their own neutral plane, so ε ≈ 30 µm/(2×2 mm) ≈ 0.75% instead of about 4% for a bonded stack. Outside the strip, the layers stay bonded with normal OCA. The closest attempt, thin or high-recovery OCA, failed because it stays bonded and so stays strained; a fluid has no shape memory. The deciding quantity is whether the perimeter seal holds the fluid gap uniform to within ±1 µm through 2000 cycles at 45 °C.
VALUE: Removes the creeping layer itself rather than reducing its creep.

IDEA 2
NAME: Tensioned drumhead hinge
MECHANISM: In the last few degrees of opening, the hinge cams pull the panel edges outward, applying a measured in-plane membrane tension that elastically pulls any residual dent flat. Load cells in the hinge store the tension that gives zero slope and adapt it with temperature. The closest attempts, perforated plates and the Oppo-mapped hinge, only support the panel from below, and supports cannot remove the panel's own set. The deciding quantity is the tension needed to flatten a 20 µm, 3 mm-wide set compared with the OCA edge-shear creep limit.
VALUE: Flatness becomes an actively controlled state rather than a material hope.

IDEA 3
NAME: Post-shakedown counter-shaped support
MECHANISM: Each panel is first aged in the factory with about 300 hot folds until its crease depth saturates. Its residual profile is then laser-mapped at 0.3 µm, and a matching inverse shim is printed onto the support plate. The closest attempt, Oppo's liquid printing, maps the surface before use, while the creep has not happened yet. Here the mapping happens after the creep has stopped. The deciding quantity is whether depth drift between cycle 300 and cycle 2300 stays ≤2 µm under 60 °C folded holds.
VALUE: Cancels the stable part of the crease while reusing existing Oppo-style tooling.