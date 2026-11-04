# BSM research workflow

For a research exploration, use this chat as coordinator and delegate the gauge/matter and scalar/vacuum tasks to separate tool-using subagents when those roles are needed. Follow `research/DESIGN.md` and the briefs in `research/agents/`. Infrastructure-only changes do not require specialist agents.

Create an attempt with `research/tools/records.py` before delegating. Save exact task prompts, input revisions, explicit derivations, code, command outputs, check records, sources, and reports. Give each specialist separate owned files; the coordinator owns the manifest and shared journal. Use the recording helper for calculation commands. Native subagent activity is not automatically exported as a complete transcript; record coverage honestly.

Use exact charges and weights when feasible. Distinguish `pass`, `fail`, `unknown`, and `not_applicable` for scientific checks. A timeout, missing tool, or bounded unsuccessful search is not a physical exclusion. Preserve rejected attempts and approximation assumptions. Do not claim realistic models or novelty from this benchmark alone.

Use Python standard-library tools for the initial record infrastructure. Run `python3 -m unittest discover -s research/tests` after changing that infrastructure. Do not launch external agent processes, install frameworks, or publish results as part of the chat workflow.
