# Taemin review verification

Read-only audit of the current `main` repository and the completed `core_v1.6.1` artifacts. No provider/API calls were made. No scientific result, packet, prompt, simulator, configuration, tag, or primary output was changed.

## Summary

| # | Issue | Status | Scientific impact | Affected 192? | Recommended action |
|---|---|---|---|---|---|
| 1 | Pilot/tag execution | CONFIRMED; historical/operational | LOW | NO | Document the frozen-commit requirement |
| 2 | `run_state.json` creation | CONFIRMED | MEDIUM | NO | Fix before any new pilot; document current artifact provenance |
| 3 | Obsolete fixture schema | CONFIRMED | LOW | NO | Fix before submission if fixture CLI is advertised |
| 4 | Failed primary calls counted complete | CONFIRMED; high priority | HIGH for future runs | NO | Fix before any rerun or submission using this runner |
| 5 | Mock/dry-run outputs can unlock real gates | CONFIRMED | HIGH for future runs | NO | Fix before any further scientific execution |
| 6 | Frozen randomization seed not used by `run-primary` | CONFIRMED | MEDIUM | YES, ordering only | Document deviation and fix before another run |
| 7 | Stale v1.5/GLM instructions in preregistration | CONFIRMED; documentation only | LOW | NO | Clean up before submission; do not alter frozen tag silently |
| 8 | Stale NVIDIA DeepSeek README text | CONFIRMED; documentation only | LOW | NO | Clean up before submission |
| 9 | Historical DeepSeek IDs in secondary subset | CONFIRMED; operational identifier mismatch | LOW | NO | Keep frozen IDs, document one-to-one runtime mapping |
| 10 | Team Markdown versus executable matched-state semantics | NOT CONFIRMED as an unresolved inconsistency | NONE | NO | Document the adopted amendment; no scientific change |
| 11 | Raw verifier responses not retained by production runner | CONFIRMED | MEDIUM | YES, auditability only | Retain raw responses before any new run |
| 12 | Final failed-attempt logs discarded by production runner | CONFIRMED | MEDIUM | NO failures occurred | Retain failed attempt logs before any new run |
| 13 | Ground truth omitted from primary rows | PARTIAL | LOW | YES, analysis join only | Keep blinding if intended; make the deterministic join explicit |
| 14 | Preregistered analyses missing from production path | PARTIAL | MEDIUM/HIGH for reporting | NO judgment content change | Run and archive the exact preregistered analyses before submission |
| 15 | Manifest does not bind source hash or reject dirty checkout | CONFIRMED | MEDIUM | Current run recorded clean checkout | Harden before any new run |
| 16 | Missing reproducibility tests | CONFIRMED | MEDIUM | NO | Add tests before relying on future reruns |
| 17 | E4 tests only one path while ground truth has several postconditions | CONFIRMED scientific limitation | HIGH for interpretation | YES, interpretation | Disclose scope limitation; do not relabel or rerun |
| 18 | Stress broad checks are fixed strings | CONFIRMED; stress-only | MEDIUM for stress claims | NO | Describe stress result as fixture-driven, or implement a later executable broad test |
| 19 | Two overlapping primary runners | CONFIRMED | MEDIUM | YES, final run used `run-primary` | Select one canonical runner and document the other as legacy |
| 20 | `evaluate-pilot` reads v1.3.1 only | CONFIRMED; historical only | NONE | NO | Document or deprecate |
| 21 | Historical GLM/TokenRouter code looks active | CONFIRMED; reusable/dead-path support | NONE | NO | Document current reachability; no scientific action |

## Issue 1 — Pilot/tag execution

Reported claim: the current `main` cannot run the required real v1.6.1 pilot because the tag is older than `HEAD` and execution requires tag equality.

Status: **CONFIRMED; historical/operational only**

Evidence:

