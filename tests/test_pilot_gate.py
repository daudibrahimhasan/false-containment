from pathlib import Path

import pytest

from falsecontain.pipeline import evaluate_pilot_gate, read_json


ROOT = Path(__file__).resolve().parents[1]


def base_rows():
    config = read_json(ROOT / "config" / "experiment.json")
    rows = []
    index = 0
    for family in config["required_families"]:
        for intended, ground_truth in (("intended_resolved", "resolved"), ("intended_false_containment", "unresolved")):
            for model in (spec["model"] for spec in config["agent_models"]):
                index += 1
                rows.append({
                    "trajectory_id": f"trajectory-{index}",
                    "family": family,
                    "intended_stratum": intended,
                    "agent_model": model,
                    "ground_truth": ground_truth,
                    "matches_intended_stratum": True,
                    "ground_truth_source": "deterministic_final_state",
                    "invalid_action_ids": [],
                    "parsing_failed": False,
                    "served_model_matches": True,
                    "e4_matches_final_state": True,
                    "leakage_passed": True,
                    "packet_count": 4,
                })
    return config, rows


@pytest.mark.parametrize("model_index", [0, 1])
def test_v14_gate_passes_with_model_and_family_class_coverage(model_index):
    config, rows = base_rows()
    result = evaluate_pilot_gate(rows, config)
    assert result["passed"] is True
    assert result["model_class_counts"][config["agent_models"][model_index]["model"]] == {"resolved": 4, "unresolved": 4}


@pytest.mark.parametrize("model_index,forced_label", [(0, "resolved"), (1, "resolved"), (0, "unresolved"), (1, "unresolved")])
def test_v14_gate_fails_if_a_model_has_only_one_class(model_index, forced_label):
    config, rows = base_rows()
    model = config["agent_models"][model_index]["model"]
    for row in rows:
        if row["agent_model"] == model:
            row["ground_truth"] = forced_label
    result = evaluate_pilot_gate(rows, config)
    assert result["passed"] is False
    assert result["conditions"]["model_class_coverage"] is False


@pytest.mark.parametrize("missing_label", ["resolved", "unresolved"])
def test_v14_gate_fails_if_a_family_lacks_one_class(missing_label):
    config, rows = base_rows()
    family = config["required_families"][0]
    replacement = "unresolved" if missing_label == "resolved" else "resolved"
    for row in rows:
        if row["family"] == family and row["ground_truth"] == missing_label:
            row["ground_truth"] = replacement
    assert evaluate_pilot_gate(rows, config)["conditions"]["family_class_coverage"] is False


def test_v14_gate_fails_on_e4_leakage_invalid_parser_and_served_mismatch():
    config, rows = base_rows()
    rows[0]["e4_matches_final_state"] = False
    assert evaluate_pilot_gate(rows, config)["conditions"]["evidence_integrity"] is False
    config, rows = base_rows()
    rows[0]["leakage_passed"] = False
    assert evaluate_pilot_gate(rows, config)["conditions"]["evidence_integrity"] is False
    config, rows = base_rows()
    rows[0]["invalid_action_ids"] = ["bad_action"]
    assert evaluate_pilot_gate(rows, config)["conditions"]["execution_integrity"] is False
    config, rows = base_rows()
    rows[0]["parsing_failed"] = True
    assert evaluate_pilot_gate(rows, config)["conditions"]["execution_integrity"] is False
    config, rows = base_rows()
    rows[0]["served_model_matches"] = False
    assert evaluate_pilot_gate(rows, config)["conditions"]["execution_integrity"] is False


def test_v14_gate_rejects_corruption_and_unresolved_infrastructure_failures():
    config, rows = base_rows()
    assert evaluate_pilot_gate(rows, config, corrupted_trajectory_count=1)["passed"] is False
    assert evaluate_pilot_gate(rows, config, infrastructure_failures=1)["passed"] is False


def test_v14_gate_uses_final_ground_truth_not_intended_stratum():
    config, rows = base_rows()
    rows[0]["intended_stratum"] = "intended_resolved"
    rows[0]["ground_truth"] = "unresolved"
    rows[0]["matches_intended_stratum"] = False
    result = evaluate_pilot_gate(rows, config)
    assert result["passed"] is True
    assert result["conditions"]["ground_truth"] is True


def test_v14_gate_rejects_duplicate_trajectory_ids_and_ground_truth_audit_failure():
    config, rows = base_rows()
    rows[1]["trajectory_id"] = rows[0]["trajectory_id"]
    assert evaluate_pilot_gate(rows, config)["conditions"]["completion"] is False
    config, rows = base_rows()
    assert evaluate_pilot_gate(rows, config, ground_truth_audit_passed=False)["conditions"]["ground_truth"] is False
