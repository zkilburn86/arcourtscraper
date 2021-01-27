from arcourtscraper import chromedriver
from arcourtscraper.constants import navigation
from arcourtscraper.utilities import case_helper

def case(case_id):

    driver = chromedriver.driver()
    driver.get(navigation.BASE_URL + navigation.CASE_ID + case_id)

    results = case_helper.process_case(driver.page_source)

    return results