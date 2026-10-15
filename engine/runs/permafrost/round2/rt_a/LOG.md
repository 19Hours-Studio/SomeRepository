# LOG (rt_a, round 2) - scripts in calc/idea1..4.py
I1 R1 | safety: inject below last offtake, stop injection 1 transit (10 h/300 km, 72 h full line) + MCS pump-down before vents | inventory 888 t Ni(CO)4 (0.41 t/km, 12.3 t/30 km), t1/2 air 40-60 s -> 0.3-2% survives 1 km (46% if CO slows it to 300 s) | planned vents fixed, rupture residual conceded
I1 R2 | cap compressor discharge 50 C -> CO excess 0.05% (needs 0.032%) | CO 2.51 t/t Ni (was 3.70; floor 1.91) | partial fix
I1 R3 | 250 C Ni-bed polish at 60 bar | residual 0.09 ppb in gas (200 C: 4.5, 180 C: 27.7) | slip fixed (kinetics untested)
I1 R4 | cost vs best practice | line-specific $109-947/t Ni vs matte $150, pellets ~$100 (decomposer cancels), concentrate $1,067 | FAILS; break-even CO <=$56/t (free by-product CO only)
I2 R1 | propane -> n-butane (no simple hydrate; 1960s SRF desalination fluid) | vp 0.97 bar at -2 C, 0.30 at -30 C; 309 m3/s exhaust | hydrate fixed
I2 R2 | staged freezing, ice-weighted Tf | mean Tf -0.7..-0.9 C; final -11 (salting-out 30 g/kg) to -32 C; 90% case 30-57 wt% acid | 80% cap, 90% conceded
I2 R3 | real approaches + fans 100 Pa | net 3.3 kJ/kg ice at -35 C air (fans ~50% of gross) | worse than claimed
I2 R4 | natural-draft dry tower 60-80 m (47-52 Pa) + dispatch to coldest hours | Udachny 42-63% of EW, Chara 24-44% (fans: 18-42 / 2-22%) | partial
I2 R5 | no wash column ($41M), costs | 2.5 g/L: off-grid 0.83-1.08x, Udokan grid 0.56-0.86x vs SX-EW | fails at 2.5 g/L
I2 R6 | PLS 10 g/L | ice 123 kg/kg Cu, freeze step $105-165/t, engine ~12% of EW; route ~1.1-1.4x off-grid | NICHE
I3 R1 | field 150 kV/m, 0.5 m gap (75 kV) | drift 17-23 cm/side (200 kV/m hits plates at 27.6 cm) | fixed
I3 R2 | self-excitation current balance | 0.4-1.4 uA per m width vs 10 uA leak at 1e10 ohm -> need >=5e10 ohm per 10 m channel | conditional
I3 R3 | space charge -> alternating-polarity stack, 0.5 m pitch | 0.17-0.50 t/h/m -> 1,730-5,250 m width for 1 Mt/yr (170-525 channels of 10 m) | sizing, not fatal
I3 R4 | closed air loop via -30 C outdoor cold trap + genset waste heat | 2% RH; ore ice 0.2-0.4%: 9-19 MJ/t (mill heat 21-31); 1%: 47; 3%: 140 MJ/t (> waste heat 97) | OK to ~2% ice
I3 R5 | cascade vs split | 85/45: 8 st, 6.2%, 82%, 6.5x load; 80/50: 22 st, 6.0%, 75%, 22.8x; 75/55: impossible | split decides
I3 R6 | cost per t Li2O recovered | cascade $4,100-4,960 vs XRT+DMS $6,430-7,390, DMS+flot $7,400-8,270, raw haul $8,750 | NICHE 1.3-1.8x
I4 R1 | sub-eutectic CaCl2 with heat pump to -40/-45 C air | 5.5-15 MWh/t LCE ($275-1,500 power only), 450-910 t brine/t LCE, residue still ~30% CaCl2 | anchor FAILS
I4 R2 | niche: RO first (37 bar at 6 g/L), freeze only 6->20 g/L | 23.8 m3 water/t LCE (vs 188-626) | volume cut 8-26x
I4 R3 | spray-freeze 2 stages + drainage + fractional melt (Alberta data) | product 20.6 g/L (Tf -14 C), 53% Li/pass, late melt <=1.1 g/L to RO feed, 62 t ice/t LCE | works on paper
I4 R4 | cost vs MVR | $110-240/t LCE vs MVR $470-1,085 (2-4x on step, 5-15% of route); storage 0.37 Mm3 | NICHE without anchor

## Consistency checks (rate x duration vs window)
I1: CO >=0.032% for 50 C vs dose 0.05% OK | discharge temp <=50 C (aftercoolers) REQUIRED | sat at -20 C 61% OK | slip 0.09 ppb vs PEL 1 ppb OK | purge 72 h vs planned-repair notice (days) OK | rupture inventory 12.3 t vs IDLH volume 8.8e8 m3 FAIL (residual) | Fe(CO)5 favoured at pCO 0.088 bar UNKNOWN rate | no Ni source on line FAIL (site)
I2: n-butane 0.30-0.97 bar vacuum (air-ingress) RISK | Tf path mean -0.8 C, final -11..-32 C vs air -25..-45 C OK at 80%, FAIL at 90% | Mg <=0.39-0.73 g/L feed REQUIRED | draft 47-52 Pa vs coil 40-60 Pa OK only <= -25 C air | coldest 1,500 h at Chara mean -33.8 C (est. from monthly means, sd 5-8 K) | pond 1.2-5 Mm3 per 10 kt Cu RISK
I3: 150 kV/m vs breakdown 3 MV/m (5%) OK | drift 17-23 cm vs half-gap 25 cm OK | charge current vs leak needs R>=5e10 ohm UNKNOWN | counterfield <=10-30% sets 0.17-0.5 t/h/m | RH 2% from trap at -30 C OK | ore ice <=2% vs heat 97 MJ/t OK, 3% FAIL | split 85/45 needed (80/50 marginal) UNKNOWN
I4: eutectic -50 C vs Udachny ~273 h <=-45 C FAIL | product Tf -14 C needs air <=-26 C: Udachny Dec-Feb means -35..-39 OK, Chara marginal | RO 37 bar at 6 g/L vs 70-80 bar limit OK | storage 0.37 Mm3 over 7 months RISK | partition data are wastewater (NaCl) not LiCl UNKNOWN
