=== IDEAS ===
IDEA 1
NAME: Legality-split hull-day swing
MECHANISM: The anchor is unchanged: ice-class hulls stay on the short ice leg wherever a lawful onward hull exists, and train output is set by hull-days. The design now splits cargo by legal status. From 1 Jan 2027 the EU ban removes Zeebrugge and about 15 Mt/y of EU sales. Yamal LNG (not on the US SDN list) would then run its 15 existing Arc7s as a winter shuttle from Sabetta to a Kildin ship-to-ship (STS) transfer point near Murmansk, not the Saam FSU, whose owner is on the SDN list. Clean non-EU conventional hulls take the cargo on to Asia. In summer the fleet splits into 40 direct NSR-east cargoes plus 64 shuttle cargoes. Winter needs only 9.7–11.4 of the 15 hulls, so all 19.7 Mt/y is delivered, against 7.4 Mt/y if the Arc7s carry every cargo to Asia themselves. Arctic LNG 2 cargo has no lawful onward hull, so it moves only on Russian-built Zvezda Arc7s delivering straight to the Chinese buyer (0.49 Mt per hull per year). Train 1 runs at the rate those hulls allow, a 30% duty factor with 4 hulls, and Trains 2–3 become a spares pool. Train 3 is not commissioned.
VALUE: Yamal LNG's full cost falls from about $657/t to about $387/t delivered (ratio 0.59) against realised prices of $442–494/t. Arctic LNG 2 earns about $110–160/t in cash on each delivered tonne, but its full cost (about $1,216/t with 4 hulls) stays far above price until about 33 Zvezda hulls exist.

IDEA 2
NAME: Size Sever to hulls
MECHANISM: The anchor is unchanged: each month Bukhta Sever receives only what the Russian-built Arc hulls can lift, about 1.54 Mt/y per 69 kt hull on the 15.5-day Murmansk cycle (1.2 Mt/y if winter stretches the cycle to 20 days). The allocation is reversed. Vankor-cluster oil (about 11.6–12.3 Mt in 2026–27) stays on the existing Vankor–Purpe line. That line is rated 25 Mt/y and has 12.7–13.4 Mt/y spare. The oil goes to the export outlet it already sells to, not to domestic refineries, which are already crude-long. South is the cheaper margin: about $57/t to an Asian buyer via Transneft and Kozmino, against about $86/t north via Sever, Murmansk and Suez. The north carries only Payakha oil, and Payakha drilling is scheduled to Zvezda Arc hull deliveries, so no well is drilled whose oil cannot be lifted. Because of that, no surplus ever has to go south and the Payakha–Vankor segment never needs reverse flow.
VALUE: Delivered cost per tonne falls by about $29/t on every Vankor tonne kept south, and holding back 15–25 Mt/y of Payakha capacity by 2–3 years saves $2.4–5.8bn in present value. That is about $80–190 per tonne of the capacity deferred, against the published plan of 30 Mt/y in H2 2027, which needs about 19 hulls that do not exist.

=== NOTES ===
**How I read the constraints.** "Russian-built only" is applied to any hull or equipment the plan adds. Existing hulls, such as Yamal's 15 Korean-built Arc7s, count as capacity already built. "Legal buyer" means a buyer whose own law permits the purchase, with declared cargo documents. It excludes shadow carriers, disguised STS and SDN-owned FSUs, so Arctic LNG 2's current Saam and shadow-carrier chain (Kpler forecasts 5.7 Mt for 2026) is excluded as a baseline.

The models are `idea1_lng.py` and `idea2_oil.py`. Round-by-round notes are in `LOG.md` and the consistency tables are in `NOTES.md`, all in the repair folder. Several inputs are my assumptions, not sourced numbers: the $400M Zvezda Arc7 price, charter rates, opex, a $10/MMBtu Asian price in 2027 and the 12% real capital charge. The calculation is set up so these can be swapped.

**Idea 1.** Anchor kept: yes. The design moves from Arctic LNG 2 to Yamal LNG after 2027, because only there does a lawful onward hull exist.
- **Decisive numbers:**
  - Cycles: winter shuttle 14–16.4 days (FACTS 359 and 364); NSR leg 19–21 days and Suez leg 35 days (FACT 308).
  - Per hull: shuttling gives 2.3–2.5 Mt/y, against 0.49 Mt/y when the Arc7 sails all the way to the buyer (4.5–4.9 times more).
  - Yamal winter logistics: $148–153/t for shuttle + STS + onward hull, against $156/t for the Arc7 sailing direct via Suez. The gain comes from volume, not the freight rate.
- **Baselines:**
  - Cheapest, if all winter output had to be carried direct: idle the trains in winter. Summer-only output of 8.1 Mt carries $425/t of plant capital.
  - Arc7 direct to Asia only: 7.4 Mt/y at $657/t full cost.
  - Repaired design: 19.7 Mt/y at $387/t.
  - Arctic LNG 2 on Zvezda direct delivery: marginal $200/t against realised $312–364/t; full $1,216/t with 4 hulls and $394/t with 21. Breakeven needs about 33 hulls.
- **Consistency:**
  - Summer NSR hull-days are fully used (2,250 of 2,250).
  - Winter leaves 3.6–5.3 spare Arc7s.
  - STS demand is about 0.7 transfers a day, which needs at least 2 STS stations.
  - Utrenneye tanks fill in about 5.7 days, so Train 1 has to cycle between full rate and turndown.
  - The ice-free berth window of about 90 days is used only as a bonus.
