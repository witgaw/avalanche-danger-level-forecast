# Data

## Raw

Subdirectory containing raw data

### `Any_snowprofiles_1993-12-20_to_2024-04-13.csv`

Snow profile data downloaded from [SAIS](https://www.sais.gov.uk/snow-profiles/), collated into a single csv with [this script](https://github.com/witgaw/utils/blob/main/csv/collate.py) (the website seems to allow downloading only around 10y worth of data at a time) opened with MS Excel and saved as csv again (to remove excel formula artefacts that seem to be present in the SAIS data - e.g. `="192744"` become `192744` after this operation). No further processing was done on this data.
