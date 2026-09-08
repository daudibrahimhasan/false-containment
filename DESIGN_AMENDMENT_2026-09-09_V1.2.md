# Design Amendment: Preregistration v1.2

Date: 2026-09-09

This amendment was made before any primary-verifier judgment and before any Qwen or Nemotron scientific call.

The preregistration-v1.1.0 response-agent pilot could not complete because Agent 2, `gemini-3.8-flash`, repeatedly returned HTTP 429 after the full preregistered retry policy. This is treated as an infrastructure and quota limitation, not as a scientific task failure. No primary-verifier data existed when the replacement was chosen, and no v1.2 scientific outcome had been observed.

Agent 2 is replaced as follows:

- Previous provider and model: Gemini, `gemini-3.8-flash`
- New provider and model: Gemini, `gemini-3.7-flash`

Gemini 3.7 Flash was selected before observing any v1.2 scientific outcome. Its endpoint, role-specific API-key environment variable, maximum completion-token limit, low thinking level, absence of temperature and top-p overrides, and fixed retry policy remain the same as the v1.1 Agent 2 configuration.

Only Agent 2 model identity changed. Agent 1, all incident families and matched setups, simulator semantics, hidden mechanisms, shared one-shot agent prompt, evidence conditions, verifier prompt, primary verifier, secondary verifier, metrics, 192-judgment design, fixed 32-judgment secondary subset, stress tests, intended strata, exclusions, and stopping rules remain unchanged.

The v1.2 response-agent pilot starts fresh in a versioned output directory. No v1.0 or v1.1 trajectory may be reused. Before the first v1.2 provider call, a manifest must bind the pilot to the frozen preregistration, configuration, prompt, incident specifications, simulator, exact model parameters, Git commit and tag, and the planned 16 logical pilot IDs. Any hash mismatch blocks cache reuse.
