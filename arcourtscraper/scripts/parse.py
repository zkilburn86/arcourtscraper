from arcourtscraper import chromedriver
from arcourtscraper._constants import _navigation
from arcourtscraper.utilities import _case_helper

def case(case_id):

    driver = chromedriver.driver()
    driver.get(_navigation.BASE_URL + _navigation.CASE_ID + case_id)

    results = _case_helper.process_case(driver.page_source)

    print(results)