I worked out each mechanism first and picked the names afterward.

=== IDEAS ===
IDEA 1
NAME: Conserved Flow Pipe Lattice
MECHANISM: A fixed lattice of cells each holds a fluid level. Each link between neighboring cells holds a width, and the widths are the only thing the system stores. Input pours amounts into entry cells, and fluid moves along each link at a rate of width times level difference until nothing changes; the answer is how much has pooled in each outlet cell. To learn, each outlet's shortfall is poured in (and any excess drawn out) as a second settling run. Each width then changes by its forward flow times its second-run flow, is clipped at zero, and loses a small fixed amount.
DIFFERENCE: Every answer is an exact redistribution of the input amount, so it can report precisely which part of the input ended up in which output, and it can never produce output with nothing behind it.

IDEA 2
NAME: Bankruptcy-Pruned Trader Population
MECHANISM: Each trader stores a cash balance, an asking price and a tiny rule that turns a few purchased numbers into one output number. At each step, traders buy other traders' outputs at their asking prices, compute, and sell their own output. The environment pays only the final seller, and only when the answer is correct, while every trader pays rent for each input it buys. A trader whose cash drops below zero is deleted. A trader whose cash goes above a threshold splits in two, each half taking half the cash, and the copy's rule is randomly perturbed. Prices rise when buyers compete and fall when nothing sells.
DIFFERENCE: It grows, prunes and rewires itself continuously while it runs, driven by a single payoff number with no global derivative pass, so its size is set by what its computation earns rather than fixed in advance.

IDEA 3
NAME: Stored-Edit Chaining Solver
MECHANISM: It stores solved cases as (input, answer) pairs, plus edit records. Each edit record pairs an input change with the answer change seen between two similar solved cases, and keeps a success count. To answer a new input, it finds a solved case and a chain of at most three records whose input changes turn that case's input into the new one. It then applies the matching answer changes to the case's answer. When the true answer arrives, each record that was used gains or loses count, records whose count falls below zero are deleted, records that keep appearing together are fused into one, and the new case adds fresh records against the closest stored cases.
DIFFERENCE: It can answer inputs far from anything it has seen by chaining relative edits from a known case, and every answer is a derivation that can be replayed and corrected by deleting one record.