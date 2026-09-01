# Outputs / tables

Supplementary tables generated during the analysis, kept alongside the authoritative
summary tables in [`data/processed/tables`](../../data/processed/tables/).

`key_findings.csv` and `lulc_change_summary.csv` restate the authoritative figures used
throughout the README and reports.

`transition_area_from_raster.csv` and `suitability_allocation_summary.csv` are raw
pixel-count tabulations converted to area using a flat nominal resolution
(900 m² per pixel), rather than the precise per-pixel area sum used to derive the
authoritative `built_up_area_2035_sqkm` and `allocated_new_built_up_pixels` figures in
`data/processed/tables/Abuja_Prediction_Summary.csv`. As a result, totals in these two
files differ from the authoritative figures by a small margin (about 0.09% for the 2035
built-up area, about 0.004% for the allocated-pixel count) — this is an expected artifact
of the flat-resolution approximation, not a data error. Treat
`Abuja_Prediction_Summary.csv` / `key_findings.csv` as the authoritative source for any
figure quoted in the README or reports.
