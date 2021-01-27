# Arkansas Court Scraper

This is a work-in-progress repo that will eventually be packaged when planned initial functionality is complete.
The goal of this project is to offer an easy way to both search and retrieve detailed case results from the Arkansas Administrative Office of the Courts CourtConnect site - https://caseinfo.arcourts.gov/cconnect/PROD/public/ck_public_qry_main.cp_main_idx

## Planned Features

1. Search and pull back results as a DataFrame by the 5 methods available:
   * Person Name, Business Name, or Case Type
   * Judgements Against a Person or Business
   * Case Information or Activities
   * Cases Filed by Date
   * Docket Filings by Date

2. Parse case details into custom objects

## Currently Available Features

### Retrieve search results for cases filed by date

```
from arcourtscraper.scripts import search

df = search.by_date(
        begin_date='12/01/2020',
        end_date='12/01/2020',
        case_type='CS - CUSTODY',
        county_code='04 - BENTON',
        cort_code='04 - BENTON',
        locn_code='CI - CIRCUIT'
    )
```

The `begin_date` and `end_date` arguments are required, and the default values for **kwargs can be found in `arcourtscraper.constants`. Be careful using defaults, start with small date ranges to avoid long-running requests. 

### Parse a specific case into it's components

```
from arcourtscraper.scripts import parse
import pprint

#Must know case_id
pprint.pprint(parse.case('04CR-20-181'))

...
{'Case Description': {'Case ID:': '04CR-20-181 - STATE V DANIEL '
                                  'FELICIANO-HERNANDEZ-PLEA/STIPULATION',
                      'Court:': '04 - BENTON',
                      'Filing Date:': 'Monday   , January   27th, 2020',
                      'Images:': '',
                      'Location:': 'CI - CIRCUIT',
                      'Status:': 'CLOSED - CASE CLOSED',
                      'Type:': 'DI - FELONY'},
                      ...
```