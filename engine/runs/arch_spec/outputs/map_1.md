Three tasks where AI has barely been tried. Each has a small physics or rule model at its core, so it can be trained on one RTX 3060.

**1. Transcribing historical shorthand archives.** Millions of pages of Gabelsberger, Pitman and Gregg diaries, court records and parliamentary notes have never been transcribed. Handwriting recognition fails on them because meaning sits in stroke thickness, slant and position against the ruled line. There are also almost no paired transcriptions.

**2. Reviving dances from Labanotation scores.** Archives hold thousands of Labanotation scores that only a few certified readers can interpret. Motion-generation models ignore the notation because there are no paired score-and-motion datasets.

**3. Predicting how a specific wooden board will warp.** Woodworkers guess cup, twist and seasonal movement of an individual board from its grain. No model reads one plank. Existing wood-science AI grades lumber in sawmills with industrial scanners.

=== IDEAS ===
IDEA 1
NAME: Rule-Rendered Shorthand Decoder
MECHANISM: Task: historical shorthand archives, which AI has avoided because meaning is carried by stroke weight, slant and line position, and there is almost no labeled data. A procedural renderer encodes each shorthand system's rulebook and turns modern text into synthetic pages with jittered, pen-pressure strokes. These synthetic pages train a 25M-parameter stroke-vectorizing CNN encoder. That encoder feeds a differentiable finite-state transducer, built from the same rulebook, which outputs a phonetic lattice. A 100M-parameter language model of the target era rescores the lattice. The model then self-trains on unlabeled scans by keeping only high-confidence lattice paths. All models are small and the FST is sparse, so training fits in 12 GB of VRAM and synthetic data costs nothing to generate.
VALUE: It can read a writing system that has no training corpus, because the shorthand rules themselves supply the labels.

IDEA 2
NAME: Notation-to-Physics Choreography Engine
MECHANISM: Task: Labanotation dance scores, which motion AI has ignored because no paired score-and-motion data exists. A rule-based notator converts public motion-capture data (for example AMASS) into Labanotation symbol columns, which creates millions of synthetic pairs. A symbol-graph transformer (about 60M parameters) reads each column's symbols, durations and body-part staff. It outputs target poses and timing for a physics-simulated skeleton, run as a GPU rigid-body simulation at 24 joints. Training combines pose-reconstruction loss, a loss for re-notating the generated motion and matching the score, and balance and torque penalties. Then the model is fine-tuned on a few dozen real scores that have archival film.
VALUE: Archival scores become physically plausible performances that a dancer can watch and learn from.

IDEA 3
NAME: Single-Board Warp Forecaster
MECHANISM: Task: forecasting how one specific plank will move. AI has been absent because wood science works at species level and grading AI needs industrial scanners. Phone photos of both end-grain faces and two long faces feed a 30M-parameter U-Net. It infers a 3D field of growth-ring orientation, density and sapwood/heartwood. That field drives a differentiable finite-element model with about 20k elements, using orthotropic shrinkage, which predicts cup, bow and twist under any humidity schedule. The network pretrains on procedurally grown synthetic logs sawn virtually. It then self-supervises from users photographing the same board at two humidity levels: the measured deformation becomes the loss, backpropagated through the finite-element model. The finite-element model runs in milliseconds on the GPU, and the photo-to-field network is small.
VALUE: Woodworkers can choose and orient individual boards before cutting, which no lumber-grading system or species table can do.