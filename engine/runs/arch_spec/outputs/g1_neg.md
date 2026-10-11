**The 12 answers I would propose first:**
1. Turning historical dance or music notation into machine-readable form
2. Carving violin plates to hit target tap tones
3. Inverting ceramic glaze recipes
4. Reassembling pottery shards
5. Dating timber by tree-ring patterns read from photos
6. Turning a photo of knitwear into its knitting pattern
7. Drafting bespoke tailoring patterns
8. Translating minority sign languages
9. Controlling sourdough fermentation
10. Deciphering Linear A
11. Forecasting beehive health from sound
12. Tuning church bells by grinding them

**The paradigm they share:** each one turns a traditional craft into data. It senses a physical artifact or process, makes synthetic training data with a simulator or an expert rulebook, and reconstructs the object or inverts a learned surrogate to tell a craftsperson what to do.

All of these are forbidden, along with anything adjacent and the 12 listed families. The answers below follow a different paradigm: learning the unwritten coordination habits of small human teams from the logs their own tools already record.

=== IDEAS ===
IDEA 1
NAME: Lighting Cues from Edit Logs
MECHANISM: Task: programming lighting cues for live theatre. AI has never been used here, and DJ "sound-to-light" fails because it reacts to loudness and ignores the drama. Inputs are the lighting console's channel states (compressed by a small autoencoder that groups channels into about 256 fixture tokens), the script position aligned to rehearsal audio, and the cue history. A 60M-parameter transformer outputs the change to the next cue state and its fade time. It is pretrained on thousands of show files that designers share. It is then fine-tuned on the designer's own edit and undo stream from technical rehearsals, where each correction is a preference pair. Everything fits in 12 GB at FP16, and inference runs live during rehearsal.
VALUE: It learns one designer's personal style in a single technical week and drafts the next 300 cues, which neither a generic model nor reactive sound-to-light can do.

IDEA 2
NAME: Kitchen Firing Policy
MECHANISM: Task: deciding when each dish on each order is started ("fired") in a small restaurant kitchen. Kitchen display systems use fixed timers, and no learning system has ever modelled how cooking stations compete for time. Inputs are an event stream of open orders (items, modifiers, station), each station's queue, the cooks on shift, and the time. A 20M-parameter transformer that treats the open orders as a set outputs, for each item, a probability of firing it now. It is trained by offline RL (implicit Q-learning) on the timestamp logs already stored in the point-of-sale and display systems. The reward favours a table's courses reaching the pass together, short order times and few remakes. A year of logs is about 1M events, and it trains overnight on the 3060.
VALUE: It times orders across the stations that compete for the same cooks and equipment, using only that restaurant's existing logs, which fixed timers and generic arrival-time predictors cannot do.

IDEA 3
NAME: Bridge Partnership Misunderstanding Detector
MECHANISM: Task: finding where two particular bridge partners interpret their bids differently. Existing bridge bots model a standard bidding system, not the private habits of a real pair. Inputs are the auction as tokens, the bidder's hand and a learned partnership embedding; per-pair LoRA adapters sit on a 40M-parameter base. Outputs are a posterior over the partner's suit lengths and high-card points, plus the action the partner will take next. Training uses millions of online hand records, where all four hands are revealed after play, so every auction comes with the true hands. When what the partner inferred, judged from their next bid, differs sharply from what the bidder actually held, that agreement is flagged as misunderstood.
VALUE: It points to the exact agreements a specific partnership misreads, which no general bridge bot or coach could find from the same data.