# Repair log (all numbers from `python3 calc.py`)

| idea | round | change | decisive number | result |
|---|---|---|---|---|
| 1 sugar-glass | R1 | original: pos+neg radicals in one melt | Smoluchowski k=2e7 /M/s at 0.5 Pa s -> t1/2 1e-7 s; melt heat 1.6 kWh_th/kWh_e (0.16 after 90% recovery) | FAIL: needs two separate granule streams |
| 1 | R2 | separate streams + porous separator | invariant f x eta = (RT/F)(c_aD_a/sum c_iD_i) = 15.7 mV -> 31% crossover at 50 mV | FAIL |
| 1 | R3 | bulky oligomeric actives (r 2.5 nm) + small decoupled carrier (10x SE) ; electron hopping (Dahms-Ruff) for electrode access | f x eta = 0.53 mV -> 1.1% crossover at 50 mV; D_app 2.5e-12; 15 um half-channels: 15 A/m2, 16 mV ohmic, 1.5 bar per 2 cm | WORKS physically |
| 1 | R4 | cost closure, regime | cell 0.30 m2/kWh at 300 h ($7.6/kWh), 0.09 at 1000 h ($2.3); actives need <=$0.5-1.9/kg (V 1.0-1.4) for <=$10/kWh | works only at >=300 h and with sub-$2/kg oligomeric quinones |
| 2 locked rubber | R1 | lightly crosslinked NR (shape-memory NR) | neo-Hookean G 0.25 MPa: 0.7 Wh/kg at lam 5, 2.9 at lam 10; at $1.7/kg -> $810/kWh | FAIL (medium cost) |
| 2 | R2 | require medium <= $0.02/kg (scrap) | $10/kWh at 3 Wh/kg x 0.7 | only scrap rubber qualifies |
| 2 | R3 | cord-free tread strips from scrap truck tyres, lam 4 (300%; EB ~400-500%), M300 11-17 MPa | input 4.35 Wh/kg, ~2.4 Wh/kg recoverable; 418 kg/kWh; yard $7/kWh; 900 kN winch | energy OK, fixity of filled vulcanizate at ambient not shown |
| 2 | R4 | lock by winter cold (store below crystal melting) ; seasonal 1 cycle/yr | resource: 35M truck tyres x 6 kg -> 0.5 GWh/yr | NICHE only (resource- and fixity-limited) |
| 3 twin ditch | R1 | original floor electrode, flow-by | i_lim ~9.6 A/m2 at 20 mM; crossover 1.5%; $3/W | marginal: mass-transfer bound |
| 3 | R2 | electrodes = flow-through felts on both faces of the divider; ditch = feed channel | i_lim 290-480 A/m2; run 50 A/m2: 48 mV ohmic, 0.31% crossover, $0.98/W -> $4.9/kWh at 200 h, $2.0 at 500 h | WORKS (converter) |
| 3 | R3 | powder cost | 7.5-12.4 kg/kWh -> $11-19/kWh at $1.5/kg; ditch residence 17 min must be < nucleation induction | molecule-limited (<=$1.5/kg, 2 e-, ~200 g/mol) |
| 4 vapour clay | R1 | plain smectite isotherm (GAB fit to Ca-montmorillonite shape) | 4.5 Wh/kg (RH 0.15-0.9), 220 kg/kWh; 1.11 m3/s/kW at 25 C | heavy |
| 4 | R2 | CaCl2-in-clay composite, step near RH 0.3-0.45 | 9.2 Wh/kg, 109 kg/kWh, $9.8/kWh; heat/work 23 -> 3 K costs 45% round trip | FAIL at 3 K |
| 4 | R3 | 6 cm beds interleaved with pond-water bags, dT<=0.5 K; operate 35 C | 7% loss per 0.5 K pair; 3.2 m2 film/kWh; 0.50 m3/s/kW, ratio 2.2 (single stage) -> $2-4k/kW -> $1.3-2.6/kWh at 1500 h | WORKS for >=1000 h, RTE ~50% |
| 4 | R4 | sorbent RH window trade-off | RH 0.1: heat/work 7.9, 0.77 m3/s/kW; RH 0.3: 15, 0.49 m3/s/kW | choose RH ~0.2-0.3 step |
| 5 earth pile | R1 | original 1 mmol/g, 3 cm, 10 vol% char | char 10 vol% below percolation -> sigma_e ~0 | FAIL (electronic) |
| 5 | R2 | 25 vol% char (4.4 S/m) ; check ordinary bentonite 0.4 mmol/g | 0.25 kWh/m2 -> foil $24/kWh | FAIL with common bentonite; needs Fe-rich smectite |
| 5 | R3 | Fe-rich smectite 1.5 mmol e/g accessible (NAu-2 has 4.1 mmol Fe/g, partly inactive), 4 cm, 2 M brine, 4-week discharge | 1.25 kWh/m2, 59 mV total loss of 600 mV, mediator shuttle 0.1-0.7%/2 wk; ~$16/kWh | WORKS (resource-limited to Fe-rich clays) |
| 6 floating PV pond | R1 | Zn / polybromide-quaternary dense phase on coke, open water gap 3 cm | night cooling Ra 9.5e5 -> convective self-discharge ~43%/10 d | FAIL |
| 6 | R2 | gap filled with nonwoven (k 1e-10 m2) | Darcy-Ra 0.1 (<39.5) -> diffusive 1.4%/10 d | WORKS |
| 6 | R3 | per-cell PV sub-string (4 c-Si cells ~1.95 V) charges each isolated tray cell, no shared electrolyte | 86% of MPP; night dark leak 2 mA (<0.1%/10 d); cost ~$34/kWh | WORKS; core cell = known minimal Zn-Br (Biswas 2017), novelty in per-cell PV coupling |

Sources: WLF (Williams, Landel, Ferry 1955); Smoluchowski/Stokes-Einstein; Dahms-Ruff hopping; Archie's law; Magnus p_sat; Keren & Shainberg 1975 (Clays Clay Miner., montmorillonite isotherms, shape only); Gorski et al. 2012 ES&T 46:9360 (mediated Fe-smectite capacities, NAu partly inactive); NAu-2 4.1 mmol Fe/g (characterisation cited in search); Katzenberg, Heuwers, Tiller Adv. Mater. 2011 (shape-memory/superheated NR); US5132357 (tread M300 11-17 MPa, TS 18-22 MPa); Biswas et al. EES 2017 10:114 (minimal-architecture Zn-Br, >90% CE, <$100/kWh projected); PNNL freeze-thaw battery (closest to idea 1 "freeze to stop self-discharge"); redox-targeting/solid-booster RFB review (PMC8067695) for idea 3. Prices marked as assumptions in calc.py (felt $18/m2, ZnBr2 $3/kg, machine $3-6k per m3/s, Fe-clay $50/t, Mn ore $250/t, char $250/t).
