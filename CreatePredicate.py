import pandas as pd
import requests
import json
from tqdm import tqdm  # Import tqdm for the progress bar



def main():

    #read csv file
    df = pd.read_csv('Data/EnrichedGameEntities_checkpoint_39000.csv')
    df = df.drop(columns=["Entities"])
    cols = ["video_gameLabel","genre","platform","gameModes","inputDevice"]

    genreSet = set()
    platformSet = set()
    gameModesSet = set()
    inputDeviceSet = set()

    #print(df.head())
    #processing 

    for index, values in tqdm(df.iterrows(), total=df.shape[0], desc="Fetching Wikidata Details"):
        for col in cols:
            if col == "video_gameLabel":
                continue
            if values[col] != "":
                value = values[col].split("; ")
                if col == "genre":
                    genreSet.update(value)
                elif col == "platform":
                    platformSet.update(value)
                elif col == "gameModes":
                    gameModesSet.update(value)
                elif col == "inputDevice":
                    inputDeviceSet.update(value)
        break
        
    
    predicatebase = """
    (isa <Name> Predicate)
    (arity <Name> 1)
    (arg1Isa <Name> Place)
    """

    predicateMap = {}
    for col in cols:
        if col == "video_gameLabel":
            continue
        if col == "genre":
            givenSet = genreSet
            for element in givenSet:
                print(element)
                element_ = element.replace(" ","_")
                predicateName = col+"_"+element_
                predicate = predicatebase.replace("<Name>",predicateName)
                
                #write predicatemap value to file 
                with open('Data/Predicates.txt', 'a') as f:
                    f.write("%s\n" % predicate)
                print(predicate)
                predicateMap[predicateName] = element

    #store the predicates in a file
    with open('Data/PredicateMap.txt', 'w') as f:
        for key,value in predicateMap.items():
            f.write("%s,%s\n" % (key,value))

if __name__ == '__main__':
    main()