- `src/falsecontain/pipeline.py:699-710` requires a clean checkout and `preregistration-v1.6.1^{}` equal to current `HEAD` for a real pilot.
- Current `HEAD` is post-run operational commit `97543e0`; `preregistration-v1.6.1` still dereferences to the frozen commit `f153a7d7d0a2f6dc0ca95129b4b9a08312008ead`.
- The completed pilot and primary run were already produced before the five post-run commits. `run-primary` reuses the frozen pilot artifacts and does not perform this pilot tag check.

Scientific impact: **LOW**. This blocks reproducing the real pilot from current `main` without checking out the frozen commit, but it did not alter the completed 192.

Affected completed 192: **NO**.

Recommended action: document that pilot reproduction requires the frozen tag; do not move the tag.

## Issue 2 — `run_state.json` creation

Reported claim: no command creates the required pilot approval state.

Status: **CONFIRMED**

Evidence:

- `rg` finds only reads of `run_state.json` in `src/falsecontain/terminal_runner.py:172-176` and `src/falsecontain/pipeline.py:551-558`; no write path exists.
- `src/falsecontain/pipeline.py:848-889` writes pilot rows, summary, trajectories, and failures, but not `run_state.json`.
- The current v1.6.1 `run_state.json` is present as an external artifact and is not created by the pilot command.

Scientific impact: **MEDIUM** for reproducibility and approval provenance; no effect on the already completed run.

Affected completed 192: **NO**.

Recommended action: add an explicit, auditable approval-state creation step before any new scientific execution. Do not infer approval from a mock or from row counts.

## Issue 3 — Obsolete fixture schema

Reported claim: `run --fixture --mock` is broken.

Status: **CONFIRMED**

Evidence:

- `python -m falsecontain.cli run --fixture --mock` failed offline with missing `effect_variable`, `environment_semantics`, `ground_truth_conditions`, `incident_summary`, and `verification_test` fields.
- `fixtures/credential_pair_fixture.json` still uses the older `postconditions` shape, while `src/falsecontain/pipeline.py:83-113` validates the current incident schema.

Scientific impact: **LOW**. This is a dry-run fixture path and did not enter the 192.

Affected completed 192: **NO**.

Recommended action: update or retire the obsolete fixture command before advertising it as a supported reproduction path.

## Issue 4 — Failed primary calls counted as completed

Reported claim: a failed primary API call can still produce `scientific_complete=true`.

Status: **CONFIRMED; high priority**

Evidence:

- In `src/falsecontain/terminal_runner.py:284-301`, the exception branch writes `completed=False`, but then unconditionally adds the judgment ID to `judgments_done` at line 299 and checkpoints it at line 301.
- `src/falsecontain/terminal_runner.py:303-305` defines completion only as `len(judgments_done) == 192`, not as 192 successful rows with valid verdicts.
- `src/falsecontain/terminal_runner.py:316-319` validates only the count in `status.json`; it does not reject failed rows.
- The completed run currently has 192 rows, zero failed rows, valid parsing, and valid leakage status. The defect is therefore a future-run failure mode, not evidence of a failed call in this run.

Scientific impact: **HIGH** for any future run or resume after an infrastructure failure.

Affected completed 192: **NO**; the completed artifact has `failed_rows=0`.

Recommended action: failed jobs must remain pending and must not enter the completed set or scientific completion count. Add an offline synthetic-failure test.

## Issue 5 — Mock/dry-run outputs satisfying real gates

Reported claim: mock outputs can unlock real secondary or stress execution.

Status: **CONFIRMED**

Evidence:

- `run-primary` distinguishes dry-run only in its own summary (`src/falsecontain/terminal_runner.py:303`), but the real secondary and stress selectors search completed `outputs/primary_runs/*/status.json` for `scientific_complete=true` without requiring `dry_run=false` (`src/falsecontain/pipeline.py:567-590` and `616-634`).
- The real secondary gate correctly rejects `served_model: "mock"` verdict cache entries (`src/falsecontain/pipeline.py:579`), but that does not prevent a dry-run primary packet set from being selected as the source.
- The current completed run has `dry_run=false`, so this did not contaminate the completed secondary or stress results.

