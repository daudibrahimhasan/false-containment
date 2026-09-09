# False Containment submission finalization checklist

This checklist is based primarily on the completed local `core_v1.6.1` artifacts, the secondary-verifier output, the stress-test output, and the hostile-review standard from the research-competition-winner skill. The existing Google Doc and PDF are drafts and are not scientific sources of truth. The final paper may be rebuilt from the verified local results rather than repaired line by line.

Status key:

- `[x]` completed in the saved experiment artifacts
- `[ ]` still needs to be done in the paper or submission package
- `[~]` exists, but the paper currently reports it incorrectly or incompletely

## Locked scientific work: do not rerun

- [x] Primary run completed: **192/192 unique judgments**.
- [x] Sample structure verified: **16 trajectories -> 64 unique evidence packets -> 192 verifier judgments**.
- [x] Evidence balance verified: **48 judgments each for E1, E2, E3, and E4**.
- [x] Source-agent balance verified: **96 DeepSeek-source + 96 Gemini-source judgments**.
- [x] Replication verified: **3 Qwen verifier replicates per packet**.
- [x] Integrity verified: **0 duplicate jobs, 0 missing jobs, 0 parse failures, and leakage checks passed**.
- [x] Secondary verifier completed: **32/32 Nemotron judgments**, with no mock verdicts.
- [x] Exploratory stress arm completed: **4/4 narrow checks missed the residual compromise; 4/4 fixture-defined broad checks exposed it**.
- [x] Five-bin calibration, permutation control, replicate agreement, coverage, and evidence-level analyses exist locally.

## P0: submission blockers

| Done | Task | Owner | Exact requirement |
|---|---|---|---|
| [ ] | Remove author placeholders | You + Klova | Replace all six `Author name / Affiliation` placeholders with final names, affiliations, and contribution text. |
| [ ] | Build the final paper within the competition page limit | Klova + You | Rebuild from verified local artifacts. Confirm the exact rule, then keep the final main paper to **8 pages or fewer if that is the limit**, excluding only what the rules explicitly exclude. The old PDF's page count does not constrain the new paper. |
| [~] | Fix the duplicated coverage phrase in the abstract | Klova | Keep one statement only: **coverage was 34.9% (67/192)**. The current abstract repeats coverage a second time before balanced accuracy. |
| [~] | Correct replicate agreement everywhere | Klova | Replace **96.9% (62/64)** with **93.8% (60/64)**. Add pairwise agreement **95.8% (184/192 replicate pairs)** and Fleiss kappa **0.919** where space allows. |
| [~] | Correct the permutation-control result | Guru + Klova | The preregistered statistic was false-containment detection, not balanced accuracy. Report: observed **77.42%**, null mean **44.78%**, null SD **6.18%**, 95% null interval **32.35%-57.14%**, one-sided plus-one **p = 0.00001**, seed **20260909**, 100,000 permutations within family x source-agent strata. |
| [ ] | Remove the current false permutation wording | Klova | Delete claims such as `balanced accuracy dropped to 50.0%` or that the control `confirmed` performance. Say it supports an association under the specified negative-control diagnostic and is not a new confirmatory hypothesis test. |
| [~] | Report calibration precisely | Klova + Guru | Keep **five-bin ECE = 6.2%**, computed over the **67 non-abstaining judgments** using bins 0-20, 21-40, 41-60, 61-80, and 81-100. Remove every old 39.4% ECE value. |
| [ ] | Temper the calibration claim | Klova | Do not simply call the verifier `well calibrated`. The 61-80 bin had only 9 judgments and a **43.3 percentage-point gap**; the 81-100 bin had 58 judgments and a **0.4-point gap**. State that the pooled ECE is low but bin support is sparse and uneven. |
| [~] | State coverage and abstention together | Klova | Overall abstention **65.1% (125/192)**; overall coverage **34.9% (67/192)**. Do not confuse overall coverage with the **6.2% E4 abstention rate** or the **6.2% ECE**. |
| [~] | Make every denominator explicit | Klova + Guru | False-containment detection **77.4% (24/31)** and true-resolution accuracy **83.3% (30/36)** are among non-abstaining judgments in their respective ground-truth classes. Committed accuracy is **80.6% (54/67)**. |
| [~] | Report E1 correctly | Klova + Taemin | E1 produced **48/48 abstentions**, coverage **0%**, and class-conditional accuracy/detection metrics are **N/A**, not zero. |
| [ ] | Correct the ordering-deviation disclosure | Guru + Klova | The completed `run-primary` path executed the fixed job-plan order and **did not apply the preregistered seed-20260909 shuffle**. The current paper incorrectly says the run was shuffled. State that packet content and blinding were preserved, but execution ordering deviated. |
| [~] | Narrow the E4 claim | Klova + Guru | Describe E4 as a **family-specific critical-path operational check**. It tested one persistence mechanism, while deterministic ground truth was a conjunction of several security postconditions. It was not equivalent to the full ground-truth evaluator. |
| [~] | Narrow the stress-test claim | Klova + Guru | Say: `In four exploratory fixture-driven stress cases, broader postcondition evidence exposed the residual compromise in 4/4 cases.` Do not describe the broad check as an executable production-wide audit or universal proof. |
| [x] | Report actual secondary-verifier behavior | Guru + Klova | Inserted truth-joined Nemotron accuracy, abstention, coverage, class-conditional metrics, and agreement with Qwen on the same frozen 32 packets. Current raw Nemotron verdict counts are **5 resolved, 3 unresolved, and 24 uncertain**. |
| [ ] | Add incident-to-benchmark mapping | Klova | Map the four benchmark families to the sprint incident motivation: credential persistence, scheduled execution, surviving access-control binding, and alternate relay path. State clearly that the benchmark isolates a closure-verification mechanism and **does not reconstruct the real incident**. |
| [ ] | Remove unsupported novelty claims | Guru + Klova | Recheck `first`, `no existing framework`, and similar claims against the cited literature. Use `to our knowledge` only if the search actually supports it, and narrow the claim to this benchmark setting. |

