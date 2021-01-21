from arcourtscraper._constants import _defaults

class Case:

    def __init__(self, case_id, filing_date, court_location, 
                case_type, status):

                self.case_id = case_id
                self.filing_date = filing_date
                self.court_location = court_location
                self.case_type = case_type
                self.status = status 


class Party:

    def __init__(self, sequence_number, association, end_date,
                party_type, party_id, name):

                self.sequence_number = sequence_number
                self.association = association
                self.end_date = end_date
                self.party_type = party_type
                self.party_id = party_id
                self.name = name 

class DateSearch:

    def __init__(self, search_type=_defaults.SEARCH_TYPE, begin_date=_defaults.BEGIN_DATE, 
                end_date=_defaults.END_DATE,case_type=_defaults.CASE_TYPE, county_code=_defaults.COUNTY_CODE, 
                cort_code=_defaults.CORT_CODE, locn_code=_defaults.LOCN_CODE,
                case_id=False):

                self.search_type = search_type
                self.begin_date = begin_date 
                self.end_date = end_date 
                self.case_type = case_type
                self.county_code = county_code 
                self.cort_code = cort_code
                self.locn_code = locn_code
                self.case_id = case_id