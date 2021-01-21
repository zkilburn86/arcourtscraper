from arcourtscraper.scripts import search


### Test Searching By Month ###
def test_search_by_date():
    df = search.by_date('01/01/2021','01/05/2021',county_code='04 - BENTON')
    assert len(df.index) == 52

def test_no_results():
    df = search.by_date(
        begin_date='12/01/2020',
        end_date='12/01/2020',
        case_type='CS - CUSTODY',
        county_code='04 - BENTON',
        cort_code='04 - BENTON',
        locn_code='CI - CIRCUIT'
    )
    
    assert df is None
