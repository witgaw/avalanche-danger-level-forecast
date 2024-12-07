# Notes

## SAIS

### Ideas

There's an [avalanche map](https://www.sais.gov.uk/avalanche_map/?area=-1&type=All) available, perhaps it could be scraped for some additional information to do with aspects and angles?

### Questions

- Where can 'Avalanche Code' and 'AV cat' be looked-up?
  - Seems this relate to observed avalanches.
- How to I decipher 'Grid'? They all seem to point to somewhere in Celtic Sea - so somehow wrong, but not entirely so (as it's close-ish)?

## TODO

- Look at feature correlation & distribution
- Use PCA to reduce dimensionality and visualise most relevant data points.
- Visualise predictions on a map.
- Add one hot encoding of area to see how much it helps fits

## USFS

- Extract subregions for each region which contain them and for which hazard levels are specified at sufficient granularity.

## Next steps

- Look into scraping additional data from SAIS website.
- Aspec/elevation type?
  - See if it's possible to use data relating to observations of snowpack at different locations within each area to add more granularity to the model (still predict overall hazard level for a forecast area, but see if it can be locally raised or lowered depening on aspects, elevations, angles and altitudes).
- Avalanche problem type?

## Weather providers

- [Meteostat](https://meteostat.net)
- [VisualCrossing](https://www.visualcrossing.com/)
- [Meteoblue](https://www.meteoblue.com)
