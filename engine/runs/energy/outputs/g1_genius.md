**1. Borrowed idle hardware**
- Why it's hard: Storage that lasts for weeks needs converters and grid connections sized for the whole load, and they are used only a few weeks a year. The hidden assumption is that a store needs its own power hardware.
- Dissolve, move (c): Remove that hardware. During a calm, dark spell the wind generators, solar inverters, transformers and transmission lines are idle, so the store can discharge through them.
- Simplicity: A cheap bulk medium sits on each plant's DC link and discharges through the plant's own idle converter and line.
- Inevitability: These assets are idle exactly when the store is needed, so its power hardware costs nothing. Surprising, but of course.
- Honesty: The closest work is DC-coupled solar-plus-storage, which shares an inverter but runs on a daily cycle. What is new here is sizing the store for long durations based on that timing.

**2. Solar-pond separator**
- Why it's hard: Tanks, pumps and membranes dominate the cost per kWh of storage capacity. The hidden assumption is that charged electrolytes must be kept apart by hardware.
- Dissolve, move (b): Salt-gradient solar ponds already keep hot brine under cool water for months, using only a density gradient. Applied here, a dense charged electrolyte lies below a lighter one, and the still gradient zone acts as both the separator and the ionic conductor. What does not map: the active species diffuse, so the chemistry must be chosen for low crossover. Power is limited by pond area, but a pond several metres deep holds weeks of energy.
- Simplicity: A lined pond, two layers separated by density, and two electrode meshes.
- Honesty: The closest work is lab-scale biphasic membraneless flow batteries, which are centimetres in size, not ponds.

**3. Forecast-charged leaky store**
- Why it's hard: Stores must hold their charge for months, which requires membranes and sealed tanks. The hidden assumption is that the store must be full whenever a lull might begin.
- Dissolve, move (a): Lulls can be forecast days ahead, so the store only has to hold charge for about two weeks. Mixed-reactant electrolyte in an earthen pit leaks charge too fast to be useful today, but that rate becomes acceptable.
- Simplicity: A forecast, a pit of mixed-reactant electrolyte, and electrodes that each react with only one reactant.
- Honesty: The closest work is mixed-reactant fuel cells. They are not used as forecast-scheduled storage.

=== IDEAS ===
IDEA 1
NAME: Lull-idle converters do discharge
MECHANISM: A cheap bulk storage medium is attached to the DC link of each wind or solar plant. During calm, dark spells it discharges through the plant's own generator electronics, inverter, transformer and grid line, which are otherwise idle at those times. Charging uses the same path when output would otherwise be curtailed. The store is sized by how often the plant's hardware sits idle.
VALUE: Storage lasting for weeks then costs little more than its storage medium, because the power hardware and grid connection are already paid for.

IDEA 2
NAME: Density-stratified pond battery
MECHANISM: A lined pond holds a dense charged electrolyte layer under a lighter one. A still salt-gradient zone, as in solar ponds, blocks mixing while still conducting ions. Electrode meshes lie on either side of that zone. Each layer circulates within itself, so energy capacity grows with depth at the cost of earthworks.
VALUE: Electrochemical storage lasting for weeks needs no tanks, pumps or membranes.

IDEA 3
NAME: Forecast-charged leaky storage pits
MECHANISM: Weather forecasts trigger charging a few days before a predicted lull. The store is a membraneless pit of mixed electrolyte, read by electrodes that each react with only one reactant. It loses its charge over a couple of weeks, which is acceptable because it only has to last through the predicted lull.
VALUE: Accepting charge loss over about two weeks allows the cheapest possible containment for storage covering whole lulls.