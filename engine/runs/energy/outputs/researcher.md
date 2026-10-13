None of these ideas makes multi-day storage ten times cheaper by itself. Each one cuts the cost of the discharge converter (the machine that turns stored energy back into electricity) by roughly 2 to 9 times, but only for one slice of the problem. I tried 19 ideas. Each new idea got 1 to 3 web searches and a Python check of the number that decides whether it works. I kept 6, dropped 13, and found 7 already existed.

The checks ran on a 100% wind-and-solar version of Germany. It is built from real daily German consumption, wind and solar data for 2012-2017 (6 years only, at daily rather than hourly resolution). That system's worst daily-average shortfall is 61 GW, and a converter that size runs only about 900 full-load hours a year. At that duty a new hydrogen turbine adds $0.10-0.19 per kWh delivered and a reversible solid-oxide cell (rSOC) adds $0.35-0.7. So the converter, not the storage medium, is the problem. All six kept ideas attack that cost.

=== IDEAS ===
IDEA 1
NAME: Range-extender fleet as peaker
MECHANISM: Plug-in hybrids with range extenders (EREVs) already carry a mass-produced engine-generator that is paid for, idle and parked during winter dark spells. Bidirectional chargers turn it into a distributed power plant. A whole-shortfall version loses: running on e-methanol, its round-trip efficiency is 0.18, which forces wind and solar capacity from 1.3 to 1.5 times demand (19.3 vs 20.1 B$/yr for a new-turbine path). The repaired design gives the fleet only the top slice of the shortfall: hydrogen turbines are built to 50% of peak, and the cars cover 6.6 TWh over 621 h/yr. That cuts discharge-side cost 22% (6.15 vs 7.90 B$/yr), with the converter costing $73/kW (the charger premium) instead of $900/kW. A 15% EREV share of German cars, half plugged in at 11 kW, gives 40 GW. One limit: a full car tank lasts only about 13 h at 11 kW, so the design needs lower export per car from more cars.
VALUE: It removes about half of the new firm capacity a renewable grid needs, and EREV owners (a fast-growing segment in China) earn from a machine that otherwise sits idle.

IDEA 2
NAME: Dual-shaft hydrogen heat pumps
MECHANISM: Large open-drive district-heating heat pumps get a clutched hydrogen engine on the compressor's free shaft end. In a dark spell the electric motor goes offline and the engine turns the compressor, with its exhaust heat also fed into the heating network. So the biggest winter load leaves the grid without fuel ever becoming electricity. 1 kWh of fuel gives 1.65 kWh of heat, which displaces 0.55 kWh of grid electricity, versus 0.40 from a hydrogen turbine. Overall round-trip efficiency is 0.36 instead of 0.26, at about $109 per kW of displaced load instead of $900/kW. The German scale is about 9 GW of the 61-120 GW need.
VALUE: District-heating utilities become dark-spell resources that are both more efficient and much cheaper than new turbines.

IDEA 3
NAME: Farm machinery dark-spell gensets
MECHANISM: Tractors are mostly idle in winter. Farms already have grid export connections built for rooftop solar, and that capacity is unused in a dark spell. Farms also hold their own diesel tanks, which can store renewable diesel (HVO) or e-diesel. A $150/kW tractor-driven (PTO) generator joins the three into a dispatchable unit with no new engine, grid connection or fuel store. Germany has about 80 GW of tractor shaft power, limited to about 15 GW by export capacity. A 3000 L tank gives 162 h at 60 kW, and the cost is $0.029/kWh at 600 h/yr.
VALUE: It turns rural farm sites into a multi-day distributed reserve and gives farmers winter income from machines that sit unused.

IDEA 4
NAME: Electrolyser grid interface reused
MECHANISM: Electrolysers run only during surplus, so their transformers, rectifiers and grid connections sit idle in exactly the hours discharge is needed. Their size also matches: about 55 GW of electrolysers needed against a 61 GW discharge need. Making the rectifier bidirectional (about $40/kW) and putting cheap mass-produced DC sources (such as engine-rectifier sets or automotive fuel cells) on the same bus removes about $250/kW of interface cost. That is about 14 B$ of investment in Germany, or $0.028/kWh at 900 h.
VALUE: It roughly halves the non-stack cost of hydrogen round-trip storage without needing a reversible stack.

IDEA 5
NAME: Dormant boilers as discharge
MECHANISM: In a cold dark spell, heat pumps add about 57 GW of electric load, which roughly doubles the shortfall. Germany's existing boiler fleet (about 380 GW of heat output, already paid for) can instead burn stored hydrogen or biomethane in dark spells, removing that load. Fuel-to-displaced-electricity efficiency is 0.42 at the heat pumps' cold-weather efficiency of 2.2, about the same as a turbine's 0.40, but with zero new converter capital.
VALUE: Keeping boilers as dormant backup could avoid roughly half of the firm capacity a fully electrified winter would otherwise need.

