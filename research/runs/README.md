# Exploration records

Each attempt has a unique directory. The coordinator creates it, saves exact specialist prompts, delegates through the chat, records handoffs, and reviews results. Use a new attempt with a parent link for a revised scientific investigation. A candidate ID is separate from an attempt ID.

```text
research/runs/<attempt-id>/
  manifest.json         # Inputs, source revision, runtime and logging coverage
  events.jsonl          # Append-only lifecycle, handoffs and explicit decisions
  inputs/               # Campaign, briefs and infrastructure snapshots
  sessions/<role>/      # Exact task prompt and specialist report
  candidates/           # Versioned candidate handoffs
  checks/               # Structured individual scientific checks
  code/                 # Reproducible calculations
  commands/<id>/        # argv, cwd, timeout, stdout, stderr and execution result
  artifacts/            # Generated calculation outputs
  report.md             # Combined reviewed results and next questions
  artifacts.json        # File hashes after sealing
```

Run these commands from the repository root, replacing the attempt name:

```sh
python3 research/tools/records.py --run research/runs/my-attempt init --campaign research/campaigns/su5-benchmark.json
python3 research/tools/records.py --run research/runs/my-attempt status
python3 research/tools/records.py --run research/runs/my-attempt exec --actor explorer --timeout 60 -- python3 code/explorer.py
python3 research/tools/records.py --run research/runs/my-attempt event --type run_interrupted --payload '{"reason":"continue later"}'
python3 research/tools/records.py --run research/runs/my-attempt event --type run_resumed
python3 research/tools/records.py --run research/runs/my-attempt event --type run_completed
python3 research/tools/records.py --run research/runs/my-attempt seal
python3 research/tools/records.py --run research/runs/my-attempt verify
```

Only mark an attempt completed after all intended work has been reviewed and active commands have ended. Do not edit sealed attempts. The helper rejects lifecycle transitions out of completed/failed states; corrections require another attempt. The manifest is provenance; `status` derives the current execution state from the journal. `run_completed` says execution finished, not that the theory is viable.

Each event has an ID, sequence, UTC timestamp, actor, type, and JSON payload. Supported lifecycle events are `run_created`, `run_interrupted`, `run_resumed`, `run_completed`, and `run_failed`. Other event types describe assignments, handoffs, commands, and review. File locking protects cooperating journal writers; workers use separate output files.

Each scientific check should name `check_id`, `candidate_id`, `candidate_revision`, `status`, `statement`, `scope`, `assumptions`, `approximation`, `evidence_paths`, and `limitations`. Allowed statuses are `pass`, `fail`, `unknown`, and `not_applicable`. Paths are relative to the attempt directory. Software assertions and checks must be interpreted within their stated scope.

The journal and saved reports are an explicit research log. They are not an automatic full export of native subagent conversations or every tool invocation. Use the command recorder for calculations; save sources and concise reports for other work. Record missing provenance honestly. Private reasoning and unavailable per-agent cost totals are not part of the archive.

The helper uses no external Python packages and runs on the local macOS/Linux filesystem. Tests: `python3 -m unittest discover -s research/tests`. After interruption, inspect the journal and any command with a start but no finish record, then have this chat reconstruct the next task from the saved files. This preserves scientific work without promising exact restoration of a live agent context.
