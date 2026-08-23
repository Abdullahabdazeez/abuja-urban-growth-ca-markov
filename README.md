# Abuja Urban Growth CA–Markov — Reconstruction in Progress

> **Scientific status: provisional / under reconstruction.**
>
> The original 2025–2035 CA–Markov scenario remains public for provenance, but its historical LULC inputs and validation framework are currently being rebuilt. The existing 2035 scenario should **not** be treated as a final forecast or as the definitive project result until the reconstruction is complete.

## Why the project is being rebuilt

A later scientific audit identified three problems in the original workflow:

1. **Historical simulation agreement was weak.** The original hindcast produced **49.27% overall accuracy** and **0.366 Kappa** on 1,500 comparison points.
2. **The 2015–2025 transition matrix contains physically questionable instability.** Built-up persistence was only about **0.648**, implying substantial Built-up → non-Built-up change. Cropland and Bare-land persistence were also weak. This is more consistent with classification instability than with reliable land-change dynamics at the reported scale.
3. **Suitability discrimination needs stronger testing.** The original suitability surface clustered tightly around its central range, so the reconstruction will explicitly test whether it meaningfully separates observed expansion from non-expansion locations.

Because the CA–Markov projection inherits errors from the historical LULC maps, the current priority is to **repair the input classifications first** before rebuilding the transition, suitability and allocation stages.

## Reconstruction plan

The project is being rebuilt in the following order:

1. Freeze the original 2005, 2015, 2025 and 2035 outputs as baseline provenance.
2. Audit class areas, persistence and all 2005→2015 and 2015→2025 transitions.
3. Review Built-up reversions and other implausible transitions spatially.
4. Reconstruct a stronger human-reviewed reference dataset.
5. Rebuild the historical LULC classifications using a leakage-free validation design.
6. Test temporal consistency before rebuilding Markov probabilities.
7. Evaluate historical land-change simulation using **Figure of Merit**, **quantity disagreement** and **allocation disagreement**, with conventional accuracy statistics retained only as supplementary context where useful.
8. Rebuild and test the suitability model against observed historical expansion.
9. Validate an historical hindcast before producing any new 2035 scenario.
10. Freeze the new results only after the complete validation sequence passes.

## Original scenario retained for provenance

The original workflow combined historical LULC maps, a 2015–2025 Markov transition matrix, an urban-expansion suitability surface and quantity-constrained cellular allocation.

It produced the following **provisional historical scenario values**:

| Indicator | Original value |
|---|---:|
| Built-up area, 2025 | 1,167.85 km² |
| Simulated built-up area, 2035 | 1,351.30 km² |
| Simulated net increase | 183.45 km² |
| Simulated relative increase | 15.71% |
| Historical hindcast OA | 49.27% |
| Historical hindcast Kappa | 0.366 |

These values are preserved only so the reconstruction remains transparent and auditable. They are **not currently endorsed as final planning results**.

## Current scientific position

The model should not be used for parcel-level development decisions, deterministic forecasting or definitive statements about Abuja's 2035 urban footprint while reconstruction is underway.

The final project will only publish a new 2035 scenario if the rebuilt historical classifications and hindcast validation provide defensible evidence that the transition and allocation logic are working as intended.

## Repository contents

Historical maps, tables, scripts and outputs remain in the repository as provenance for the original workflow. During reconstruction, newer validated products will supersede these files in a controlled sequence rather than silently overwriting the scientific record.

## Author

**Abdullah Abdazeez Ayomide**  
Geo-spatial Planner | GIS & Remote Sensing Analyst | Urban & Environmental Planning Researcher

- [GitHub profile](https://github.com/Abdullahabdazeez)
- [LinkedIn](https://ng.linkedin.com/in/abdazeez-abdullah-4b814719a)
- [Email](mailto:abdazeezabdullah1@gmail.com)

## Status

**Reconstruction in progress — original CA–Markov scenario retained for provenance only.**
