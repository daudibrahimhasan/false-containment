import json
from pathlib import Path

from false_containment.core import calculate_metrics, run_experiment, validate_incident


ROOT = Path(__file__).resolve().parents[1]


def test_incident_has_manual_truth_and_five_taxonomized_conditions():
    incident = json.loads((ROOT / "incidents" / "ssh_unauthorized_key.json").read_text(encoding="utf-8"))
    validate_incident(incident)
    assert incident["ground_truth"]["model_generated"] is False
    assert len(incident["evidence_conditions"]) == 5
    assert all(condition["taxonomy_tags"] for condition in incident["evidence_conditions"])


def test_fcr_uses_resolved_verdicts_as_denominator():
    rows = [
        {"verdict": "resolved", "ground_truth": "unresolved", "error": ""},
        {"verdict": "resolved", "ground_truth": "resolved", "error": ""},
        {"verdict": "unresolved", "ground_truth": "unresolved", "error": ""},
    ]
    metrics = calculate_metrics(rows)
    assert metrics["false_containment_rate"] == 0.5
    assert metrics["false_containment_frequency"] == 1 / 3


def test_mock_run_writes_complete_100_run_matrix(tmp_path):
    for name in ["config", "incidents"]:
        destination = tmp_path / name
        destination.mkdir()
        for source in (ROOT / name).glob("*.json"):
            (destination / source.name).write_bytes(source.read_bytes())
    manifest = run_experiment(tmp_path, mock=True)
    assert manifest["metrics"]["total_planned_runs"] == 100
    assert manifest["metrics"]["failed_runs"] == 0
    assert len(list((tmp_path / "outputs" / "raw_trajectories").glob("*.json"))) == 100
    assert (tmp_path / "outputs" / "plots" / "false_containment_by_condition.svg").exists()
    assert (tmp_path / "outputs" / "tables" / "by_condition.md").exists()