## P1: main results presentation

| Done | Task | Owner | Exact requirement |
|---|---|---|---|
| [~] | Add the main E1-E4 figure | Taemin | Use the saved evidence-level metrics. Panel A: coverage/abstention by E1-E4. Panel B: committed performance and safety metrics. Show E1 as N/A where classification metrics are undefined. |
| [~] | Add the five-bin reliability diagram | Taemin | Use the existing `reliability_diagram.svg`. Make empty bins visibly empty rather than zero-valued. Caption must say **n = 67 non-abstaining judgments**. |
| [ ] | Add the compact E1-E4 results table | Klova + Taemin | Include N, verdict counts, abstention, coverage, false-containment detection, true-resolution accuracy, false-positive rate, balanced accuracy, and committed accuracy. |
| [ ] | Add the 12 high-confidence error table | Guru + Klova | Include family, source agent, evidence level, deterministic truth, Qwen verdict, confidence, and error direction. Keep it compact; move full reasons to the appendix if needed. |
| [ ] | Add the Qwen-Nemotron comparison table | Guru + Taemin | Same frozen 32 packets only. Report coverage, committed accuracy, class-conditional metrics where defined, and exact cross-verifier agreement. Do not imply 32 packets establish verifier independence. |
| [~] | Keep the stress figure small | Taemin | Label it **exploratory, n = 4**, and distinguish narrow executable checks from fixture-defined broader evidence. |
| [ ] | Replace `marginal effect` language | Klova | The ladder is cumulative and not a randomized isolation of each evidence component. Use `descriptive cumulative evidence-level comparison`. |
| [ ] | Redesign pooled verdict charts | Taemin | Use compact academic styling, raw counts where useful, muted colors, readable labels, and no infographic-style decoration. |

## P1: interpretation and limitations

| Done | Task | Owner | Exact requirement |
|---|---|---|---|
| [ ] | Rewrite the central claim narrowly | Klova + Guru | The result supports evidence sufficiency for this synthetic packet ladder and Qwen verifier. It does not prove a general production closure standard. |
| [ ] | Strengthen threats to validity | Klova + Guru | Cover synthetic incidents, 16 trajectories, 64 unique packets, three dependent replicates per packet, two response agents, one primary verifier, 65.1% abstention, E4 scope, ordering deviation, and fixture-defined stress evidence. |
| [ ] | State the experimental units correctly | Klova | Use: **64 unique evidence packets, each evaluated by three verifier replicates, yielding 192 judgments**. Do not call the 192 judgments independent incident cases. |
| [ ] | Separate confirmatory and exploratory claims | Guru + Klova | Primary 192 and preregistered analyses are core; secondary replication is limited robustness evidence; stress cases are exploratory; any new baseline or interval analysis is supplementary/post-hoc. |
| [ ] | Explain the abstention-performance tradeoff | Klova | Detection and accuracy are conditional on commitment. Report 77.4%/83.3% together with 34.9% coverage so the verifier is not presented as broadly accurate across all 192 judgments. |
| [ ] | Avoid interpreting ECE alone as safety | Klova | Low pooled ECE does not remove the 12 high-confidence errors or the selective-coverage problem. |

## P2: useful supplementary work, clearly labeled post-hoc

