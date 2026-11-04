# SU(5) chat-native benchmark: reviewed result

Attempt: 2026-11-03-su5-001. Candidate: su5 r1. This is a known-model reproducibility benchmark, not a new BSM theory or a claim of full phenomenological viability.

## Outcome

The chat-native workflow produced a frozen candidate, two specialist-authored calculation scripts, recorded command executions, explicit scientific check records, and reproducible outputs. Both native specialist sessions stopped with usage-limit errors before completing their reports. The coordinator continued from saved files, strengthened the vacuum handoff validation, completed the missing reports/checks, and verified both calculations. This is a demonstrated file-based recovery of scientific work, not a successful resumption of the interrupted specialist contexts.

## Established physics within scope

The exact weight calculation reproduces 10+5bar -> Q+u^c+e^c+d^c+L, with conventional rational hypercharges, no additional fermions, and three net chiral generations (45 Weyl components). The local SU(5) cubic and SM gauge/mixed gravitational anomaly sums cancel. Twelve weak doublets satisfy the ordinary SU(2) Witten parity test on spin spacetime. The block subgroup is globally S(U(3)xU(2)), or (SU(3)xSU(2)xU(1))/Z6.

For a real adjoint Sigma, the vacuum investigator constructed

V=-m^2 Tr(Sigma^2)/2+a(Tr(Sigma^2))^2/4+b Tr(Sigma^4)/2,

with the cubic coefficient set to zero. At a=b=v=1, m^2=44, the target v diag(2,2,2,-3,-3) is stationary, and the potential is bounded below in the sufficient region a>0,b>0. The full 24-direction rational Hessian with the kinetic metric gives scalar mass squares:

| Sector | Multiplicity | Mass squared at the benchmark point |
|---|---:|---:|
| Gauge Goldstone directions | 12 | 0 |
| Color octet | 8 | 5 |
| Weak triplet | 3 | 20 |
| Radial singlet | 1 | 44 |

Thus the point is locally stable modulo gauge orbits in the cubic-free tree-level scalar sector. The target stabilizer has twelve generators and the SM gauge algebra. The control diag(1,1,1,1,-4) leaves sixteen generators and su(4)+u(1), correctly failing the SM-stabilizer check.

## Verification

- Seven infrastructure tests passed: immutable attempt creation/input snapshots, cross-process interruption/resume, concurrent journal writers, failed and timed-out commands with retained outputs, unfinished-command protection, artifact tamper detection, and visible failure on a truncated journal.
- code/review.py reproduces both calculation outputs in a fresh temporary directory.
- It checks all 24 diagonal and 276 mixed scalar Hessian entries by independent exact full-matrix polynomial evaluation of V(D+tX), rather than reusing the Hessian formula.
- All fourteen scientific check records have the required fields and existing evidence paths. Nine pass, one intentionally fails for the negative control, and four remain unknown.

The independent calculation checks passed. This does not turn the unknown scientific questions into passes.

## Unresolved questions

Global minimality, a complete global anomaly classification, realistic electroweak/Yukawa completion, and full phenomenological viability remain unknown. The cubic-free restriction, tree-level approximation, absence of right-handed neutrinos, and deferred neutrino/dark-matter questions are explicit. No general Lie-algebra search backend or autonomous scheduler was implemented.

## Reproduction

From the repository root, validate the saved archive:

```sh
python3 research/tools/records.py --run research/runs/2026-11-03-su5-001 verify
python3 -m unittest discover -s research/tests
```

For a fresh calculation, copy code/ and candidates/ from this attempt to a temporary directory, create artifacts/ there, and run code/explorer.py followed by code/vacuum.py from that directory. Run the original code/review.py to perform an automatic fresh-directory check. Do not modify the archived attempt; create a parent-linked follow-up for new physics work.

## Where evidence lives

- candidates/su5-r1.json: frozen embedding and matter handoff.
- sessions/explorer/prompt.txt and sessions/vacuum/prompt.txt: exact assignments.
- sessions/*/report.md: coordinator-completed role reports, with authorship stated.
- code/: specialist calculations and coordinator verification.
- artifacts/: structured computed outputs.
- checks/: per-claim statuses, assumptions and evidence references.
- commands/: recorded argv, timestamps, return codes and stdout/stderr.
- manifest.json and events.jsonl: provenance, handoff and interruption history.
- sources.json: inspected references and their use.

The archive covers explicit assignments, reports, recorded calculations and coordinator decisions. It does not automatically contain every native chat message, every tool invocation, private reasoning, or authoritative per-agent usage/cost totals.

## Next bounded investigation

Review the benchmark conventions and choose a small set of embeddings/scalar bounds. One useful immediate extension is to restore the adjoint cubic invariant and map which parameter regions retain a locally stable SM-preserving vacuum. Another is to add the electroweak 5 and test its couplings, mass splitting and vacuum alignment. Neither has been carried out in this attempt.
