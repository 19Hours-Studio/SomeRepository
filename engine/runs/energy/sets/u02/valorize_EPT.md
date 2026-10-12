=== CHECKED T01 ===
ANCHOR: forecast lead allows a kinetically locked charged state
VERDICT: REGIME
ESTIMATE: The deciding quantity is how much faster the medium must discharge than it may decay while held. Holding at 1%/yr needs k ≈ 0.01/3.15e7 s ≈ 3e-10 s⁻¹, and discharging over 100 h needs k ≈ 3e-6 s⁻¹. That is a ratio of about 9e3 (ln ≈ 9.1). With Ea ≈ 130 kJ/mol and A ≈ 1e13 s⁻¹, this is a step from 293 K to about 353 K. Heating only the slice passing through a reactor (c_p ≈ 1.5 kJ/kg·K × 60 K ≈ 90 kJ/kg) costs about 8% of a 0.3 kWh/kg medium before heat recovery. Forecasts warn 3–5 days ahead, against activation times of hours. So the idea works for solid or liquid fuel-like media fed through a small activation reactor (metal powders, LOHC-type carriers). It does not work for cells activated in place, and it is known (reserve batteries, metal fuels).
NAME: Thermally gated fuel-like reserve
MECHANISM: A charged state behind a barrier of about 130 kJ/mol loses under 1%/yr at 20 °C and discharges in about 100 h at about 80 °C. So a solid medium can sit in an open pile and be fed through a small heated or catalysed reactor, with no containment. A 3–5 day forecast covers activation times of hours to a day, but the first hours of each lull must come from a fast tier.
VALUE: It allows bulk piles with no containment, so cost is about the medium's $/kWh plus yard space. But self-discharge and containment are rarely the main cost, so this alone gives well under 10x.

=== CHECKED T02 ===
ANCHOR: make the medium only just before the lull
VERDICT: FALSE
ESTIMATE: The deciding quantity is the production power and surplus energy needed inside the forecast window. Making 1 TWh in 72 h needs about 14 GW of production plant. It also needs about 14 GW of surplus above load in exactly the days before an anticyclone lull, which is about 1.4x the mean load of a 10 GW grid. The plant itself, at about $500/kW, costs about $7/kWh of capacity, sits idle over 95% of the year, and still needs permanent containers. Capital does not disappear; it moves into a plant with worse utilisation.
NAME: Just-in-time media shift capital
MECHANISM: What is actually true: yearly capacity cost is CRF × permanent hardware. A medium made just in time swaps medium cost for plant cost of c_plant/t_make (about $7/kWh at $500/kW and 72 h). It also needs E/t_make of surplus right before the lull. A durable medium at ≤$20/kWh, charged over weeks with charge power close to discharge power, is cheaper and more reliable.
VALUE: No gain. Utilisation does not improve; it gets worse and adds a surplus-timing risk.

=== CHECKED T03 ===
ANCHOR: cost the rarely used deep tiers per use
VERDICT: REGIME
ESTIMATE: The deciding quantity is the cost of lost energy per use × uses per year, compared with annualised capex. A tier used 0.1 times a year at η = 0.3 with $0.02/kWh surplus loses 0.02×(1/0.3−1) ≈ $0.05/kWh per use, about $0.005/kWh·yr. Capex at $1/kWh × CRF 0.08 is $0.08/kWh·yr, so efficiency hardly matters. But the deep tier still needs its own full discharge power. An open-cycle H₂ turbine at about $600/kW over E/P ≈ 150 h is about $4/kWh, on top of salt-cavern H₂ at about $0.5/kWh. With 60% of capacity at about $4.5/kWh, total cost falls about 2x, not 3–5x. Charging the deep tier over 5 years needs only about 46 MW of electrolyser per 0.6 TWh. The idea is known from seasonal-hydrogen planning studies.
NAME: Low-efficiency deep reserve tier
MECHANISM: For tiers cycled at most 0.1 times a year, round-trip efficiency as low as 0.1–0.3 adds under $0.01/kWh·yr, so only capex counts. The deepest 50–60% of capacity should be a near-free bulk medium (salt-cavern H₂, about $0.5/kWh) refilled over years by a small electrolyser (tens of MW per TWh). Its discharge power (about $4/kWh at E/P ≈ 150 h) is the binding cost, unless existing gas turbines are reused.
VALUE: About 2x lower total storage cost (up to about 3x with reused turbines). Real, but already in the planning literature.

=== CHECKED T04 ===
ANCHOR: generators that travel to where the wind is
VERDICT: FALSE
ESTIMATE: The deciding quantity is the distance to uncorrelated weather, set against how the energy gets back. Wind correlation lengths are about 500–1000 km and winter anticyclones span about 1500 km. A ship at 28 km/h (15 kn) therefore needs 1–2 days each way. With no cable, the energy comes back as onboard storage of P × cycle time: about 4 GW × 96 h ≈ 0.4 TWh of mobile storage, plus about 300 ships carrying about 15 MW of turbines each, at a large premium per kW. The store is moved, not removed.
NAME: Moving generators still need storage
MECHANISM: What is actually true: fixed generation in uncorrelated regions 1000–2000 km away, joined by HVDC, lowers the multi-day storage needed. HVDC costs about $0.5/kW·km plus about $200/kW per converter end, so about $1400/kW for 2000 km. That compares with $5000/kW for 250 h of storage at $20/kWh. This continental smoothing is known.
VALUE: Mobility adds no gain. The real smoothing benefit comes from fixed HVDC links, which is standard.

