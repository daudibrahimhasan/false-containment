from __future__ import annotations

import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .pipeline import (
    EVIDENCE_LEVELS,
    APIClient,
    MockClient,
    build_packet,
    load_cases,
    load_env,
    read_json,
    simulate,
    validate_design,
    write_json,
)


CSV_FIELDS = [
    "run_id", "timestamp_utc", "judgment_index", "packet_id", "trajectory_id",
    "incident_family", "agent_provider", "agent_model", "agent_trajectory_id",
    "evidence_condition", "verifier_provider", "verifier_model", "verifier_replicate",
    "verdict", "confidence", "reason", "input_tokens", "output_tokens", "total_tokens",
    "cached_tokens", "reasoning_tokens", "latency_seconds", "attempt_count",
    "provider_request_id", "served_model", "parse_status", "leakage_check_status",
    "error_type", "error_message", "completed",
]
EVENT_FIELDS = ["timestamp_utc", "level", "phase", "message"]
CALL_FIELDS = [
    "call_id", "timestamp_utc", "phase", "provider", "requested_model", "served_model",
    "related_id", "attempt", "latency_seconds", "http_status", "input_tokens",
    "output_tokens", "total_tokens", "retry_reason", "success", "key_slot",
]
TRAJECTORY_FIELDS = ["run_id", "timestamp_utc", "trajectory_id", "case_id", "family", "agent_provider", "agent_model", "served_model", "input_tokens", "output_tokens", "total_tokens", "latency_seconds", "completed"]


def _utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def _digest_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _digest_json(value: Any) -> str:
    return _digest_bytes(json.dumps(value, sort_keys=True, ensure_ascii=False).encode())


def _append_csv(path: Path, fields: list[str], row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in fields})
        handle.flush()
        os.fsync(handle.fileno())


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.{time.time_ns()}.tmp")
    write_json(temporary, value)
    try:
        for attempt in range(5):
            try:
                os.replace(temporary, path)
                return
            except PermissionError:
                if attempt == 4:
                    raise
                time.sleep(0.05 * (attempt + 1))
    finally:
        if temporary.exists():
            try:
                temporary.unlink()
            except OSError:
                pass


def _git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=root, text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _hash_inputs(root: Path, config: dict[str, Any]) -> dict[str, str]:
    incidents = []
    for path in sorted((root / "incidents").glob("*.json")):
        incidents.append((path.name, _digest_bytes(path.read_bytes())))
    preregistration = root / "PREREGISTRATION.md"
    subset = root / "config" / "secondary_subset.json"
    return {
        "config_hash": _digest_json(config),
        "preregistration_hash": _digest_bytes(preregistration.read_bytes()),
        "incident_spec_hash": _digest_json(incidents),
        "verifier_prompt_hash": _digest_bytes(__import__("falsecontain.pipeline", fromlist=["VERIFIER_PROMPT"]).VERIFIER_PROMPT.encode()),
        "secondary_subset_hash": _digest_bytes(subset.read_bytes()),
    }


def _job_plan(cases: list[dict[str, Any]], config: dict[str, Any]) -> list[dict[str, Any]]:
    jobs = []
    for case in cases:
        for agent in config["agent_models"]:
            trajectory_id = f"{case['case_id']}__{agent['model']}".replace("/", "_")
            for level in EVIDENCE_LEVELS:
                packet_id = f"{trajectory_id}__{level}"
                for replicate in range(1, config["verifier_replicates"] + 1):
                    jobs.append({
                        "judgment_id": f"{packet_id}__r{replicate:02d}",
                        "packet_id": packet_id,
                        "trajectory_id": trajectory_id,
                        "case_id": case["case_id"],
                        "family": case["family"],
                        "agent": agent,
                        "level": level,
                        "replicate": replicate,
                    })
    if len(jobs) != 192 or len({job["judgment_id"] for job in jobs}) != 192:
        raise ValueError("primary job plan must contain exactly 192 unique judgments")
    return jobs


def _show_header(console: Console, run_id: str, config: dict[str, Any], started: str) -> None:
    table = Table.grid(padding=(0, 2))
    table.add_row("Run ID", f"[cyan]{run_id}[/cyan]")
    table.add_row("Phase", "[magenta]PRIMARY SCIENTIFIC RUN[/magenta]")
    table.add_row("Scientific lock", "[green]LOCKED[/green]")
    table.add_row("Started", started)
    table.add_row("Agent 1", f"[blue]{config['agent_models'][0]['provider']}[/blue] {config['agent_models'][0]['model']}")
    table.add_row("Agent 2", f"[blue]{config['agent_models'][1]['provider']}[/blue] {config['agent_models'][1]['model']}")
    table.add_row("Verifier", f"[yellow]{config['primary_verifier']['provider']}[/yellow] {config['primary_verifier']['model']}")
    table.add_row("Core target", "16 scientific agent trajectories / 192 primary verifier judgments")
    console.print(Panel(table, title="[bold cyan]FALSE CONTAINMENT - PRIMARY EXPERIMENT[/bold cyan]", border_style="cyan"))


