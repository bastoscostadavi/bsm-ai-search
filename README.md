# BSM AI Search

BSM AI Search explores how AI can help search the space of theories beyond the Standard Model (BSM) at scale, including complex constructions that may address several outstanding problems in particle physics together. Its approach uses AI models and scientific software to propose theories, derive their consequences, compute predictions, and compare them with experimental observations, following the workflow of BSM physicists.

[bsm-atlas](https://github.com/bastoscostadavi/bsm-atlas) provides a structured, source-backed resource of BSM theories and their defining papers to support this exploration. The complementary [bsm-foundation-model](https://github.com/bastoscostadavi/bsm-foundation-model) project explores learning the inverse direction: training neural networks on simulated datasets to infer probability distributions over candidate theories and their parameters from experimental observations. Both approaches can use the atlas and contribute to the broader goal of AI-assisted BSM discovery.

For a proposed model that satisfies all current experimental constraints and theoretical consistency requirements, including anomaly cancellation, the atlas would serve two important roles:

1. **Novelty:** A standard notation for model entries would make it possible to compare a proposal directly with catalogued models and immediately check whether it is new relative to the atlas.
2. **Interestingness:** Assessing how well the proposed model addresses current open problems in particle physics would provide a direct measure of its scientific interest.

## Research workflow

Research runs inside this chat, with native tool-using explorer and vacuum subagents. The repository stores the questions, role briefs, candidate handoffs, calculation code, check results, and exploration history.

- [Architecture and implementation limits](research/DESIGN.md)
- [Explorer brief](research/agents/explorer.md) and [vacuum investigator brief](research/agents/vacuum.md)
- [SU(5) benchmark](research/campaigns/su5-benchmark.json)
- [Record commands and run history](research/runs/README.md)

The Python standard-library record helper creates attempts, journals events, captures calculation commands, and hashes completed records. Agent delegation is performed by the active chat; the helper is not an autonomous agent launcher. See the design for logging coverage and recovery limits.

The [first reviewed SU(5) benchmark](research/runs/2026-11-03-su5-001/report.md) demonstrates the record workflow and exact calculations, including recovery from interrupted specialist sessions. It establishes a locally stable tree-level adjoint vacuum within its stated scope; global minimality and complete model viability remain unresolved.
