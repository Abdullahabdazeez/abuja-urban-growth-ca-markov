from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

CLASS_MAP = {1: "Built-up", 2: "Vegetation", 3: "Cropland", 4: "Bare land", 5: "Water"}
REQUIRED_BASE = ["candidate_id", "target_year", "latitude", "longitude"]
FINAL_CLASS_CANDIDATES = [
    "A1R2N_final_class",
    "A1R2M_final_class",
    "A1R2L_final_class",
    "A1R2K_final_class",
    "A1R2I_recommended_class",
    "reference_class",
    "candidate_class",
]
CONFIDENCE_CANDIDATES = [
    "A1R2N_human_confidence",
    "A1R2K_resolution_confidence",
    "human_confidence",
]


def first_existing(df: pd.DataFrame, columns: list[str]) -> str | None:
    return next((c for c in columns if c in df.columns), None)


def normalize_class(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce").astype("Int64")


def build_final_reference(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_BASE if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    out = df.copy()
    final_col = first_existing(out, FINAL_CLASS_CANDIDATES)
    if final_col is None:
        raise ValueError("No usable final/reference class column found")

    out["final_class"] = normalize_class(out[final_col])
    out["final_class_name"] = out["final_class"].map(CLASS_MAP)

    conf_col = first_existing(out, CONFIDENCE_CANDIDATES)
    if conf_col:
        out["final_confidence"] = out[conf_col].astype("string").str.upper().str.strip()
    else:
        out["final_confidence"] = pd.Series(pd.NA, index=out.index, dtype="string")

    if "A1R2N_final_resolution" in out.columns:
        out["final_resolution"] = out["A1R2N_final_resolution"].astype("string")
    elif "review_status" in out.columns:
        out["final_resolution"] = out["review_status"].astype("string")
    else:
        out["final_resolution"] = "UNKNOWN"

    out["is_valid_class"] = out["final_class"].isin(CLASS_MAP)
    out["is_resolved"] = out["is_valid_class"] & out["final_class"].notna()
    return out


def compute_gate_metrics(df: pd.DataFrame) -> dict[str, Any]:
    n = len(df)
    resolved = int(df["is_resolved"].sum())
    duplicate_ids = int(df["candidate_id"].duplicated().sum())
    coord_missing = int(df[["latitude", "longitude"]].isna().any(axis=1).sum())
    bad_year = int((~pd.to_numeric(df["target_year"], errors="coerce").isin([2005, 2015, 2025])).sum())

    class_counts = (
        df.loc[df["is_resolved"], "final_class"]
        .value_counts(dropna=False)
        .sort_index()
        .to_dict()
    )
    year_counts = (
        df.loc[df["is_resolved"], "target_year"]
        .value_counts(dropna=False)
        .sort_index()
        .to_dict()
    )

    unresolved = n - resolved
    coverage = resolved / n if n else 0.0
    return {
        "rows": n,
        "resolved": resolved,
        "unresolved": unresolved,
        "resolved_fraction": round(coverage, 6),
        "duplicate_candidate_ids": duplicate_ids,
        "missing_coordinates": coord_missing,
        "invalid_target_years": bad_year,
        "class_counts": {str(k): int(v) for k, v in class_counts.items()},
        "year_counts": {str(k): int(v) for k, v in year_counts.items()},
    }


def evaluate_gate(metrics: dict[str, Any], min_resolved_fraction: float = 1.0) -> tuple[bool, list[str]]:
    failures: list[str] = []
    if metrics["resolved_fraction"] < min_resolved_fraction:
        failures.append(
            f"resolved_fraction={metrics['resolved_fraction']:.3f} < {min_resolved_fraction:.3f}"
        )
    if metrics["duplicate_candidate_ids"]:
        failures.append(f"duplicate_candidate_ids={metrics['duplicate_candidate_ids']}")
    if metrics["missing_coordinates"]:
        failures.append(f"missing_coordinates={metrics['missing_coordinates']}")
    if metrics["invalid_target_years"]:
        failures.append(f"invalid_target_years={metrics['invalid_target_years']}")
    missing_classes = [str(c) for c in CLASS_MAP if str(c) not in metrics["class_counts"]]
    if missing_classes:
        failures.append("missing_classes=" + ",".join(missing_classes))
    return (not failures), failures


def run(input_csv: Path, output_dir: Path, min_resolved_fraction: float = 1.0) -> bool:
    output_dir.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(input_csv, low_memory=False)
    final_df = build_final_reference(df)
    metrics = compute_gate_metrics(final_df)
    passed, failures = evaluate_gate(metrics, min_resolved_fraction=min_resolved_fraction)

    final_df.to_csv(output_dir / "final_reference_normalized.csv", index=False)
    pd.DataFrame(
        [{"candidate_id": r.candidate_id, "target_year": r.target_year}
         for r in final_df.loc[~final_df["is_resolved"], ["candidate_id", "target_year"]].itertuples(index=False)]
    ).to_csv(output_dir / "unresolved_reference_queue.csv", index=False)

    report = {
        "gate": "REFERENCE_INTEGRITY",
        "status": "PASS" if passed else "FAIL",
        "metrics": metrics,
        "failures": failures,
    }
    (output_dir / "reference_gate_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return passed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/reconstruction/reference_gate"))
    parser.add_argument("--min-resolved-fraction", type=float, default=1.0)
    args = parser.parse_args()
    ok = run(args.input_csv, args.output_dir, args.min_resolved_fraction)
    raise SystemExit(0 if ok else 2)


if __name__ == "__main__":
    main()
