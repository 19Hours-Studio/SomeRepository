# rt_b repair log (one line per round: idea | change | decisive number | result)
Sources used (search summaries; WebFetch not used): Shao & Lu 2000 threshold formula (A_N=0.0123, gamma 1.65-5e-4); Douglas et al. 2023 JGR-ES "Ablation-limited erosion rates of permafrost riverbanks" (erosion linear in water T, ~3x smooth-wall theory when sediment is carried away; natural banks slower); Majhi et al. 2007 Kolyma streamflow (Srednekolymsk Nov-Apr flow +130..268 m3/s, +43..454 %, 1720 km below dam); BLM/USBM Koyukuk prefeasibility (surface placer required value $4.23-18.43 per loose yd3); kuzstu 2023 (sluice optimum ~3 m3 water/m3 sand); Obogashchenie Rud 2019 Langeri sluice (fine-gold losses 40-50 %); Froehlich breach formula; WA dry-blowing ~80 % recovery (forum, weak). Everything else tagged [A] in calc_*.py.

I1 R1 | original flat harrowed field, Tiksi climate, hourly energy balance | flat E = 0.04-0.05 kg/m2/d (Mar), 0.26-0.31 (Apr 1-20); surface > -2 C from ~Apr 21 | snow+liquid-water window real; only Mar15-Apr20 usable
I1 R2 | 37 deg south faces of autumn-drained pay windrows (snow-shedding, self-clearing face, 2.6x irradiance) | face E 0.08-0.13 (Mar), 0.41-0.67 (Apr); 0.5 mm skin halves E, 3 mm lag cuts 6x; season 5.2 kg/m2 | retreat only 0.02-0.09 m/season
I1 R3 | lower pore ice (drained windrow 0.06) | 100,000 m3 needs 213 km of 3 m ridges (4.7 km2) or 0.91 km2 flat field raked daily | area/handling explode
I1 R4 | sorting: keep saltation fraction on site (inter-ridge trough trap), only suspension leaves | suspended: quartz <63-97 um, gold <23-35 um; extra gold loss vs sluice 0-0.4 % | sorting defect fixed (no 5 % threshold gap needed)
I1 R5 | cost per g (0.7 g/m3, 85 % rec) | idea $4.4-12.1/m3 = $7.4-20.3/g vs baseline wash $1.7-6.0/m3 = $2.9-10.1/g | FAILS at scale (0.5x); niche only
I2 R1 | original 1-2 mm film over 40-100 m face | tau 10 Pa, clears <14 mm | debris coat confirmed
I2 R2 | concentrate flow into a toe channel along the face (niche undercut, block fall) | 47 L/s, 0.6 m, S 0.05: tau 30 Pa, clasts <42 mm; 100 L/s S 0.08: 57 Pa, <78 mm; heat e-fold length 10-31 m | self-dosing kept, oversize removed by grizzly+loader
I2 R3 | drop water-retaining role of ore pile; lined 0.7-1.5 ha solar pond (0.4 m) pre-heats creek +4-6 K | feed 4 C creek 54,500 m3/season; 9 C pond 123,000 m3 | defect 3 fixed by pond
I2 R4 | fixed weir bypass keeps chute >= 4 m3/m3 | face ratio 12.1 (2 K) .. 2.4 (10 K) | in band
I2 R5 | breach: pond V 4,000 m3, H 1.5 m | Qp 128 -> 11.6 m3/s (Froehlich) | hazard reduced, not zero
I2 R6 | per gram, underground placer total $40-80/m3 [A] | 1.03-1.13x cheaper per g | NICHE
I3 R1 | ice never reaches floor (gap >= 0.3 m in 99 % winters); only boulders >1.2 m left standing on mined floor are gripped | plowed ice 1.8+-0.08 m, depth 2.12 m, P(grip, protrusion >=1.2 m)=1.00; no matrix capture | defects 1,2,3 fixed
I3 R2 | lift/grip | net lift 101-126 kg/m2 (plowed) vs -4..21 unplowed; D 1.5 m boulder needs 21-31 m2 floe; adfreeze grip margin 1.6-4.9x (D 1.5), 0.6-1.8x (D 2.5) | works to D ~2 m
I3 R3 | economics vs secondary blasting of oversize only | saving $0.02-0.28 per m3 pay = 0.04-2.5 % of total; delay NPV 0.65 % | NICHE
I4 R1 | trim window vs shell melt with HDPE top skid mu 0.15 | Bmax 90-404 kg; loss 3.7/11/18.4 kg/d at +0.01/+0.03/+0.05 K | trip length capped
I4 R2 | rigid shell is essential (flexible bag: 0.7 m draft change = 390 kg) | keep ice shell 7-13 cm; fill in autumn at -4 C (cold reserve +10 kg vs +65) | soak/slot defect removed
I4 R3 | low pod 1.2 m tall (CdA 6.6) | U 0.3: 256-428 km at +0.05/+0.03 K; U 0.2: 76-127 km | short routes only
I4 R4 | route Zyryanka->Srednekolymsk (1,400+ km below Kolyma HPP polynya), early winter (ice 0.6-1.0 m) | late-winter Q ~327 m3/s -> U 0.18-0.33; depth need 1.75-2.1 m | riffle depth unknown
I4 R5 | economics vs winter road on same ice / barge+stockpile | pod $10-20/t vs road $39/t (1.9-3.9x), barge $12-37/t (0.6-3.7x) | NICHE / unproven