- **Years to added cargo:** 0–1. Kildin STS was already done in November 2020.
- **Hazards:**
  - Repeated train stops and restarts at −40 °C.
  - Winter STS in Barents weather.
  - Ice damage to Arc7 hulls, as possibly happened to Kosygin.
  - The US sanctions act signed in September 2026 (reported as the Graham Act), whose review of Novatek, the 60% Yamal LNG shareholder, is pending.
- **Deciding unknowns:**
  - Whether Yamal LNG stays off the SDN list.
  - Whether about 34 non-EU, non-SDN conventional hull-equivalents will lift at Kildin.
- **Cheapest experiment:** offer about 10 FOB-Kildin cargoes for Q1 2027 to Asian buyers and count bids from clean hulls. Fewer than 3 kills the idea.
- **Closest existing work:** the 2020 Kildin STS (Nikolay Yevgenov to Yamal Spirit), Novatek's Saam shuttle, and the Zeebrugge contract. What this adds is the routing rule by legal status, and running Arctic LNG 2 trains with a duty factor set by hull count, using T2/T3 as spares.
- **Verdict:** WORKS for Yamal LNG after 2027, if the deciding unknowns go its way. NICHE for Arctic LNG 2, where it cuts losses but cannot make full cost.

**Idea 2.** Anchor kept: yes.
- **Decisive numbers:**
  - Purpe line rated 25 Mt/y (FACT 361); Vankor output 14.8 Mt in 2023, declining about 6% a year by my assumption.
  - Valentin Pikul is 69,000 dwt (gCaptain). The cycle is 15.5 days (Carnegie, FACT 146).
  - The 2026 ESPO tariff is 3,896.5 RUB/t. This may be a through tariff; I have not confirmed the entry point.
  - 30 Mt/y would need 19 hulls.
  - Carnegie expects no meaningful Payakha output before 2028.
- **Baselines:**
  - Rosneft's plan (push 30 Mt/y north) needs hulls that do not exist. North full cost is $1,196/t at 6 Mt/y and $356/t at 30 Mt/y, against realised $366/t.
  - The cheapest alternative is to send all Vankor oil south (marginal $57/t). The repaired rule is that alternative plus north volume limited to the hulls available.
- **Consistency:**
  - Sever tanks (420 kt) give 51 days of buffer at 3 Mt/y but only 5 days at 30 Mt/y. There is a precedent of a tanker waiting 84 days.
  - Yenisei Gulf fast ice lasts until about July.
  - The rule never needs reverse flow from Payakha to Vankor.
  - Icebreaker demand is about 25–30 winter escorts a year with 2 hulls. Dikson coal ships in open water in summer, so it does not compete for winter escorts.
- **Hazards:**
  - OPEC+ quota caps national output, so the gains are cost cuts, not net extra tonnes.
  - The builder of Valentin Pikul is unverified. If it is not Russian-built, the north route waits for Zvezda hulls.
  - Rosneft is on the US SDN list, which gives the same buyer exposure on both routes.
- **Deciding unknown:** the actual winter cycle of the Yenisei Gulf hulls.
- **Cheapest experiment:** log the first 10 winter cycles between December 2026 and March 2027.
- **Closest existing work:** S&P/Ronald Smith on one tanker shuttling to Murmansk STS, and Rosneft's 2021 plan to use existing tankers. What this adds is the reversed allocation (Vankor stays south) and gating Payakha drilling to hull arrivals.
- **Verdict:** WORKS as a sequencing rule that saves cost. It does not add tonnes.

Sources: [gCaptain – Graham Act and Yamal fleet](https://gcaptain.com/u-s-sanctions-law-puts-russias-arctic-yamal-lng-fleet-in-crosshairs/), [Kyiv Independent](https://kyivindependent.com/us-could-hit-putins-arctic-gas-empire-by-sanctioning-14-lng-tankers/), [Wood Mackenzie](https://woodmac.com/news/opinion/could-an-expansion-of-western-sanctions-derail-yamal-lng), [Gas Processing News – condensate ban](https://www.gasprocessingnews.com/news/2026/04/fresh-eu-sanctions-set-to-hit-condensate-imports-from-russias-yamal-lng/), [LNG Prime – Kildin STS](https://lngprime.com/vessels/novatek-in-first-kildin-island-lng-sts/7573), [Cyprus Shipping News](https://cyprusshippingnews.com/2020/11/26/novatek-completes-first-ship-to-ship-lng-transshipment-in-the-murmansk-region/), [Argus – NSR/Arc7](https://www.argusmedia.com/en/news/2154877-nsr-to-stay-open-until-december-novatek), [S&P Global – Vostok Oil launch](https://www.spglobal.com/energy/en/news-research/latest-news/crude-oil/090626-russia-launches-major-vostok-oil-project-with-first-arctic-loading), [gCaptain – Vostok Oil](https://gcaptain.com/russia-launches-massive-vostok-oil-project-marking-new-arctic-shipping-era/), [Barents Observer – 84-day wait](https://www.thebarentsobserver.com/news/tanker-crew-waited-84-days-at-remotest-arctic-terminal/457741), [OilPrice](https://oilprice.com/Energy/Energy-General/Vostok-Oil-One-Tanker-Four-Trillion-Rubles.amp.html), [Carnegie](https://carnegieendowment.org/russia-eurasia/politika/2025/07/russia-new-oil-project), [Investfuture – Transneft 2026 tariffs](https://investfuture.ru/articles/transneft-povysit-tarify-na-transportirovku-nefti-na-5-1-v-2026-godu-CF4B40A61443632D43258D55005837BD)