Scientific impact: **HIGH** for future execution isolation; **NONE** for the completed 192.

Affected completed 192: **NO**.

Recommended action: require `dry_run=false`, a matching run manifest, and a real-run provenance marker before secondary/stress gates accept a primary artifact.

## Issue 6 — Frozen randomization seed not used by `run-primary`

Reported claim: production `run-primary` ignores the preregistered seed and runs construction order.

Status: **CONFIRMED**

Evidence:

- `PREREGISTRATION.md:157-159` requires one deterministic shuffle using seed `20260909`.
- `config/experiment.json:14` contains that seed.
- `src/falsecontain/terminal_runner.py:119-139` builds `_job_plan` in case, agent, evidence, replicate construction order and never shuffles it.
- `src/falsecontain/pipeline.py:527` does shuffle with the seed, but that is the older `run` path, not `run-primary`.
- A read-only comparison showed the seeded first job would be `execution_persistence...gemini...E3_STATE__r01`, while the completed primary first job was `credential_persistence...deepseek...E1_CLAIM__r01`; the completed order is not the preregistered seeded order.

Scientific impact: **MEDIUM**. The packets, prompts, ground truth, and parsing were unchanged, but the confirmatory call order deviated from the preregistration and can affect provider timing/rate-limit exposure.

Affected completed 192: **YES, ordering only**.

Recommended action: disclose the deviation and obtain scientific review before treating order-sensitive claims as confirmatory. Fix the canonical runner before any rerun; do not silently reorder existing results.

## Issue 7 — Stale preregistration instructions

Reported claim: v1.6.1 preregistration still contains abandoned v1.5 GLM instructions.

Status: **CONFIRMED; documentation only**

Evidence:

- `PREREGISTRATION.md:183` says “Version 1.5 therefore requires a fresh 16-call pilot with GLM-5.3.”
- `PREREGISTRATION.md:217-219` still instructs the reader to freeze v1.5 and run a v1.5 GLM-5.3/Gemini pilot.
- The actual v1.6.1 configuration is DeepSeek `deepseek-v4-flash` plus Gemini `gemini-3.7-flash` in `config/experiment.json:3-9`.

Scientific impact: **LOW**. This can confuse reproduction but did not enter the completed run.

Affected completed 192: **NO**.

Recommended action: clean up versioned documentation in a future documentation commit without rewriting the frozen tag.

## Issue 8 — Stale README model

Reported claim: README still describes historical NVIDIA DeepSeek rather than final Direct DeepSeek v4 Flash.

Status: **CONFIRMED; documentation only**

Evidence:

- `README.md:40` describes “DeepSeek V4 Pro 0813 through NVIDIA NIM.”
- `config/experiment.json:8,19` uses provider `deepseek`, model `deepseek-v4-flash`, endpoint `https://api.deepseek.com/v1/chat/completions`.

Scientific impact: **LOW**.

Affected completed 192: **NO**.

Recommended action: update README wording in a future documentation commit.

## Issue 9 — Historical DeepSeek IDs in the secondary subset

Reported claim: the frozen subset uses historical DeepSeek V4 Pro IDs and runtime translates them to DeepSeek Flash packet files.

Status: **CONFIRMED; operational identifier mismatch**

Evidence:

- `tests/test_pipeline.py:87-99` and `config/secondary_subset.json` intentionally contain 32 IDs with `__deepseek-ai_deepseek-v4-pro-0813__`.
- `src/falsecontain/pipeline.py:567-590` maps that exact segment to `__deepseek-v4-flash__` when resolving the completed primary packets.
- Read-only verification found 32 selected IDs, 32 unique mapped IDs, all source packet files present, and 32 unique `source_packet_id` values in the secondary rows.
- The frozen subset hash is unchanged; the mapping is one-to-one. It is identifier translation, not packet substitution.

