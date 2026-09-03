# Project Report: Predicting Urban Growth to Support Better Planning — Abuja, Nigeria

## Project overview

This project explores where Abuja may experience further urban expansion by 2035 and how that information can support earlier planning decisions. Historical land-cover transitions were combined with an urban-expansion suitability surface and a quantity-constrained CA–Markov allocation model.

The purpose of the scenario is not to claim certainty about the future. It is to provide a spatial early-warning layer that can support discussion about infrastructure, development control, environmental protection and locations that may need closer investigation.

## Planning question

**Where is Abuja most likely to expand next, and how can planners prepare for that growth?**

## Method

The workflow used land-cover transitions from 2015 to 2025 to estimate Markov transition probabilities. The model then calculated the quantity of additional built-up land required for 2035. An urban-expansion suitability surface ranked candidate locations, and new built-up cells were allocated under a quantity constraint until the modelled demand was approached.

The main outputs are:

1. 2025 land-cover baseline;
2. predicted 2035 land-cover scenario;
3. predicted built-up expansion between 2025 and 2035;
4. urban-expansion suitability surface;
5. predicted land-cover transitions; and
6. scenario and validation summary tables.

The scenario rasters use a 30 m grid in WGS 84 / UTM Zone 32N (EPSG:32632).

## Scenario results

| Indicator | Result |
|---|---:|
| Built-up area, 2025 | 1,167.85 km² |
| Built-up area, 2035 scenario | 1,351.30 km² |
| Net built-up increase | 183.45 km² |
| Relative built-up increase | 15.71% |
| Required new built-up pixels | 206,027 |
| Allocated new built-up pixels | 203,889 |
| Allocation difference | 2,138 pixels |

### Land-cover change

| Class | 2025 (km²) | 2035 scenario (km²) | Net change (km²) | Relative change |
|---|---:|---:|---:|---:|
| Bare land | 1,741.57 | 1,722.86 | -18.70 | -1.07% |
| Built-up | 1,167.85 | 1,351.30 | +183.45 | +15.71% |
| Cropland | 2,170.11 | 2,016.37 | -153.74 | -7.08% |
| Vegetation | 2,177.91 | 2,166.91 | -11.00 | -0.51% |
| Water | 93.86 | 93.86 | 0.00 | 0.00% |

The scenario therefore shows a substantial increase in built-up land and a modelled reduction in several non-built classes, particularly cropland.

## Validation and uncertainty

The historical CA–Markov simulation was compared with observed 2025 land cover using 1,500 validation samples.

| Metric | Result |
|---|---:|
| Overall Accuracy | 0.4927 (49.27%) |
| Cohen's Kappa | 0.3658 |

This level of agreement means that the exact spatial pattern of the 2035 scenario should be interpreted cautiously. The map is most appropriate for metropolitan-scale planning discussion and screening, not parcel-level prediction.

## Planning interpretation

The strongest planning use of the scenario is as an early-warning layer. Likely growth locations can be reviewed against current and planned roads, utilities, schools, healthcare, drainage, public transport and environmental constraints.

The scenario can support:

- early identification of possible growth corridors;
- prioritisation of locations for more detailed planning investigation;
- discussion of infrastructure capacity before development pressure intensifies;
- review of development-control priorities; and
- monitoring of cropland and other non-built land facing potential conversion pressure.

The scenario should be used alongside current development plans, population trends, infrastructure projects, field evidence and updated satellite imagery.

## Limitations

The historical validation achieved 49.27% Overall Accuracy and Kappa 0.366. Future urban expansion is also affected by policy, infrastructure investment, land markets, demographic change and other factors that may not be fully represented by historical land-cover transitions.

The 2035 output should therefore be treated as a strategic scenario rather than a deterministic forecast. It is not suitable for parcel-level decisions without additional local evidence.

## Tools

Google Earth Engine · GIS · Remote Sensing · CA–Markov · Suitability Modelling · Spatial Analysis · Python · Git · GitHub

## Author

**Abdullah Abdazeez Ayomide**  
Urban & Regional Planner · GIS & Remote Sensing · Spatial Decision Support
