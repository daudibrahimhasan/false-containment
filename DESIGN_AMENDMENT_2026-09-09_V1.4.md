# Design Amendment: Preregistration v1.4

Date: 2026-09-09

Status: frozen as `preregistration-v1.4.0` on 2026-09-09; pilot gate passed offline, no verifier calls.

The frozen v1.3.1 pilot completed all 16 logical response-agent trajectories and generated 64 evidence packets. It made zero Qwen and Nemotron calls. Invalid actions, served-model mismatches, E4 correctness, leakage, and artifact integrity all passed. One intended-resolved DeepSeek access-control setup produced environment-derived unresolved ground truth because the model chose an incomplete remediation plan. The read-only diagnosis found no implementation bug, parser or schema bug, one-shot interface ambiguity, truncation, retry contribution, or served-model mismatch. The model intentionally omitted termination and primary-token revocation.

This amendment changes only the pilot completion gate. The previous gate required every response-agent trajectory to match its intended setup stratum. The completed pilot demonstrates that a valid response agent can fail remediation in an environment configured to permit genuine resolution. Requiring every intended-resolved setup to become resolved would encourage rerunning or selecting trajectories until a desired outcome appears, which would undermine environment-derived ground truth and introduce outcome-selection bias.

The v1.4 gate therefore evaluates benchmark integrity and class coverage rather than requiring every agent trajectory to match its intended setup label. Intended setup remains an environment-design stratum. Final scientific labels remain exclusively the deterministic labels computed from each trajectory's final simulator state.

This amendment is made before any primary-verifier or secondary-verifier scientific judgment. It does not change the four families, setup strata, response-agent models, prompt, simulator semantics, evidence conditions, verifier prompt, metrics, abstention treatment, randomization, fixed secondary subset, stress tests, or the 192-judgment design.
