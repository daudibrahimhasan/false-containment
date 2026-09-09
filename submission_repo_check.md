# Submission repository check

Checked after publishing the completed `core_v1.6.1` results. This report covers repository cleanup and packaging only. No provider/API calls, scientific reruns, or judgment changes were made.

## Published repository

- Repository: https://github.com/daudibrahimhasan/false-containment
- Branch: `main`
- Packaging commit: `4cad9aec1f6d0f88f0b21a98163412821b24d827`
- Frozen preregistration tag: `preregistration-v1.6.1`
- Frozen tag commit (peeled): `f153a7d7d0a2f6dc0ca95129b4b9a08312008ead`

The frozen tag was not moved, recreated, amended, or rewritten. The push used a normal non-force update.

## Included submission artifacts

- [Final results ledger and paper numbers](docs/FINAL_RESULTS.md)
- [Post-run errata and disclosures](docs/POST_RUN_ERRATA.md)
- [Final analysis outputs](outputs/primary_runs/core_v1.6.1/results/final_analysis/)
- [Primary judgments](outputs/primary_runs/core_v1.6.1/results/primary_judgments.csv)
- [Primary manifest and planned jobs](outputs/primary_runs/core_v1.6.1/manifest.json)
- [All 16 trajectories](outputs/primary_runs/core_v1.6.1/trajectories/)
- [All 64 evidence packets](outputs/primary_runs/core_v1.6.1/packets/)
- [32 secondary-verifier judgments](outputs/primary_runs/core_v1.6.1/secondary_verifier/)
- [Exploratory stress outputs](outputs/stress_scientific/)
- [Analysis audit](diagnostics/final_submission_analysis_check.md)
- [Submission finalization checklist](SUBMISSION_FINALIZATION_CHECKLIST.md)

The package includes the truth join, manifests/hashes, calibration and permutation outputs, replicate agreement, figures, high-confidence error audit, secondary subset outputs, and stress-test outputs.

## Integrity and tests

- Primary validator: passed; `192/192` judgments; `16` agent trajectories; `scientific_complete=true`.
- Offline test suite: `39 passed`.
- `git diff --check`: passed.
- Secret scan: no credential values found in staged/published artifacts. `.env` remains untracked/ignored; only an empty-key instruction in a legacy README was detected.
- Primary result artifacts, packets, trajectories, truth data, verdicts, and preregistration configuration were not modified during packaging.
- No APIs or model providers were called during cleanup, verification, or publication.

## Git state after publication

The packaging commit was pushed from `main` to `origin/main` without force-push. The final repository state was checked for a clean working tree and matching local/remote heads after the report commit was added.

