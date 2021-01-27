from arcourtscraper.constants import navigation
import urllib.parse
from bs4 import BeautifulSoup
import pandas as pd
import re


def process_case(content):
    results = {}
    soup = BeautifulSoup(content, features='lxml')
    all_u_tags = soup.find_all('u')
    for tag in all_u_tags:
        heading = tag.text.strip()
        if heading in [] and heading not in navigation.NON_TABLE_DATA: ## should be navigation.HEADINGS
            results[heading] = _determine_parser(heading, tag)
        elif heading in navigation.NON_TABLE_DATA and heading == 'Violations':
            results[heading] = _handle_custom_parsing(heading, tag)
    return results

def _determine_parser(heading, tag):
    parser = navigation.CASE_DETAIL_HANDLER.get(heading)
    table = tag.find_next('table')
    results = globals()[parser](table)
    return results

def _handle_custom_parsing(heading, tag):
    parser = navigation.CASE_DETAIL_HANDLER.get(heading)
    results = globals()[parser](tag)
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

def _parse_violations(tag):
    violations = _violation_scrubber(tag.find_all_next(string=True))

    results = []
    indexer = 0
    output = {}
    for violation in violations:
        if violation[-1] == ':' and violation != ':':
            if violation == 'Violation:':
                if violations[indexer + 1] == '1':
                    output['Party'] = violations[indexer - 1]
                else:
                    output['Level'] = re.sub('\xa0','',output.get('Level'))
                    results.append(output)
                    output = {}
                    output['Party'] = violations[indexer - 1]
            if indexer + 1 < len(violations):
                output[re.sub(':','',violation)] = violations[indexer + 1]
        elif violation[0] == ':' and violation != ':':
            output[violations[indexer - 1]] = violation.replace(':','',1).strip()
        elif violation == ':':
            output[re.sub(':','',violations[indexer - 1] + violation)] = 'N/A'
        if violation == 'Plea':
            output['Description'] = violations[indexer + 2] + ', ' + violations[indexer + 3]
        indexer += 1
        if len(violations) == indexer:
            output['Level'] = re.sub('\xa0','',output.get('Level'))
            results.append(output)
    
    return results

def _violation_scrubber(all_strings):
    violations = []
    for item in all_strings:
        clean_item = item.strip()
        if clean_item != '':
            if clean_item == 'Sentence':
                break
            else:
                violations.append(clean_item)
    return violations
      
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