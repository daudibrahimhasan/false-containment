# Frozen paper-results ledger: core_v1.6.1

Frozen at: `2026-09-09T19:06:54.743Z`

This is the paper-facing source of truth for `core_v1.6.1`. It was built from the completed local CSV/JSON artifacts. It does not replace or modify any judgment, packet, trajectory, ground-truth value, prompt, configuration, or frozen tag. Verify its SHA-256 before using it.

## Sample and integrity

| Item | Frozen value |
|---|---:|
| Incident families | 4 |
| Matched setups | 8 |
| Source-agent models | 2 |
| Trajectories | 16 |
| Unique evidence packets | 64 |
| Primary replicates per packet | 3 |
| Primary judgments | 192 |
| Secondary-verifier judgments | 32 |
| Duplicate primary jobs | 0 |
| Missing primary jobs | 0 |
| Parse failures | 0 |
| Leakage failures | 0 |
| Truth join | 192/192 valid |

Use this sample wording:

> Sixteen trajectories produced 64 unique evidence packets; each packet received three primary-verifier replicates, yielding 192 judgments.

## Primary results

| Metric | Frozen paper value | Denominator |
|---|---:|---|
| Abstention | **65.1% (125/192)** | All primary judgments |
| Coverage | **34.9% (67/192)** | All primary judgments |
| False-containment detection | **77.4% (24/31)** | Non-abstaining unresolved-truth judgments |
| False-containment miss rate | **22.6% (7/31)** | Non-abstaining unresolved-truth judgments |
| True-resolution accuracy | **83.3% (30/36)** | Non-abstaining resolved-truth judgments |
| False-positive rate | **16.7% (6/36)** | Non-abstaining resolved-truth judgments |
| Balanced accuracy | **80.4%** | Non-abstaining judgments |
| Committed-judgment accuracy | **80.6% (54/67)** | Non-abstaining judgments |
| Resolution precision | **81.1% (30/37)** | Judgments classified resolved |
| High-confidence errors | **12** | Incorrect committed verdicts with confidence >=80 |

Primary verdict counts: 37 resolved, 30 unresolved, and 125 uncertain.

## Evidence-level results

| Evidence | N | Resolved | Unresolved | Uncertain | Abstention | Coverage | FC detection | True-resolution accuracy | False-positive rate | Balanced accuracy | Committed accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E1 claim | 48 | 0 | 0 | 48 | 100.0% | 0.0% | N/A | N/A | N/A | N/A | N/A |
| E2 action | 48 | 6 | 0 | 42 | 87.5% | 12.5% | 0.0% | 100.0% | 0.0% | 50.0% | 50.0% |
| E3 state | 48 | 7 | 9 | 32 | 66.7% | 33.3% | 42.9% | 33.3% | 66.7% | 38.1% | 37.5% |
| E4 verification | 48 | 24 | 21 | 3 | 6.2% | 93.8% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% |

E1 class-conditional metrics are N/A, not zero, because every E1 judgment abstained.

## Calibration

The preregistered five-bin ECE among the 67 non-abstaining judgments is **6.2%** (exact: 0.06194029850746269). The bins are 0-20, 21-40, 41-60, 61-80, and 81-100.

| Confidence bin | N | Mean confidence | Accuracy | Absolute gap |
|---|---:|---:|---:|---:|
| 0-20 | 0 | N/A | N/A | N/A |
| 21-40 | 0 | N/A | N/A | N/A |
| 41-60 | 0 | N/A | N/A | N/A |
| 61-80 | 9 | 76.7% | 33.3% | 43.3 points |
| 81-100 | 58 | 88.4% | 87.9% | 0.4 points |

Do not report the earlier 39.4% calculation as the preregistered ECE. Do not use the pooled 6.2% alone to claim uniformly good calibration because the bins are sparse and uneven.

## Permutation negative control

- Statistic: pooled false-containment detection among non-abstaining assigned-unresolved judgments.
- Seed: **20260909**.
- Draws: **100,000**.
- Method: permute deterministic truth labels within family x source-agent strata while preserving stratum counts.
- Observed: **77.42%**.
- Null mean: **44.78%**; SD: **6.18%**.
- Null 95% interval: **32.35%-57.14%**.
- One-sided plus-one p-value: **0.00001**.

This is a post-analysis preregistered negative-control diagnostic. Do not describe it as balanced accuracy dropping to 50.0%, and do not call it a new confirmatory hypothesis test.

## Primary replicate agreement

| Measure | Frozen value |
|---|---:|
| Exact three-way agreement | **93.8% (60/64 packets)** |
| Pairwise agreement | **95.8% (184/192 replicate pairs)** |
| Fleiss kappa | **0.919** |

The value **96.9% (62/64)** is incorrect and must not appear in the paper.

## Secondary-verifier descriptive results

The frozen Nemotron subset contains 32 packets: 16 resolved-truth and 16 unresolved-truth packets. Verdict counts were 5 resolved, 3 unresolved, and 24 uncertain.

| Metric | Frozen value |
|---|---:|
| Coverage | **25.0% (8/32)** |
| Committed accuracy | **87.5% (7/8)** |
| False-containment detection | **75.0% (3/4)** |
| True-resolution accuracy | **100.0% (4/4)** |
| False-positive rate | **0.0% (0/4)** |
| Balanced accuracy | **87.5%** |
| Resolution precision | **80.0% (4/5)** |
| Agreement with Qwen packet-majority verdict | **87.5% (28/32)** |

Agreement with Qwen majority was 100.0% at E1, 75.0% at E2, 75.0% at E3, and 100.0% at E4. This is a small fixed-subset robustness check, not proof of verifier-independent performance.

## Exploratory stress arm

- Narrow verification produced false confidence in **4/4** cases.
- Fixture-defined broader evidence exposed the residual compromise in **4/4** cases.

Report this as exploratory. The broader checks were fixture-defined evidence strings, not executable broad simulator tests.

## Required disclosures

- The completed `run-primary` path used fixed job-plan order and did not apply the preregistered seed-20260909 shuffle. Packet content and blinding were preserved, but execution ordering deviated.
- E4 is a family-specific critical-path operational check. Deterministic ground truth is a conjunction of multiple security postconditions.
- The 192 judgments are replicated observations over 64 unique packets, not 192 independent incident cases.
- Primary class-conditional metrics exclude abstentions and must be interpreted with 34.9% coverage.
- The secondary results are a 32-packet fixed-subset robustness check.
- The stress arm is exploratory and its broader evidence is fixture-defined.

## Provenance

- Run validator: passed; 16 trajectories; 192/192 primary judgments; scientific complete.
- Run manifest commit: `3377c6178c739308ea1e8e516aca71c14373b3af`.
- Repository HEAD when this ledger was frozen: `97543e0d702fbea0e1cb9ded15f3d647c0134d5d`.
- Frozen tag: `preregistration-v1.6.1` at `f153a7d7d0a2f6dc0ca95129b4b9a08312008ead`.
- Aggregate trajectory-set SHA-256: `af99cae1464230ed08d6c6591cad3eae7496b0224d935aa68ef809668798cd90` over 16 files.
- Aggregate packet-set SHA-256: `87108ce8c6384fe28369b093dfbfa91a6736c36bac31250d9ecb0b13dc18d0d2` over 64 files.

The exact source-file hashes and aggregate-hash method are stored in `paper_results_ledger.json`.
