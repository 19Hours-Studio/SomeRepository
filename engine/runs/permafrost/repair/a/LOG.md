# Repair log (run a) - one line per round. Scripts: idea1_carbonyl.py ... idea4_sky_freeze.py; outputs: idea*_out.txt

## Sources used
- S1 Ni(CO)4 vapour pressure ln P[kPa]=14.5275-2836.86/(T-28.762), 228-337 K (Chemeo/NIST): https://www.chemeo.com/cid/35-741-0/Nickel-tetracarbonyl.pdf
- S2 Power of Siberia 38 bcm/yr, 1420 mm, 9.8 MPa, permafrost route: https://www.gazprom.com/projects/power-of-siberia
- S3 Metal-carbonyl guard beds / guard catalysts (US6165428; Clariant ActiSorb 400); 1961 French study: activated carbon inefficient for Ni(CO)4 (cited in US4740361)
- S4 Ni concentrate payability 70-76 % (Centaurus Jaguar FS 2024: 76 %; CRU via RNC 2018: conventional 70-75 %): https://mining-journal.com/base-metals/news/1345264/analysis-confirms-improved-dumont-nickel-payability
- S5 Kun-Manie PFS needs a 338 km road to BAM: https://www.miningweekly.com/article/kun-manie-nickelcopper-sulphide-project-russian-far-east-2018-07-06
- S6 Glaciothermal engine (freezing water boils organic fluid, polar-air condenser, 9-11 % net at interior sites): Smith, PhD thesis, Univ. Tasmania https://figshare.utas.edu.au/articles/thesis/Evaluation_of_glaciothermal_engines_for_the_generation_of_polar_renewable_energy/23240213 ; Lock 1989, Arctic 42(3):253 (~5 %, 0 C water vs -25 C air)
- S7 Isolated Far-North diesel power 10-40 RUB/kWh: https://ipolytech.elpub.ru/jour/article/download/289/289
- S8 Udokan leach-SX-EW cathode start Sept 2026: https://www.kitco.com/news/off-the-wire/2026-09-02/russias-udokan-launches-copper-cathode-production-after-fire-related
- S9 Freeze crystallisation of copper leachate (water/Na2SO4 target): IMWA 2018 Maree; Chilean solar-evaporation chalcanthite from PLS (78 % Cu recovery)
- S10 Free-fall tribo separators work on 0.1-2 mm grains: https://link.springer.com/article/10.1007/s00501-016-0515-1 ; feldspar/quartz free-fall needs feed preheated >100 C (Peretti & Zucca, CNR); STET belt separators (Bittner 2014)
- S11 Mekhanobr-Tekhnika separator: friction-charged dielectric drum makes the field, particles still HV-precharged: https://rudmet.ru/journal/1762/article/30164
- S12 Siberian Ca-Cl brines 170-631 g/L, Li up to 600 mg/L: https://rudmet.ru/journal/694/article/9081/ ; mean LiCl ~2.5 g/L, high Ca/Mg (Bull. TPU 2004 307(7))
- S13 LiCl-CaCl2-H2O has a LiCl.CaCl2.5H2O double-salt field (J. Chem. Eng. Data 2019, 10.1021/acs.jced.8b00777)
- S14 Udachny January mean -39.4 C (Wikipedia climate table)
- S15 Brine/DLE lithium $3.4-6.2/kg LCE (Argonne overview): https://techconnectworld.com/World2026/a.php?i=594
- S16 Polar regions lowest radiative-cooling capacity: https://arxiv.org/pdf/2410.04109
- Physics constants / thermo: NIST/CRC (Ni(CO)4 dHf -602.9 kJ/mol, S 410.6 J/molK; CuSO4 14.3 g/100 g at 0 C); Gauss surface-charge limit eps0*3 MV/m; Planck integration; Murphy-Koop ice vapour pressure.

