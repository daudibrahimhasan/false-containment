# Design Amendment: Preregistration v1.3

Date: 2026-09-09

Status: frozen as `preregistration-v1.3.0` on 2026-09-09; pilot in progress, no verifier calls.

The preregistration-v1.2.0 pilot completed one Agent 1 trajectory, then Agent 2 returned HTTP 403 after the fixed retry policy. No Gemini 3.7 Flash trajectory, primary-verifier judgment, secondary-verifier judgment, Qwen call, or Nemotron call was produced.

This amendment adds a second Google Gemini API key as infrastructure fallback for Agent 2. It does not add or replace a model. Both key slots call the exact same Google Gemini endpoint with model `gemini-3.7-flash`, the byte-identical shared prompt and request payload, no temperature or top-p override, `max_tokens=1400`, and `reasoning_effort=low`.

Agent 2 key slots:

- Primary: `AGENT_2_API_KEY_PRIMARY`
- Fallback: `AGENT_2_API_KEY_FALLBACK`

The primary key receives the existing fixed policy of one initial attempt plus three retries, with 2, 4, and 8 second backoff and a 120 second timeout per attempt. Fallback is permitted only after every primary attempt fails for an eligible quota or temporary-service condition: HTTP 429, HTTP 503, quota exhaustion, resource exhaustion, service unavailable, or temporary unavailability. A noneligible failure, including HTTP 403, does not activate fallback. A malformed or scientifically undesirable model response does not activate fallback.

When eligible, fallback receives the same fixed attempt, timeout, and backoff policy for the exact same serialized request body. The first valid successful response from either slot becomes the one scientific trajectory. Responses are never combined, and primary and fallback attempts never count as separate trajectories. If both slots exhaust the allowed policy, the logical call is saved as infrastructure-failed and pending without a scientific outcome or model substitution.

Every attempt record contains only the key slot name, attempt number, status, HTTP status where available, failure reason, latency, scheduled retry backoff where applicable, token usage where available, and provider request ID where available. Actual API key values are never stored or printed.

Only this Agent 2 credential-routing behavior changes. The provider, endpoint, model identity, prompt, generation settings, cases, simulator, matched strata, evidence conditions, verifier prompt, primary and secondary verifiers, metrics, 192-judgment design, fixed 32-packet subset, stress tests, exclusions, and stopping rules remain unchanged.