IDEA 6
NAME: Hemispheric powership rotation
MECHANISM: Dark-spell seasons in the northern and southern hemispheres do not overlap. Ship-mounted plants can serve November to February in the north and June to August in the south, which doubles converter use after 34 days of transit. The cost is $0.064/kWh versus $0.106/kWh for a fixed turbine.
VALUE: One converter fleet serves two continents' winters, which helps southern-hemisphere grids with no seasonal storage.

NOTES
Closest existing work, and how each idea differs:
1. Range-extender fleet: a Beijing Institute of Technology paper tests control of range-extender feed-in to the grid, and a patent on "multiplexed low-cost engines" proposes new car-engine gensets. Neither uses existing car fleets at fleet scale, and neither assigns them only to the top slice of the shortfall.
2. Dual-shaft heat pumps: a gas-engine-driven heat pump runs in Ejby, Denmark, and the Danish EUDP13-I project puts an electric heat pump beside a gas engine. I found no single compressor with a clutched dual drive that switches for dark spells.
3. Farm machinery: tractor-driven generators are sold only for farm backup, and Gridtractor works on electric-tractor batteries. I found nothing using them to export power to the grid.
4. Electrolyser interface: reversible solid-oxide cells share hardware by design, and CAISO filings treat a separate electrolyser plus fuel cell as hybrid storage. Sharing the interface across separate, cheap stacks is the new part.
5. Dormant boilers: hybrid heat pumps are well studied for peak relief (arXiv 2012.01831, Artelys, studies in Canada). Only the framing is mine: counting the boiler fleet as an already-paid seasonal discharge converter, with the check that its efficiency matches a turbine. Novelty is partial.
6. Powership rotation: powerships and rental-generator redeployment exist. I found no seasonal rotation between hemispheres.

Dropped because they already exist: duty-matched car-engine peakers (patent), automotive fuel cells as peakers (iScience 2024), retired jet engines as turbines (FTAI Power, CFM56), a strategic e-methanol reserve, and dual-fuel loads that store gas by burning surplus power instead.

The 3 most informative things the checks taught me:
1. Round-trip loss hurts mainly through the overbuild it forces, not through the size of the charging plant. With wind and solar at 1.5 times demand, efficiency as low as 0.18 can still be charged from surplus, by a charging plant running 47% of the time. At 1.3 times demand, anything below about 0.25 cannot be charged at all. So cheap, inefficient converters only pay off when they serve the few-hundred-hour top slice of the shortfall. Used for all of it, they lose: the range-extender fleet broke even at best until repaired.
2. Shrinking the converter by adding a multi-day buffer does not work. The buffer then needs its own 30 GW of output and must cost under about $9/kWh including that output, so it is itself long-duration storage.
3. In winter the converter question reverses. Heat pumps roughly double the shortfall, and a heat pump's cold-weather efficiency is about the inverse of a turbine's. So burning stored fuel at the heat load, in a boiler or an engine-driven compressor, matches or beats turning it back into electricity, with converters that are already paid for or cost about $100/kW.

Everything is in /home/user/SomeRepository/engine/runs/energy/researcher/. LOG.md has all 19 attempts. The scripts are s01_converter_burden.py through s08_quick_checks.py, and the data is in data/opsd_germany_daily.csv.

Sources: [Multiplexed low-cost engines patent](https://patents.justia.com/patent/20230187964), [Automotive fuel cells for peak power, iScience 2024](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11246014/), [FTAI CFM56 power](https://www.eplaneai.com/news/cfm56-engine-repurposed-to-power-ai-data-centers), [Ejby gas-engine heat pump](https://iifiir.org/en/fridoc/gas-engine-driven-heat-pump-central-in-ejby-denmark-8564), [EUDP13-I hybrid heat pump](https://energiforskning.dk/en/node/14953), [Heat demand peaks study](https://arxiv.org/pdf/2012.01831), [Ultra-deep e-methanol storage](https://www.pv-magazine-australia.com/2023/11/15/the-case-for-ultra-deep-e-methanol-storage), [CAISO hybrid storage presentation](https://stakeholdercenter.caiso.com/InitiativeDocuments/SDG-EPresentation-EnergyStorageEnhancementsWorkingGroup-Jul26-2021.pdf), [Gridtractor](https://www.newswire.com/news/gridtractor-led-farm-electrification-consortium-awarded-california-21870007), [Leroy-Somer Gearlec PTO generator](https://acim.nidec.com/generators/leroy-somer/products/industrial/tractelec-gearlec/gearlec), [BIT range-extender V2G paper](https://pure.bit.edu.cn:443/en/publications/%E5%B8%A6%E6%9C%89v2g%E5%B9%B6%E7%BD%91%E7%9A%84%E7%94%B5%E5%8A%A8%E6%B1%BD%E8%BD%A6%E7%94%A8%E5%A2%9E%E7%A8%8B%E5%99%A8%E6%8E%A7%E5%88%B6%E7%AD%96%E7%95%A5), [Dunkelflaute in Europe (Kittel et al.)](https://ar5iv.labs.arxiv.org/html/2411.17683)