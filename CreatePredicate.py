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

            #check for empty and None values
            if values[col] is not None and values[col] != "[]" and not isinstance(values[col], float):
                value = values[col].split("; ")
                if col == "genre":
                    genreSet.update(value)
                elif col == "platform":
                    platformSet.update(value)
                elif col == "gameModes":
                    gameModesSet.update(value)
                elif col == "inputDevice":
                    inputDeviceSet.update(value)
        
    
    predicatebase = """
    (isa <Name> Predicate)
    (arity <Name> 1)
    (arg1Isa <Name> Place)
    """

    predicateMap = {}
    givenSet = set()

    for col in cols:
        with open('Data/Predicates.txt', 'a', encoding='utf-8') as f:
            f.write(";;; Predicates defined for Type : %s\n" % col)
        if col == "video_gameLabel":
            continue
        if col == "genre":
            givenSet = genreSet
        if col == "platform":
            givenSet = platformSet
        elif col == "gameModes":
            givenSet = gameModesSet
        elif col == "inputDevice":
            givenSet = inputDeviceSet

        
        for element in givenSet:
            element_ = element.replace(" ","_")
            predicateName = col+"_"+element_
            predicate = predicatebase.replace("<Name>",predicateName)
            
            #write predicatemap value to file 
            with open('Data/Predicates.txt', 'a', encoding='utf-8') as f:
                f.write("%s\n" % predicate)
            predicateMap[predicateName] = element
    #store the predicates in a file
    with open('Data/PredicateMap.txt', 'w', encoding='utf-8') as f:
        for key,value in predicateMap.items():
            f.write("%s,%s\n" % (key,value))

if __name__ == '__main__':
    main()