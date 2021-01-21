from arcourtscraper import chromedriver, arcourt
from arcourtscraper.utilities import _search_helper


def by_date(begin_date, end_date, **kwargs):

    driver = chromedriver.driver()
    date_search = arcourt.DateSearch(
        begin_date=begin_date,
        end_date=end_date
    )

    date_search = _search_helper.parse_args(date_search, kwargs)

    url = _search_helper.build_url(date_search)

    driver.get(url)

    return _search_helper.parse_results(driver.page_source)