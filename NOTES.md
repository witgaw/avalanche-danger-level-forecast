# Notes

## SAIS

### Ideas

There's an [avalanche map](https://www.sais.gov.uk/avalanche_map/?area=-1&type=All) available, perhaps it could be scraped for some additional information to do with aspects and angles?

### Questions

- Where can 'Avalanche Code' and 'AV cat' be looked-up?
  - Seems this relate to observed avalanches
- How to I decipher 'Grid'? They all seem to point to somewhere in Celtic Sea - so somehow wrong, but not entirely so (as it's close-ish)?

## TODO

- Add one hot encoding of area to see how much it helps fits
- Construct alternative long vector with hourly data for n most recent days.
- Try applying deep learning method (CNN) and random forrest classifier.
- Use PCA to reduce dimensionality and visualise most relevant data points.
- Revisit reference paper.

### Stretch goals

- If the above shows promise re-run it on US Forrest Service dataset.
- US data enablers:
  - area polygons
  - summit / chosen weather observation point coordinates
- See if it's possible to use data relating to observations of snowpack at different locations within each area to add more granularity to the model (still predict overall hazard level for a forecast area, but see if it can be locally raised or lowered depening on aspects, elevations, angles and altitudes).
- Visualise predictions on a map.

## Weather providers

- [Meteostat](https://meteostat.net)
- [VisualCrossing](https://www.visualcrossing.com/)
- [Meteoblue](https://www.meteoblue.com)
