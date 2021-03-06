

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

CASE_DETAIL_HANDLER = {
    'Report Selection Criteria': '_parse_report_or_desc',
    'Case Description': '_parse_report_or_desc',
    'Case Event Schedule': '_parse_events',
    'Case Parties': '_parse_parties_or_docket',
    'Violations': '_parse_violations',
    'Sentence': '_parse_sentence',
    'Milestone Tracks': '_skip_parse',
    'Docket Entries': '_parse_parties_or_docket'
}

NON_TABLE_DATA = [
    'Violations',
    'Sentence',
    'Milestone Tracks'
]

UNAVAILABLE_STATEMENTS = {
    'Case Event Schedule': 'No case events were found.',
    'Sentence': 'No Sentence Info Found.',
    'Milestone Tracks': 'No Milestone Tracks found.'
}

### New Web Layout ###

CASE_ID_SEARCH = 'https://caseinfonew.arcourts.gov/pls/apexpcc/f?p=313:15:206076974987427::NO:::'