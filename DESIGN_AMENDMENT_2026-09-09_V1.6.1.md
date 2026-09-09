# Operational Amendment: Preregistration v1.6.1

Date: 2026-09-09

The v1.6 direct DeepSeek `deepseek-v4-flash` pilot returned reasoning tokens and malformed or truncated JSON at the 1,400-token cap. Version 1.6.1 uses DeepSeek's supported `reasoning_effort=low` control and raises only Agent 1's completion cap to 4,096 tokens so reasoning and the required JSON response can fit.

Agent 2, the shared prompt, simulator, evidence conditions, deterministic ground truth, metrics, 192-judgment design, verifier configuration, and unchanged 32-packet subset remain unchanged. The fresh pilot starts from an empty v1.6.1 directory, reuses no prior trajectory, and makes zero verifier calls.
