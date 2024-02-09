import requests
import csv

def call_wikidata_api(query):
    url = 'https://www.wikidata.org/w/rest.php/wikibase/v0'
    headers = {'Accept': 'text/csv'}
    params = {'query': query}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    return response.text

def save_results_as_csv(results, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for row in results.splitlines():
            writer.writerow(row.split(','))

# Example usage
def get_query_with_pagination(limit, offset):
    return f'''
    SELECT ?video_game ?video_gameLabel ?genreLabel ?awardsLabel ?developerLabel ?platformLabel ?gamemodeLabel ?inputDeviceLabel ?partsLabel WHERE {{
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
      ?video_game wdt:P31 wd:Q7889.
      ?video_game wdt:P136 ?genre.
      ?video_game wdt:P166 ?awards.
      ?video_game wdt:P178 ?developer.
      ?video_game wdt:P400 ?platform.
      ?video_game wdt:P404 ?gamemode.
      ?video_game wdt:P479 ?inputDevice.
      ?video_game wdt:P527 ?parts.
    }}
    
    ORDER BY ASC(?video_game)

    LIMIT {limit}
    OFFSET {offset}
    '''

limit = 100
offset = 0

while True:
    query = get_query_with_pagination(limit, offset)
    results = call_wikidata_api(query)
    save_results_as_csv(results, 'wikidata_results'+offset+'.csv')
    
    # Check if there are more results
    if len(results.splitlines()) < limit:
        break
    
    offset += limit

results = call_wikidata_api(query)
save_results_as_csv(results, 'wikidata_results'+offset+'.csv')