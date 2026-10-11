TASK: Identifying unknown scrap steel (carbon class, main alloying elements) from a slow-motion phone video of grinder sparks, then recommending a heat treatment. Smiths and hobby machinists depend on spark testing, but it is a fading craft that people judge by eye from printed charts. There is no labelled corpus. Spectrometers cost thousands. Earlier AI attempts were small image classifiers that failed when the grinder, pressure or lighting changed.

1. GOALS
- G1: Turn noisy video into individual spark trajectories and burst events.
- G2: Infer composition from features that do not change with grinding pressure, wheel or speed.
- G3: Calibrate from a handful of known bars per session, with honest uncertainty.

2. PARADIGM NEGATED
Mainstream approaches train a supervised end-to-end network that maps pixels to a label using a large labelled dataset. That is forbidden here as the mechanism.

3. Known families: none of the three ideas uses a renderer or simulator to make data, an inverse surrogate, recipe search or library cross-correlation.

4. PERIPHERY
- G1 comes from high-energy physics track and vertex reconstruction (Kalman-filter track following plus secondary-vertex finding).
- G2 comes from phylodynamics: estimating a branching process's offspring distribution from observed genealogies (birth-death models as in BEAST).
- G3 comes from population pharmacokinetics: nonlinear mixed-effects models (NONMEM style), with fixed effects shared across subjects and random effects per subject.

5. HONESTY CHECK
- Closest prior work is CNN spark-image classifiers (small academic studies) and handbook spark charts.
- Idea 1 is not a pixel classifier. It reconstructs physical events, and its only learned part is trained self-supervised.
- Idea 2 resembles BEAST only in its maths. No one has inferred metallurgy from spark genealogies.
- Idea 3 uses NONMEM's structure but takes the place of chart lookup. None of the three is essentially existing work.

=== IDEAS ===
IDEA 1
NAME: Spark Kalman Vertex Tracker
MECHANISM: A tiny convolutional hit detector (~2M parameters) runs on each frame of 240 fps video and outputs streak-segment "hits" with position, direction and two-colour brightness ratio. A bank of Kalman filters follows each spark with a ballistic state (position, velocity, drag coefficient, temperature) and a predict/correct update, as charged-particle tracking does. Vertex finding detects burst points where one track ends and several begin. The detector is trained self-supervised: it is rewarded for hits that Kalman tracks predict with high likelihood, and frames are alternated with track refits (EM). No labels are needed. Everything fits easily in 12 GB and runs at video rate on a 3060.
VALUE: It turns an unlabelled phone clip into a physical event record: drag-derived particle size, colour temperature and burst vertices. Pixel classifiers trained on the same budget cannot produce these quantities, and they break when the camera or lighting changes.

IDEA 2
NAME: Phylodynamic Spark Burst Inference
MECHANISM: The tracked bursts from Idea 1 form genealogies: carrier line, first fork, second-generation forks. These are scored under a multitype Galton–Watson branching process with timed delays. The process's offspring mean, generation depth and delay distribution are estimated by exact tree likelihood, as phylodynamics estimates R from pathogen trees. Carbon drives CO-explosion branching. Elements such as Mn, Cr, W and Mo shift the delay distribution, the colour type and terminal shapes (W gives dull red; Mo gives detached "arrowhead" tips). Pressure changes how many trees appear, not the statistics within each tree, so the estimates do not depend on it. Inference is CPU-bound over a few thousand trees and runs in seconds in 32 GB RAM.
VALUE: Its composition estimates come from per-tree statistics that stay the same across grinders, wheels and operators, which no same-budget image model can match.

IDEA 3
NAME: Mixed-Effects Session Calibration
MECHANISM: Following population-pharmacokinetics practice, the branching and track parameters are modelled as composition fixed effects (shared across every user) plus random effects for each session (wheel grit, RPM, camera white balance), with fixed and random effects fitted jointly by Laplace approximation. In each session the user grinds one or two reference bars of known grade, which pin down that session's random effects. Each unknown bar then gets a posterior over a grade list, with credible intervals. Fixed effects are refined as uploaded sessions accumulate, and each new session needs only seconds of CPU on the PC. The posterior feeds a small lookup table of heat treatments (hardening temperature, quench medium, temper) that takes the uncertainty into account.
VALUE: It gives calibrated "this is probably 1080 versus O1, here is how sure" answers, and recommends the right quench for unknown scrap, from two reference bars per session instead of thousands of labelled samples.