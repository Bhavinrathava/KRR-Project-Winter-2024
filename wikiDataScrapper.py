# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import json

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT 
  ?video_game 
  (SAMPLE(?video_gameLabel) AS ?gameLabel)
  (GROUP_CONCAT(DISTINCT ?genreLabel; separator=", ") AS ?genres)
  #(GROUP_CONCAT(DISTINCT ?awardsLabel; separator=", ") AS ?awards)
  #(GROUP_CONCAT(DISTINCT ?developerLabel; separator=", ") AS ?developers)
  (GROUP_CONCAT(DISTINCT ?platformLabel; separator=", ") AS ?platforms)
  (GROUP_CONCAT(DISTINCT ?gamemodeLabel; separator=", ") AS ?gamemodes)
  (GROUP_CONCAT(DISTINCT ?inputDeviceLabel; separator=", ") AS ?inputDevices)
WHERE { 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
  ?video_game wdt:P31 wd:Q7889. 
  { ?video_game wdt:P136 ?genre. ?genre rdfs:label ?genreLabel. FILTER(LANG(?genreLabel) = "en") }
  #OPTIONAL { ?video_game wdt:P166 ?awards. ?awards rdfs:label ?awardsLabel. FILTER(LANG(?awardsLabel) = "en") }
  #OPTIONAL { ?video_game wdt:P178 ?developer. ?developer rdfs:label ?developerLabel. FILTER(LANG(?developerLabel) = "en") }
  { ?video_game wdt:P400 ?platform. ?platform rdfs:label ?platformLabel. FILTER(LANG(?platformLabel) = "en") }
  { ?video_game wdt:P404 ?gamemode. ?gamemode rdfs:label ?gamemodeLabel. FILTER(LANG(?gamemodeLabel) = "en") }
  { ?video_game wdt:P479 ?inputDevice. ?inputDevice rdfs:label ?inputDeviceLabel. FILTER(LANG(?inputDeviceLabel) = "en") }
}
GROUP BY ?video_game
LIMIT 5
"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

finalResults = []

print("Querying Wikidata.....")

results = get_results(endpoint_url, query)
resultLen = len(results["results"]["bindings"])
limit = 5
offset = 0 
count = 1
while resultLen == limit:
    print("Current Page : ", count)
    with open('results'+str(count)+'.json', 'w') as f:
        json.dump(results["results"]["bindings"], f)
    offset += limit
    newQuery = query + " OFFSET " + str(offset)
    results = get_results(endpoint_url, newQuery)
    resultLen = len(results["results"]["bindings"])
    count += 1



#Saving results to a file
with open('results'+str(count)+'.json', 'w') as f:
    json.dump(results["results"]["bindings"], f)
