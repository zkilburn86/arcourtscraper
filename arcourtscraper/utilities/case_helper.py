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
        elif heading in navigation.NON_TABLE_DATA and heading in ['Violations','Sentence']:
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

def _parse_sentence(tag):
    sentence_strings = _page_string_scrubber(tag.find_all_next(string=True), 'Milestone Tracks')

    results = []
    indexer = 0
    output = {}
    for sentence_string in sentence_strings:
        if sentence_string[-1] == ':' and sentence_string != ':':
            if indexer + 1 < len(sentence_strings):
                output[re.sub(':','',sentence_string)] = sentence_strings[indexer + 1]
        elif sentence_string[0] == ':' and sentence_string != ':':
            output[sentence_strings[indexer - 1]] = sentence_string.replace(':','',1).strip()
        elif sentence_string == ':':
            output[re.sub(':','',sentence_strings[indexer - 1] + sentence_string)] = 'N/A'
        indexer += 1
        if len(sentence_strings) == indexer:
            output = {k:_scrub_output_values(v) for k, v in output.items()}
            results.append(output)
    
    return results

def _parse_violations(tag):
    violation_strings = _page_string_scrubber(tag.find_all_next(string=True), 'Sentence')

    results = []
    indexer = 0
    output = {}
    for violation_string in violation_strings:
        if violation_string[-1] == ':' and violation_string != ':':
            if violation_string == 'Violation:':
                if violation_strings[indexer + 1] == '1':
                    output['Party'] = violation_strings[indexer - 1]
                else:
                    output = {k:_scrub_output_values(v) for k, v in output.items()}
                    results.append(output)
                    output = {}
                    output['Party'] = violation_strings[indexer - 1]
            if indexer + 1 < len(violation_strings):
                output[re.sub(':','',violation_string)] = violation_strings[indexer + 1]
        elif violation_string[0] == ':' and violation_string != ':':
            output[violation_strings[indexer - 1]] = violation_string.replace(':','',1).strip()
        elif violation_string == ':':
            output[re.sub(':','',violation_strings[indexer - 1] + violation_string)] = 'N/A'
        if violation_string == 'Plea':
            output['Description'] = violation_strings[indexer + 2] + ', ' + violation_strings[indexer + 3]
        indexer += 1
        if len(violation_strings) == indexer:
            output = {k:_scrub_output_values(v) for k, v in output.items()}
            results.append(output)
    
    return results

def _page_string_scrubber(all_strings, stop_string):
    clean_strings = []
    for item in all_strings:
        clean_item = item.strip()
        if clean_item != '':
            if clean_item == stop_string:
                break
            else:
                clean_strings.append(clean_item)
    return clean_strings
      
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

def _scrub_output_values(output_value):
    output_value = re.sub('\xa0','',output_value)
    return output_value

def _key_check(dict_to_check, key_to_check):
    if key_to_check in dict_to_check:
        return True
    else:
        return False