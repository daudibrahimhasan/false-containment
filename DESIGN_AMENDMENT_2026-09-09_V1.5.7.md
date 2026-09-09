# Operational Amendment: Preregistration v1.5.7

Date: 2026-09-09

The v1.5.6 GLM pilot still returned reasoning-only responses at the 4,096-token cap. Version 1.5.7 removes only the `response_format` request field for TokenRouter, because that provider/model route exposes text chat but did not produce a text answer under the forced structured-output request. The shared prompt still requires valid JSON and the parser still rejects malformed or non-JSON output.

Agent 2, prompts, simulator, evidence conditions, deterministic ground truth, metrics, 192-judgment design, verifier configuration, and unchanged 32-packet subset remain unchanged. The fresh pilot starts from an empty v1.5.7 directory, reuses no prior trajectory, and makes zero verifier calls.
