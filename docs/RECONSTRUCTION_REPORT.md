# Reconstruction Report: Abuja Urban Growth CA–Markov Model

## Why this project is being rebuilt

The first version of this project produced a 2035 urban-growth scenario for Abuja using historical land-cover maps, Markov transition probabilities, an urban-suitability surface and cellular allocation.

The maps looked plausible, but a later review showed that the historical evidence feeding the model was not strong enough for me to treat the 2035 scenario as final.

I decided to keep the original work public and rebuild the project rather than quietly replace it.

## What the audit showed

The original historical hindcast achieved **49.27% overall accuracy** and **0.366 Kappa** on 1,500 comparison points.

The 2015-2025 transition matrix also showed unusual instability. Built-up persistence was only about **0.648**, which implied a large amount of Built-up to non-Built-up change. Cropland and Bare-land persistence were also weak.

Those patterns suggested that classification instability may have been entering the transition model.

The original suitability surface also clustered tightly around its central range, so it was not clear enough whether the surface genuinely separated observed expansion from non-expansion areas.

## Why this matters for CA-Markov modelling

A future scenario can look convincing even when the historical maps behind it are weak. In a CA-Markov workflow, classification error can pass into the transition probabilities, then into the suitability model and finally into the simulated future map.

That means the future map should not be treated as stronger evidence than the historical inputs that produced it.

## Original scenario kept for transparency

The original project reported **1,167.85 km²** of built-up land in 2025 and **1,351.30 km²** in the simulated 2035 scenario, an increase of **183.45 km² or 15.71%**.

Those values remain in the repository as part of the project's history, but they are not currently presented as final planning results.

## What I am rebuilding

The reconstruction starts with the historical land-cover maps rather than with the 2035 output.

The main sequence is:

1. preserve the original results as provenance;
2. audit the 2005, 2015 and 2025 historical classifications;
3. review implausible transitions spatially;
4. rebuild a stronger human-reviewed reference dataset;
5. reconstruct the historical classifications with leakage-free validation;
6. check temporal consistency;
7. rebuild Markov transition probabilities;
8. test the suitability model against observed expansion;
9. validate a historical hindcast using Figure of Merit, quantity disagreement and allocation disagreement; and
10. produce a new 2035 scenario only if the earlier stages pass.

## Current interpretation

The repository is useful as a transparent record of the original experiment and the reconstruction process. The current 2035 scenario should not be used as a parcel-level development guide or as a deterministic forecast of Abuja's future urban footprint.

## What I expect from the final version

The goal is not simply to obtain a higher accuracy score. The final model needs to show that:

- the historical classes are stable enough to support change modelling;
- the transition logic is physically plausible;
- the suitability surface separates observed expansion from non-expansion locations;
- the hindcast reproduces meaningful historical change better than a weak baseline; and
- the final scenario is clearly presented as a scenario rather than a guaranteed forecast.

## Final note

Keeping a provisional result public can feel uncomfortable, but it is more useful than pretending the first version was stronger than it really was. The reconstruction is part of the scientific record of the project, not something I want to hide.
