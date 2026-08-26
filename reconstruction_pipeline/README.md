# Abuja CA-Markov Reconstruction Automation

This directory is the fail-closed automation layer for the 2026 reconstruction. The pipeline is designed to preserve provenance, prevent leakage, stop on failed scientific gates, and publish only validated products.

## Execution order

1. `REFERENCE_INTEGRITY` — normalize the adjudicated reference set; reject unresolved labels, duplicate candidate IDs, missing coordinates, invalid years, and missing classes.
2. `REFERENCE_SPLIT` — freeze spatially separated calibration, validation, and locked-holdout partitions before model fitting.
3. `HISTORICAL_CLASSIFICATION` — train year-specific/harmonized Landsat classifiers from approved labels only.
4. `CLASSIFICATION_VALIDATION` — report confusion matrices, OA, balanced accuracy, macro-F1, per-class precision/recall/F1 and locked-holdout results. No training data may appear in validation folds.
5. `TEMPORAL_CONSISTENCY` — quantify persistence and implausible reversions; flag Built-up→non-Built-up and Water→Built-up/Bare transitions for targeted audit.
6. `CHANGE_ACCOUNTING` — produce 2005→2015 and 2015→2025 transition matrices and class-area reconciliation checks.
7. `SUITABILITY_VALIDATION` — test whether the suitability model discriminates observed historical expansion from non-expansion locations before any future simulation.
8. `HINDCAST` — simulate a known historical interval and evaluate Figure of Merit, quantity disagreement, allocation disagreement and supplementary OA/Kappa.
9. `CA_MARKOV_2035` — only run after all preceding gates pass. The 2035 product is a scenario, not a deterministic forecast.
10. `RELEASE_GATE` — verify required maps, tables, metadata, provenance and QA reports before repository/portfolio publication.

## Fail-closed policy

A stage may consume only outputs from a preceding stage marked `PASS`. Any failed gate stops the run. Threshold changes must be documented; the pipeline must never silently lower a threshold merely to obtain a pass.

## Current starting point

The latest Drive reconstruction contains A1R2D–A1R2N evidence and adjudication outputs. A1R2N includes a final human-adjudicated reference table plus a separate remaining-uncertain queue. The automation therefore begins by testing whether the reference set is complete enough to freeze training/validation partitions. Until that gate passes, historical classifier retraining is blocked.

## Reference gate

Run locally or in Colab:

```bash
python reconstruction_pipeline/reference_gate.py /path/to/A1R2N_Final_Human_Adjudicated_Reference.csv \
  --output-dir outputs/reconstruction/reference_gate
```

The command exits with status 0 only when the reference integrity gate passes. It writes a normalized reference table, unresolved queue and machine-readable JSON gate report.

## CI

`.github/workflows/reconstruction-ci.yml` runs deterministic unit tests and repository-integrity checks. Earth Engine operations remain runtime-dependent and are intentionally separated from unit tests so that cloud credentials are never committed to the repository.