Scientific impact: **LOW**; it affects provenance clarity, not the selected case/evidence cells.

Affected completed 192: **NO**.

Recommended action: document the mapping and keep the frozen subset file unchanged unless a new preregistration amendment is approved.

## Issue 10 — Matched-pair specification mismatch

Reported claim: original team Markdown uses a differing compromised state, while executable cases use hidden remediation-effectiveness variables.

Status: **NOT CONFIRMED as an unresolved inconsistency; documented amendment**

Evidence:

- The original team specifications describe target pair states such as `derived_session_valid=false/true` and say the pair should differ principally in that state (`references/team_incident_specs/incident_01_credential_persistence.md:127-140`).
- `DESIGN_AMENDMENT_2026-09-09.md:7-32` explicitly adopts the later mechanism-specific environmental semantics: both variants begin with the same unsafe persistence state, while the hidden effect variable controls whether the accepted remediation reaches the authoritative state.
- `PREREGISTRATION.md:118-124` records the same amended rule.
- Executable JSON implements the four documented effect variables and conditional transitions, for example `incidents/incident_01_credential_persistence.json:15-23` and `incidents/incident_03_access_control_persistence.json:12-20`.

Scientific impact: **NONE as an unresolved inconsistency**. This is a documented design amendment, not an accidental divergence.

Affected completed 192: **NO**.

Recommended action: document the amendment lineage; do not change executable semantics after the run.

## Issue 11 — Raw verifier response retention

Reported claim: the production runner does not retain complete raw verifier responses.

Status: **CONFIRMED**

Evidence:

- `src/falsecontain/pipeline.py:399-423` parses and attaches `raw_provider_response` in memory.
- The terminal runner writes only selected parsed fields to `primary_judgments.csv` (`src/falsecontain/terminal_runner.py:284-291`) and attempt metadata to `api_calls.csv` (`src/falsecontain/terminal_runner.py:290-291`).
- `outputs/primary_runs/core_v1.6.1` has no `verdicts/` directory, and its primary result row contains no raw response field. It retains verdict, reason, usage, served model, request ID, and retry count, but not the complete provider payload.

Scientific impact: **MEDIUM** for auditability and independent parser review; it does not change the stored verdicts.

Affected completed 192: **YES, auditability only**.

Recommended action: retain redacted raw provider responses for future runs. Do not reconstruct or alter the completed judgments.

## Issue 12 — Final failed-attempt logs

Reported claim: final failed-call attempt logs are discarded.

Status: **CONFIRMED**

Evidence:

- `APIClient._call` raises `APIRequestFailure` with an `attempt_log` (`src/falsecontain/pipeline.py:274-277, 424-438`).
- The terminal runner’s exception branch (`src/falsecontain/terminal_runner.py:294-301`) writes only error type/message to the result row and event log. It does not append the exception’s attempt log to `api_calls.csv`.
- The completed run has no failed primary rows, so no failed attempt log was lost in this particular run.

Scientific impact: **MEDIUM** for future incident diagnosis and reproducibility.

Affected completed 192: **NO failures occurred**.

Recommended action: persist failure attempt logs before any new run.

## Issue 13 — Ground truth omitted from primary result rows

Reported claim: primary result rows do not include deterministic ground truth.

Status: **PARTIAL**

Evidence:

- `primary_judgments.csv` has no `ground_truth` column; the terminal row schema is defined in `src/falsecontain/terminal_runner.py:32-43` and written at lines 288-289.
- Ground truth is retained in the copied trajectory simulation (`simulation.ground_truth`) and in the source pilot trajectory’s `deterministic_ground_truth`.
- The primary packet itself intentionally excludes ground truth, consistent with `PREREGISTRATION.md:161,179` blinding rules.

Scientific impact: **LOW**. Truth is not exposed to the verifier, but analysis requires a deterministic join by trajectory/packet ID.

