from __future__ import annotations

from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch

ROOT = Path(__file__).resolve().parents[2]
RASTERS = ROOT / "data/processed/rasters"
TABLES = ROOT / "data/processed/tables"
MAPS = ROOT / "outputs/maps"
CHARTS = ROOT / "outputs/charts"

MAPS.mkdir(parents=True, exist_ok=True)
CHARTS.mkdir(parents=True, exist_ok=True)

labels = ["Built-up", "Vegetation", "Cropland", "Bare land", "Water"]
colors = ["#d7191c", "#1a9641", "#fdae61", "#a6611a", "#2c7bb6"]
cmap = ListedColormap(colors)
norm = BoundaryNorm([0.5, 1.5, 2.5, 3.5, 4.5, 5.5], cmap.N)
handles = [Patch(facecolor=c, label=l) for c, l in zip(colors, labels)]

boundary = gpd.read_file(ROOT / "data/processed/boundary/Abuja_FCT_Boundary.geojson")


def read_raster(name: str):
    with rasterio.open(RASTERS / name) as src:
        arr = src.read(1).astype(float)
        arr[arr == 0] = np.nan
        extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]
        crs = src.crs
    return arr, extent, crs


def plot_lulc(name: str, title: str, output: str) -> None:
    arr, extent, crs = read_raster(name)
    fig, ax = plt.subplots(figsize=(8.2, 8.8))
    ax.imshow(arr, extent=extent, origin="upper", cmap=cmap, norm=norm)
    boundary.to_crs(crs).boundary.plot(ax=ax, color="black", linewidth=0.8)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("Easting (m) — WGS 84 / UTM Zone 32N")
    ax.set_ylabel("Northing (m)")
    ax.legend(handles=handles, loc="lower right", fontsize=8)
    ax.set_aspect("equal")
    fig.tight_layout()
    fig.savefig(MAPS / output, dpi=220, bbox_inches="tight")
    plt.close(fig)


plot_lulc("Abuja_Derived_LULC_2025.tif", "Abuja Land Use and Land Cover — 2025", "01_lulc_2025.png")
plot_lulc("Abuja_Predicted_LULC_2035.tif", "Predicted Abuja Land Use and Land Cover — 2035", "02_predicted_lulc_2035.png")

area = pd.read_csv(TABLES / "Abuja_LULC_Area_2025_2035.csv")
pivot = area.pivot(index="class_name", columns="year", values="area_sqkm").loc[labels]
fig, ax = plt.subplots(figsize=(9, 5.4))
pivot.plot(kind="bar", ax=ax)
ax.set_title("Land-cover area comparison, 2025 and 2035", fontweight="bold")
ax.set_ylabel("Area (km²)")
ax.set_xlabel("Land-cover class")
ax.tick_params(axis="x", rotation=0)
fig.tight_layout()
fig.savefig(CHARTS / "01_area_comparison_2025_2035.png", dpi=220, bbox_inches="tight")
plt.close(fig)

print("Repository figures regenerated.")