=== CHECKED T05 ===
ANCHOR: hold energy in stocks that exist anyway
VERDICT: FALSE
ESTIMATE: The deciding quantities are stock mass × specific energy, and the medium's share of total cost. Cheap actives that can reach TWh scale cost little per kWh already: Fe at about $0.4/kg and 0.5–1 kWh/kg is under $1/kWh, and Zn at about $2.7/kg and about 1 kWh/kg is about $3/kWh. That is ≤5–15% of a $20/kWh target, so a free medium saves at most about 1.2x. Expensive actives, where a free medium would matter, have stocks of only tens of GWh: vanadium needs about 3.3 kg/kWh, and world output of about 110 kt/yr is about 33 GWh/yr. Heat in warehouse goods (1 kJ/kg·K × 20 K ≈ 6 Wh_th/kg) is low-grade heat, not electricity.
NAME: Free medium saves little
MECHANISM: What is actually true: a free medium removes only the medium's share of capex. In cheap-active long-duration stores, cost is in cell hardware per kWh, so the lever is thicker electrodes (the transport-length law), not free mass. Known cases where a host or lent medium works are existing reservoir pairs for pumped hydro and vanadium electrolyte leasing, both capped by the size of the host.
VALUE: At most about 1.2x for chemistries that can scale. Not a 10x lever.

=== CHECKED T06 ===
ANCHOR: make the medium with curtailed electricity
VERDICT: FALSE
ESTIMATE: The deciding quantities are the energy share f of the medium's price and the plant's capacity factor. Energy is about 20–40% of bulk-material price (Al: 14 kWh/kg × $0.05 ≈ $0.70 of about $2.4/kg; chlor-alkali about 50%), so free power saves at most 1/(1−f) ≈ 1.3–2x. A plant running only on curtailment (1000–2000 h/yr, capacity factor 15–20%) carries 5–7x the capex per kg. For aluminium, about $0.4/kg·yr of capex at full load becomes about $2/kg, which cancels the saving. The medium is also bought once per 20–30 years.
NAME: Embodied energy is minor
MECHANISM: What is actually true: making the medium with surplus power saves at most 1/(1−f_energy), about 1.3–2x, and only on the medium. That disappears once process capex is spread over curtailment-only hours (capacity factor below about 30%). Surplus power is worth more as the store's own charge.
VALUE: Close to zero net gain once low plant utilisation is counted.

=== CHECKED T07 ===
ANCHOR: borrow a commodity stockpile as the active mass
VERDICT: FALSE
ESTIMATE: The deciding quantity is the present value of leasing a resellable commodity versus owning it. Owning material that stays in spec and is resold after 20 years costs PV = P(1−1.05^−20) ≈ 0.62P. Leasing at 5%/yr costs 0.05P × 12.46 ≈ 0.62P. They are equal once resale value is counted, so the gain is about 1x. A 10–30x gain would need borrowing for only 2–4 weeks a year, which means charging E within days (the same 14 GW surplus problem as T02). As in T05, scalable actives already cost only about $1–3/kWh. Aluminium re-smelted in a Hall-Héroult cell does come back in spec, but its round trip is only about 4.2/14 ≈ 30%.
NAME: Leasing equals owning resellable actives
MECHANISM: What is actually true: for an active that is not consumed and keeps its resale value, capacity cost is already interest plus handling, whether bought or leased. Leasing changes financing, not cost. It pays only for expensive actives with small world stocks, such as vanadium at tens of GWh/yr.
VALUE: About 1x. It is a financing choice, not a cost lever.

=== CHECKED T08 ===
ANCHOR: an applied field switches discharge instead of separators
VERDICT: FALSE
ESTIMATE: The deciding quantity is how far an applied signal reaches into the electrolyte, set against how much it must suppress the reaction. Electric fields are screened within the Debye length, λ_D ≈ 0.30 nm/√I ≈ 0.3 nm at 1 M, so they act only at the electrode interface. Mixed charged species react in the bulk at k c² ≈ 1e8–1e10 M⁻¹s⁻¹, about 10^10 faster than useful discharge. Magnetic spin effects change radical-pair rates by only tens of percent, and light penetrates only about mm into absorbing electrolyte. Nothing comes close to 10^10.
NAME: Separation stays, but cheaply
MECHANISM: What is actually true: charged reactants must stay apart, but the separation can be cheap. If both actives are immobile solids on their electrodes (Fe, Zn, MnO₂, air), only electronic insulation is needed, and a cheap porous separator gives near-zero crossover (D_active ≈ 0 in the crossover-ohmic invariant). Fluid actives need a spent-electrolyte buffer with s ≫ √(Dt). Signals can gate only interface side reactions, such as hydrogen-evolution poisons.
VALUE: Membrane cost can be avoided with solid, immobile actives (known, e.g. iron-air), not with field gating.