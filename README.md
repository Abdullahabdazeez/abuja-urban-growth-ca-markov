# Abuja Urban Growth CA–Markov Model — Reconstruction in Progress

> **Current status:** the original 2035 scenario is kept here for transparency, but I am rebuilding the historical LULC and validation workflow. The existing 2035 map should be treated as **provisional**, not as a final forecast.

## What this project is trying to answer

Can historical land-cover change in Abuja support a defensible simulation of where urban growth may occur by 2035?

The original project combined historical LULC maps, Markov transition probabilities, an urban-suitability surface and cellular allocation. A later audit showed that some of the historical inputs were not strong enough to support the confidence I wanted for the final scenario.

Rather than hide that weakness, I kept the original work public and started rebuilding the model from the historical classifications upward.

## Why I am rebuilding it

Three issues stood out during the audit.

First, the original historical hindcast achieved only **49.27% overall accuracy** and **0.366 Kappa** on 1,500 comparison points. That is too weak to treat the later scenario as a confident forecast.

Second, the 2015–2025 transition matrix showed questionable instability. Built-up persistence was only about **0.648**, which implied an unusually large amount of Built-up → non-Built-up change. Cropland and Bare-land persistence were also weak. That pattern is more consistent with classification instability than with reliable land-change dynamics at the reported scale.

Third, the original suitability surface was tightly clustered around its middle range. The rebuilt workflow therefore needs to test whether the suitability model can genuinely separate observed expansion from non-expansion locations.

## Original scenario retained for provenance

| Indicator | Original value |
|---|---:|
| Built-up area, 2025 | **1,167.85 km²** |
| Simulated built-up area, 2035 | **1,351.30 km²** |
| Simulated net increase | **183.45 km²** |
| Simulated relative increase | **15.71%** |
| Historical hindcast OA | **49.27%** |
| Historical hindcast Kappa | **0.366** |

I keep these numbers because they are part of the project's history. They are **not currently endorsed as final planning results**.

## Reconstruction plan

1. Preserve the original 2005, 2015, 2025 and 2035 products as a baseline record.
2. Audit class areas, persistence and the 2005→2015 and 2015→2025 transitions.
3. Inspect Built-up reversions and other implausible transitions spatially.
4. Rebuild a stronger human-reviewed reference dataset.
5. Reclassify the historical LULC maps with leakage-free validation.
6. Check temporal consistency before rebuilding the Markov probabilities.
7. Validate historical change with **Figure of Merit, quantity disagreement and allocation disagreement**, while keeping conventional accuracy measures as supporting context.
8. Test the suitability model against observed historical expansion.
9. Run and validate a historical hindcast.
10. Produce a new 2035 scenario only if the earlier stages pass.

## Why this matters

A CA–Markov model can produce a convincing-looking future map even when the historical classifications feeding it are unstable. For planning, that is dangerous because the map may look more certain than the evidence really is.

The reconstruction is therefore focused less on making the 2035 output look impressive and more on making sure the chain of evidence behind it is defensible.

## Current use

The repository is useful as a transparent record of the original workflow and the reconstruction process. The current 2035 scenario should **not** be used for parcel-level decisions, deterministic forecasting or definitive statements about Abuja's future urban footprint.

A new scenario will only replace it after the rebuilt historical classifications, transition logic, suitability model and hindcast have passed the full validation sequence.

## Repository contents

The repository keeps the original maps, tables, scripts and outputs for provenance while the reconstructed products are added in a controlled sequence. Superseded material is not silently rewritten as though it had always been final.

## Tools

Google Earth Engine · Python · GIS · Remote sensing · LULC change analysis · CA–Markov · Suitability modelling · Validation diagnostics

## Author

**Abdullah Abdazeez Ayomide**  
Geospatial Planner · GIS & Remote Sensing Analyst · Urban & Environmental Planning Researcher

[GitHub](https://github.com/Abdullahabdazeez) · [LinkedIn](https://ng.linkedin.com/in/abdazeez-abdullah-4b814719a)

## Status

**Reconstruction in progress — original CA–Markov scenario retained for provenance only.**
