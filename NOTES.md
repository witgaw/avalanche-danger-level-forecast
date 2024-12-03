# Notes

## SAIS

### Ideas

There's an [avalanche map](https://www.sais.gov.uk/avalanche_map/?area=-1&type=All) available, perhaps it could be scraped for some additional information to do with aspects and angles?

### Questions

- Where can 'Avalanche Code' and 'AV cat' be looked-up?
  - Seems this relate to observed avalanches
- How to I decipher 'Grid'? They all seem to point to somewhere in Celtic Sea - so somehow wrong, but not entirely so (as it's close-ish)?

## TODO

- Construct long vectors of weather data
  - mixture of existing snowprofiles and weather data, weather data only
- Try applying deep learning method and random forrest classifier
- Revisit reference paper
- Explore deep learning methods
Nice to have:
- If the above shows promise re-run it on US Forrest Service dataset.
- US data enablers:
  - area polygons
  - summit / chosen weather observation point coordinates
- See if it's possible to use data relating to observations of snowpack at different locations within each area to add more granularity to the model (still predict overall hazard level for a forecast area, but see if it can be locally raised or lowered depening on aspects, elevations, angles and altitudes).
- Visualise predictions on a map.

### Nice-to-have

- Revisit possibility of creating [simulated snow profiles](https://snowpack.slf.ch})

## Weather providers

- [Meteostat](https://meteostat.net)
- [VisualCrossing](https://www.visualcrossing.com/)
- [Meteoblue](https://www.meteoblue.com)