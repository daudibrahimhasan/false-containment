import io
import json
import urllib.error
from copy import deepcopy
from pathlib import Path

import pytest

from falsecontain.pipeline import APIClient, APIRequestFailure, load_cases, read_json

ROOT = Path(__file__).resolve().parents[1]


class FakeResponse:
    def __init__(self, payload, request_id="req-success"):
        self.payload = payload
        self.status = 200
        self.headers = {"x-request-id": request_id}

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return False

    def read(self, *_):
        return json.dumps(self.payload).encode()


def http_error(code, message, request_id):
    return urllib.error.HTTPError("https://gemini.invalid", code, message, {"x-request-id": request_id}, io.BytesIO(json.dumps({"error": {"message": message}}).encode()))


def client_and_spec(monkeypatch):
    config = read_json(ROOT / "config" / "experiment.json")
    spec = deepcopy(config["agent_models"][1])
    monkeypatch.setenv("AGENT_2_API_KEY_PRIMARY", "primary-secret")
    monkeypatch.setenv("AGENT_2_API_KEY_FALLBACK", "fallback-secret")
    monkeypatch.setattr("falsecontain.pipeline.time.sleep", lambda _: None)
    return APIClient(config), spec


def valid_response(request_id="req-success"):
    payload = {
        "id": request_id,
        "model": "gemini-3.7-flash",
        "usage": {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15},
        "choices": [{"message": {"content": json.dumps({"selected_action_ids": [], "final_claim": "Done", "reasoning_summary": "No action"})}}],
    }
    return FakeResponse(payload, request_id)


def test_primary_success_never_uses_fallback(monkeypatch):
    client, spec = client_and_spec(monkeypatch)
    requests = []

    def fake_urlopen(request, **_):
        requests.append(request)
        return valid_response()

    monkeypatch.setattr("falsecontain.pipeline.urllib.request.urlopen", fake_urlopen)
    result = client._call(spec, [{"role": "user", "content": "same"}])
    assert len(requests) == 1
    assert requests[0].get_header("Authorization") == "Bearer primary-secret"
    assert result["key_slot"] == "primary"
    assert result["retry_count"] == 0
    assert result["attempt_log"][0]["provider_request_id"] == "req-success"


def test_quota_exhaustion_uses_fallback_with_identical_payload(monkeypatch):
    client, spec = client_and_spec(monkeypatch)
    outcomes = [http_error(429, "quota exhausted", f"req-primary-{index}") for index in range(4)] + [valid_response("req-fallback")]
    requests = []

    def fake_urlopen(request, **_):
        requests.append(request)
        outcome = outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    monkeypatch.setattr("falsecontain.pipeline.urllib.request.urlopen", fake_urlopen)
    result = client._call(spec, [{"role": "user", "content": "same"}])
    assert len(requests) == 5
    assert len({request.data for request in requests}) == 1
    assert all(request.get_header("Authorization") == "Bearer primary-secret" for request in requests[:4])
    assert requests[4].get_header("Authorization") == "Bearer fallback-secret"
    assert result["key_slot"] == "fallback"
    assert result["retry_count"] == 4
    assert [item["key_slot"] for item in result["attempt_log"]] == ["primary"] * 4 + ["fallback"]
    assert [item["retry_backoff_seconds"] for item in result["attempt_log"][:4]] == [2, 4, 8, None]
    encoded = json.dumps(result)
    assert "primary-secret" not in encoded and "fallback-secret" not in encoded


def test_403_never_activates_fallback(monkeypatch):
    client, spec = client_and_spec(monkeypatch)
    requests = []

    def fake_urlopen(request, **_):
        requests.append(request)
        raise http_error(403, "forbidden", f"req-{len(requests)}")

    monkeypatch.setattr("falsecontain.pipeline.urllib.request.urlopen", fake_urlopen)
    with pytest.raises(APIRequestFailure) as captured:
        client._call(spec, [{"role": "user", "content": "same"}])
    assert len(requests) == 4
    assert all(request.get_header("Authorization") == "Bearer primary-secret" for request in requests)
    assert all(not item["fallback_eligible"] for item in captured.value.attempt_log)


def test_both_key_slots_exhaust_to_one_pending_failure(monkeypatch):
    client, spec = client_and_spec(monkeypatch)
    requests = []

    def fake_urlopen(request, **_):
        requests.append(request)
        raise http_error(503, "service unavailable", f"req-{len(requests)}")

    monkeypatch.setattr("falsecontain.pipeline.urllib.request.urlopen", fake_urlopen)
    with pytest.raises(APIRequestFailure) as captured:
        client._call(spec, [{"role": "user", "content": "same"}])
    assert len(requests) == 8
    assert [item["key_slot"] for item in captured.value.attempt_log] == ["primary"] * 4 + ["fallback"] * 4
    encoded = json.dumps(captured.value.attempt_log)
    assert "primary-secret" not in encoded and "fallback-secret" not in encoded


def test_schema_failure_does_not_activate_fallback(monkeypatch):
    client, spec = client_and_spec(monkeypatch)
    calls = []
    invalid = FakeResponse({"model": "gemini-3.7-flash", "choices": [{"message": {"content": json.dumps({"final_claim": "missing actions"})}}]})

    def fake_urlopen(request, **_):
        calls.append(request)
        return invalid

    monkeypatch.setattr("falsecontain.pipeline.urllib.request.urlopen", fake_urlopen)
    with pytest.raises(ValueError, match="invalid agent response schema"):
        client.agent(load_cases(ROOT)[0], spec)
    assert len(calls) == 1
    assert calls[0].get_header("Authorization") == "Bearer primary-secret"


def test_malformed_http_200_logs_request_id_without_fallback(monkeypatch):
    client, spec = client_and_spec(monkeypatch)
    calls = []
    malformed = FakeResponse({"model": "gemini-3.7-flash", "usage": {"prompt_tokens": 7}, "choices": [{"message": {"content": "not-json"}}]}, "req-malformed")

    def fake_urlopen(request, **_):
        calls.append(request)
        return malformed

    monkeypatch.setattr("falsecontain.pipeline.urllib.request.urlopen", fake_urlopen)
    with pytest.raises(APIRequestFailure) as captured:
        client._call(spec, [{"role": "user", "content": "same"}])
    assert len(calls) == 4
    assert all(item["provider_request_id"] == "req-malformed" for item in captured.value.attempt_log)
    assert all(item["token_usage"] == {"prompt_tokens": 7} for item in captured.value.attempt_log)
    assert all(item["key_slot"] == "primary" for item in captured.value.attempt_log)
