

BASE_URL = 'https://caseinfo.arcourts.gov/cconnect/PROD/public/'

### Search Results ###
PERSON_SUFFIX = 'ck_public_qry_cpty.cp_personcase_srch_details?backto=P&'
JUDGEMENT_SUFFIX = 'ck_public_qry_judg.cp_judgment_srch_rslt?'
CASE_SUFFIX = 'ck_public_qry_doct.cp_dktrpt_docket_report?backto=D&'
DATE_SUFFIX = 'ck_public_qry_doct.cp_dktrpt_new_case_report?backto=C&'
DOCKET_SUFFIX = 'ck_public_qry_doct.cp_dktrpt_new_case_report?backto=F&'

SEARCH_TYPE_CONVERTER = {
    'name': PERSON_SUFFIX,
    'judgement': JUDGEMENT_SUFFIX,
    'case': CASE_SUFFIX,
    'date': DATE_SUFFIX,
    'docket': DOCKET_SUFFIX
}

### Details for Known ID's ###
CASE_ID = 'ck_public_qry_doct.cp_dktrpt_docket_report?case_id='

### Case Page Navigation ###
HEADINGS = [
    'Report Selection Criteria',
    'Case Description',
    'Case Event Schedule',
    'Case Parties',
    'Violations',
    'Sentence',
    'Milestone Tracks',
    'Docket Entries'
]