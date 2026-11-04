#!/usr/bin/env python3
"""Local evidence records for chat-coordinated research. Does not launch agents."""
import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import uuid


ROOT = Path(__file__).resolve().parents[2]
TRANSITIONS = {
    "run_created": ({None}, "running"),
    "run_interrupted": ({"running"}, "interrupted"),
    "run_resumed": ({"interrupted"}, "running"),
    "run_completed": ({"running"}, "completed"),
    "run_failed": ({"running", "interrupted"}, "failed"),
}


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2) + "\n")


def read_events(run):
    return [json.loads(line) for line in (run / "events.jsonl").read_text().splitlines()]


def state(events):
    current = None
    for event in events:
        if event["event_type"] in TRANSITIONS:
            allowed, target = TRANSITIONS[event["event_type"]]
            if current not in allowed:
                raise ValueError("invalid lifecycle transition in journal")
            current = target
    return current


@contextmanager
def locked(run):
    # The run must already exist; never silently create a mistyped run path.
    with (run / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def append_unlocked(run, actor, kind, payload):
    events = read_events(run)
    current = state(events)
    if kind in TRANSITIONS:
        allowed, _ = TRANSITIONS[kind]
        if current not in allowed:
            raise ValueError(f"cannot apply {kind} to {current}")
        if kind in {"run_interrupted", "run_completed", "run_failed"}:
            started = {e["payload"]["command_id"] for e in events if e["event_type"] == "command_started"}
            finished = {e["payload"]["command_id"] for e in events if e["event_type"] == "command_finished"}
            if started - finished:
                raise ValueError("unfinished commands must be inspected and resolved before closing or interrupting the attempt")
    elif current != "running":
        raise ValueError(f"cannot append research events to {current} run")
    event = {
        "schema_version": "0.2", "event_id": str(uuid.uuid4()),
        "run_id": json.loads((run / "manifest.json").read_text())["run_id"],
        "sequence": len(events) + 1, "timestamp_utc": now(),
        "actor": actor, "event_type": kind, "payload": payload,
    }
    with (run / "events.jsonl").open("a") as stream:
        stream.write(json.dumps(event) + "\n")
        stream.flush()
        os.fsync(stream.fileno())
    return event


def append(run, actor, kind, payload):
    with locked(run):
        return append_unlocked(run, actor, kind, payload)


def initialize(run, campaign_path, parents):
    campaign = json.loads(campaign_path.read_text())
    if not campaign.get("campaign_id") or not campaign.get("roles"):
        raise ValueError("campaign requires campaign_id and roles")
    run.mkdir(parents=True, exist_ok=False)
    for folder in ["inputs", "sessions", "candidates", "checks", "code", "artifacts", "commands"]:
        (run / folder).mkdir()
    sources = [ROOT / "README.md", ROOT / "AGENTS.md", ROOT / "research/DESIGN.md",
               ROOT / "research/agents/explorer.md", ROOT / "research/agents/vacuum.md",
               Path(__file__).resolve(), campaign_path]
    snapshots = []
    for source in sources:
        relative = source.resolve().relative_to(ROOT)
        destination = run / "inputs" / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())
        snapshots.append({"source": str(relative), "snapshot": str(destination.relative_to(run)), "sha256": digest(destination)})
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    dirty = bool(subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True, check=True).stdout)
    patch = subprocess.run(["git", "diff", "--binary", "HEAD"], cwd=ROOT, capture_output=True, check=True).stdout
    (run / "inputs/working-tree.patch").write_bytes(patch)
    manifest = {
        "schema_version": "0.2", "is_template": False, "run_id": run.name,
        "parent_run_ids": parents, "candidate_ids": [], "created_at_utc": now(),
        "campaign_id": campaign["campaign_id"],
        "repository": {"commit": commit, "dirty": dirty, "patch_path": "inputs/working-tree.patch", "note": "Untracked inputs are preserved by explicit snapshots; the patch covers tracked files only."},
        "runtime": {"backend": "codex-chat-native-subagents", "model": None, "python": sys.version},
        "sessions": [], "tools": [], "limits": campaign.get("limits", {}),
        "usage": {"input_tokens": None, "output_tokens": None, "cost_usd": None},
        "input_snapshots": snapshots,
        "logging": {"available": ["explicit prompts", "coordinator events", "recorded calculation commands", "saved outputs and reports"], "unavailable": ["automatic full chat/subagent transcript export", "private model reasoning", "complete tool-call interception", "authoritative per-session token and cost totals"]},
    }
    write_json(run / "manifest.json", manifest)
    (run / "events.jsonl").touch()
    (run / "report.md").write_bytes((ROOT / "research/templates/run/report.md").read_bytes())
    return append(run, "coordinator", "run_created", {"campaign_id": campaign["campaign_id"]})


