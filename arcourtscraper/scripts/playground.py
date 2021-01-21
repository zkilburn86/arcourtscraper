from arcourtscraper.scripts import search

df = search.by_date('01/01/2021','01/05/2021',county_code='04 - BENTON')

print(len(df.index))