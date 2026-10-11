**1. Goals**
- G1: Bring the cost of energy capacity (storage medium plus container) under about $2/kWh.
- G2: Storage sized for rare, uncertain worst-case lulls sits idle most of the year, so cut how much power capacity (kW) it needs.
- G3: Charge and discharge stacks that run only a few hundred hours a year need about 10x lower cost per kW.

**2. Paradigm:** Mainstream approaches push electricity into a medium bought for the purpose, hold it in containment built for the purpose, and pull it back through a durable converter that is always ready and sized for peak demand. That is forbidden here as the mechanism.

**3.** None of the mechanisms below uses OREFLOW through V27.

**4. Mechanisms borrowed from distant fields**
- G1, from detergent chemistry: laundry powders store "active oxygen" for years as coated, dry sodium percarbonate crystals rather than as liquid peroxide. A second source is the bombardier beetle, which keeps an inert reservoir and releases the energy only in a catalytic chamber.
- G2, from computer storage hierarchies (tape and disk tiers with predictive prefetch). In computing, the state is which blocks sit in which tier, the update rule moves blocks predicted to be needed within the lead time, and the driving signal is an access forecast. Ported here: the state is the energy in each tier, the update rule discharges the cold tier at forecast deficit divided by (lead time plus lull length), and the driving signal is an ensemble weather forecast.
- G3, from papermaking: retention aids flocculate fine particles onto fibre webs at about 1 km/min for cents per m². Ported here, they bind carbon and catalyst onto cellulose webs to make electrode-separator laminates.

**5. Honesty check**
- Percarbonate: the closest work is H2O2 fuel cells (Fukuzumi) and electrosynthesis of H2O2 from O2 (H. Wang group). What is new is using a dry crystalline adduct as bulk inventory for multi-week storage, with the carbonate recycled. Kept.
- Cold tier: the closest work is forecast-based predictive control of hybrid storage. That work schedules hardware that already exists. Here the forecast sets the hardware specification itself, a C/500 tier. Kept, but the difference is narrow.
- Paper stacks: the closest work is paper microfluidic fuel cells (PowerPAD). That work is milliwatt-scale and single-use. Here the stacks are grid-scale consumables rated in MW. Kept.

=== IDEAS ===
IDEA 1
NAME: Percarbonate Silo Battery
MECHANISM: Surplus electricity reduces air oxygen to hydrogen peroxide on cheap carbon cathodes in soda-ash solution, and the peroxide is crystallized as sodium percarbonate, the same powder used in laundry detergent. The coated dry crystals are piled in ordinary warehouses or silos, where they lose almost nothing for months. During a lull, the powder is dissolved and fed to membraneless cells in which selective catalysts both oxidize and reduce the peroxide, and the carbonate liquor goes back to the charging plant. In theory this stores about 0.3 kWh/kg using only water, air and reusable soda ash. Round-trip efficiency is a low 25-35%, which matters less for storage that cycles only a few times a year.
VALUE: Multi-week storage built from water, air and a bulk detergent chemical, at roughly $1-3/kWh of capacity.

IDEA 2
NAME: Forecast-Prefetched Trickle Tier
MECHANISM: Storage is split into a small fast tier (the existing daily batteries) and a huge cold tier deliberately built to discharge at only about C/500. Ensemble weather forecasts several days ahead trigger the cold tier to start a flat trickle and to keep the fast tier full. The trickle rate is set to the forecast total deficit spread over lead time plus lull duration, and the fast tier absorbs hour-by-hour mismatch. The rate is re-planned every forecast cycle.
VALUE: The power rating of long-duration storage falls from the peak deficit to roughly the mean deficit, so the cold tier can use very slow, nearly catalyst-free and extremely cheap hardware.

IDEA 3
NAME: Paper-Machine Throwaway Stacks
MECHANISM: Electrode-separator laminates are made on existing paper machines, where retention-aid chemistry flocculates carbon and catalyst particles onto cellulose fibre webs at kilometres per minute. Because discharge stacks run only a few hundred hours a year, they are treated as consumables: they run in membraneless or laminar-flow configurations, are swapped every few years, and are then re-pulped to recover the catalyst.
VALUE: Conversion hardware drops toward a few dollars per kW, so stacks that sit idle most of the year stop dominating the cost of storage.