import csv
import json
from pathlib import Path

import pytest

from falsecontain.pipeline import load_cases, read_json
from falsecontain.terminal_runner import _job_plan, run_primary, status_run, validate_run


ROOT = Path(__file__).resolve().parents[1]


def test_primary_job_plan_is_exactly_192_unique_jobs():
    config = read_json(ROOT / "config" / "experiment.json")
    jobs = _job_plan(load_cases(ROOT), config)
    assert len(jobs) == 192
    assert len({job["judgment_id"] for job in jobs}) == 192


def test_dry_run_writes_incremental_results_and_status(tmp_path):
    result = run_primary(ROOT, dry_run=True, run_id="test_run", output=tmp_path)
    assert result["primary_judgments"] == 192
    csv_path = tmp_path / "test_run" / "results" / "primary_judgments.csv"
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 192
    assert all(row["completed"] == "True" for row in rows)
    run_dir = tmp_path / "test_run"
    assert all((run_dir / name).exists() for name in ("trajectories.csv", "api_calls.csv", "run_events.csv", "planned_primary_jobs.csv", "manifest.json", "checkpoint.json", "run_summary.json"))
    assert status_run(ROOT, "test_run", tmp_path)["primary_judgments"] == 192
    assert validate_run(ROOT, "test_run", tmp_path)["passed"] is True


def test_resume_reuses_completed_judgments(tmp_path):
    run_primary(ROOT, dry_run=True, run_id="resume_run", output=tmp_path)
    second = run_primary(ROOT, dry_run=True, resume=True, run_id="resume_run", output=tmp_path)
    assert second["primary_judgments"] == 192
    csv_path = tmp_path / "resume_run" / "results" / "primary_judgments.csv"
    with csv_path.open(newline="", encoding="utf-8") as handle:
        assert len(list(csv.DictReader(handle))) == 192


def test_resume_refuses_changed_manifest(tmp_path):
    run_primary(ROOT, dry_run=True, run_id="hash_run", output=tmp_path)
    manifest_path = tmp_path / "hash_run" / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["config_hash"] = "changed"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    with pytest.raises(ValueError, match="config_hash changed"):
        run_primary(ROOT, dry_run=True, resume=True, run_id="hash_run", output=tmp_path)