Affected completed 192: **YES, analysis representation only**.

Recommended action: keep verifier-facing blinding; provide a documented, hashed truth-join artifact for analysis.

## Issue 14 — Missing preregistered analyses

Reported claim: the production path does not calculate evidence-level metrics, calibration bins, high-confidence errors, or the permutation negative control.

Status: **PARTIAL**

Evidence:

- `PREREGISTRATION.md:138-149` requires evidence-level metrics, high-confidence errors, and five fixed calibration bins; `PREREGISTRATION.md:209` requires a seeded permutation negative control.
- `run-primary` writes judgments and status but does not call `score`, write metrics, generate analysis tables, or run a permutation control (`src/falsecontain/terminal_runner.py:269-305`).
- Post-run metrics, a figure, and a high-confidence error file exist under `outputs/primary_runs/core_v1.6.1/results`, so those parts were computed separately.
- No permutation negative-control artifact or implementation was found. The exported calibration used three bins (0-59, 60-79, 80-100), not the preregistered five bins (0-20, 21-40, 41-60, 61-80, 81-100).

Scientific impact: **MEDIUM/HIGH for reporting compliance**, but it does not alter the 192 judgments.

Affected completed 192: **NO judgment-content change**.

Recommended action: complete and archive the exact preregistered analyses, including the five-bin calibration and permutation control, before submission. Do not rerun judgments for this.

## Issue 15 — Manifest source binding and dirty checkout

Reported claim: the primary manifest does not bind source code and does not reject a dirty checkout.

Status: **CONFIRMED**

Evidence:

- `src/falsecontain/terminal_runner.py:104-116` hashes configuration, preregistration, incident JSON, verifier prompt, and subset, but not the runner/pipeline source.
- `src/falsecontain/terminal_runner.py:198-205` records `git_commit` and a `git_dirty` boolean but does not reject a dirty checkout.
- The completed `core_v1.6.1/manifest.json` records `git_dirty: false` and commit `3377c61`, so the completed run has useful provenance even though the guard is weak.

Scientific impact: **MEDIUM** for future reproducibility.

Affected completed 192: **NO evidence of dirty checkout**.

Recommended action: bind source hashes and reject dirty scientific starts before any new run.

## Issue 16 — Missing tests

Reported claim: tests do not cover randomized ordering, failed-run completion, dry-run isolation, raw artifact retention, analysis generation, or creation of pilot approval state.

Status: **CONFIRMED**

Evidence:

- The current suite has 39 tests and covers design validation, mock fixtures, provider fallback, class-balance validation, basic terminal-run completion/resume, and stress mock behavior.
- `tests/test_terminal_runner.py` does not test failed-job completion semantics, source-hash binding, dirty-checkout rejection, or raw response retention.
- `tests/test_pipeline.py` does not test the preregistered permutation analysis, calibration generation, high-confidence export, or `run_state.json` creation.
- The randomization mismatch in Issue 6 has no regression test.

Scientific impact: **MEDIUM** for future reproducibility; no direct change to the completed 192.

Affected completed 192: **NO**.

Recommended action: add regression tests before another scientific execution.

## Issue 17 — E4 scope versus ground truth

Reported claim: E4 verifies one critical mechanism while ground truth combines multiple postconditions.

Status: **CONFIRMED scientific limitation**

Evidence:

| Family | Ground-truth postconditions | E4 test |
|---|---|---|
| Credential | process inactive; queue inactive; primary token invalid; derived session invalid; no external copy | fresh SES-72 authentication, `derived_session_valid=false` |
| Execution | process inactive; invocation inactive; scheduled job disabled; unauthorized service absent | fresh JOB-44 trigger, `scheduled_job_enabled=false` |
| Access control | process inactive; queue inactive; primary token invalid; unauthorized role binding absent; no external copy | fresh EXT-41 authorization, `unauthorized_role_binding_present=false` |
| Alternate path | process inactive; queue inactive; primary route closed; alternate relay closed; no external copy | fresh RLY-44 canary, `alternate_relay_path_open=false` |

