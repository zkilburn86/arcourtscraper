from arcourtscraper import chromedriver
from arcourtscraper._constants import _navigation

def case(case_id):

    driver = chromedriver.driver()

    driver.get(_navigation.BASE_URL + _navigation.CASE_ID + case_id)

    #helper will build array of frames {'Violations': violation_df, etc..}