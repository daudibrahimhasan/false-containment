# Post-run errata and provenance notes

This document describes operational and interpretation notes for the completed `core_v1.6.1` results. It does not rewrite or amend the frozen `preregistration-v1.6.1` tag.

## Final provider configuration

The completed run used:

- Response Agent 1: direct `deepseek-v4-flash`.
- Response Agent 2: `gemini-3.7-flash`.
- Primary verifier: `qwen-max`.
- Secondary verifier: `nvidia/nemotron-3-super-120b-a12b`.

Earlier NVIDIA DeepSeek, GLM, and other provider attempts remain historical. They are not the source of the completed `core_v1.6.1` results.

## Primary ordering deviation

The preregistered design specified fixed-seed randomization using seed `20260909`. The completed `run-primary` execution instead processed the fixed job-plan/construction order because that execution path did not apply the preregistered shuffle. Packet contents, deterministic truth assignment, verifier prompt, blinding, and recorded judgments were unchanged.

This was verified against `src/falsecontain/terminal_runner.py`: `_job_plan` constructs jobs in case, agent, evidence, and replicate order and does not call the shuffle used by the legacy pipeline path.

## E4 scope

E4 tests one mechanism-specific critical persistence path per family:

- Credential: session/persistence check.
- Execution: scheduled-job check.
- Access control: privileged-role binding check.
- Alternate path: relay/path check.

E4 is therefore a family-specific critical-path operational check. Ground truth is computed from deterministic final simulator state using a conjunction of security postconditions, so E4 is not equivalent to exposing the full ground-truth evaluator.

## Stress-test scope

The stress arm is exploratory and fixture-driven (`n=4`). Narrow checks are executable simulator operations, whereas the broader evidence is fixture-defined rather than an executable production-wide broad verification test. The 4/4 result is not a prevalence estimate or universal validation.

Source: [stress rows](../outputs/stress_scientific/results/rows.csv) and [stress metrics](../outputs/stress_scientific/results/metrics.json).

## Secondary packet-ID translation

The historical frozen subset contains packet IDs with the DeepSeek NIM identifier. Those IDs map one-to-one to the corresponding v1.6.1 direct-API `deepseek-v4-flash` packets at runtime. This is identifier translation only. The selected cases, evidence levels, subset composition, and subset hash were not changed.

Source: [frozen subset](../config/secondary_subset.json), [secondary rows](../outputs/primary_runs/core_v1.6.1/secondary_verifier/results/rows.csv), and [run manifest](../outputs/primary_runs/core_v1.6.1/manifest.json).

## Stale preregistration instructions

The frozen preregistration retains historical v1.5/GLM execution text as part of its immutable lineage. Those instructions should not be used to reproduce `core_v1.6.1`. Use the committed manifest, `docs/FINAL_RESULTS.md`, and the current README for the completed run.

## Canonical execution path

`run-primary` produced the completed `core_v1.6.1` terminal artifacts. The overlapping legacy `run` path is retained for historical compatibility and should not be used to recreate the completed run.

