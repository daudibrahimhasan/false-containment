# Operational Amendment: Preregistration v1.5.5

Date: 2026-09-09

The v1.5.4 GLM pilot still returned reasoning-only responses through TokenRouter. Version 1.5.5 sends the same declared `reasoning_effort=low` value both as the top-level OpenAI-compatible field and inside `chat_template_kwargs`, covering the provider's supported request paths.

This is a transport-only correction. The model, prompt, simulator, evidence conditions, deterministic labels, metrics, 192-judgment design, Gemini configuration, verifier configuration, and unchanged 32-packet subset remain unchanged. The pilot starts from an empty v1.5.5 directory, reuses no earlier trajectory, and makes zero verifier calls.
