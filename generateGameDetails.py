# Read CSV File 

import csv
import json

# Open the CSV
f = open('Data/PredicateMap.csv', 'r', encoding='utf-8')

fields = ['genre', 'platform', 'gameModes', 'inputDevice']
fieldName = {"genre": "Genre", "platform": "Platform", "gameModes": "GameMode", "inputDevice": "InputDevice"}
#baseString = f"(isa {predicateType} {predicateName})"
# For each entry in CSV file, read each row and build a string 
for row in f:
    try:
        
        t,n = row.split(",")
        n = n.strip().replace(" ","_")
        # find if the t begins with any of the fields
        for field in fields:
            if t.startswith(field):
                print(f" ( isa {fieldName[field]} {field}_{n} ) ")
                # write to a file 
                with open('Data/predicateMap2.txt', 'a', encoding="utf-8") as file:
                    file.write(f" ( isa {fieldName[field]} {field}_{n} ) \n")
    except:
        pass


