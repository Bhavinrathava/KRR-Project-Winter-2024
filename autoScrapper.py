import pandas as pd
import requests
import json
from tqdm import tqdm  # Import tqdm for the progress bar

def fetch_wikidata_details(entity_id):
    query = """
    SELECT ?genreLabel ?platformLabel ?gameModeLabel ?inputDeviceLabel WHERE {
      OPTIONAL { wd:""" + entity_id + """ wdt:P136 ?genre. }
      OPTIONAL { wd:""" + entity_id + """ wdt:P400 ?platform. }
      OPTIONAL { wd:""" + entity_id + """ wdt:P404 ?gameMode. }
      OPTIONAL { wd:""" + entity_id + """ wdt:P479 ?inputDevice. }
      SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    """
    url = 'https://query.wikidata.org/sparql'
    headers = {'User-Agent': 'YourAppName/1.0 (your_email@example.com)'}  # Replace with your app's name and your email
    r = requests.get(url, headers=headers, params={'format': 'json', 'query': query})
    #print(r.content)
    # Check HTTP status code for error handling
    if r.status_code != 200:
        print(f"Error fetching data for {entity_id}. HTTP Status Code: {r.status_code}")
        print(r.text)  # Print response text for debugging
        return {'genre': '', 'platform': '', 'gameModes': '', 'inputDevice': ''}  # Return empty details on error

    try:
        data = json.loads(r.content.decode("utf-8"))
    except ValueError as e:  # Catch JSON decode error
        print(f"Error decoding JSON for {entity_id}: {e}")
        print(r.text)  # Print response text for debugging
        return {'genre': '', 'platform': '', 'gameModes': '', 'inputDevice': ''}  # Return empty details on error

    # Proceed with data extraction if JSON was successfully decoded
    details = {'genre': set(), 'platform': set(), 'gameModes': set(), 'inputDevice': set()}
    for item in data['results']['bindings']:
        if 'genreLabel' in item:
            details['genre'].add(item['genreLabel']['value'])
        if 'platformLabel' in item:
            details['platform'].add(item['platformLabel']['value'])
        if 'gameModeLabel' in item:
            details['gameModes'].add(item['gameModeLabel']['value'])
        if 'inputDeviceLabel' in item:
            details['inputDevice'].add(item['inputDeviceLabel']['value'])

    # Convert sets to semicolon-separated strings
    for key in details:
        details[key] = '; '.join(details[key])

    return details


# Parameters
checkpoint_interval = 500
start_from_checkpoint = 0  # Example: start from row 200; adjust this as needed

# Load the CSV file
df = pd.read_csv('GameEntities.csv')

# Optionally, load enriched data from the last checkpoint if needed
enriched_data = []
if start_from_checkpoint > 0:
    try:
        checkpoint_df = pd.read_csv(f'EnrichedGameEntities_checkpoint_{start_from_checkpoint}.csv')
        enriched_data = checkpoint_df.to_dict('records')
    except FileNotFoundError:
        print(f"No checkpoint file found for index {start_from_checkpoint}. Starting from the beginning.")

# Enriching data with a progress bar and checkpointing
for index, row in tqdm(df.iterrows(), total=df.shape[0], desc="Fetching Wikidata Details", initial=start_from_checkpoint):
    if index < start_from_checkpoint:
        continue  # Skip rows before the checkpoint index
    
    entity_details = fetch_wikidata_details(row['Entities'])
    enriched_data.append({
        'video_gameLabel': row['video_gameLabel'],
        'Entities': row['Entities'],
        **entity_details
    })

    # Checkpoint: Save progress at regular intervals
    if (index + 1 - start_from_checkpoint) % checkpoint_interval == 0 or (index + 1) == df.shape[0]:
        partial_df = pd.DataFrame(enriched_data)
        partial_df.to_csv(f'EnrichedGameEntities_checkpoint_{index + 1}.csv', index=False)
        print(f"Checkpoint saved at index {index + 1}")

# Save the final complete dataframe at the end as well
enriched_df = pd.DataFrame(enriched_data)
enriched_df.to_csv('EnrichedGameEntities_final.csv', index=False)