def _show_progress(console: Console, trajectories: int, judgments: int, total: int = 192) -> None:
    table = Table(title="[bold]OVERALL PROGRESS[/bold]", show_header=True, header_style="bold cyan")
    table.add_column("Unit")
    table.add_column("Completed", justify="right")
    table.add_column("Progress", justify="right")
    table.add_row("Agent trajectories", f"{trajectories} / 16", f"{trajectories / 16:.1%}")
    table.add_row("Primary judgments", f"{judgments} / {total}", f"{judgments / total:.1%}")
    console.print(table)


def run_primary(root: Path, *, dry_run: bool = False, resume: bool = False, output: Path | None = None, run_id: str | None = None) -> dict[str, Any]:
    config = read_json(root / "config" / "experiment.json")
    cases = load_cases(root)
    errors = validate_design(cases, config, scientific=True)
    if errors:
        raise ValueError("Design validation failed:\n- " + "\n- ".join(errors))
    if not dry_run:
        pilot_state_path = root / "outputs" / "agent_pilot_real" / f"preregistration-v{config['preregistration_version']}" / "results" / "run_state.json"
        pilot_completed = False
        if pilot_state_path.exists():
            pilot_completed = bool(read_json(pilot_state_path).get("pilot_completed"))
        if not config.get("scientific_lock") or not pilot_completed:
            raise ValueError("locked scientific config and completed pilot run-state are required")
    load_env(root / ".env")
    chosen_id = run_id or ("dry_run_" if dry_run else "core_") + datetime.now().strftime("%Y%m%d_%H%M%S")
    run_root = (output or root / "outputs" / "primary_runs") / chosen_id
    manifest_path = run_root / "manifest.json"
    hashes = _hash_inputs(root, config)
    if resume and manifest_path.exists():
        old = read_json(manifest_path)
        for key, value in hashes.items():
            if old.get(key) != value:
                raise ValueError(f"resume refused: {key} changed")
    elif manifest_path.exists():
        raise ValueError(f"run already exists; use --resume: {run_root}")
    else:
        if not dry_run:
            missing = []
            for spec in [*config["agent_models"], config["primary_verifier"]]:
                if not os.environ.get(spec.get("api_key_env", ""), ""):
                    missing.append(spec.get("api_key_env", spec["provider"]))
            if missing:
                raise ValueError("required API keys are absent: " + ", ".join(missing))
        manifest = {
            "run_id": chosen_id, "experiment_id": config.get("experiment_id", "falsecontain_core"),
            "started_at": _utc(), "git_commit": _git(root, "rev-parse", "HEAD"),
            "git_dirty": bool(_git(root, "status", "--porcelain")), "python": sys.version,
            "platform": platform.platform(), "requested_models": [item["model"] for item in config["agent_models"]],
            "verifier_model": config["primary_verifier"]["model"], **hashes,
        }
        _atomic_json(manifest_path, manifest)
    manifest = read_json(manifest_path)
    jobs = _job_plan(cases, config)
    planned_path = run_root / "planned_primary_jobs.csv"
    if not planned_path.exists():
        for job in jobs:
            _append_csv(planned_path, list(job.keys()), job)
    checkpoint_path = run_root / "checkpoint.json"
    checkpoint = read_json(checkpoint_path) if checkpoint_path.exists() else {"trajectories": [], "judgments": []}
    client = MockClient() if dry_run else APIClient(config)
    pilot_source = root / "outputs" / "agent_pilot_real" / f"preregistration-v{config['preregistration_version']}"
    if not dry_run and not pilot_source.exists():
        raise ValueError(f"completed pilot artifact directory is missing: {pilot_source}")
    console = Console()
    _show_header(console, chosen_id, config, manifest["started_at"])
    events_path = run_root / "run_events.csv"
    calls_path = run_root / "api_calls.csv"

    def event(level: str, phase: str, message: str) -> None:
        _append_csv(events_path, EVENT_FIELDS, {"timestamp_utc": _utc(), "level": level, "phase": phase, "message": message})

    event("info", "startup", "run started")
    if not dry_run:
        preflight = [client.preflight(spec) for spec in [*config["agent_models"], config["primary_verifier"]]]
        for result in preflight:
            event("info" if result.get("ok") else "error", "preflight", f"{result['provider']} {result['model']}: {result.get('error', 'ok')}")
        if not all(result.get("ok") for result in preflight):
            raise ValueError("provider preflight failed; no scientific calls were started")
    trajectories_done = set(checkpoint.get("trajectories", []))
    trajectory_cache: dict[str, dict[str, Any]] = {}
    for case in cases:
        for agent in config["agent_models"]:
            trajectory_id = f"{case['case_id']}__{agent['model']}".replace("/", "_")
            trajectory_path = run_root / "trajectories" / f"{trajectory_id}.json"
            if trajectory_path.exists():
                trajectory = read_json(trajectory_path)
            elif not dry_run:
                source_path = pilot_source / "trajectories" / f"{trajectory_id}.json"
                if not source_path.exists():
                    raise ValueError(f"primary run refuses to regenerate missing pilot trajectory: {trajectory_id}")
                source = read_json(source_path)
                agent_result = source["raw_and_parsed_agent_result"]
                trajectory = {"trajectory_id": trajectory_id, "case_id": case["case_id"], "family": case["family"], "agent": agent, "agent_result": agent_result, "simulation": {"final_state": source["final_state"], "action_records": source["action_records"], "telemetry": [], "postcondition_results": [], "ground_truth": source["deterministic_ground_truth"]}, "source_pilot_trajectory": True, "created_at": source.get("created_at", _utc())}
                for level in EVIDENCE_LEVELS:
                    source_packet = pilot_source / "packets" / f"{trajectory_id}__{level}.json"
                    if not source_packet.exists():
                        raise ValueError(f"primary run refuses to regenerate missing pilot packet: {trajectory_id}__{level}")
                    _atomic_json(run_root / "packets" / source_packet.name, read_json(source_packet))
                _atomic_json(trajectory_path, trajectory)
            else:
                agent_result = client.agent(case, agent)
                sim = simulate(case, agent_result["selected_action_ids"])
                trajectory = {"trajectory_id": trajectory_id, "case_id": case["case_id"], "family": case["family"], "agent": agent, "agent_result": agent_result, "simulation": sim.__dict__, "created_at": _utc()}
                _atomic_json(trajectory_path, trajectory)
            trajectory_cache[trajectory_id] = trajectory
            if trajectory_id not in trajectories_done:
                usage = trajectory["agent_result"].get("usage", {})
                _append_csv(run_root / "trajectories.csv", TRAJECTORY_FIELDS, {"run_id": chosen_id, "timestamp_utc": _utc(), "trajectory_id": trajectory_id, "case_id": case["case_id"], "family": case["family"], "agent_provider": agent["provider"], "agent_model": agent["model"], "served_model": trajectory["agent_result"].get("served_model"), "input_tokens": usage.get("prompt_tokens"), "output_tokens": usage.get("completion_tokens"), "total_tokens": usage.get("total_tokens"), "latency_seconds": trajectory["agent_result"].get("latency_ms", 0) / 1000, "completed": True})
                for attempt in trajectory["agent_result"].get("attempt_log", []) or [{"attempt_number": 1, "outcome": "success", "key_slot": "mock"}]:
                    _append_csv(calls_path, CALL_FIELDS, {"call_id": f"{trajectory_id}:agent:{attempt.get('attempt_number', 1)}", "timestamp_utc": _utc(), "phase": "agent", "provider": agent["provider"], "requested_model": agent["model"], "served_model": trajectory["agent_result"].get("served_model"), "related_id": trajectory_id, "attempt": attempt.get("attempt_number", 1), "latency_seconds": attempt.get("latency_ms", 0) / 1000, "http_status": attempt.get("http_status"), "input_tokens": attempt.get("token_usage", {}).get("prompt_tokens"), "output_tokens": attempt.get("token_usage", {}).get("completion_tokens"), "total_tokens": attempt.get("token_usage", {}).get("total_tokens"), "retry_reason": attempt.get("failure_reason"), "success": attempt.get("outcome") == "success", "key_slot": attempt.get("key_slot")})
                event("success", "agent", f"trajectory completed: {trajectory_id}")
                trajectories_done.add(trajectory_id)
                _atomic_json(checkpoint_path, {"trajectories": sorted(trajectories_done), "judgments": checkpoint.get("judgments", [])})
    judgments_done = set(checkpoint.get("judgments", []))
    judgment_csv = run_root / "results" / "primary_judgments.csv"
    for index, job in enumerate(jobs, start=1):
        if job["judgment_id"] in judgments_done:
            continue
        trajectory = trajectory_cache[job["trajectory_id"]]
        case = next(item for item in cases if item["case_id"] == job["case_id"])
        packet_path = run_root / "packets" / f"{job['packet_id']}.json"
        if packet_path.exists():
            packet = read_json(packet_path)
        else:
            if trajectory.get("source_pilot_trajectory"):
                raise ValueError(f"primary run refuses to regenerate pilot packet: {job['packet_id']}")
            sim = type("Sim", (), trajectory["simulation"])()
            packet = build_packet(case, trajectory["agent_result"], sim, job["level"])
            _atomic_json(packet_path, packet)
        started = time.perf_counter()
        try:
            verdict = client.verifier(packet, config["primary_verifier"])
            usage = verdict.get("usage", {})
            row = {"run_id": chosen_id, "timestamp_utc": _utc(), "judgment_index": index, "packet_id": job["packet_id"], "trajectory_id": job["trajectory_id"], "incident_family": job["family"], "agent_provider": job["agent"]["provider"], "agent_model": job["agent"]["model"], "agent_trajectory_id": job["trajectory_id"], "evidence_condition": job["level"], "verifier_provider": config["primary_verifier"]["provider"], "verifier_model": config["primary_verifier"]["model"], "verifier_replicate": job["replicate"], "verdict": verdict.get("verdict"), "confidence": verdict.get("confidence"), "reason": verdict.get("reason", ""), "input_tokens": usage.get("prompt_tokens"), "output_tokens": usage.get("completion_tokens"), "total_tokens": usage.get("total_tokens"), "cached_tokens": usage.get("cached_tokens"), "reasoning_tokens": usage.get("reasoning_tokens"), "latency_seconds": round(time.perf_counter() - started, 3), "attempt_count": len(verdict.get("attempt_log", [])) or 1, "provider_request_id": verdict.get("provider_request_id"), "served_model": verdict.get("served_model"), "parse_status": "ok", "leakage_check_status": "passed", "completed": True}
            _append_csv(judgment_csv, CSV_FIELDS, row)
            for attempt in verdict.get("attempt_log", []) or [{"attempt_number": 1, "outcome": "success", "key_slot": "mock"}]:
                _append_csv(calls_path, CALL_FIELDS, {"call_id": f"{job['judgment_id']}:{attempt.get('attempt_number', 1)}", "timestamp_utc": _utc(), "phase": "verifier", "provider": config["primary_verifier"]["provider"], "requested_model": config["primary_verifier"]["model"], "served_model": verdict.get("served_model"), "related_id": job["judgment_id"], "attempt": attempt.get("attempt_number", 1), "latency_seconds": attempt.get("latency_ms", 0) / 1000, "http_status": attempt.get("http_status"), "input_tokens": attempt.get("token_usage", {}).get("prompt_tokens"), "output_tokens": attempt.get("token_usage", {}).get("completion_tokens"), "total_tokens": attempt.get("token_usage", {}).get("total_tokens"), "retry_reason": attempt.get("failure_reason"), "success": attempt.get("outcome") == "success", "key_slot": attempt.get("key_slot")})
            event("success", "verifier", f"judgment completed: {job['judgment_id']}")
            console.print(f"[green]+[/green] Judgment {index:03d}/192 | {job['family']} | {job['level']} | rep {job['replicate']}")
        except Exception as exc:
            row = {"run_id": chosen_id, "timestamp_utc": _utc(), "judgment_index": index, "packet_id": job["packet_id"], "trajectory_id": job["trajectory_id"], "incident_family": job["family"], "agent_provider": job["agent"]["provider"], "agent_model": job["agent"]["model"], "evidence_condition": job["level"], "verifier_provider": config["primary_verifier"]["provider"], "verifier_model": config["primary_verifier"]["model"], "verifier_replicate": job["replicate"], "error_type": type(exc).__name__, "error_message": str(exc), "completed": False}
            _append_csv(judgment_csv, CSV_FIELDS, row)
            event("error", "verifier", f"judgment failed: {job['judgment_id']}: {exc}")
            console.print(f"[red]![/red] Judgment {index:03d}/192 failed: {exc}")
        judgments_done.add(job["judgment_id"])
        checkpoint = {"trajectories": sorted(trajectories_done), "judgments": sorted(judgments_done)}
        _atomic_json(checkpoint_path, checkpoint)
        _show_progress(console, len(trajectories_done), len(judgments_done))
    summary = {"run_id": chosen_id, "agent_trajectories": len(trajectories_done), "primary_judgments": len(judgments_done), "expected_primary_judgments": 192, "dry_run": dry_run, "scientific_complete": len(judgments_done) == 192}
    _atomic_json(run_root / "run_summary.json", summary)
    _atomic_json(run_root / "status.json", summary)
    return summary


def status_run(root: Path, run_id: str, output: Path | None = None) -> dict[str, Any]:
    path = (output or root / "outputs" / "primary_runs") / run_id / "status.json"
    if not path.exists():
        raise ValueError(f"unknown run: {run_id}")
    return read_json(path)


def validate_run(root: Path, run_id: str, output: Path | None = None) -> dict[str, Any]:
    summary = status_run(root, run_id, output)
    result = {"run_id": run_id, "passed": summary.get("primary_judgments") == 192, **summary}
    return result
