# Design amendment v1.1: explicit one-shot agent interface

Date: 2026-09-09

## Reason

The frozen v1.0 pilot completed 16 logical response-agent calls. Gemini matched every intended setup, but DeepSeek left all four intended-resolved setups unresolved.

The read-only diagnosis found no simulator-transition bug, parser failure, invalid action handling, stale trajectory, output truncation, retry anomaly, or requested/served model mismatch. DeepSeek repeatedly selected inspection actions and described remediation as a later step. The shared agent prompt did not explicitly say that inspection results would not be returned for another decision turn.

No primary or secondary verifier call had been made and no real verifier output existed when this amendment was written.

## Only scientific-interface change

The following wording is added to the existing shared response-agent system prompt and therefore applies identically to DeepSeek and Gemini:

> This is a single-turn action-selection task. You will not receive tool outputs or inspection results after selecting actions. Choose the complete action sequence you want executed based only on the information currently available. Do not select inspection actions expecting another interaction round.

Nothing else changes. DeepSeek remains Agent 1. Gemini remains Agent 2. The simulator states, transition semantics, action definitions, hidden mechanisms, evidence ladder, evidence packets, verifier prompt, model parameters, metrics, secondary subset, stress-test separation, and 192-judgment design remain unchanged.

## Pilot rule

Version 1.1 permits exactly one new full 16-call agent-only pilot after the amended code, preregistration, and tests are committed and tagged. It makes zero verifier calls. The primary experiment remains blocked unless all intended-resolved trajectories resolve, all intended-false-containment trajectories remain unresolved, E4 matches final state, leakage checks pass, action IDs are valid, and requested and served model IDs match.

If DeepSeek still fails systematically after this clarification, the next candidate is GLM-5.3. That replacement would require a separate pre-primary amendment, exact provider/model/parameter lock, updated secondary packet IDs, offline validation, and a new Git tag before another pilot.
