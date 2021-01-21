from arcourtscraper import chromedriver, arcourt, _helper
import pandas as pd


def by_date(begin_date, end_date, **kwargs):

    driver = chromedriver.driver()
    date_search = arcourt.DateSearch(
        begin_date=begin_date,
        end_date=end_date
    )

    date_search = _helper.parse_args(date_search, kwargs)

    url = _helper.build_url(date_search)

    driver.get(url)

    return _helper.parse_results(driver.page_source)