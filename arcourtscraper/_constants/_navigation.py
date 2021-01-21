

BASE_URL = 'https://caseinfo.arcourts.gov/cconnect/PROD/public/'

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