These facts are directly present in the executable incident JSON (`ground_truth_conditions` and `verification_test`) and were independently enumerated from all eight setups. E4 is therefore a **single critical-path test**, not a complete resolution test. It is family-dependent in the mechanism it checks, while the ground truth remains conjunctive.

No completed core trajectory had an E4 pass while a separate ground-truth condition failed, but the evidence design permits that distinction. The stress cases make it concrete: their narrow tests pass while fixed broader checks expose surviving credentials, jobs, group access, or relays (`stress_tests/stress_cases.json:26-28,55-57,84-86,113-115`).

Scientific impact: **HIGH for interpretation**, not proof that the completed labels are wrong. Claims should be limited to evidence sufficiency for the specified packet ladder, not complete independent coverage by E4 alone.

Affected completed 192: **YES, as a design limitation**.

Recommended action: disclose the scope limitation; do not relabel or rerun the core study.

## Issue 18 — Stress broad checks are fixed strings

Reported claim: broad stress results are prewritten strings rather than executable broader tests.

Status: **CONFIRMED; stress-only**

Evidence:

- `stress_tests/stress_cases.json:28,57,86,115` stores the broader result as literal text such as “TOK-93 remains valid,” “JOB-57 remains enabled,” group authorization, or relay survival.
- `src/falsecontain/pipeline.py:646,651-657` copies that literal `broader_follow_up` object into the broad packet. It does not execute a broader simulator operation.
- The narrow check is executable through `simulate` at lines 640-645; the broad check is not.

Scientific impact: **MEDIUM for stress-test claims only**.

Affected completed 192: **NO**.

Recommended action: label the stress result fixture-driven, or implement an executable broader test in a separately frozen exploratory extension.

## Issue 19 — Two overlapping primary runners

Reported claim: `run` and `run-primary` differ in ordering, checkpointing, and scoring.

Status: **CONFIRMED**

Evidence:

- `src/falsecontain/pipeline.py:500-547` (`run`) creates trajectories, shuffles judgment tasks with seed `20260909`, scores rows, and writes metrics/summary/figure.
- `src/falsecontain/terminal_runner.py:165-306` (`run-primary`) copies frozen pilot packets, checkpoints every job, executes `_job_plan` order, and writes raw rows/status; it does not shuffle or score.
- The completed `core_v1.6.1` artifacts contain `manifest.json`, `checkpoint.json`, `run_events.csv`, and terminal-run `primary_judgments.csv`, confirming that `run-primary` produced the final 192.

Scientific impact: **MEDIUM**, because the canonical execution path did not match the preregistered ordering and did not automatically produce the preregistered analyses.

Affected completed 192: **YES**.

Recommended action: designate one canonical runner and document the other as legacy; disclose the ordering/analysis-path deviation.

## Issue 20 — `evaluate-pilot` historical-only behavior

Reported claim: generic `evaluate-pilot` reads only historical v1.3.1 artifacts.

Status: **CONFIRMED; historical only**

Evidence:

- `src/falsecontain/cli.py:61-62` hard-codes `evaluate_pilot_artifacts(root, version="1.3.1")`.
- `src/falsecontain/pipeline.py:795-845` reads `outputs/agent_pilot_real/preregistration-v1.3.1` and writes its v1.4 gate evaluation there.
- It is not used by `run-primary`, the completed primary validator, or the secondary/stress commands.

Scientific impact: **NONE** for the completed 192.

Affected completed 192: **NO**.

Recommended action: document or deprecate this historical command; do not treat it as a current v1.6.1 validator.

## Issue 21 — Historical GLM/TokenRouter code looks active

Reported claim: old GLM/TokenRouter support remains active-looking although the final model does not use it.

Status: **CONFIRMED; reusable/dead-path support**

Evidence:

