#!/usr/bin/env python3
"""Abuja CA-Markov reconstruction automation controller.

This controller is deliberately conservative: ambiguous reference cases are excluded,
never auto-invented. It is designed for Colab/Drive execution and for CI unit tests.
Earth Engine-dependent classification/model steps are represented as gated stage hooks;
local QA/validation utilities are fully executable and fail closed.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd

CLASS_IDS = (1, 2, 3, 4, 5)
CLASS_NAMES = {1: "Built-up", 2: "Vegetation", 3: "Cropland", 4: "Bare land", 5: "Water"}


@dataclass(frozen=True)
class GateThresholds:
    min_reference_per_class_year: int = 20
    min_oa: float = 0.85
    min_kappa: float = 0.80
    min_macro_f1: float = 0.80
    min_built_precision: float = 0.80
    min_built_recall: float = 0.80
    min_built_persistence: float = 0.90
    max_water_to_built_fraction: float = 0.05
    min_hindcast_fom: float = 0.15
    max_quantity_disagreement: float = 0.20
    max_allocation_disagreement: float = 0.30
    min_suitability_auc: float = 0.70


@dataclass
class StageResult:
    stage: str
    passed: bool
    metrics: Dict[str, float | int | str]
    failures: List[str]

    def to_dict(self):
        return asdict(self)


def _safe_numeric(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def build_reference_gate(df: pd.DataFrame, thresholds: GateThresholds) -> Tuple[pd.DataFrame, StageResult]:
    """Produce a conservative training/validation reference subset.

    Resolution priority:
      1) explicit A1R2N final class when A1R2N_final_resolution is not uncertain/manual;
      2) existing human label when present;
      3) otherwise exclude.
    No uncertain case is forced into a class.
    """
    x = df.copy()
    final = pd.Series(np.nan, index=x.index, dtype="float64")
    source = pd.Series("EXCLUDED_UNRESOLVED", index=x.index, dtype="object")

    if "A1R2N_final_class" in x:
        vals = _safe_numeric(x["A1R2N_final_class"])
        status = x.get("A1R2N_final_resolution", pd.Series("", index=x.index)).astype(str).str.upper()
        safe = vals.isin(CLASS_IDS) & ~status.str.contains("UNCERTAIN|MANUAL_REQUIRED|PENDING", regex=True)
        final.loc[safe] = vals.loc[safe]
        source.loc[safe] = "A1R2N_FINAL"

    if "A1R2N_human_label" in x:
        vals = _safe_numeric(x["A1R2N_human_label"])
        safe = final.isna() & vals.isin(CLASS_IDS)
        final.loc[safe] = vals.loc[safe]
        source.loc[safe] = "A1R2N_HUMAN"

    if "human_label" in x:
        vals = _safe_numeric(x["human_label"])
        safe = final.isna() & vals.isin(CLASS_IDS)
        final.loc[safe] = vals.loc[safe]
        source.loc[safe] = "PRIOR_HUMAN"

    x["final_reference_class"] = final.astype("Int64")
    x["final_reference_name"] = x["final_reference_class"].map(CLASS_NAMES)
    x["reference_resolution_source"] = source
    x["reference_usable"] = x["final_reference_class"].isin(CLASS_IDS)

    failures: List[str] = []
    usable = x[x["reference_usable"]].copy()
    if "target_year" not in usable:
        failures.append("target_year column missing")
    else:
        counts = usable.groupby(["target_year", "final_reference_class"]).size()
        for year in sorted(pd.unique(_safe_numeric(usable["target_year"]).dropna()).astype(int)):
            for cid in CLASS_IDS:
                n = int(counts.get((year, cid), 0))
                if n < thresholds.min_reference_per_class_year:
                    failures.append(f"reference shortage: year={year}, class={cid}, n={n}")

    metrics = {
        "input_rows": int(len(x)),
        "usable_rows": int(x["reference_usable"].sum()),
        "excluded_rows": int((~x["reference_usable"]).sum()),
        "usable_fraction": float(x["reference_usable"].mean()) if len(x) else 0.0,
    }
    return x, StageResult("01_REFERENCE_GATE", not failures, metrics, failures)


def confusion_metrics(y_true: Iterable[int], y_pred: Iterable[int]) -> Dict[str, float]:
    yt = np.asarray(list(y_true), dtype=int)
    yp = np.asarray(list(y_pred), dtype=int)
    labels = np.asarray(CLASS_IDS)
    cm = np.zeros((len(labels), len(labels)), dtype=np.int64)
    idx = {c: i for i, c in enumerate(labels)}
    for a, b in zip(yt, yp):
        if a in idx and b in idx:
            cm[idx[a], idx[b]] += 1
    total = cm.sum()
    oa = float(np.trace(cm) / total) if total else np.nan
    row = cm.sum(axis=1)
    col = cm.sum(axis=0)
    pe = float((row * col).sum() / (total * total)) if total else np.nan
    kappa = float((oa - pe) / (1 - pe)) if total and pe < 1 else np.nan
    f1s = []
    prec = {}
    rec = {}
    for i, c in enumerate(labels):
        tp = cm[i, i]
        p = float(tp / col[i]) if col[i] else 0.0
        r = float(tp / row[i]) if row[i] else 0.0
        f1 = float(2 * p * r / (p + r)) if p + r else 0.0
        prec[int(c)] = p
        rec[int(c)] = r
        f1s.append(f1)
    return {
        "oa": oa,
        "kappa": kappa,
        "macro_f1": float(np.mean(f1s)),
        "built_precision": prec[1],
        "built_recall": rec[1],
    }


def classification_gate(y_true, y_pred, thresholds: GateThresholds, stage="CLASSIFICATION") -> StageResult:
    m = confusion_metrics(y_true, y_pred)
    failures = []
    checks = {
        "oa": thresholds.min_oa,
        "kappa": thresholds.min_kappa,
        "macro_f1": thresholds.min_macro_f1,
        "built_precision": thresholds.min_built_precision,
        "built_recall": thresholds.min_built_recall,
    }
    for k, v in checks.items():
        if not np.isfinite(m[k]) or m[k] < v:
            failures.append(f"{k}={m[k]:.4f} < {v:.4f}")
    return StageResult(stage, not failures, m, failures)


def transition_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = np.asarray(a).astype(int).ravel()
    b = np.asarray(b).astype(int).ravel()
    cm = np.zeros((5, 5), dtype=np.int64)
    for x, y in zip(a, b):
        if x in CLASS_IDS and y in CLASS_IDS:
            cm[x - 1, y - 1] += 1
    return cm


def temporal_transition_gate(a: np.ndarray, b: np.ndarray, thresholds: GateThresholds, stage="TEMPORAL_TRANSITION") -> StageResult:
    cm = transition_matrix(a, b)
    row = cm.sum(axis=1)
    built_persistence = float(cm[0, 0] / row[0]) if row[0] else 0.0
    water_to_built = float(cm[4, 0] / row[4]) if row[4] else 0.0
    failures = []
    if built_persistence < thresholds.min_built_persistence:
        failures.append(f"built_persistence={built_persistence:.4f} < {thresholds.min_built_persistence:.4f}")
    if water_to_built > thresholds.max_water_to_built_fraction:
        failures.append(f"water_to_built={water_to_built:.4f} > {thresholds.max_water_to_built_fraction:.4f}")
    return StageResult(stage, not failures, {"built_persistence": built_persistence, "water_to_built_fraction": water_to_built}, failures)


def hindcast_metrics(observed_change: np.ndarray, simulated_change: np.ndarray) -> Dict[str, float]:
    o = np.asarray(observed_change, dtype=bool).ravel()
    s = np.asarray(simulated_change, dtype=bool).ravel()
    hits = int(np.sum(o & s))
    misses = int(np.sum(o & ~s))
    false_alarms = int(np.sum(~o & s))
    denom = hits + misses + false_alarms
    fom = float(hits / denom) if denom else 1.0
    n = len(o)
    quantity = float(abs(int(o.sum()) - int(s.sum())) / n) if n else np.nan
    allocation = float(2 * min(misses, false_alarms) / n) if n else np.nan
    return {"fom": fom, "quantity_disagreement": quantity, "allocation_disagreement": allocation}


def hindcast_gate(observed_change, simulated_change, thresholds: GateThresholds) -> StageResult:
    m = hindcast_metrics(observed_change, simulated_change)
    failures = []
    if m["fom"] < thresholds.min_hindcast_fom:
        failures.append(f"fom={m['fom']:.4f} < {thresholds.min_hindcast_fom:.4f}")
    if m["quantity_disagreement"] > thresholds.max_quantity_disagreement:
        failures.append("quantity disagreement exceeds gate")
    if m["allocation_disagreement"] > thresholds.max_allocation_disagreement:
        failures.append("allocation disagreement exceeds gate")
    return StageResult("HINDCAST_GATE", not failures, m, failures)


def save_stage_result(result: StageResult, outdir: Path):
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / f"{result.stage}.json").write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")


def run_reference_gate(input_csv: Path, output_dir: Path, thresholds: Optional[GateThresholds] = None) -> StageResult:
    thresholds = thresholds or GateThresholds()
    df = pd.read_csv(input_csv, low_memory=False)
    gated, result = build_reference_gate(df, thresholds)
    output_dir.mkdir(parents=True, exist_ok=True)
    gated.to_csv(output_dir / "Reference_Gate_All_Candidates.csv", index=False)
    gated[gated["reference_usable"]].to_csv(output_dir / "Reference_Usable.csv", index=False)
    gated[~gated["reference_usable"]].to_csv(output_dir / "Reference_Excluded_Unresolved.csv", index=False)
    save_stage_result(result, output_dir)
    return result


def main():
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--reference-csv", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--min-reference-per-class-year", type=int, default=20)
    args = p.parse_args()
    t = GateThresholds(min_reference_per_class_year=args.min_reference_per_class_year)
    result = run_reference_gate(args.reference_csv, args.output_dir, t)
    print(json.dumps(result.to_dict(), indent=2))
    raise SystemExit(0 if result.passed else 2)


if __name__ == "__main__":
    main()
