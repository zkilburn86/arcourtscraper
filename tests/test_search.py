from arcourtscraper.scripts import search


### Test Searching By Month ###
def test_search_by_date():
    df = search.by_date('01/01/2021','01/05/2021',county_code='04 - BENTON')
    assert len(df.index) == 52