- `config/experiment.json:8-12,18-23` selects direct DeepSeek, Gemini, Qwen, and Nemotron; no current role uses `tokenrouter` or GLM.
- `src/falsecontain/pipeline.py:281-287,364-379` retains provider/key and request branches for TokenRouter and reasoning controls. Those branches are reachable only if a future configuration selects that provider.
- The current completed manifest records only `deepseek-v4-flash`, `gemini-3.7-flash`, and `qwen-max`.

Scientific impact: **NONE** for the completed 192.

Affected completed 192: **NO**.

Recommended action: label the provider adapter as historical/reusable support or remove it in a separately reviewed cleanup. No scientific change is needed.

## Independent completed-192 verification

Read-only verification of `outputs/primary_runs/core_v1.6.1` found:

- 192 rows and 192 unique judgment IDs
- 48 E1, 48 E2, 48 E3, 48 E4
- 96 `deepseek-v4-flash` source judgments and 96 `gemini-3.7-flash` source judgments
- 64 packets with exactly 3 verifier replicates each
- 0 duplicate jobs, 0 missing jobs, 0 unexpected jobs
- all rows parse successfully and are marked completed
- all leakage checks passed
- `python -m falsecontain.cli validate-run core_v1.6.1` passed with 192/192

No audited issue changed the packet contents, verifier prompt, deterministic ground-truth assignment, verdict parser, or stored primary verdict values in the completed run. The confirmed ordering deviation and missing automatic analyses affect procedural compliance and reporting, not the already recorded packet/verdict cells.

## Critical before submission

- Complete the exact preregistered analyses, especially five-bin calibration and the seeded permutation negative control.
- Disclose the actual `run-primary` ordering deviation and the fact that E4 is a single critical-path test rather than a conjunction of all ground-truth postconditions.
- Do not claim that the current runner is safe for another scientific run until failed-job counting and dry-run gate isolation are fixed.

## Operational fixes before submission

- Make failed jobs remain pending and make completion validation inspect row status, not only counts.
- Reject dry-run primary artifacts in real secondary/stress gates.
- Persist raw responses and failed attempt logs, bind source hashes, reject dirty starts, and add regression tests.
- Create pilot approval state through an explicit auditable command or artifact-producing path.

## Documentation cleanup

- Remove or clearly mark the stale v1.5/GLM instructions in `PREREGISTRATION.md`.
- Correct the historical NVIDIA DeepSeek wording in `README.md`.
- Explain the historical DeepSeek packet-ID mapping and the `evaluate-pilot` v1.3.1 behavior.

## Scientific limitations / interpretation

- E4 is a mechanism-specific operational test, while deterministic ground truth is conjunctive over several postconditions.
- Stress broad checks are fixed exploratory evidence strings, not executable broad simulator tests.
- The completed 192 should be reported with the ordering deviation and analysis-completeness caveats; these do not justify relabeling or rerunning it automatically.

## False positives / obsolete findings

- The matched-pair “mismatch” is not an unresolved bug. The hidden remediation-effect amendment is explicit in `DESIGN_AMENDMENT_2026-09-09.md` and `PREREGISTRATION.md`.
- The claim that the secondary mapping is many-to-many or changes selected scientific cells is not supported: the current mapping is 32-to-32 and one-to-one.
- No evidence was found that the completed 192 has duplicate, missing, failed, unparsable, or leakage-failing judgments.

## Final counts

- Confirmed: **18**
- Partially confirmed: **2**
- Not confirmed as an unresolved issue: **1**
- Issues threatening validity of the completed 192: none demonstrated as packet/ground-truth/parser corruption; the ordering deviation and E4 scope are material reporting limitations.
- Fix before submission: exact analyses, disclosure of ordering/E4 limitations, and runner hardening before any future scientific run.
- Document only: amendment lineage, historical commands/adapters, and the secondary ID mapping.
- API/provider calls: **none**.
- Scientific artifacts changed: **none**; only this diagnostic report was added.
