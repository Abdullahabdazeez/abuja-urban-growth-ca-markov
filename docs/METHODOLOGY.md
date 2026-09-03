# Methodology

The project uses a quantity-constrained CA-Markov framework to explore a 2035 urban-growth scenario for the Federal Capital Territory, Abuja.

Historical land-cover transitions from 2015 to 2025 were used to estimate Markov transition probabilities. The model then calculated the required quantity of future built-up land. An urban-expansion suitability surface ranked candidate locations, and cellular allocation assigned new built-up cells until the modelled demand was approached.

The resulting products include a predicted 2035 LULC raster, built-up-expansion raster, transition raster, suitability surface and summary tables.

The scenario rasters use a 30 m grid in WGS 84 / UTM Zone 32N (EPSG:32632).

## Historical validation

The historical simulation was validated against observed 2025 LULC using **1,500 samples**.

| Metric | Result |
|---|---:|
| Overall Accuracy | **49.27%** |
| Cohen's Kappa | **0.366** |

These values limit forecast confidence. The 2035 output is therefore communicated as a **strategic planning scenario**, not a deterministic forecast.

## Interpretation

The model is most useful for metropolitan-scale screening: identifying locations where future development pressure may justify earlier review of infrastructure, development control and environmental safeguards. Site-specific decisions require current plans, field evidence and updated spatial data.