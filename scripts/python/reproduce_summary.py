from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import rasterio

ROOT = Path(__file__).resolve().parents[2]
TABLES = ROOT / "data/processed/tables"
RASTERS = ROOT / "data/processed/rasters"

summary = pd.read_csv(TABLES / "Abuja_Prediction_Summary.csv").iloc[0]
validation = pd.read_csv(TABLES / "Abuja_Historical_Validation_Summary.csv").iloc[0]

assert np.isclose(summary["built_up_area_2025_sqkm"], 1167.8509076325397, atol=1e-6)
assert np.isclose(summary["built_up_area_2035_sqkm"], 1351.2966732891698, atol=1e-6)
assert np.isclose(summary["built_up_net_change_sqkm"], 183.4457656566301, atol=1e-6)
assert np.isclose(validation["overall_accuracy_percent"], 49.266666666666666, atol=1e-6)

for raster_name in [
    "Abuja_Derived_LULC_2025.tif",
    "Abuja_Predicted_LULC_2035.tif",
    "Abuja_BuiltUp_Expansion_2025_2035.tif",
    "Abuja_Transition_2025_2035.tif",
    "Abuja_Urban_Expansion_Suitability_uint16.tif",
]:
    with rasterio.open(RASTERS / raster_name) as src:
        if src.crs.to_epsg() != 32632:
            raise ValueError(f"Unexpected CRS for {raster_name}: {src.crs}")
        if not np.isclose(abs(src.transform.a), 30):
            raise ValueError(f"Unexpected resolution for {raster_name}: {src.transform.a}")
        if raster_name == "Abuja_Urban_Expansion_Suitability_uint16.tif":
            if src.dtypes[0] != "uint16":
                raise ValueError(f"Unexpected suitability dtype: {src.dtypes[0]}")
            if not np.isclose(src.scales[0], 0.0001):
                raise ValueError(f"Unexpected suitability scale: {src.scales[0]}")

print("REPRODUCTION CHECK: PASSED")
print(f"Built-up area: {summary['built_up_area_2025_sqkm']:.2f} km² (2025) -> {summary['built_up_area_2035_sqkm']:.2f} km² (2035)")
print(f"Net built-up increase: {summary['built_up_net_change_sqkm']:.2f} km²")
print(f"Historical validation: {validation['overall_accuracy_percent']:.2f}% OA; Kappa {validation['kappa']:.3f}")
