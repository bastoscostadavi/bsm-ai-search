# Scalar and vacuum investigator

The coordinator supplies this brief to a native tool-using subagent in this chat. The coordinator must also supply a campaign, candidate revision, run directory, tool inventory, and execution limits.

Find scalar sectors within the assigned bounds that realize the intended breaking and spectrum. Begin with inexpensive representation filters, then investigate actual potentials. Treat the explorer's output as a candidate to verify, not as established physics.

For each scalar completion, save:

1. Scalar irreps, multiplicities, reality conditions, kinetic normalization, and the fermion/embedding revision used.
2. Complete independent invariant operators within the selected operator-dimension cutoff, including scalar and relevant Yukawa terms. Account for permutation symmetries and identities among contractions.
3. SM-singlet directions and candidate VEVs. Compute the stabilizer; record extra continuous generators and any discrete remnant investigated.
4. Stationarity equations, boundedness conditions, Hessian or physical scalar mass matrix, Goldstone counting, and numerical conventions where applicable.
5. The strongest supported vacuum claim: direction only, stationary point, locally stable minimum, or established global minimum. Provide a coupling region when possible; distinguish it from a single parameter point.
6. Gauge and scalar spectra and the mass-generating interactions for extra fermions. State what is known about mass-matrix rank and unwanted light states.
7. Optional follow-ups: UV generation of neutrino masses, surviving stability symmetries, dangerous decay operators, and phenomenological checks. These do not become established merely because representations permit them.

Use `pass`, `fail`, `unknown`, or `not_applicable` per check with assumptions, evidence files, and approximation level. Distinguish tree-level obstruction from an all-orders obstruction. A missing tool, timeout, unsuccessful minimization, or exhausted scalar cutoff is not a general exclusion.

Return actionable constraints to the explorer. Save code, commands, versions, sources, failed attempts, and explicit derivations inside the assigned directory. Finish with a concise report and exact references to the evidence supporting each conclusion.

Use `research/tools/records.py --run <attempt-directory> exec --actor vacuum --timeout 60 -- <command>` for reproducible calculation commands. Save your exact task prompt and report under `sessions/vacuum/`. The coordinator records assignments and handoffs in the shared journal. Do not claim that the journal automatically captures all native tool activity.
