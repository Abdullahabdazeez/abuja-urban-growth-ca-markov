# Predicting Urban Growth to Support Better Planning — Abuja, Nigeria

<p align="center">
  <img src="outputs/maps/03_built_up_expansion_2025_2035.png" alt="Predicted built-up expansion in Abuja, 2025–2035" width="100%">
</p>

## Planning question

**Where is Abuja most likely to expand next, and how can planners prepare for that growth?**

Abuja continues to expand as new neighbourhoods, roads and commercial areas extend beyond the established urban core. I used historical land-cover transitions, an urban-expansion suitability surface and a quantity-constrained CA–Markov model to explore a **2035 strategic urban-growth scenario**.

The central result is that built-up land increases from about **1,168 km² in 2025 to 1,351 km² in 2035**, adding roughly **183 km²** of development. Because the historical simulation has moderate-to-low validation performance, the 2035 map is presented as an **early-warning and planning-screening scenario, not a certain forecast**.

## Key scenario findings

| Indicator | Result |
|---|---:|
| Built-up area, 2025 | **1,167.85 km²** |
| Built-up area, 2035 scenario | **1,351.30 km²** |
| Net built-up increase | **183.45 km²** |
| Relative built-up increase | **15.71%** |
| Required new built-up pixels | **206,027** |
| Allocated new built-up pixels | **203,889** |
| Allocation difference | **2,138 pixels** |
| Historical validation sample | **1,500** |
| Historical Overall Accuracy | **49.27%** |
| Historical Cohen's Kappa | **0.366** |

## Map suite

The project includes five core maps showing the baseline landscape, future scenario, modelled expansion, suitability and predicted transitions.

| Map | View |
|---|---|
| Land cover, 2025 | [Open map](outputs/maps/01_lulc_2025.png) |
| Predicted land cover, 2035 | [Open map](outputs/maps/02_predicted_lulc_2035.png) |
| Predicted built-up expansion, 2025–2035 | [Open map](outputs/maps/03_built_up_expansion_2025_2035.png) |
| Urban-expansion suitability | [Open map](outputs/maps/04_urban_expansion_suitability.png) |
| Predicted land-cover transitions, 2025–2035 | [Open map](outputs/maps/05_predicted_transitions_2025_2035.png) |

## Visual evidence

### Land-cover area comparison
<p align="center"><img src="outputs/charts/01_area_comparison_2025_2035.png" alt="Abuja land-cover area comparison, 2025 and 2035" width="85%"></p>

### Net land-cover change
<p align="center"><img src="outputs/charts/02_net_change_2025_2035.png" alt="Net land-cover change in Abuja, 2025–2035" width="85%"></p>

### Markov transition probabilities
<p align="center"><img src="outputs/charts/03_markov_transition_probabilities.png" alt="Markov transition probabilities" width="85%"></p>

### Suitability and allocation
<p align="center"><img src="outputs/charts/04_suitability_allocation.png" alt="Urban suitability and allocation summary" width="85%"></p>

### Historical simulation validation
<p align="center"><img src="outputs/charts/05_validation_summary.png" alt="Historical CA-Markov validation summary" width="80%"></p>

## Method

The scenario uses a quantity-constrained CA–Markov framework. Historical land-cover transitions from **2015 to 2025** were used to estimate transition probabilities. The model then estimated the quantity of additional built-up land required by 2035 and used an urban-expansion suitability surface to rank potential locations for growth.

The workflow was:

1. Estimate 2015–2025 land-cover transition probabilities.
2. Calculate the quantity of built-up growth required for 2035.
3. Develop an urban-expansion suitability surface.
4. Rank candidate development cells by suitability.
5. Allocate new built-up cells under a quantity constraint.
6. Produce the 2035 LULC, built-up-expansion and transition surfaces.
7. Compare 2025 and 2035 land-cover areas.
8. Report historical simulation validation and uncertainty alongside the scenario.

The scenario rasters use a **30 m grid** in **WGS 84 / UTM Zone 32N (EPSG:32632)**.

## Land-cover change in the scenario

| Class | 2025 (km²) | 2035 scenario (km²) | Net change (km²) | Relative change |
|---|---:|---:|---:|---:|
| Bare land | 1,741.57 | 1,722.86 | -18.70 | -1.07% |
| **Built-up** | **1,167.85** | **1,351.30** | **+183.45** | **+15.71%** |
| Cropland | 2,170.11 | 2,016.37 | -153.74 | -7.08% |
| Vegetation | 2,177.91 | 2,166.91 | -11.00 | -0.51% |
| Water | 93.86 | 93.86 | 0.00 | 0.00% |

The scenario therefore allocates substantial new built-up land while reducing the modelled extent of several non-built classes, particularly cropland.

## Validation and uncertainty

The historical CA–Markov simulation was evaluated against observed 2025 land cover using **1,500 validation samples**.

| Metric | Result |
|---|---:|
| Overall Accuracy | **0.4927 (49.27%)** |
| Cohen's Kappa | **0.3658** |

These results limit confidence in the exact location of future growth. The scenario should therefore be interpreted at a **metropolitan and strategic scale**. It is useful for identifying areas that may deserve closer review, but it should not be used as a parcel-level prediction or as a substitute for current planning data.

## Planning value

The value of the model is not certainty about 2035. Its value is helping planners ask better questions earlier. The scenario can support:

- early identification of possible urban-growth corridors;
- discussion of where roads and utilities may require future upgrades;
- screening of pressure on schools, healthcare, drainage and public transport;
- identification of cropland and other non-built land facing potential conversion pressure;
- stronger development-control attention in likely expansion areas; and
- prioritisation of locations for more detailed field and planning investigation.

The scenario should be reviewed together with current development plans, population trends, infrastructure projects, field evidence and newer satellite imagery before site-specific decisions are made.

## Repository guide

- [`outputs/maps`](outputs/maps/) — final scenario maps
- [`outputs/charts`](outputs/charts/) — statistical, model and validation figures
- [`outputs/tables`](outputs/tables/) — machine-readable results
- [`docs/DATA_SOURCES.md`](docs/DATA_SOURCES.md) — data and source notes
- [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) — analytical method
- [`docs/RESULTS.md`](docs/RESULTS.md) — detailed scenario findings
- [`docs/LIMITATIONS.md`](docs/LIMITATIONS.md) — uncertainty and interpretation boundaries
- [`docs/PROJECT_REPORT.md`](docs/PROJECT_REPORT.md) — portfolio report source
- [`reports/Abuja_Urban_Growth_Portfolio_Report.pdf`](reports/Abuja_Urban_Growth_Portfolio_Report.pdf) — portfolio PDF report

## Tools

Google Earth Engine · GIS · Remote Sensing · CA–Markov · Suitability Modelling · Spatial Analysis · Python · Git · GitHub

## Limitations

- Historical validation achieved **49.27% Overall Accuracy** and **Kappa 0.366**.
- The 2035 output is a modelled scenario, not a deterministic forecast.
- Future growth is influenced by policy, infrastructure investment, land markets, population change and other factors that may not be fully represented by historical land-cover transitions.
- The suitability surface and transition probabilities should be updated as newer evidence becomes available.
- The scenario should not be used for parcel-level development decisions without additional local evidence.

## Author

**Abdullah Abdazeez Ayomide**  
Urban & Regional Planner · GIS & Remote Sensing · Spatial Decision Support

## Citation

**Abdullah Abdazeez Ayomide (2026). _Predicting Urban Growth to Support Better Planning — Abuja, Nigeria_.**
