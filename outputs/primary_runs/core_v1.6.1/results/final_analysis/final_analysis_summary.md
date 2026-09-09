# Final submission analysis - core_v1.6.1

All analyses use the existing 192 primary judgment rows and a deterministic truth join from the saved trajectory simulation state. No trajectories, packets, labels, prompts, or provider calls were changed.

## Evidence-level metrics

| Evidence | N | Resolved | Unresolved | Uncertain | Abstention | Coverage | FC detection | True-resolution accuracy | False-positive rate | Balanced accuracy | Committed accuracy |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E1_CLAIM | 48 | 0 | 0 | 48 | 100.0% | 0.0% | N/A | N/A | N/A | N/A | N/A |
| E2_ACTION | 48 | 6 | 0 | 42 | 87.5% | 12.5% | 0.0% | 100.0% | 0.0% | 50.0% | 50.0% |
| E3_STATE | 48 | 7 | 9 | 32 | 66.7% | 33.3% | 42.9% | 33.3% | 66.7% | 38.1% | 37.5% |
| E4_VERIFICATION | 48 | 24 | 21 | 3 | 6.2% | 93.8% | 100.0% | 100.0% | 0.0% | 100.0% | 100.0% |

E1 class-conditional rates are N/A because every E1 judgment abstained; they are not zero.

## Five-bin calibration

The preregistered bins are 0-20, 21-40, 41-60, 61-80, and 81-100, computed among non-abstaining judgments only. ECE is **6.2%**. The earlier reported 39.4% used a non-preregistered three-bin/all-row calculation; the five-bin ECE therefore **does change** that number.

| Bin | N | Mean confidence | Empirical accuracy | Absolute gap |
|---|---:|---:|---:|---:|
| 0-20 | 0 | N/A | N/A | N/A |
| 21-40 | 0 | N/A | N/A | N/A |
| 41-60 | 0 | N/A | N/A | N/A |
| 61-80 | 9 | 76.7% | 33.3% | 43.3% |
| 81-100 | 58 | 88.4% | 87.9% | 0.4% |

## Permutation negative control

Seed: **20260909**. Labels were permuted within each family x source-agent stratum, preserving each stratum label count. The implementation used **100,000** seeded permutations and no model calls.

Observed false-containment detection statistic: **77.42%**. Null mean: **44.78%**; SD: **6.18%**; 2.5-97.5% interval: **32.35%-57.14%**; one-sided plus-one p-value: **0.00001**.

The observed statistic is unusually high relative to this within-stratum label-shuffle null. This is a post-analysis negative-control diagnostic, not a new confirmatory hypothesis test.

## Replicate agreement

Across 64 packets, exact 3-way agreement was **93.8%**, pairwise agreement was **95.8%**, and Fleiss kappa was **0.919**.

| Evidence | Exact 3-way | Pairwise | Fleiss kappa |
|---|---:|---:|---:|
| E1_CLAIM | 100.0% | 100.0% | N/A |
| E2_ACTION | 87.5% | 91.7% | 0.619 |
| E3_STATE | 87.5% | 91.7% | 0.833 |
| E4_VERIFICATION | 100.0% | 100.0% | 1.000 |

## Coverage and committed accuracy

Overall coverage is **34.9%** and overall committed-judgment accuracy is **80.6%**. Coverage and committed accuracy by evidence level are in `evidence_level_metrics.csv`.

## Truth join check

Truth join: 192/192 rows; all labels valid: yes.
