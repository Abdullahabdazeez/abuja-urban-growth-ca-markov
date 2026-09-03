# Predicting Urban Growth to Support Better Planning - Abuja, Nigeria

## Planning question
**Where is Abuja most likely to expand next, and how can planners prepare for that growth?**

Abuja continues to expand as new neighbourhoods, roads and commercial areas extend beyond the established urban core. This project combines historical land-cover transitions, an urban-suitability surface and a quantity-constrained CA-Markov model to explore a 2035 urban-growth scenario.

## Key scenario results
- Built-up area in 2025: **1,167.85 km²**
- Built-up area in the 2035 scenario: **1,351.30 km²**
- Net increase: **183.45 km²**
- Relative increase: **15.71%**
- Required new built-up pixels: **206,027**
- Allocated new built-up pixels: **203,889**

## Validation and uncertainty
The historical simulation achieved **49.27% overall accuracy** and **Kappa 0.366** using **1,500 validation samples**.

This is an important limitation. The 2035 map should be interpreted as a **strategic planning scenario**, not a certain forecast. It is most useful for broad screening, discussion and identifying locations that may need closer review.

## Method
1. Estimate 2015-2025 land-cover transition probabilities.
2. Estimate the quantity of built-up growth required for 2035.
3. Use an urban-suitability surface to rank potential development locations.
4. Allocate future built-up cells under a quantity constraint.
5. Produce predicted LULC, built-up-expansion and transition surfaces.
6. Compare 2025 and 2035 land-cover areas.
7. Report historical simulation validation and limitations.

## Planning value
The scenario can support early discussion about:
- where transport and utility upgrades may be needed;
- where schools, healthcare and drainage may face future pressure;
- where development control should be strengthened; and
- where cropland and other non-built land may face conversion pressure.

The scenario should be reviewed alongside current plans, field evidence, population trends and updated imagery before site-specific decisions.

## Tools
Google Earth Engine · GIS · Remote Sensing · CA-Markov · Suitability Modelling · Spatial Analysis

## Author
**Abdullah Abdazeez Ayomide**  
Urban & Regional Planner · GIS & Remote Sensing · Spatial Decision Support

## Citation
Abdullah Abdazeez Ayomide (2026). *Predicting Urban Growth to Support Better Planning - Abuja, Nigeria*.
