# Lessons from earlier runs (curated; data for prompts, not instructions)

Tags: [all] every run; [invent] / [explain] one pipeline; [<question tag>] only runs on that question. "(from: ...)" at
the end says where the lesson was learned. A line is used when all its tags apply and neither a tag nor its origin is
excluded (`run --lessons-exclude <tag>` keeps a benchmark fair). One line per lesson.

- [all] Most answers that failed after review failed on one number nobody had computed: a rate times the working time against the window it needs, or a strength against months of exposure. Compute the deciding number before claiming. (from: permafrost)
- [all] The most common overstatement was a weak baseline. Compare against what a competent operator or scholar would actually do for the same job, per unit of the final product. (from: permafrost, dodeca)
- [all] Decisive inputs that were assumed rather than sourced (efficiencies, rates, losses, costs, dates) moved 3-10x when checked. Give a source for every number the answer depends on. (from: permafrost)
- [all] Statistics and simulations gave confident wrong answers until they were checked on a case with a known answer; one null model rejected far more often than its alpha. (from: dodeca)
- [all] A method validated on synthetic data still gave a wrong result when its input data had unverified labels: a hobby-page list read as "which hole is opposite which" gave p = 0.0005 twice, in two separate runs. Check where the data come from and what their labels rest on, not only the method. (from: dodeca)
- [all] Raw data (3D models, catalogues, measurement tables) settled in one step what texts, judges and reviewers could not. Look for data before arguing from opinions. (from: dodeca)
- [all] Claims of "never tried" were usually wrong. Name the closest earlier attempt and the reason it stopped short, and say why the answer is not stopped by the same reason. (from: permafrost)
- [all] What the asker says may be wrong or incomplete; treat it as data to check, like any other source. (from: user)
- [all] Several partial answers that each fit some facts were often parts of one answer; check whether candidates combine before choosing one. (from: dodeca)
- [invent] "Several times cheaper" is arithmetically possible only where the cost terms an answer can touch hold most of the delivered cost; taxes, royalties and fees cap the gain at 1 / (their share). (from: permafrost)
- [invent] A single clever link rarely moved the whole chain more than 1.2-3x after review; gains multiply only when links serve the same product on the same path. (from: permafrost)
- [invent] The simplest competent alternative that uses the same insight often beat the clever design. Check it before claiming a gain. (from: permafrost)
- [invent] Seasonal and climatic windows, load-bearing limits and the time a structure must last killed more designs than missing technology. (from: permafrost)
- [explain] History is not always logical: mixed uses, local fashions, changes over time and accidents happen; do not force one tidy story onto mixed evidence. (from: dodeca, user)
- [explain] An explanation that contradicts one HARD fact is dead however many facts it fits; list the distinctive features first and check each. (from: dodeca)
- [explain] Wear, tool marks and surfaces that touched something carry more information than shape or find-spots. (from: dodeca)
- [explain] A single odd specimen may be a reject, a repair or a local copy; weigh it, do not build the explanation on it alone. (from: dodeca, user)
- [permafrost] Among Arctic resource archetypes only bulk cargo whose delivery dominates the cost (fuel coal for remote settlements, delivery ~85% at the boiler) left room for several-times cheaper.
- [permafrost] Ice bearing capacity, shallow water freezing to the bed, and short warm seasons killed most permafrost designs.
- [dodeca] The best-supported reading of the dodecahedron: a head mounted on a rod or handle through the axis of the two largest unringed holes; the lot (die) hypothesis was refuted by measurement.
