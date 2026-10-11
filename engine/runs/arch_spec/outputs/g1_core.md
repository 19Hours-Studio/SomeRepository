TASK: Predicting where undiscovered cave passages are, for volunteer cave explorers. AI has never been applied well here. The useful data is tiny and scattered: club survey files (Survex/Therion), cheap loggers and dig notes. The reward signal is slow, because a lead can take decades to "go". The field has also been left to geology rules of thumb and personal intuition. The model takes in survey centrelines with passage dimensions, survey dates, entrance airflow and pressure loggers, a surface elevation model and the dip of the rock layers. It outputs a probability map of unseen passage and a ranked list of leads.

1. GOALS: (a) estimate how much hidden volume lies behind each entrance or draught; (b) work out which known passage ends connect, and how far apart they are; (c) rank which leads to push next, given a limited number of trips.

2. PARADIGM NEGATION: Current approaches extrapolate forward from known geometry or from how caves form geologically (speleogenesis models, GIS overlays, interpolation). That is forbidden as a mechanism here.

3. Families checked: these ideas avoid RULESYN, SURRINV, DIFFEM, CHEMINV, FRACSEQ, SERMATCH, STITCHPS, GARMSIM, SIGNLR, FERMODE, DECIPH and HIVEAUD.

4. PERIPHERY SOURCES: (a) lung testing by the forced oscillation technique; (b) gap-filling between sequenced fragments in genome assembly (scaffolding); (c) aftershock forecasting with the ETAS model from seismology.

5. HONESTY CHECK:
- Idea 1: The closest work is single-volume barometric "breathing cave" estimates (Conn 1966; Pflitsch). These fit one resonator, not a map of several compartments conditioned on the known survey, so the idea is kept.
- Idea 2: The closest work is genome scaffolders such as SSPACE and OPERA, plus manual guessing of where caves connect. The domain, the evidence types and the learned edge prior are all new, so it is kept.
- Idea 3: The closest work is ETAS itself and Hawkes-process crime forecasting. Nothing like it exists for exploration history, so it is kept.

=== IDEAS ===
IDEA 1
NAME: Cave Impedance Plethysmograph
MECHANISM: Natural changes in air pressure (barometric tides and weather fronts) serve as the forcing signal, and a cheap ultrasonic anemometer at each entrance records the airflow response. Together they give an impedance spectrum Z(f) per entrance, the same way the forced oscillation technique tests lungs. A small transformer maps the spectrum, plus the volume and resistance already known from the survey, to a posterior over a multi-compartment model (an Otis-style network of resistances and compliances): how many hidden compartments there are, how big they are, and how strongly they are connected. It is trained on millions of synthetic networks made by deleting passages from real surveys, then fine-tuned on caves whose volume was later measured. The model is under 20M parameters and trains in hours on the 3060.
VALUE: It gives a measured, uncertainty-bounded estimate of volume nobody has entered yet from a $40 sensor, where the same budget otherwise buys only geologic guesswork.

IDEA 2
NAME: Passage Scaffolding From Mate-Evidence
MECHANISM: Surveyed passage segments are treated like contigs (assembled genome fragments). "Mate-pair" links between separate passage ends come from dye traces, cave radio fixes, cross-correlated temperature and airflow loggers (the lag gives the travel distance), and shared sediments. A genome-scaffolder engine keeps a graph of passage ends with a distribution of gap lengths on each edge. It solves ordering and orientation with an exact integer program, held in RAM. A graph network, trained on the dated history of club surveys (hide connections found later, then predict them), scores how plausible each edge is from rock-layer orientation and fracture alignment taken from the elevation model. The output is the most likely set of connections with gap lengths, which turns into dig targets.
VALUE: It combines different kinds of weak evidence into connection hypotheses that can be checked, which no geometric interpolation can do.

IDEA 3
NAME: ETAS Discovery Forecaster
MECHANISM: Every dated survey leg is treated as an event in a self-exciting point process, as in aftershock forecasting. A background intensity field comes from a small CNN over the elevation model and geology layers, and each discovery raises the chance of more discoveries nearby, fading over time and distance (Omori-like kernels). Parameters are fitted by maximum likelihood on decades of version-controlled club survey history. The output is the expected new passage per trip for each open lead, which feeds a simple scheduler for expedition planning. The whole model fits in under 1 GB and fits in minutes.
VALUE: It turns the exploration record itself into a calibrated forecast of where effort will pay off, which caver intuition and geology-only maps cannot provide.