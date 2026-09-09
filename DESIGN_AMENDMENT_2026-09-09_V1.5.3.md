# Operational Amendment: Preregistration v1.5.3

Date: 2026-09-09

The v1.5.2 GLM pilot showed that TokenRouter returned only reasoning tokens and no text content because the existing request builder applied the declared disabled-thinking control only to NVIDIA requests. This is an implementation/provider-routing mismatch, not a scientific outcome.

Version 1.5.3 applies the same existing `thinking=false` request control to TokenRouter. The shared prompt, model ID, temperature, maximum tokens, simulator, evidence conditions, metrics, 192-judgment design, and unchanged 32-packet subset are not changed. The malformed-response handling from v1.5.2 remains. The fresh pilot starts from an empty v1.5.3 directory, reuses no DeepSeek or failed GLM trajectory, and makes zero verifier calls.
