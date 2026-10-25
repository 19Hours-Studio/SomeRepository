# LOG — rusres2__p3 repair (scripts in calc/)
Prices base Ni 16k, Cu 10.5k $/t, Pd 1300, Pt 1800 $/oz (Legor May-2026 snapshot higher = P_hi); 85 RUB/$; 12% real, 20 y CRF. Group 2024 output from memory (Ni 205.6 kt, Cu 433 kt, Pd 2.77 Moz, Pt 0.66 Moz) -> 789 kt Ni-eq; opex 5.1 bn$ (F62) + capex at 37% -> ~10,260 $/t Ni-eq full cost (base.py). Gross 12.6 bn$ ≈ reported revenue, so this checks out.
Recoveries: NOF Ni 71.9/71.3/70.6% (2018-20), TOF 83.2->87.9% (Nornickel AR2020 via search). Cu/PGM recoveries are ASSUMED.

| round | idea | change | decisive number | result |
|---|---|---|---|---|
| 1 | I1 | Ni-eq valued with PGM (base.py) | Maslovskoye 2.66% Ni-eq ≈ Talnakh avg 2.67%, Norilsk-1 1.70%; PGM = 73-76% of value of N1/Masl | "600k RUB/t Ni" framing for Masl is wrong: Ni is 11% of its value |
| 2 | I1 | pair model, defer credit (idea1.py) | credit can exceed capex -> negative ratios | model ill-posed, rebuilt |
| 3 | I1 | full incremental cost per t Ni-eq for alone / pair / Nornickel plan (idea1b.py) | pair 6,826 vs plan 7,894 $/t (0.88 median, 0.76-1.00 range); break-even NOF life-ext = 90 bn RUB | WORKS vs plan, small at group level (~1%) |
| 4 | I1 | regime: Talnakh mines add no new ore | TOF-3 alone 26,794 $/t (6.2 kt/yr), pair 9,664, plan 11,840 | anchor strongest here: gate cuts step cost 2.8x |
| 5 | I1 | XRT as gated option once NOF is full (idea1c.py) | +6.9-12.7 kt/yr at 7,400-10,200 $/t (98% metal); 95% metal -> 10,700-20,500 $/t | XRT is demoted to an option; needs >=97% metal recovery |
| 6 | I1 | NOF pile life check (approx SP 25.13330 adfreeze) | 1 cm/yr thaw alone -> -2.3% capacity by 2050; ground warming 0.02-0.05 K/yr -> -14..-62% | life extension is decided by borehole ground-T forecast + defect closure, not thaw depth |
| 7 | I2 | Poisson pooling, 6 mines, 9-mo lead (idea2.py) | pooled stock 46-62% of separate; same budget 80% -> 99.5% fill | pooling is strong under long lead times |
| 8 | I2 | rank by Ni-eq: rich vs N1 fleets | rich-ore LHD-hour 6.3 t Ni-eq vs 1.2 (5.2x) | targeting is the anchor's lever |
| 9 | I2 | first availability model (idea2.py) | penalty mis-specified -> zeros | rebuilt |
| 10 | I2 | downtime split model (idea2b.py) | +7.3 pp, +28.6 kt/yr (3.6%), 2,730 $/t added; group full cost -2.6%; break-even domestic part life 0.30x OEM; targeting x1.71 | WORKS as cheapest increment, not as 1.5x cut |
