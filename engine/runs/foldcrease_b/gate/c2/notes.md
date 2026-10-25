# Gate c2 notes (arithmetic in gate_calc.py, output in gate_calc_out.txt)
- Known-answer checks: D(UTG 30um)=1.68e-4 N*m (idea4 states 1.6e-4); bonded t/2R for 160um at R=2mm = 4% (idea2 states 4%).
- Ideas 1/2: layers are bonded at both ends of the zone, so every layer has the same free length. The fluid carries no shear,
  so the layers cannot slide past each other to relieve the mismatch. A length mismatch above the clamped Euler strain
  pi^2 t^2/(3L^2) buckles the layer. Thermal mismatch (dCTE 1-3.5 ppm/K x 40 K) is 7-24x that strain for 20um PI.
  Folding adds a membrane mismatch of pi*d/L: 0.63% (idea1) and 1.41% per interface (idea2).
- Ideas 3/4: residual ratio = Dk^2/(Dk^2+T), k=pi/3mm. Lower bound for stack D (layers not coupled) = 3.9e-4 N*m.
- Best current practice measured: iPhone Duo 48um new -> 167um after 3000 folds (HTX Studio via ithinkdiff).
