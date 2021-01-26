from arcourtscraper.constants import navigation
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd


def process_case(content):
    results = {}
    soup = BeautifulSoup(content, features='lxml')
    all_u_tags = soup.find_all('u')
    for tag in all_u_tags:
        heading = tag.text.strip()
        if heading in ['Report Selection Criteria','Case Description','Case Event Schedule','Case Parties']: ## should be navigation.HEADINGS
            results[heading] = _determine_parser(heading, tag)
    return results

def _determine_parser(heading, tag):
    table = tag.find_next('table')
    parser = navigation.CASE_DETAIL_HANDLER.get(heading)
    results = globals()[parser](table)
    return results

def _parse_rsc(table):
    clean_cells = []
    results = {}

    rows = table.findChildren('tr')
    for row in rows:
        clean_cells.extend(_clean_cells(row))
    
    results = _build_results_with_colon(results, clean_cells)
    
    return results

def _parse_events(table):
    results = []

    if table is not None:
        headers = _clean_headers(table)
        rows = table.findChildren('tr')
        for row in rows:
            clean_row = _build_standard_row(row, headers)
            if clean_row != {}:
                results.append(clean_row)
    
    return results

def _parse_parties(table):
    results = []

    if table is not None:
        headers = _clean_headers(table)
        rows = table.findChildren('tr')
        for row in rows:
            len_of_cells = len(row.findChildren('td'))
            if len_of_cells == len(headers):
                clean_row = _build_standard_row(row, headers)
                if clean_row != {}:
                    results.append(clean_row)
            elif results != []:
                additional_details = _build_non_standard_row(row)
                results[-1].update(additional_details)
            
    return results
      
def _clean_cells(row):
    clean_cells = []
    cells = row.findChildren('td')
    for cell in cells:
        clean_cell = cell.text.strip().replace('\n', '')
        clean_cells.append(clean_cell)
    return clean_cells

def _build_results_with_colon(results, clean_cells):
    for cell in clean_cells:
        next_index = clean_cells.index(cell) + 1
        if cell != '' and cell[-1] == ':' and next_index < len(clean_cells):
            results[cell] = clean_cells[next_index]
        elif cell != '' and cell[-1] == ':' and next_index > len(clean_cells):
            results[cell] = ''
    return results

def _clean_headers(table):
    headers = table.findChildren('th')
    clean_headers = []
    for header in headers:
        clean_headers.append(header.text.strip())
    return clean_headers

def _build_standard_row(row, headers):
    clean_row = {}
    cells = row.findChildren('td')
    indexer = 0
    for cell in cells:
        header = headers[indexer]
        clean_row[header] = cell.text.strip()
        indexer += 1
    return clean_row

def _build_non_standard_row(row):
    row_dict = {}
    cells = row.findChildren('td')
    for cell in cells:
        find_bold = cell.findChildren('b')
        if find_bold != [] and cell.text != ' ':
            next_cell = cell.find_next('td')
            row_dict[cell.text.strip()] = next_cell.text.strip()
    return row_dict