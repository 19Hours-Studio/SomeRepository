Answer A is just a status note pointing to a different answer. It contains no approaches, estimates, coverage, quality analysis or prior-art comparison, so the asker gets nothing usable from it.

Answer B is a full response. It gives concrete approaches:
- line-run references;
- batched clearing tuned with an EOQ rule;
- capped suffix speculative decoding;
- errata-based cache-stable layout;
- KV splicing;
- a content-addressed segment cache with a shadow gate;
- tiered retention.

For each approach it states which cases it covers, where it runs, its cost, its effect on quality and how to test it, and how it relates to prior art. It also lists clearly what cannot reach ~100%.

Some of B's specifics cannot be verified here, such as its citations and its replay numbers. Even so, it is far more useful than A.

WINNER: B
MARGIN: far
WHY: A is a stray progress message with no substantive content on prompt caching. B gives multiple concrete approaches that address every required element: cases covered, quantitative cost and hit-rate estimates, deployment location, quality tests, prior art, and honest limits. Someone acting on A gets nothing, while B gives them a usable plan.