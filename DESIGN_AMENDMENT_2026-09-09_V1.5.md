# Design Amendment: Preregistration v1.5

Date: 2026-09-09

Status: frozen as `preregistration-v1.5.0` on 2026-09-09; fresh response-agent pilot required; no verifier calls.

## Reason for amendment

The DeepSeek response-agent pilot did not satisfy the locked pilot gate. Its access-control intended-resolved trajectory produced environment-derived `unresolved` ground truth because the model selected an incomplete remediation sequence. The read-only diagnosis found no simulator, parser, schema, one-shot-interface, retry, or served-model implementation defect. This was a model-behavior failure.

Agent 1 is therefore replaced with the preselected GLM-5.3-free candidate:

- provider: TokenRouter
- model: `z-ai/glm-5.3-free`
- API key environment variable: `AGENT_1_API_KEY_PRIMARY`
- endpoint: `https://api.tokenrouter.com/v1/chat/completions`

The new Agent 1 uses the same shared agent prompt, temperature, maximum tokens, and disabled-thinking setting as the replaced Agent 1. Agent 2 remains Gemini `gemini-3.7-flash` with its existing primary/fallback policy. Qwen and Nemotron remain configured but are not called during this pilot.

## Scope boundary

This amendment changes only the Agent 1 model/provider selection and the requirement to run a fresh 16-call pilot. It does not change the four incident families, eight simulator setups, simulator semantics, prompts, evidence ladder, deterministic ground truth, metrics, 192-judgment design, verifier configuration, or frozen 32-packet secondary subset. The existing DeepSeek pilot artifacts remain preserved as historical data and are not reused as GLM trajectories.

The v1.5 pilot must start in a new versioned output directory and complete 16 logical calls: eight GLM-5.3-free trajectories and eight Gemini trajectories. It generates 64 evidence packets, makes zero verifier calls, and may not reuse any DeepSeek trajectory. The existing pilot gate is applied unchanged to the fresh final-state labels and evidence integrity checks.

