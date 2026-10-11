**Pair 1. Shared move:** both parents get a correctness signal from a difference whose expected value is fixed by construction, not from an absolute answer. In Parent A it is zero loop misclosure. In Parent B it is the known effect of a spike. Neither parent ever asks "is this true?"; each asks "did the known structure come back?". The offspring keeps only that one move and applies it to the system's own belief store. Instead of computing redundancy in theory or building adapters for each input type, it measures how strongly the store pulls planted errors back.

Closest existing work: Baarda's reliability theory; denoising autoencoders and masked modelling; standard addition. It differs from all of these because the corruption is planted online into the live belief store, and the store's measured stiffness becomes the per-region warrant for revision. It is not a training objective, and it is not a closed-form redundancy number.

**Pair 2. Shared move:** a belief earns credit only by what it adds to predicting raw data that the system did not write. Parent A uses innovation statistics; Parent B uses student gain. Desroziers needs covariance machinery, and teachability needs a separate student. The offspring drops both. The "student" is the system itself with the belief removed, and the judge is the next real datum.

Closest existing work: influence functions and data attribution; Knowledge-Based Trust; teaching-based scoring. It differs because it is computed online for each stored belief rather than for each training example, against future raw observations, and it directly sets update gain.

=== IDEAS ===
IDEA 1
NAME: Restoring-Force Belief Sounding
MECHANISM: In the background, the system copies verified source values (numbers, relations, entities) into its belief store and corrupts them by graded known amounts. It then measures what fraction of each corruption its next inferences pull back toward what neighbouring beliefs imply. This restoring-force slope is stored for each region of the belief store. A slope near zero marks the region as uncheckable. A real belief that deviates from its neighbour-implied value by more than the measured slope allows is flagged as a likely blunder and revised. Regions whose slope drops trigger targeted relearning, and the slope is measured again afterwards.
VALUE: Without an oracle or self-grading, the system can tell which of its beliefs are actually held in check by other knowledge, and can find specific errors there using only errors it planted with known size.

IDEA 2
NAME: Leave-Out Forecast Credit
MECHANISM: For each stored belief, the system runs a cheap twin forward pass with that belief masked out. Whenever a new raw observation arrives (a document token, sensor value, tool output or user reply), it records the difference in prediction error between the full pass and the masked pass. This running per-belief credit is the only quality signal. It sets how strongly each belief is weighted and how much new data may overwrite it. Beliefs with persistently negative credit are retracted, and sources whose added beliefs earn negative credit are down-weighted.
VALUE: Every belief is graded continuously by the outside world's next data rather than by the model's own judgment, so learning can stay open-ended in domains with no labels.