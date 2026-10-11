**Offspring 1 (Pair 1: Footprint Decay Clock × Phylodynamic Spark Burst Inference)**
Task: working out when hidden water damage began in a building. This decides insurance claims, tenant disputes and health liability. AI has been absent because nobody has mould growth with known start times, and growth depends on the humidity and temperature since the leak. Lab inspectors only say "weeks to months."
Crossover: Parent B's genealogy likelihood replaces Parent A's learned elapsed-hour scorer. Parent A's weather integral then sets the parameters of the branching process, so neither part works alone.
- A 3M-parameter CNN traces hyphal networks in clip-on-macro phone photos and turns each colony into a rooted branching tree with segment lengths.
- A multitype Galton–Watson process with timed delays scores each tree. Its branching rate and delay distribution are a small learned function of the humidity-temperature dose summed from each candidate start hour. The dose comes from a hygrometer log or the smart thermostat's history.
- The posterior over the start hour combines every colony's tree likelihood. It is like dating the common ancestor of a set of colonies.
- Training uses drywall, timber and OSB coupons inoculated at logged times in humidity cabinets and photographed every 6 h. The loss is the likelihood of the true start time, plus an ordering penalty that forces later photos to be judged older.

**Offspring 2 (Pair 2: Difference-Map Field Drain Recovery × Seasonal Riverbed Reveal)**
Task: mapping weak lake and river ice over springs, warm inflows and currents for ice fishers, snowmobilers and northern communities. Many people drown this way every winter. AI has been absent because no one knows what flows under the ice.
Crossover: Parent A's physics difference map and R-free edit loop now runs on a hidden inflow graph rather than a drain graph. Parent B's seasonal reveal gives the free ground truth, and the inferred graph also changes what the reveal is used to supervise.
- At freeze-up and break-up, a fixed shore phone camera records where the ice opens first. Aligned by landmarks, those spots are the true weak zones for the winter surface.
- In winter, a dawn drone thermal and RGB pass over the snow-covered ice gives the input.
- A non-differentiable heat-flux solve on a 512² grid predicts the snow-surface temperature and slush pattern from the current inflow graph (point springs and current channels). Observed minus predicted gives the difference map.
- A 15M-parameter U-Net, trained on the reveal pairs, proposes edits wherever residual ridges or troughs pass ±3σ. An edit is kept only if the error on 5% of held-out pixels and on the reveal mask improves.
- The output is a hazard map of the graph plus calibrated thin-ice probabilities.

**Honesty check**
- Offspring 1: the closest work is the VTT/Hukka–Viitanen mould-growth index model, plus CNN mould detectors and Rajs et al.'s fingerprint-age work. VTT predicts growth forward from climate and never dates anything from images. The detectors only classify presence. It is not CHEMINV or FERMODE, because nothing is inverted in recipe space and no process is controlled.
- Offspring 2: the closest work is SmartICE (thickness sensors plus SAR), Sentinel-1 lake-ice classification and Allred's UAV drain mapping. None infers a hidden inflow graph through physics-validated edits, and none uses the break-up reveal as labels. It is not DIFFEM, because the solver is non-differentiable and edits are discrete.

=== IDEAS ===
IDEA 1
NAME: Mould Genealogy Leak Clock
MECHANISM: A 3M-parameter CNN traces hyphal networks in macro phone photos into rooted branching trees. A timed multitype Galton–Watson likelihood scores each tree, with its branching rate and delay distribution set by a small learned function of the humidity-temperature dose summed from each candidate start hour, so the posterior over when the leak began combines all colonies, like dating a common ancestor. It is trained on inoculated building-material coupons timed in humidity cabinets and photographed every 6 h, with a true-start likelihood loss and an ordering penalty that makes later photos older. The trees and dose tables take megabytes, likelihoods run on CPU in 32 GB, and the CNN trains on the RTX 3060 in about a day.
VALUE: It gives a calibrated "leak began 5–9 weeks ago" from phone photos and a humidity log, which no same-budget detector or forward mould model can do.

IDEA 2
NAME: Break-Up Validated Ice Hazards
MECHANISM: A non-differentiable heat-flux solve on a 512² grid predicts the snow-surface temperature and slush pattern on ice from a hidden inflow graph of springs and current channels, and a dawn drone thermal/RGB pass minus that prediction gives the difference map. A 15M-parameter U-Net, trained on free seasonal pairs (the winter surface matched to the spots where a fixed shore camera saw ice open first at break-up), proposes graph edits at residuals beyond ±3σ. Each edit is kept only if the error on 5% of held-out pixels and on the reveal mask improves. The U-Net, solver and batches fit easily in 12 GB, and one lake is processed in minutes.
VALUE: It turns one drone flight into a physics-checked map of thin ice with honest error bars, which no same-budget sensor network or pixel classifier can provide without labels.