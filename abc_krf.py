# To read the games_info from the provided CSV file and generate the .krf output, we'll first parse the CSV file.

import pandas as pd

def clean_string(s):
    # Keep only letters and spaces
    cleaned = ''.join([char for char in s if char.isalpha()])
    return cleaned

# Read the CSV file into a DataFrame
csv_path = 'Data/EnrichedGameEntities_checkpoint_39000.csv'
games_df = pd.read_csv(csv_path)

# Simplify the DataFrame for demonstration purposes, focusing on necessary columns
games_df = games_df[['video_gameLabel', 'genre', 'platform', 'gameModes', 'inputDevice']]

# Now, let's generate the .krf content based on the DataFrame
def generate_krf_from_df(games_df, output_file_path):
    with open(output_file_path, 'a', encoding="utf-8") as file:
        for _, row in games_df.iterrows():
            # Simplify the game name for use in the KRF file (remove spaces, special characters)
            game_name = clean_string(row['video_gameLabel'])
            file.write(f";;; {row['video_gameLabel']}\n")
            file.write(f"(isa {game_name} Game)\n")
            
            if pd.notna(row['genre']):
                for genre in row['genre'].split('; '):
                    genre = clean_string(genre)
                    file.write(f"(inGenre {game_name} genre_{genre})\n")
            if pd.notna(row['platform']):
                for platform in row['platform'].split('; '):
                    platform = clean_string(platform)
                    file.write(f"(onPlatform {game_name} platform_{platform})\n")
            if pd.notna(row['gameModes']):
                for mode in row['gameModes'].split('; '):
                    mode = clean_string(mode)
                    file.write(f"(hasGameMode {game_name} gameModes_{mode})\n")
            if pd.notna(row['inputDevice']):
                for device in row['inputDevice'].split('; '):
                    device = clean_string(device)
                    file.write(f"(withInputDevice {game_name} inputDevice_{device})\n")
            file.write("\n")



def createPredicateDefinitions():
    # Open the CSV
    f = open('Data/PredicateMap.csv', 'r', encoding='utf-8')

    fields = ['genre', 'platform', 'gameModes', 'inputDevice']
    fieldName = {"genre": "Genre", "platform": "Platform", "gameModes": "GameMode", "inputDevice": "InputDevice"}
    #baseString = f"(isa {predicateType} {predicateName})"
    # For each entry in CSV file, read each row and build a string 
    for row in f:
        try:
            
            t,n = row.split(",")

            #remove all punctuation and spaces from n 
            n = clean_string(n)
            # find if the t begins with any of the fields
            for field in fields:
                if t.startswith(field):
                    #print(f" ( isa {fieldName[field]} {field}_{n} ) ")
                    # write to a file 
                    with open('Data/generatedGameDetailsFromCSVtest.krf', 'a') as file:
                        file.write(f" ( isa {fieldName[field]} {field}_{n} ) \n")
        except:
            pass



# Define the output file path
output_krf_path = 'Data/generatedGameDetailsFromCSVtest.krf'

# Generate the predicate definitions
createPredicateDefinitions()

# Generate the KRF file
generate_krf_from_df(games_df, output_krf_path)

