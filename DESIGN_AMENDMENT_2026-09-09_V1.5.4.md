# Operational Amendment: Preregistration v1.5.4

Date: 2026-09-09

The v1.5.3 GLM pilot still returned reasoning-only responses because GLM-5.3 always enables reasoning and does not honor the disabled-thinking control used by the replaced model. The provider's supported control is a reasoning-effort level. Version 1.5.4 therefore sends `chat_template_kwargs.reasoning_effort=low` for Agent 1.

This changes only the GLM-specific generation control required for a valid text response. The model ID, shared agent prompt, simulator, evidence conditions, deterministic ground truth, metrics, 192-judgment design, Gemini configuration, verifier configuration, and unchanged 32-packet subset remain unchanged. The fresh pilot starts from an empty v1.5.4 directory, reuses no prior trajectory, and makes zero verifier calls.
