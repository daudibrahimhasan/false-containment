# Design Amendment: Preregistration v1.6

Date: 2026-09-09

The GLM-5.3-free Agent 1 pilot was stopped before producing any trajectory. Across the frozen GLM attempts, TokenRouter returned HTTP 200 responses with reasoning tokens consuming the full completion budget and no text `message.content`. The retries produced no evidence packets and no verifier calls. The route was not usable for the response-agent role.

Agent 1 is replaced with the Option B direct DeepSeek endpoint:

- provider: DeepSeek direct API
- model: `deepseek-v4-flash`
- endpoint: `https://api.deepseek.com/v1/chat/completions`
- API key environment variable: `DEEPSEEK_1`

This is a model/provider substitution only. Agent 2 Gemini, Qwen, Nemotron, the shared prompt, simulator, evidence conditions, deterministic ground truth, metrics, 192-judgment design, and frozen 32-packet secondary subset remain unchanged. The v1.6 pilot must start from an empty versioned directory, make 16 fresh response-agent calls, and make zero verifier calls. No DeepSeek NIM or GLM trajectory may be reused.
