**Goals (from the center):**
- (a) Find which of the system's own beliefs are wrong.
- (b) Keep learning from untrusted real-world streams without drifting.
- (c) Reason over many steps without errors compounding into confident self-confirmation.

**Paradigm negated:** mainstream approaches have one trained model produce outputs and improve them using a scalar score from some judge (labels, a reward model or itself). That is forbidden here as a mechanism.

**Periphery sources and the crux:** Each idea gets its correctness signal from statistical identities over redundant, independently produced observations. A self-judge is not used.
- (a) Geodetic network adjustment. Surveyors catch measurement blunders with no ground truth by using loop misclosure and Baarda data-snooping.
- (b) Numerical weather data assimilation. Desroziers innovation diagnostics estimate both model error and observation error from innovation statistics alone.
- (c) Turbo decoding. Decoders exchange only *extrinsic* information, which prevents self-reinforcement.

**Honesty check:**
- (a) Closest work: self-consistency decoding, SLAM loop closure and truth maintenance. What is new: quantitative misclosure, statistically tested blunder localization, and redundancy numbers that mark claims as uncheckable.
- (b) Closest work: Kalman online learning and Dawid–Skene source reliability. What is new: joint error covariances for the model and for each source, taken from innovation identities with no labels.
- (c) Closest work: multi-agent debate and belief propagation. What is new: prior subtraction, a decorrelating interleaver, and EXIT-chart convergence prediction.

=== IDEAS ===
IDEA 1
NAME: Survey-Adjusted Belief Network
MECHANISM: Every quantitative or relational claim the system holds is treated as a surveyed observation with a variance, and it is linked to independent observations (retrieved sources, tool outputs, sensor readings) through closed constraint loops. Weighted least-squares adjustment spreads each loop's misclosure across its claims. Baarda's normalized-residual test then names the specific claim that is most likely a blunder, which gets revised or discarded. For each claim the system stores a redundancy number that says how far other observations control it. Claims with near-zero redundancy are marked as structurally unverifiable rather than as trusted.
VALUE: The system can locate and fix its own errors, and knows which beliefs nothing can currently check, without an oracle or a self-grading model.

IDEA 2
NAME: Innovation-Diagnosed Continual Assimilation
MECHANISM: The model's beliefs act as a background state. Each new datum from a document, user, instrument or tool is an observation, and the system computes the innovation (observation minus prediction) and the analysis residual. Desroziers consistency identities over these statistics give separate estimates of the model's error covariance and of each source's error covariance, so no labels are needed. These estimates set the gain that decides how much each observation changes the stored beliefs and parameters. A source whose estimated error grows is down-weighted automatically, and so is a model region whose estimated error grows.
VALUE: The system learns continuously from noisy, adversarial real-world streams while measuring its own reliability and each source's reliability from the data alone.

IDEA 3
NAME: Extrinsic-Exchange Turbo Reasoning
MECHANISM: A problem is decomposed in two deliberately different orders (an interleaver). This produces two reasoning chains whose intermediate claims are scored as log-likelihood ratios against parity-like constraints (units, conservation laws, cited values). On each pass, a chain subtracts the belief it received from the other chain before sending its own update. Only extrinsic evidence crosses over, so neither chain counts its own conclusions twice. Mutual-information transfer (EXIT) curves are stored per problem type. They predict whether the exchange will converge, and when it will not, the answer is withheld and the system goes looking for more constraints.
VALUE: Long reasoning chains can correct each other without an echo chamber, and the system can tell beforehand when internal checking cannot reach a reliable answer.