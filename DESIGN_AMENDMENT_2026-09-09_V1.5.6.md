# Operational Amendment: Preregistration v1.5.6

Date: 2026-09-09

The v1.5.5 GLM pilot continued to consume the complete 1,400-token cap as reasoning and returned no text content. Version 1.5.6 raises only Agent 1's completion cap to 4,096 tokens so the model has room for both reasoning and the required JSON action response. The low reasoning-effort setting remains unchanged.

This is a model-serving compatibility correction. Agent 2, prompts, simulator, evidence conditions, deterministic ground truth, metrics, 192-judgment design, verifier configuration, and unchanged 32-packet subset are unchanged. The fresh pilot starts from an empty v1.5.6 directory, reuses no prior trajectory, and makes zero verifier calls.
