# BSM exploration inside this chat

Status: first implementation, 2026-11-03. This chat coordinates native specialist subagents. Research records and executable calculations live in the repository. No external research framework, SDK service, separate agent process, or API key is required by the record helper.

## Scientific scope and identities

Start with four-dimensional, weakly coupled, nonsupersymmetric gauge theories with elementary scalars. An exploration is a bounded research attempt; a campaign groups related attempts. A physical candidate can have multiple revisions, scalar completions, and investigations. Keep those identities separate.

The first campaign is a known SU(5) benchmark. It tests the workflow and calculations, not novelty or complete phenomenological viability. The electroweak Higgs and realistic Yukawa sector are deferred.

## How the agents run

The user and this chat choose the question, search bounds, and available tools. The main assistant acts as coordinator: it creates the record, delegates work using native subagent tools, checks handoffs, reruns calculations, and writes the combined report.

1. **Explorer:** specify the gauge algebra/group, SM embedding, hypercharge convention, fermion irreps, full branchings, chirality, anomaly contributions, and unresolved questions.
2. **Vacuum investigator:** consume that exact candidate revision, construct scalar invariants and a potential, compute stabilizers and extrema, investigate stability and spectra, and return specific obstacles or useful follow-ups.

Each is a real tool-using subagent, with its own task context and access subject to the chat's tools and permissions. A role brief is supplied explicitly; merely saving a Markdown file does not register or launch an agent. We use the current model configuration without assuming a fixed model name.

```text
User <-> coordinator in this chat
             | creates attempt and assigns exact prompts
             v
          explorer -> saved candidate + evidence
                            | explicit versioned handoff
                            v
                          vacuum -> saved completion + evidence
                            |
                            v
                   coordinator verification -> report
```

Independent preparations can run concurrently; candidate-dependent conclusions wait for the handoff. Agents own separate scripts and outputs. The coordinator owns shared manifest edits and catalogue promotion. There is no autonomous scheduler: work runs when this chat is active. File recovery can reconstruct a new task after interruption; it does not promise exact restoration of private subagent context.

## Persistent record

`tools/records.py` is a Python standard-library helper. It creates a new attempt directory and snapshots the campaign, role briefs, design, helper, root guidance, and README. It records the base Git revision and a patch of tracked changes; explicit snapshots preserve selected untracked inputs. Later-written calculation code is retained and hashed at sealing.

The append-only JSONL journal is authoritative for lifecycle state. Its states are running, interrupted, completed, and failed. An interrupted attempt can resume with an explicit event; revised scientific investigations should use a new attempt ID and parent link. Events are flushed and protected with a local advisory file lock. A process crash during a write may leave a damaged final line; parsing will fail visibly rather than silently dropping it. This is a local evidence helper, not a transactional distributed runtime.

The command recorder executes argument arrays without a shell, applies a per-command timeout, and stores the command, return code, stdout, and stderr. It runs in the attempt directory and inherits the caller's OS permissions; it adds no sandbox. It does not intercept every tool call, enforce campaign-wide budgets, or supervise the subagents. Long or interrupted commands can leave a started event without a finished event; inspect those before resuming.

After review, mark an attempt completed or failed, then seal it. Sealing inventories files with SHA-256 hashes; verification detects modified, missing, and added files. Hashes detect accidental changes, not scientific correctness or tampering by someone who can rewrite the inventory.

## Logging coverage

Save exact delegated prompts, assigned agent IDs when available, explicit input files and revisions, concise responses/reports, calculations, command outputs, sources, check records, handoffs, and coordinator decisions. Native chat tools do not provide a general automatic full-transcript export here. This implementation therefore does not claim to archive every agent message, every web/tool invocation, private reasoning, or authoritative token/cost totals. Such fields remain unknown where unavailable.

A clean checkout should reproduce the calculations from saved code and inputs without needing a live subagent. Session IDs are convenience references, not the research record. Retain failed and inconclusive attempts. Avoid credentials in prompts, journals, or exported outputs. Large artifacts can later use external storage with hashes and retrieval locations; initial records remain small enough for Git.

## Scientific evidence rules

For every check use `pass`, `fail`, `unknown`, or `not_applicable`, with statement, scope, assumptions, approximation, evidence paths, and limitations. Execution completion and scientific success are separate.

- Correct SM multiplets must have the intended net chirality, rational hypercharges, and multiplicities. Their presence alone is insufficient.
- Local anomaly cancellation, applicable global anomaly checks, and global-group qualifications are separate questions.
- An SM-singlet scalar direction, its exact stabilizer, stationarity, boundedness, local stability, and global minimality are separate claims.
- Include scalar/gauge spectra and actual mass-generating interactions before claiming the desired low-energy theory.
- Distinguish a single parameter point from an open viable region, and tree-level conclusions from loop-corrected ones.
- A neutral state does not establish dark matter viability; an allowed operator does not establish its UV generation or neutrino mass rank.
- Missing tools, timeouts, or exhaustion of scalar bounds are inconclusive rather than general no-go results.

## First benchmark and expansion

`campaigns/su5-benchmark.json` fixes three copies of 10 plus conjugate 5 and a real adjoint scalar. The explorer derives exact branching and anomalies. The vacuum investigator studies the SM-preserving adjoint direction and an SU(4)-preserving control. The coordinator reruns the scripts and reviews the supported vacuum claim.

The generic helper's interruption/resume and artifact verification are tested locally. This does not test restoration of a live Codex subagent after an app restart. A future continuation should read the last report, journal, manifest, and handoff, then create replacement subagents with those files.

Expand only after reviewing this benchmark: a small bounded set of embeddings, multiple scalar completions, then neutrino and dark matter tasks. Existing tools such as SuperFlocci, LieART, and Sym2Int can later supply general algebra calculations; this benchmark's scripts are narrow independent calculations, not replacements for those packages. Preserve separate feasibility, novelty, complexity, and phenomenological criteria rather than one opaque score.

## References

- [Official subagent documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [SuperFlocci](https://arxiv.org/abs/2306.16439)
- [LieART](https://arxiv.org/abs/1912.10969)
- [Sym2Int](https://arxiv.org/abs/1703.05221)
