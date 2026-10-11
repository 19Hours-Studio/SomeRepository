Paradigm: Mainstream AI learns one frozen input-to-output map by repeatedly nudging fixed parameters to shrink an error averaged over a static dataset, then applies that map statelessly to every new input.

Forbidden: the whole paradigm, meaning any system whose behaviour is a frozen map fitted to data by error-driven parameter nudging and applied without carried state. Families A to G, and their re-skins and recombinations, are also excluded.

Fields: Idea 1 uses MSC 26 (Lipschitz functions), Idea 2 uses MSC 49 (Pontryagin adjoint equations), and Idea 3 uses MSC 60 (coupling and hitting times).

=== IDEAS ===
IDEA 1
NAME: Lipschitz bands over a dial
MECHANISM: The system keeps a finite list of pairs (θᵢ, yᵢ), where θᵢ is a position on a chosen dial such as premise strength and yᵢ is the real judgment given there. Given a declared maximum rate L at which judgments may change along that dial, any unasked position θ gets the interval from max over i of (yᵢ − L|θ − θᵢ|) up to min over i of (yᵢ + L|θ − θᵢ|). Each new pair intersects the existing intervals, so bands only narrow as more is asked, and the output is the band itself.
DIFFERENCE: It returns the exact range of answers still consistent with a stated rate of change at any unasked setting of a question, a band no current architecture produces.

IDEA 2
NAME: Future-target shadow price path
MECHANISM: The system carries a vector of real present quantities x(t) on a virtual time axis from now (t=0) to a horizon T, moved by ẋ = f(x,u) under bounded levers u(t) that it sets. It minimizes the integral of L(x,u) over [0,T] plus a terminal penalty Φ(x(T)) tied to a chosen target. The adjoint p(t) runs backward from p(T) = ∂Φ/∂x, and the lever at each moment maximizes p·f − L, so the stored state is the paired path (x, p) and the output p(0) is one price per present quantity. Dynamics f and cost L are revised by adding the observed-minus-predicted path discrepancy as a forcing term.
DIFFERENCE: It states the exact exchange rate between every present quantity and a far-future target as a continuous price path, a trade-off report no current architecture gives.

IDEA 3
NAME: Premise convergence-time distribution
MECHANISM: Reasoning is a finite-state chain of stances with a fixed transition rule F(s, u), where u is drawn from one shared random seed sequence. For any two premises, the system starts two copies at their stance states and feeds both the same seed, so the copies first coincide at a random time τ (possibly infinite) and stay together after that. It stores a table over pairs of stances and computes the full law of τ by recursion on that table. It adapts by counting observed stance transitions to refine F and the seed distribution.
DIFFERENCE: It reports, for any two premises, the probability distribution of the step after which their conclusions are identical under shared randomness, a convergence-time object no current architecture computes.