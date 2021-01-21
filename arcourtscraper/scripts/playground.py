from arcourtscraper import chromedriver
from arcourtscraper._constants import _navigation
from bs4 import BeautifulSoup
from arcourtscraper.utilities import _search_helper
from arcourtscraper.arcourt import DateSearch
from arcourtscraper.scripts import search

""" driver = chromedriver.driver()

driver.get(_navigation.BASE_URL + _navigation.CASE_ID + 'SWC-21-17')

content = driver.page_source
soup = BeautifulSoup(content,features='lxml')
all_u_tags = soup.find_all('u')
for tag in all_u_tags:
    if tag.text.strip() in _navigation.HEADINGS:
        table = tag.find_next('table')
        print(tag.text.strip())
        print(table) """

date_search = DateSearch(
        search_type='date',
        begin_date='12/01/2020',
        end_date='12/01/2020',
        case_type='CS - CUSTODY',
        county_code='04 - BENTON',
        cort_code='04 - BENTON',
        locn_code='CI - CIRCUIT'
    )

driver = chromedriver.driver()
date_search = _search_helper.parse_args(date_search,{})
url = _search_helper.build_url(date_search)
driver.get(url)
df = _search_helper.parse_results(driver.page_source)
print(df)