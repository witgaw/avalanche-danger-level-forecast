# Notes

## SAIS

### Ideas

There's an [avalanche map](https://www.sais.gov.uk/avalanche_map/?area=-1&type=All) available, perhaps it could be scraped for some additional information to do with aspects and angles?

### Questions

- Where can 'Avalanche Code' and 'AV cat' be looked-up?
  - Seems this relate to observed avalanches
- How to I decipher 'Grid'? They all seem to point to somewhere in Celtic Sea - so somehow wrong, but not entirely so (as it's close-ish)?

## TODO:

- Explore geopandas options
- Create a "long-vector" time series of SAIS data and rerun softmax
- Do the same with available weather data
  - mixture of existing snowprofiles and weather data, weather data only, and [simulated snow profiles](https://snowpack.slf.ch}).
- Revisit reference paper
- Explore deep learning methods
Nice to have:
- If the above shows promise re-run it on US Forrest Service dataset.
- See if it's possible to use data relating to observations of snowpack at different locations within each area to add more granularity to the model (still predict overall hazard level for a forecast area, but see if it can be locally raised or lowered depening on aspects, elevations, angles and altitudes).
- Visualise predictions on a map.