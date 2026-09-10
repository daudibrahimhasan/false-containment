# Submission repository check

This report covers safe repository cleanup, documentation, and submission packaging around the completed `core_v1.6.1` run. No provider/API calls, scientific reruns, judgment changes, packet changes, trajectory changes, or manuscript rewrites were made.

## Final package paths

- Main paper: `paper/false_containment_main.pdf`
- Full paper and supplementary materials: `paper/false_containment_full.pdf`
- Final results ledger: `outputs/primary_runs/core_v1.6.1/results/final_analysis/paper_results_ledger.md`
- Reproducibility instructions: `docs/REPRODUCIBILITY.md`
- Final-results index: `docs/FINAL_RESULTS.md`
- Post-run errata: `docs/POST_RUN_ERRATA.md`
- Canonical completed run: `outputs/primary_runs/core_v1.6.1/`

The two paper PDFs were copied byte-for-byte from the existing `submission/false_containment_main_v2.pdf` and `submission/false_containment_full_v2.pdf`. Their SHA-256 hashes were checked after copying. The source submission files were not edited.

## Files added or modified

Added:

- `paper/false_containment_main.pdf`
- `paper/false_containment_full.pdf`
- `docs/REPRODUCIBILITY.md`
- `docs/DUAL_USE.md`
- `docs/PAPER_FINAL_QA_NOTES.md`

Modified:

- `README.md` (Start Here / Final Submission navigation)
- `submission_repo_check.md` (this packaging audit)

The existing `docs/FINAL_RESULTS.md` and `docs/POST_RUN_ERRATA.md` were used as the final-results documentation and were not scientifically rewritten.

## Required boundaries and provenance

- `preregistration-v1.6.1` remains frozen historical provenance and was not moved, retagged, amended, or rewritten.
- `core_v1.6.1` is the completed final run.
- Current README/docs are post-run packaging and navigation documentation.
- No frozen scientific artifacts were changed: primary judgments, packets, trajectories, ground truth, manifests/hashes, secondary subset, stress outputs, and run directories remain in place.
- No unverified citations were added. Candidate related work is only noted in `docs/PAPER_FINAL_QA_NOTES.md` for future verification.

## Offline checks

- Primary validation: passed for `core_v1.6.1`; 16 trajectories; `192/192` primary judgments; `scientific_complete=true`.
- Offline test suite: `39 passed`.
- `git diff --check`: passed.
- PDF packaging check: the main PDF is 7 pages and the full paper/supplement PDF is 11 pages. Both destination files have the same SHA-256 as their existing v2 source PDFs.
- Secret scan: no tracked `.env` file and no credential/token/secret value found in tracked files. The root `.env` remains ignored and untracked.
- Git status: not clean because the pre-existing `submission/` directory was untracked before this task and the added docs and `paper/` package are uncommitted. No commit or push was performed.

No APIs or model providers were called. Stop after this packaging and verification work; do not rerun experiments or alter frozen scientific history.
