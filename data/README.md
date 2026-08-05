# Data

The repository contains the compact final outputs required to review and reproduce the published figures.

## Included

- Derived 2025 LULC raster reconstructed from the first digit of the 2025–2035 transition codes.
- Predicted 2035 LULC raster.
- Built-up expansion raster for 2025–2035.
- Transition-code raster for 2025–2035.
- Urban-expansion suitability surface, stored as scaled UInt16 with DEFLATE compression; multiply stored values by 0.0001 to recover the 0–1 suitability score.
- Abuja FCT boundary as GeoJSON.
- Clean CSV tables for area, transition probabilities, prediction summary and historical validation.

## Excluded

Raw Landsat imagery, manual training polygons and Earth Engine assets are not committed. They should be acquired from their original providers and recreated using the documented cloud workflow.
