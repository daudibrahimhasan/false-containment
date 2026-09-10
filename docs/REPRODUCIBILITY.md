# Reproducibility and artifact navigation

This repository preserves the completed `core_v1.6.1` run and its analysis artifacts. The frozen `preregistration-v1.6.1` tag is historical provenance; it is not rewritten by the post-run packaging docs.

## Source of truth

Use the frozen paper-results ledger for reported numbers:

`outputs/primary_runs/core_v1.6.1/results/final_analysis/paper_results_ledger.md`

The canonical run is:

`outputs/primary_runs/core_v1.6.1/`

It contains the preserved manifest, 16 trajectories, 64 evidence packets, primary judgments, truth join, secondary subset outputs, and validation artifacts. Do not reconstruct paper numbers from older manuscript drafts.

## Offline verification

From the repository root in PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m falsecontain.cli validate-run core_v1.6.1
python -m pytest -q
```

These commands inspect local artifacts and run the offline test suite. They do not call a model provider. Do not run a provider-backed runner when only reproducing or auditing the completed results.

The validator should report 16 source trajectories, 192/192 primary judgments, and `scientific_complete=true`. The expected offline suite result is approximately 39 passing tests; record the exact local result in the repository audit rather than changing scientific artifacts.

## Result navigation

- Final values and denominators: `docs/FINAL_RESULTS.md`
- Operational and interpretation disclosures: `docs/POST_RUN_ERRATA.md`
- Frozen ledger JSON and checksums: `outputs/primary_runs/core_v1.6.1/results/final_analysis/`
- Primary rows: `outputs/primary_runs/core_v1.6.1/results/primary_judgments.csv`
- Secondary-verifier rows: `outputs/primary_runs/core_v1.6.1/secondary_verifier/results/rows.csv`

The current GitHub documentation is post-run packaging. It does not amend the preregistration tag, move files inside the frozen run, or change any judgment, packet, trajectory, or truth value.
