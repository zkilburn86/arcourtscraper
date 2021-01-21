from arcourtscraper.utilities import _search_helper
from arcourtscraper.arcourt import DateSearch


def test_parse_args():

    date_search = DateSearch(
        search_type='date',
        begin_date='12/01/2020',
        end_date='12/02/2020'
    )

    args = {
        'case_type': 'DI - FELONY',
        'county_code': '04 - BENTON',
        'cort_code': '04 - BENTON',
        'locn_code': 'CI - CIRCUIT',
        'case_id': '04CR-20-2761'
    }

    date_search = _search_helper.parse_args(date_search, args)

    assert date_search.locn_code == 'CI - CIRCUIT'
    assert date_search.case_type == 'DI - FELONY'
    assert date_search.case_id == '04CR-20-2761'

def test_build_url():

    date_search = DateSearch(
        search_type='date',
        begin_date='12/01/2020',
        end_date='12/02/2020'
    )

    args = {
        'case_type': 'DI - FELONY',
        'county_code': '04 - BENTON',
        'cort_code': '04 - BENTON',
        'locn_code': 'CI - CIRCUIT',
        'case_id': '04CR-20-2761'
    }

    date_search = _search_helper.parse_args(date_search, args)
    url = _search_helper.build_url(date_search)
    expected = 'https://caseinfo.arcourts.gov/cconnect/PROD/public/ck_public_qry_doct.cp_dktrpt_new_case_report?backto=C&begin_date=12%2F01%2F2020&end_date=12%2F02%2F2020&case_type=DI%20-%20FELONY&county_code=04%20-%20BENTON&cort_code=04%20-%20BENTON&locn_code=CI%20-%20CIRCUIT&case_id=04CR-20-2761'

    assert url == expected