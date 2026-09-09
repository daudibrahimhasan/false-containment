# Final submission analysis check

This report was generated from the completed `core_v1.6.1` primary artifacts only. No provider/API calls were made. No judgment, packet, trajectory, ground-truth value, prompt, tag, preregistration, or stress-test result was changed.

## Computed artifacts

The following files were created under `outputs/primary_runs/core_v1.6.1/results/final_analysis/`:

- `evidence_level_metrics.csv`
- `calibration_5bin.csv`
- `permutation_negative_control.json`
- `permutation_null_distribution.csv`
- `replicate_agreement.json`
- `overall_metrics.json`
- `truth_join_audit.json`
- `final_analysis_summary.md`
- `reliability_diagram.svg`
- `evidence_level_performance.svg`

## Truth and 192-row verification

- 192/192 judgment rows joined to deterministic final-state truth.
- All truth labels were valid `resolved` or `unresolved`.
- Existing primary integrity remained: 192 unique jobs, 48 judgments per evidence level, 96 per source agent, 3 replicates per packet, no duplicates, no missing jobs, parse integrity passed, and leakage integrity passed.

## Five-bin calibration

The preregistered bins were applied to non-abstaining judgments only:

| Bin | N | Mean confidence | Empirical accuracy | Absolute gap |
|---|---:|---:|---:|---:|
| 0-20 | 0 | N/A | N/A | N/A |
| 21-40 | 0 | N/A | N/A | N/A |
| 41-60 | 0 | N/A | N/A | N/A |
| 61-80 | 9 | 76.7% | 33.3% | 43.3% |
| 81-100 | 58 | 88.4% | 87.9% | 0.4% |

The exact five-bin ECE is **6.2%**. This **does change** the previously reported **39.4%** value. The earlier value used a non-preregistered three-bin/all-row calculation, so it should be replaced in the paper by the five-bin non-abstaining ECE, with the calculation definition stated clearly.

## Permutation negative control

- Seed: **20260909**
- Labels permuted within each family x source-agent stratum.
- Stratum label counts preserved.
- 100,000 seeded permutations.
- The preregistration fixes the seed and within-stratum rule but does not specify a draw count; 100,000 was the declared Monte Carlo implementation count and is recorded in the JSON artifact.
- Observed false-containment detection statistic: **77.42%**.
- Null mean: **44.78%**; SD: **6.18%**.
- Null 2.5%-97.5% interval: **32.35%-57.14%**.
- One-sided plus-one permutation p-value: **0.00001**.

Interpretation: the observed detection statistic is unusually high relative to the within-stratum label-shuffle null. This supports the observed association between verdicts and deterministic truth under this negative-control diagnostic. It is not a new confirmatory hypothesis test and does not change the 192 judgments.

## Inter-replicate agreement

Across 64 packets:

- Exact 3-way agreement: **93.8%** (60/64 packets).
- Pairwise agreement: **95.8%** (184/192 replicate pairs).
- Fleiss kappa: **0.919**.

By evidence level:

| Evidence | Exact 3-way | Pairwise | Fleiss kappa |
|---|---:|---:|---:|
| E1 | 100.0% | 100.0% | N/A |
| E2 | 87.5% | 91.7% | 0.619 |
| E3 | 87.5% | 91.7% | 0.833 |
| E4 | 100.0% | 100.0% | 1.000 |

E1 has no category variation, so its chance-corrected kappa is undefined rather than zero.

## Evidence-level metrics and coverage

| Evidence | N | Resolved | Unresolved | Uncertain | Abstention | Coverage | FC detection | True-resolution accuracy | False-positive rate | Balanced accuracy | Committed accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E1 | 48 | 0 | 0 | 48 | 100.0% | 0.0% | N/A | N/A | N/A | N/A | N/A |
| E2 | 48 | 6 | 0 | 42 | 87.5% | 12.5% | 0.0% | 100.0% | 0.0% | 50.0% | 50.0% |
| E3 | 48 | 7 | 9 | 32 | 66.7% | 33.3% | 42.9% | 33.3% | 66.7% | 38.1% | 37.5% |
| E4 | 48 | 24 | 21 | 3 | 6.2% | 93.8% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% |

Overall coverage is **34.9%** and overall committed-judgment accuracy is **80.6%**. E1 class-conditional metrics are N/A because every E1 judgment abstained; they must not be reported as zero.

## Metrics to update in the paper

Update or add:

1. Five-bin ECE: **6.2%**, replacing 39.4%.
2. The exact calibration-bin definition and non-abstaining denominator.
3. Permutation negative-control result: observed 77.42%, p=0.00001 under the seeded within-stratum shuffle.
4. Replicate agreement: exact 3-way 93.8%, pairwise 95.8%, Fleiss kappa 0.919.
5. Evidence-level coverage and committed accuracy, especially complete E1 abstention and the E4 93.8% coverage.

No primary judgment or scientific artifact was modified. Analysis outputs only were added under `final_analysis/`, plus this diagnostic check.

APIs/provider calls: **0**.