def execute(run, role, command, timeout):
    if not command or timeout <= 0:
        raise ValueError("a command and positive timeout are required")
    command_id = uuid.uuid4().hex[:12]
    location = run / "commands" / command_id
    with locked(run):
        if state(read_events(run)) != "running":
            raise ValueError("commands require a running attempt")
        location.mkdir()
        metadata = {"command_id": command_id, "actor": role, "argv": command, "cwd": str(run), "started_at_utc": now(), "timeout_seconds": timeout}
        write_json(location / "command.json", metadata)
        append_unlocked(run, role, "command_started", {"command_id": command_id, "record": str(location.relative_to(run))})
    timed_out = False
    interrupted = False
    returncode = None
    error = None
    with (location / "stdout.log").open("wb") as stdout, (location / "stderr.log").open("wb") as stderr:
        try:
            process = subprocess.Popen(command, cwd=run, stdout=stdout, stderr=stderr, start_new_session=True)
            try:
                returncode = process.wait(timeout=timeout)
            except (subprocess.TimeoutExpired, KeyboardInterrupt) as exc:
                timed_out = isinstance(exc, subprocess.TimeoutExpired)
                interrupted = not timed_out
                os.killpg(process.pid, signal.SIGKILL)
                returncode = process.wait()
        except OSError as exc:
            error = str(exc)
    result = {**metadata, "finished_at_utc": now(), "returncode": returncode, "timed_out": timed_out, "interrupted": interrupted, "error": error}
    write_json(location / "result.json", result)
    append(run, role, "command_finished", {"command_id": command_id, "returncode": returncode, "timed_out": timed_out, "interrupted": interrupted, "error": error})
    print(json.dumps(result, indent=2))
    return 0 if returncode == 0 and not timed_out and not interrupted and error is None else 1


def seal(run):
    with locked(run):
        if state(read_events(run)) not in {"completed", "failed"}:
            raise ValueError("seal only a completed or failed attempt")
        if (run / "artifacts.json").exists():
            raise ValueError("attempt is already sealed")
        entries = []
        for path in sorted(run.rglob("*")):
            if path.is_symlink():
                raise ValueError("symlinks are not supported in archived attempts")
            if path.is_file() and path.name != ".lock":
                entries.append({"path": str(path.relative_to(run)), "sha256": digest(path)})
        write_json(run / "artifacts.json", {"schema_version": "0.2", "sealed_at_utc": now(), "files": entries})
    return {"sealed_files": len(entries)}


def verify(run):
    archive = json.loads((run / "artifacts.json").read_text())
    listed = set()
    for entry in archive["files"]:
        path = run / entry["path"]
        path.resolve().relative_to(run.resolve())
        if path.is_symlink() or digest(path) != entry["sha256"]:
            raise ValueError(f"artifact mismatch: {entry['path']}")
        listed.add(entry["path"])
    actual = {str(p.relative_to(run)) for p in run.rglob("*") if p.is_file() and p.name not in {".lock", "artifacts.json"}}
    if actual != listed:
        raise ValueError("archive file inventory mismatch")
    events = read_events(run)
    if [e["sequence"] for e in events] != list(range(1, len(events) + 1)):
        raise ValueError("journal sequence mismatch")
    return {"verified_files": len(listed), "execution_status": state(events)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True)
    sub = parser.add_subparsers(dest="action", required=True)
    init = sub.add_parser("init")
    init.add_argument("--campaign", type=Path, required=True)
    init.add_argument("--parent", action="append", default=[])
    event = sub.add_parser("event")
    event.add_argument("--actor", default="coordinator")
    event.add_argument("--type", required=True)
    event.add_argument("--payload", default="{}", help="JSON object; never credentials")
    sub.add_parser("status")
    sub.add_parser("seal")
    sub.add_parser("verify")
    command = sub.add_parser("exec")
    command.add_argument("--actor", required=True)
    command.add_argument("--timeout", type=float, default=60)
    command.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    run = args.run.resolve()
    try:
        if args.action == "init":
            result = initialize(run, args.campaign.resolve(), args.parent)
        elif args.action == "event":
            payload = json.loads(args.payload)
            if not isinstance(payload, dict):
                raise ValueError("event payload must be a JSON object")
            result = append(run, args.actor, args.type, payload)
        elif args.action == "status":
            events = read_events(run)
            result = {"run_id": run.name, "execution_status": state(events), "events": len(events), "last_event": events[-1] if events else None}
        elif args.action == "exec":
            command = args.command[1:] if args.command[:1] == ["--"] else args.command
            return execute(run, args.actor, command, args.timeout)
        elif args.action == "seal":
            result = seal(run)
        else:
            result = verify(run)
        print(json.dumps(result, indent=2))
        return 0
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(f"records: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