## Rounds
| # | idea | change | decisive number | result |
|---|------|--------|-----------------|--------|
| 1 | I1 carbonyl | original 0.1 mol% at 9.8 MPa | Psat(-10 C)=11.3 kPa vs 9.8 kPa partial (87 % sat); condenses below ~-13 C (S1,S2) | FAIL at 0.1 % |
| 2 | I1 | dose cut to 0.04 mol% (70 % sat at -20 C) | 37 kt Ni/yr on 38 bcm; liquid Ni(CO)4 pumped in at 3.4 kg/s like methanol injection | dew point OK |
| 3 | I1 | stabiliser CO sized by equilibrium | 0.12 mol% CO keeps Ni(CO)4 stable to 80 C; use 0.15 % | OK |
| 4 | I1 | receiver: carbon guard bed -> hot recuperated decomposer (carbon inefficient for Ni(CO)4, S3) | 180-200 C gives 99.97-100 % capture; 395 MW recuperated, 43 MW fired = 0.12 % of gas; ~49,000 m2 exchanger; $439/t Ni | OK |
| 5 | I1 | hazard | 400 ppm Ni(CO)4 = ~1 % H2S toxic-equivalent (IDLH 2 vs 50 ppm) -> sour-gas class; inject close to plant to keep the carbonyl segment short | design-down |
| 6 | I1 | cost, sulfide concentrate (roast+SO2 fix) | $3.4-5.0k/t Ni vs selling concentrate $5.0-6.0k/t (payability 70-76 % + truck/rail $1,067) -> 1.0-1.8x | NICHE |
| 7 | I1 | feed with no roast: awaruite / pre-reduced Ni-Fe | $2.3-2.8k vs $5.5k -> 2.0-2.35x; transport step alone $7 vs $1,067/t Ni (~150x) | NICHE (geography: no Ni deposit on a GPP-bound line; Kun-Manie 338 km from BAM, S5) |
| 8 | I2 freeze engine | engine model 55 % Carnot, evap -6 C, cond air+12 K | 11.7 kJe/kg ice at -35 C air, 15 at -40, 19 at -45 (claim 15-30 too high; S6 9-11 % only in Antarctic interior) | partly |
| 9 | I2 | Cu balance | PLS 2.5 g/L, 80 % rec -> 494 kg ice/kg Cu; engine covers 80 % of EW at -35 C, 104 % at -40 C | energy OK only for dilute PLS + very cold air |
| 10 | I2 | Fe/acid ceiling | Fe0 2 g/L, acid 4 g/L -> CF max 45 -> Cu recovery 60 %; Fe0 0.5, acid 2 -> 90 % | restrict to low-Fe oxide-ore PLS (Cu/Fe>=2), Fe kept ferric |
| 11 | I2 | hardware: static ice-on-panel pond | Stefan 1.06 m/face/season, 2.55 km2 panels, $176M -> $2,795/t Cu | FAIL |
| 12 | I2 | direct-contact propane crystallizer + wash column + ACC | 127 MWth, 4.5 MWe, $63M for 10 kt/yr -> $1,090/t Cu vs SX+diesel-EW $1,417 -> 1.3x | NICHE |
| 13 | I3 frost separator | charge & drift | Gauss limit 148-590 uC/kg; at 5 % -> 10 uC/kg at 300 um drifts 30-60 cm over 1.5 m plates | OK |
| 14 | I3 | self-excitation | 5 uA/m charging, 1.35 s to 45 kV; self-excites even with 1e10 ohm leakage | OK (needs regulator, not spark gap) |
| 15 | I3 | 'cold air is dry' check | grain at air temp -40 C sees RH 90 % (claim wrong); warmed outdoor air at 0 C: RH 1.9 % (= feed preheat ~85 C in temperate plant, S10) | repair: enclosed cascade ventilated with outdoor air warmed by mill heat (692 m3/t) |
| 16 | I3 | cascade model with middlings recycle | per-stage split 0.85/0.45 -> 9 stages, 6.1 % Li2O, 82 % rec, 7.2x circulating load; 0.80/0.50 -> 25 stages | works only if per-stage enrichment >=1.9 |
| 17 | I3 | cost 300 kt/yr spodumene ore, 700 km winter haul | $27/t ore vs raw-ore haul $105 (3.9x) vs Arctic flotation+haul $43 (1.6x, ~1.2x after 10 % recovery penalty) | WORKS vs hauling ore / NICHE vs flotation |
| 18 | I4 sky freeze | radiative balance of 8-13 um film at -52 C | window band only 30 W/m2 at -50 C; zero-load depression 7.8 K at -40 C air; net removal <0 unless air <= -45 C | FAIL as stated |
| 19 | I4 | Udachny season, wind on coldest nights | 273 h/yr usable, 12.6 MJ/m2, 55 kg brine/m2/winter -> 11,600 m2 per t LCE/yr -> ~$55,000/t LCE vs DLE $3.4-6.2k | FAIL (~10x too dear) |
| 20 | I4 | brine choice above eutectic | at -40 C ambient Li concentrates only 1.0-1.55x; the gain needs ~93 % of mass solid AT the eutectic | FAIL - anchor cannot be rescued at scale |
| 21 | I4 | niche: trays on Ca-free DLE eluate (LiCl eutectic -75 C) | CF 30x at -40 C, 182 t ice per t LCE, ~100 m2 per t LCE/yr, ~$500/t LCE | NICHE (drops the Ca-eutectic part of anchor) |