| Done | Task | Owner | Exact requirement |
|---|---|---|---|
| [ ] | Add cluster-aware uncertainty intervals | Guru | Bootstrap or otherwise account for packet/trajectory clustering. Label this supplementary because it was not in the frozen core plan. |
| [ ] | Add trivial contextual baselines | Guru | Always abstain, always resolved, and always unresolved require no provider calls. Label them post-hoc context, not preregistered baselines. |
| [ ] | Add a deterministic E4-only rule baseline if useful | Guru | No provider calls. Keep it supplementary and do not imply that E4 equals full ground truth. |
| [ ] | Add an operational closure protocol | You + Klova | Present it as a **proposed protocol derived from the findings**, not an experimentally validated production standard. |

## P1: repository and reproducibility package

| Done | Task | Owner | Exact requirement |
|---|---|---|---|
| [ ] | Update stale README model text | Coding agent | Replace the old NVIDIA DeepSeek V4 Pro description with the actual frozen source agent: direct `deepseek-v4-flash`; preserve the historical record where relevant. |
| [ ] | Handle stale preregistration status safely | Coding agent + Guru | `PREREGISTRATION.md` still contains pre-run statements and old v1.5/GLM execution lines. Do **not** rewrite or move tag `preregistration-v1.6.1`. Add a clearly separate post-run status/errata document or make only an explicitly historical documentation update on current `main`. |
| [ ] | Document the secondary packet-ID translation | Coding agent | Explain that the frozen historical DeepSeek IDs map one-to-one to the v1.6.1 DeepSeek Flash packets; do not change the frozen 32-cell selection or subset hash. |
| [ ] | Package the completed outputs | Coding agent | Include or release the 192 primary rows, 64 packets, deterministic truth join, final-analysis files, 32 secondary rows, stress outputs, manifests, hashes, and instructions without exposing API keys. |
| [ ] | Choose one canonical runner in current documentation | Coding agent | Document `run-primary` as the path that produced `core_v1.6.1`; mark overlapping legacy paths clearly. Do not rerun the experiment. |
| [ ] | Run the full offline test suite | Coding agent | Expected baseline is **39 passing tests** unless new documentation-only work leaves the count unchanged. No provider calls. |
| [ ] | Commit submission-only changes safely | Coding agent | Keep the scientific tag fixed, do not force-push, do not rewrite history, and do not modify original judgment/packet/trajectory files. |

## Final submission QA

- [ ] Abstract, Methods, Results, Discussion, Conclusion, tables, captions, and repository all use the same numbers.
- [ ] Search the final paper for and remove: `39.4%`, `96.9%`, `62/64`, duplicated `coverage`, `marginal effect`, and placeholder author text.
- [ ] Verify these exact core numbers remain:
  - coverage **34.9% (67/192)**
  - abstention **65.1% (125/192)**
  - five-bin ECE **6.2%** among 67 committed judgments
  - false-containment detection **77.4% (24/31)** among non-abstaining unresolved-truth judgments
  - true-resolution accuracy **83.3% (30/36)** among non-abstaining resolved-truth judgments
  - committed accuracy **80.6% (54/67)**
  - balanced accuracy **80.4%** among non-abstaining judgments
  - exact three-way replicate agreement **93.8% (60/64)**
  - pairwise replicate agreement **95.8% (184/192)**
  - Fleiss kappa **0.919**
- [ ] Verify every figure number against the CSV/JSON artifact used to generate it.
- [ ] Verify all citations resolve and every strong related-work/novelty claim has a source.
- [ ] Export the final PDF and visually inspect every page for clipped tables, unreadable figure text, broken references, and blank pages.
- [ ] Confirm the main-body page count complies with the official submission rule.
- [ ] Confirm repository URL, artifact paths, and reproduction commands work from a clean checkout.
- [ ] Confirm no `.env`, API key, raw credential, or secret appears in Git history or the submission archive.
- [ ] Run one final read-only claim-to-artifact audit before upload.

## Do not do

- [ ] Do **not** rerun or replace any of the 192 primary judgments.
- [ ] Do **not** call Qwen, Nemotron, DeepSeek, or Gemini for new scientific results.
- [ ] Do **not** alter the 64 evidence packets, deterministic truth, incident semantics, prompts, or verifier verdicts.
- [ ] Do **not** move, recreate, amend, or overwrite `preregistration-v1.6.1`.
- [ ] Do **not** call the stress result a universal rate or production validation.
- [ ] Do **not** claim E4 directly reveals or fully equals ground truth.
- [ ] Do **not** present post-hoc baselines, cluster intervals, or the closure protocol as preregistered findings.

## Recommended execution order

1. [Completed] Freeze a paper-results ledger from the verified local CSV/JSON artifacts.
2. Compute and insert the secondary-verifier comparison.
3. Rebuild the paper using the verified ledger, two main figures, and compact result/error tables.
4. Narrow claims and strengthen limitations.
5. Keep the rebuilt paper within the page limit and remove placeholders.
6. Clean the README and add post-run documentation without touching the frozen tag.
7. Package artifacts and run offline tests.
8. Perform the final claim-to-artifact and visual PDF audit.
