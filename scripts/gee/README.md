# Google Earth Engine workflow record

The original cloud workflow was developed in Google Earth Engine and depended on five imported 2025 training-polygon layers:

- `builtUp2025`
- `vegetation2025`
- `CropLand2025`
- `BareLand2025`
- `Water2025`

It used Landsat Collection 2 Level-2 imagery, QA masking, surface-reflectance scaling, five spectral indices, balanced stratified samples, 250-tree Random Forest ensembles, and stable-label transfer to build the 2005, 2015 and 2025 LULC series.

The final archive supplied for GitHub publication did not include the complete cloud script or imported assets. No synthetic replacement is presented as the original analysis. The detailed methodology is preserved in `docs/METHODOLOGY.md`, while the local Python scripts reproduce the published figures and statistics from the supplied final outputs.
