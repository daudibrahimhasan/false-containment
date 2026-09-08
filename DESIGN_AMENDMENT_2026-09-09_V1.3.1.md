# Design Amendment: Preregistration v1.3.1

Date: 2026-09-09

Status: frozen as `preregistration-v1.3.1` on 2026-09-09; pilot in progress, no verifier calls.

The frozen v1.3.0 pilot stopped before producing a trajectory because its infrastructure-failure logger assumed provider error bodies were JSON objects. A provider returned a JSON list in an HTTP 403 response, causing the logger itself to raise an `AttributeError` before the failure could be recorded. No scientific trajectory, verifier call, or outcome was produced by that failed call.

This patch only makes error logging robust to non-object JSON error bodies. It does not change provider routing, fallback eligibility, request payloads, models, prompts, simulator semantics, evidence conditions, metrics, or the 192-judgment design. v1.3.0 remains preserved as the prior frozen audit point. The v1.3.1 pilot uses a new versioned output directory and may reuse only artifacts whose v1.3.1 manifest and hashes match exactly.
