# Final results index: `core_v1.6.1`

> **These finalized artifacts are the source of truth for all paper numbers, figures, and tables. Do not reconstruct results from older manuscript drafts.**

All links below point to the committed artifacts in this repository. The original scientific judgments, trajectories, packets, deterministic truth, and frozen subset are preserved unchanged.

## Experiment

- 4 incident families and 8 matched setups.
- 16 source trajectories: 8 cases x 2 response-agent models.
- 64 unique evidence packets: 4 cumulative evidence levels per case-agent trajectory.
- 3 Qwen verifier replicates per packet.
- 192 primary judgments.
- 48 primary judgments each for E1, E2, E3, and E4.
- 32 Nemotron secondary-verifier judgments on the frozen subset.

Source artifacts: [manifest](../outputs/primary_runs/core_v1.6.1/manifest.json), [planned primary jobs](../outputs/primary_runs/core_v1.6.1/results/planned_primary_jobs.csv), [16 trajectories](../outputs/primary_runs/core_v1.6.1/trajectories), [64 packets](../outputs/primary_runs/core_v1.6.1/packets), [primary rows](../outputs/primary_runs/core_v1.6.1/results/primary_judgments.csv), [deterministic truth join audit](../outputs/primary_runs/core_v1.6.1/results/final_analysis/truth_join_audit.json), [frozen secondary subset](../config/secondary_subset.json), and [secondary rows](../outputs/primary_runs/core_v1.6.1/secondary_verifier/results/rows.csv).

## Primary results

| Metric | Result |
|---|---:|
| False-containment detection | **77.4% (24/31)** |
| False-containment miss rate | **22.6% (7/31)** |
| True-resolution accuracy | **83.3% (30/36)** |
| False-positive rate | **16.7% (6/36)** |
| Committed-judgment accuracy | **80.6% (54/67)** |
| Coverage | **34.9% (67/192)** |
| Abstention | **65.1% (125/192)** |
| Balanced accuracy | **80.4%** |
| Resolution precision | **81.1% (30/37)** |
| Five-bin ECE | **6.2%** over 67 committed judgments |
| High-confidence errors | **12** at confidence >=80 |

Exact underlying artifacts: [overall metrics](../outputs/primary_runs/core_v1.6.1/results/final_analysis/overall_metrics.json), [evidence-level metrics](../outputs/primary_runs/core_v1.6.1/results/final_analysis/evidence_level_metrics.csv), [primary metrics table](../outputs/primary_runs/core_v1.6.1/results/primary_metrics_table.md), and [high-confidence error audit](../outputs/primary_runs/core_v1.6.1/results/high_confidence_errors.json).

E1 produced 48/48 abstentions. E1 class-conditional metrics are N/A, not zero. The 192 judgments are not 192 independent incidents: they are three replicated judgments over 64 unique packets.

## Reliability

- Exact three-way agreement: **93.8% (60/64)**.
- Pairwise agreement: **95.8% (184/192)**.
- Fleiss' kappa: **0.919**.

Source: [replicate agreement](../outputs/primary_runs/core_v1.6.1/results/final_analysis/replicate_agreement.json).

## Calibration

The preregistered five-bin analysis uses non-abstaining judgments and bins 0-20, 21-40, 41-60, 61-80, and 81-100. The resulting ECE is **6.2%**. The earlier 39.4% value is not the preregistered five-bin ECE.

Source: [five-bin calibration](../outputs/primary_runs/core_v1.6.1/results/final_analysis/calibration_5bin.csv) and [reliability diagram](../outputs/primary_runs/core_v1.6.1/results/final_analysis/reliability_diagram.svg).

## Permutation negative control

- Seed: **20260909**.
- **100,000** permutations.
- Labels permuted within family x source-agent strata.
- Observed false-containment detection: **77.42%**.
- Null mean: **44.78%**.
- Null SD: **6.18%**.
- 95% null interval: **32.35%-57.14%**.
- One-sided plus-one p-value: **0.00001**.

Source: [negative-control summary](../outputs/primary_runs/core_v1.6.1/results/final_analysis/permutation_negative_control.json) and [null distribution](../outputs/primary_runs/core_v1.6.1/results/final_analysis/permutation_null_distribution.csv).

This is a post-analysis diagnostic, not a new confirmatory hypothesis test. It is not a balanced-accuracy result.

## Evidence-level figure and analysis files

- [E1-E4 performance figure](../outputs/primary_runs/core_v1.6.1/results/final_analysis/evidence_level_performance.svg)
- [E1-E4 metrics CSV](../outputs/primary_runs/core_v1.6.1/results/final_analysis/evidence_level_metrics.csv)
- [paper-results ledger JSON](../outputs/primary_runs/core_v1.6.1/results/final_analysis/paper_results_ledger.json)
- [paper-results ledger Markdown](../outputs/primary_runs/core_v1.6.1/results/final_analysis/paper_results_ledger.md)
- [ledger SHA-256 checksums](../outputs/primary_runs/core_v1.6.1/results/final_analysis/paper_results_ledger.sha256)

## Secondary verifier

The frozen Nemotron subset has 32 judgments: 5 resolved, 3 unresolved, and 24 uncertain. Coverage is 25.0% (8/32), committed accuracy is 87.5% (7/8), false-containment detection is 75.0% (3/4), true-resolution accuracy is 100.0% (4/4), and balanced accuracy is 87.5%. Nemotron matched Qwen's three-replicate packet-majority verdict on 28/32 packets (87.5%). This is a small fixed-subset descriptive robustness check, not evidence of verifier-independent performance.

Source: [secondary rows](../outputs/primary_runs/core_v1.6.1/secondary_verifier/results/rows.csv) and [secondary verdicts](../outputs/primary_runs/core_v1.6.1/secondary_verifier/verdicts).

## Interpretation limits and disclosures

- E4 is a family-specific critical-path operational check, not the complete conjunctive ground-truth evaluator.
- The stress arm is exploratory and fixture-driven. Narrow checks are executable simulator operations; broader evidence is fixture-defined rather than an executable production-wide broad verification test.
- Stress outputs: [rows](../outputs/stress_scientific/results/rows.csv) and [metrics](../outputs/stress_scientific/results/metrics.json).
- The primary ordering deviated from the preregistered fixed-seed shuffle. The completed `run-primary` path processed its fixed job-plan/construction order; packet contents, deterministic truth, verifier prompt, blinding, and recorded judgments were unchanged.
- The full methodological and provenance record is in the [post-run errata](POST_RUN_ERRATA.md) and [analysis audit](../diagnostics/final_submission_analysis_check.md).

