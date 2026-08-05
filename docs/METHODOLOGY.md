# Methodology

## 1. Historical land-cover preparation

The cloud workflow prepared surface-reflectance composites for 2005, 2015 and 2025 using Landsat Collection 2 Level-2 imagery. QA_PIXEL and QA_RADSAT bands were used to remove cloud, shadow and saturated observations. The optical bands were scaled and renamed consistently across Landsat sensors.

## 2. Spectral predictors

The predictor stack combined blue, green, red, near-infrared, SWIR-1 and SWIR-2 bands with NDVI, NDBI, MNDWI, BSI and EVI.

## 3. Reference data and Random Forest classification

Manual 2025 polygons supplied the five land-cover classes: built-up, vegetation, cropland, bare land and water. Balanced stratified samples were split 70/30 for training and validation. The historical script used 250-tree Random Forest models and a three-seed ensemble. Stable, homogeneous and spectrally consistent 2025 labels were transferred backward to construct reference labels for 2015, and the process was repeated from 2015 to 2005.

The transferred-label agreement values for historical years are consistency checks, not independent ground-truth accuracies.

## 4. Markov transition probabilities

The 2015 and 2025 land-cover maps were cross-tabulated to estimate class-to-class transition probabilities. The matrix records persistence and conversion probabilities for all five classes.

## 5. Quantity-constrained cellular allocation

The Markov model estimated the 2035 class demand. Built-up growth required **206,027** new pixels. A suitability surface ranked available cells, and the allocation selected **203,889** pixels, equivalent to **98.96%** of the required quantity.

## 6. Output generation

The final outputs include predicted 2035 LULC, new built-up expansion, transition codes and the suitability surface. Local Python scripts clean the exported tables, derive the 2025 baseline from transition codes, regenerate the figures and validate internal consistency.
