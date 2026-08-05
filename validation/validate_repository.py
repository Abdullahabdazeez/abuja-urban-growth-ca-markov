from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

ROOT = Path(__file__).resolve().parents[1]

required_files = [
    "README.md", "LICENSE", "CITATION.cff", "project.json", "requirements.txt",
    "assets/project-cover.png", "assets/repository-social-preview.png",
    "data/processed/boundary/Abuja_FCT_Boundary.geojson",
    "data/processed/rasters/Abuja_Derived_LULC_2025.tif",
    "data/processed/rasters/Abuja_Predicted_LULC_2035.tif",
    "data/processed/rasters/Abuja_BuiltUp_Expansion_2025_2035.tif",
    "data/processed/rasters/Abuja_Transition_2025_2035.tif",
    "data/processed/rasters/Abuja_Urban_Expansion_Suitability_uint16.tif",
    "data/processed/tables/Abuja_LULC_Area_2025_2035.csv",
    "data/processed/tables/Abuja_Prediction_Summary.csv",
    "data/processed/tables/Abuja_Historical_Validation_Summary.csv",
    "outputs/maps/01_lulc_2025.png", "outputs/maps/02_predicted_lulc_2035.png",
    "outputs/maps/03_built_up_expansion_2025_2035.png",
    "outputs/charts/01_area_comparison_2025_2035.png",
    "scripts/python/reproduce_summary.py",
]

failures = []
for rel in required_files:
    if not (ROOT / rel).is_file():
        failures.append(f"Missing file: {rel}")

for path in ROOT.rglob("*"):
    if path.is_file() and ".git" not in path.parts:
        size_mb = path.stat().st_size / (1024 * 1024)
        if size_mb > 24.5:
            failures.append(f"Browser-upload limit exceeded: {path.relative_to(ROOT)} ({size_mb:.2f} MB)")

try:
    metadata = json.loads((ROOT / "project.json").read_text(encoding="utf-8"))
    if metadata.get("repository_name") != "abuja-urban-growth-ca-markov":
        failures.append("Unexpected repository_name in project.json")
except Exception as exc:
    failures.append(f"Invalid project.json: {exc}")

try:
    summary = pd.read_csv(ROOT / "data/processed/tables/Abuja_Prediction_Summary.csv").iloc[0]
    if not np.isclose(summary["built_up_net_change_sqkm"], 183.4457656566301, atol=1e-6):
        failures.append("Prediction summary does not match the verified built-up net change")
except Exception as exc:
    failures.append(f"Prediction table check failed: {exc}")

for name in [
    "Abuja_Derived_LULC_2025.tif", "Abuja_Predicted_LULC_2035.tif",
    "Abuja_BuiltUp_Expansion_2025_2035.tif", "Abuja_Transition_2025_2035.tif",
    "Abuja_Urban_Expansion_Suitability_uint16.tif",
]:
    try:
        with rasterio.open(ROOT / "data/processed/rasters" / name) as src:
            if src.crs.to_epsg() != 32632:
                failures.append(f"Unexpected CRS: {name} -> {src.crs}")
            if not np.isclose(abs(src.transform.a), 30):
                failures.append(f"Unexpected resolution: {name} -> {src.transform.a}")
            if name == "Abuja_Urban_Expansion_Suitability_uint16.tif":
                if src.dtypes[0] != "uint16":
                    failures.append(f"Unexpected suitability dtype: {src.dtypes[0]}")
                if not np.isclose(src.scales[0], 0.0001):
                    failures.append(f"Unexpected suitability scale: {src.scales[0]}")
    except Exception as exc:
        failures.append(f"Raster validation failed for {name}: {exc}")

if failures:
    print("REPOSITORY VALIDATION: FAILED")
    for failure in failures:
        print(f"- {failure}")
    sys.exit(1)

print("REPOSITORY VALIDATION: PASSED")
print("Required files, metadata, statistics, raster CRS, resolution and upload-size limits are valid.")
