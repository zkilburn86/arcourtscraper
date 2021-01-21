from arcourtscraper._constants import _navigation
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd

def parse_args(obj, args):
    
    variables = vars(locals().get('obj')).copy()
    keys = args.keys()

    for key in variables.keys():
        if key in keys:
            setattr(obj, key, args.get(key))
    
    return obj

def build_url(search):

    params = dict(vars(search))
    params.pop('search_type')

    if not params.get('case_id'):
        params.pop('case_id')
    
    search_string = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
    url = _navigation.BASE_URL + \
        _navigation.SEARCH_TYPE_CONVERTER.get(search.search_type) + \
        search_string
    
    return url

def parse_results(content):
    soup = BeautifulSoup(content,features='lxml')
    table = soup.find('table')

    if table is not None:
        headers = _get_headers(table)
        df = pd.DataFrame(columns=headers)

        rows = table.findChildren('tr')
        for row in rows:
            cells = row.findChildren('td')
            if cells != []:
                df_row = _get_df_row(cells, headers)
                df = df.append(df_row, ignore_index=True)
        
        return df
    else:
        return None

def _get_headers(table):
    header_row = table.findChildren('th')
    headers = []

    for item in header_row:
        headers.append(item.text)

    return headers

def _get_df_row(cells, headers):
    df_row = {}

    for cell in cells:
        header = headers[cells.index(cell)]
        df_row[header] = cell.text.strip()

    return df_row